import argparse
import bandit
from bandit.core import manager, config
import esprima
import re
import os
import sys
import subprocess
import traceback
import json
import logging
from typing import List, Dict, Tuple, Generator, Optional
from contextlib import contextmanager
from pathlib import Path
import concurrent.futures
from tqdm import tqdm as tqdm_lib

MAX_DISPLAY_LENGTH = 65
MAX_MATCH_LENGTH = 80
TIMEOUT_SECONDS = 60
SUPPORTED_EXTENSIONS = ('.py', '.js', '.php')
SEVERITY_ORDER = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PATTERNS = {}
PATTERNS_JSON_PATH = Path(__file__).parent / 'patterns.json'
PATTERNS_PY_PATH_MESSAGE = "internal patterns.py (package structure or local)"

# Добавляем поддержку игнорирования файлов/шаблонов
IGNORE_FILE = '.bac_detectignore'

@contextmanager
def suppress_stdout():
    original_stdout = sys.stdout
    try:
        sys.stdout = open(os.devnull, 'w')
        yield
    finally:
        if sys.stdout != original_stdout:
            sys.stdout.close()
        sys.stdout = original_stdout

def load_patterns() -> Dict:
    patterns = {}
    
    if PATTERNS_JSON_PATH.exists():
        try:
            with open(PATTERNS_JSON_PATH, 'r', encoding='utf-8') as f_patterns:
                patterns = json.load(f_patterns)
            if not isinstance(patterns, dict) or not any(isinstance(v, dict) for v in patterns.values()):
                logger.warning(f"patterns.json seems to be empty or malformed. Loaded: {str(patterns)[:100]}")
                patterns = {}
            else:
                logger.info(f"Patterns loaded successfully from {PATTERNS_JSON_PATH}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode patterns.json: {str(e)}. Check JSON validity.")
            patterns = {}
        except Exception as e:
            logger.error(f"Error loading patterns.json: {str(e)}.")
            patterns = {}

    if not patterns or not any(patterns.values()):
        patterns_py_loaded = False
        try:
            from .patterns import PATTERNS as PY_PATTERNS_PKG
            patterns = PY_PATTERNS_PKG
            patterns_py_loaded = True
            PATTERNS_PY_PATH_MESSAGE = "internal patterns.py (package structure)"
        except ImportError:
            try:
                from patterns import PATTERNS as PY_PATTERNS_SCRIPT
                patterns = PY_PATTERNS_SCRIPT
                patterns_py_loaded = True
                PATTERNS_PY_PATH_MESSAGE = "local patterns.py (script structure)"
            except ImportError:
                pass

        if patterns_py_loaded:
            if not isinstance(patterns, dict) or not any(isinstance(v, dict) for v in patterns.values()):
                logger.warning(f"Patterns from {PATTERNS_PY_PATH_MESSAGE} seem to be empty or malformed.")
                patterns = {}
            else:
                logger.info(f"Patterns loaded successfully from {PATTERNS_PY_PATH_MESSAGE}.")

    if not patterns or not any(patterns.values()):
        if PATTERNS_JSON_PATH.exists() or patterns_py_loaded:
            logger.critical("Failed to load valid patterns from available sources. Detection capability will be severely limited.")
        patterns = {"python": {}, "javascript": {}, "php": {}}
    
    return patterns

PATTERNS = load_patterns()

class Colors:
    CRITICAL = '\033[95m'
    HIGH = '\033[91m'
    MEDIUM = '\033[93m'
    LOW = '\033[94m'
    INFO = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    @staticmethod
    def format(text: str, style_key_or_direct_code: str) -> str:
        if style_key_or_direct_code.startswith('\033['):
            return f"{style_key_or_direct_code}{text}{Colors.RESET}"

        style_map = {
            'critical': Colors.CRITICAL, 'high': Colors.HIGH, 'medium': Colors.MEDIUM,
            'low': Colors.LOW, 'info': Colors.INFO, 'bold': Colors.BOLD, 'dim': Colors.DIM,
        }
        color_code = style_map.get(style_key_or_direct_code.lower(), "")
        return f"{color_code}{text}{Colors.RESET}" if color_code else text

    @staticmethod
    def is_supported() -> bool:
        return sys.platform != "win32" or (sys.platform == "win32" and os.environ.get('TERM') == 'xterm-256color')

class BackdoorDetector:
    
    def __init__(self):
        self.patterns = PATTERNS
        self.ignored_patterns = set()
        self.ignored_files = set()
        self.load_ignore_file()
        if not self.patterns or not any(self.patterns.values()):
            logger.warning("No patterns loaded. Detection capability will be limited.")

    def load_ignore_file(self, ignore_file_path: str = None):
        """Загружает шаблоны игнорирования из .bac_detectignore"""
        ignore_file = ignore_file_path or IGNORE_FILE
        try:
            if os.path.exists(ignore_file):
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if line.startswith('pattern:'):
                            self.ignored_patterns.add(line[8:].strip())
                        else:
                            self.ignored_files.add(line)
                logger.info(f"Loaded {len(self.ignored_files)} file patterns and {len(self.ignored_patterns)} issue patterns to ignore")
        except Exception as e:
            logger.error(f"Failed to load ignore file: {e}")

    def should_ignore_file(self, file_path: str) -> bool:
        """Проверяет, должен ли файл быть игнорирован"""
        for pattern in self.ignored_files:
            if re.search(pattern, file_path):
                return True
        return False

    def should_ignore_pattern(self, pattern_name: str) -> bool:
        """Проверяет, должен ли шаблон быть игнорирован"""
        return pattern_name in self.ignored_patterns

    def _analyze_with_regex(self, file_path: str, content: str, lang: str) -> List[Dict]:
        issues = []
        lang_patterns = self.patterns.get(lang, {})
        if not lang_patterns:
            return issues

        for pattern_name, pattern_regex in lang_patterns.items():
            try:
                for match in re.finditer(pattern_regex, content):
                    severity = self._determine_severity(lang, pattern_name)
                    match_text = match.group()
                    display_match = match_text[:MAX_MATCH_LENGTH] + ('...' if len(match_text) > MAX_MATCH_LENGTH else '')

                    issues.append({
                        'file': file_path,
                        'line': content[:match.start()].count('\n') + 1,
                        'type': f'regex-{lang}',
                        'message': f"Pattern '{Colors.format(pattern_name, 'bold')}' : {Colors.format(display_match, 'dim')}",
                        'severity': severity
                    })
            except re.error as re_e:
                logger.warning(f"Regex Error: Pattern '{pattern_name}' for {lang} on {file_path}: {re_e}")
            except Exception as e:
                logger.error(f"Error processing regex pattern {pattern_name} for {lang}: {e}")
        return issues

    def _determine_severity(self, lang: str, pattern_name: str) -> str:
        severity = 'medium'
        if lang == 'php':
            if any(k in pattern_name for k in ['backdoor', 'eval', 'exec', 'system', 'shell_exec', 'passthru', 'popen', 'proc_open']):
                severity = 'high'
            elif any(k in pattern_name for k in ['file_access_006', 'file_access_007', 'file_access_008', 'file_access_009', 'sql_injection']):
                severity = 'high'
        elif lang == 'python':
            if any(k in pattern_name for k in ['eval', 'exec', 'pickle', 'marshal', 'os_system', 'subprocess_shell']):
                severity = 'high'
        elif lang == 'javascript':
            if any(k in pattern_name for k in ['eval', 'Function', 'constructor_call', 'innerHTML', 'document_write']):
                severity = 'high'
        return severity

    def _safe_read_file(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            logger.error(f"Could not read file {file_path}: {e}")
            return None

    def _detect_obfuscation(self, content: str, lang: str) -> List[Dict]:
        """
        Обнаруживает потенциально обфусцированный код.
        
        Args:
            content: Содержимое файла
            lang: Язык программирования ('python', 'javascript', 'php')
            
        Returns:
            Список обнаруженных проблем
        """
        issues = []
        
        # Общие признаки обфусцированного кода
        obfuscation_indicators = {
            'base64_decode': (
                r'base64_decode\s*\(', 
                'Обнаружен вызов base64_decode, часто используемый для скрытия кода',
                'high'
            ),
            'hex_decode': (
                r'(fromCharCode|unhexlify|parseInt.*0x|"\\x|\'\\x|\\u00[0-9a-f]{2})',
                'Обнаружено hex-кодирование символов, может использоваться для обфускации',
                'medium'
            ),
            'long_string': (
                r'["\'](\\.|[^"\'\\]){200,}["\']',
                'Обнаружена подозрительно длинная строка, возможно обфусцированный код',
                'medium'
            ),
            'unusual_names': (
                r'\b[OI0l]{5,}\b',
                'Обнаружены переменные с трудноразличимыми именами (только I, O, 0, l)',
                'medium'
            ),
            'excessive_escaping': (
                r'\\\\\\\\[^"\'\\\\]{2,}',
                'Избыточное экранирование строки, часто используется для обфускации',
                'medium'
            ),
            'eval_with_encoded_content': (
                r'(eval|Function)\s*\(\s*["\'](\\.|[^"\'\\]){20,}["\']\s*\)',
                'Вызов eval/Function с закодированной строкой, возможно обфусцированный код',
                'high'
            ),
        }
        
        # Признаки обфусцированного кода для конкретных языков
        lang_specific_indicators = {
            'python': {
                'exec_with_encoded_content': (
                    r'exec\s*\(\s*["\'](\\.|[^"\'\\]){20,}["\']\s*\)',
                    'Вызов exec с закодированной строкой, возможно обфусцированный код',
                    'high'
                ),
                'chr_sequence': (
                    r'((\(\s*chr\s*\(\s*\d+\s*\)\s*\+\s*)+|(\s*\+\s*chr\s*\(\s*\d+\s*\))+)',
                    'Создание строки из последовательности chr(), часто используется для обфускации',
                    'medium'
                ),
                'encoded_attribute_access': (
                    r'getattr\s*\(\s*\w+\s*,\s*["\'](\\.|[^"\'\\]){1,}["\']\s*\)',
                    'Потенциально скрытый доступ к атрибутам объекта',
                    'low'
                )
            },
            'javascript': {
                'js_obfuscator_patterns': (
                    r'var _0x[a-f0-9]+=',
                    'Обнаружен шаблон, характерный для JavaScript-обфускаторов',
                    'high'
                ),
                'js_string_concatenation': (
                    r'(["\']\s*\+\s*["\']){10,}',
                    'Чрезмерная конкатенация строк, часто используется в обфусцированном коде',
                    'medium'
                ),
                'js_eval_with_function': (
                    r'eval\s*\(\s*function\s*\(.*\)\s*{.*return.*}\s*\(\s*\)\s*\)',
                    'Вызов eval с функцией, возвращающей код, классический признак обфускации',
                    'high'
                ),
                'js_string_array_access': (
                    r'\[["\'][^"\']*["\']\]\s*\[["\'][^"\']*["\']\]',
                    'Доступ к элементам массива через индексы в строковом формате, часто используется в обфусцированном коде',
                    'medium'
                )
            },
            'php': {
                'php_encoded_functions': (
                    r'(\$\{.{1,10}\}|\$[a-zA-Z0-9_]+)\s*\(\s*[\'"](\\.|[^\'"]){20,}[\'"]\s*\)',
                    'Вызов динамически определяемой функции с закодированной строкой',
                    'high'
                ),
                'php_complex_variable_vars': (
                    r'\$\$\{.{1,30}\}|\$\$\$.{1,20}',
                    'Сложное использование переменных переменных, часто для обфускации',
                    'medium'
                ),
                'php_create_function': (
                    r'create_function\s*\(\s*[\'"].*[\'"]\s*,\s*[\'"].*[\'"]\s*\)',
                    'Использование create_function с закодированными строками',
                    'high'
                )
            }
        }
        
        # Добавляем индикаторы, специфичные для языка
        specific_indicators = lang_specific_indicators.get(lang, {})
        all_indicators = {**obfuscation_indicators, **specific_indicators}
        
        # Проверяем все индикаторы
        for name, (pattern, message, severity) in all_indicators.items():
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
            if matches:
                for match in matches:
                    # Вычисляем номер строки
                    line_number = content[:match.start()].count('\n') + 1
                    match_text = match.group()
                    display_match = match_text[:MAX_MATCH_LENGTH] + ('...' if len(match_text) > MAX_MATCH_LENGTH else '')
                    
                    issues.append({
                        'line': line_number,
                        'type': 'obfuscation',
                        'message': f"{message}: {Colors.format(display_match, 'dim')}",
                        'severity': severity
                    })
        
        return issues

    def analyze_python_file(self, file_path: str, use_pylint: bool = False) -> List[Dict]:
        issues = []
        content = self._safe_read_file(file_path)
        if content is None:
            return [{'file': file_path, 'line': 0, 'type': 'file-error', 
                    'message': f"Could not read file: {file_path}", 'severity': 'low'}]

        try:
            with suppress_stdout():
                b_config = config.BanditConfig()
                b_mgr = manager.BanditManager(config=b_config, agg_type='file')
                b_mgr.discover_files([file_path], recursive=False)
                b_mgr.run_tests()

                for issue_raw in b_mgr.get_issue_list():
                    issues.append({
                        'file': file_path,
                        'line': issue_raw.lineno,
                        'type': 'bandit',
                        'message': issue_raw.text,
                        'severity': str(issue_raw.severity).lower()
                    })
        except Exception as e:
            logger.error(f"Bandit analysis failed for {file_path}: {e}")
            issues.append({
                'file': file_path,
                'line': 0,
                'type': 'bandit-error',
                'message': f"Bandit analysis failed: {str(e)[:100]}",
                'severity': 'low'
            })

        if use_pylint:
            issues.extend(self._run_pylint_analysis(file_path))

        issues.extend(self._analyze_with_regex(file_path, content, 'python'))

        # Добавляем проверку на обфусцированный код
        obfuscation_issues = self._detect_obfuscation(content, 'python')
        for issue in obfuscation_issues:
            issue['file'] = file_path
        issues.extend(obfuscation_issues)

        return issues

    def _run_pylint_analysis(self, file_path: str) -> List[Dict]:
        issues = []
        try:
            cmd = [
                sys.executable, "-m", "pylint",
                file_path,
                "--disable=all",
                "--enable=exec-used,eval-used",
                "--output-format=json",
                "--msg-template={line}:{column}:{C}:{msg_id}:{msg}"
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                encoding='utf-8',
                errors='ignore'
            )

            if result.stdout:
                try:
                    pylint_data = json.loads(result.stdout) if result.stdout.startswith('[') else \
                        [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
                    
                    for msg in pylint_data:
                        msg_text, symbol = msg.get('message', '').lower(), msg.get('symbol', '').lower()
                        if 'exec' in msg_text or 'eval' in msg_text or 'exec-used' in symbol or 'eval-used' in symbol:
                            issues.append({
                                'file': file_path,
                                'line': msg.get('line', 0),
                                'type': 'pylint',
                                'message': f"Pylint ({msg.get('symbol', 'N/A')}): {msg.get('message', 'Error')}",
                                'severity': 'high'
                            })
                except json.JSONDecodeError:
                    if "Your code has been rated at" not in result.stdout:
                        logger.error(f"Pylint JSON decode error. Output: {result.stdout[:80]}...")

            if result.returncode != 0 and result.stderr and "Your code has been rated at" not in result.stderr:
                logger.error(f"Pylint failed (code {result.returncode}): {result.stderr[:80]}...")

        except subprocess.TimeoutExpired:
            logger.warning(f"Pylint timed out for {file_path}")
            issues.append({
                'file': file_path,
                'line': 0,
                'type': 'pylint-error',
                'message': "Pylint timed out (60s).",
                'severity': 'low'
            })
        except Exception as e:
            logger.error(f"Pylint run error for {file_path}: {e}")
            issues.append({
                'file': file_path,
                'line': 0,
                'type': 'pylint-error',
                'message': f"Pylint run error: {str(e)[:100]}",
                'severity': 'low'
            })
        return issues

    def analyze_js_file(self, file_path: str) -> List[Dict]:
        issues = []
        content = self._safe_read_file(file_path)
        if content is None:
            return [{'file': file_path, 'line': 0, 'type': 'file-error', 
                    'message': f"Could not read file: {file_path}", 'severity': 'low'}]

        try:
            ast = esprima.parseScript(content, options={'loc': True})
            if hasattr(ast, 'body'):
                for node in ast.body:
                    if (hasattr(node, 'type') and node.type == 'CallExpression' and
                            hasattr(node, 'callee') and hasattr(node.callee, 'name') and
                            node.callee.name in ['eval', 'Function']):
                        line = node.loc.start.line if node.loc and hasattr(node.loc, 'start') else 0
                        issues.append({
                            'file': file_path,
                            'line': line,
                            'type': 'esprima-ast',
                            'message': f"Suspicious call to {Colors.format(node.callee.name, 'bold')}",
                            'severity': 'high'
                        })
        except esprima.Error as e:
            logger.error(f"JS parsing failed for {file_path}: {e}")
            issues.append({
                'file': file_path,
                'line': getattr(e, 'lineNumber', 0),
                'type': 'esprima-error',
                'message': f"JS parsing failed: {getattr(e, 'description', str(e))}",
                'severity': 'low'
            })
        except Exception as e:
            logger.error(f"Esprima analysis error for {file_path}: {e}")
            issues.append({
                'file': file_path,
                'line': 0,
                'type': 'esprima-error',
                'message': f"Esprima analysis error: {str(e)[:100]}",
                'severity': 'low'
            })

        issues.extend(self._analyze_with_regex(file_path, content, 'javascript'))

        # Добавляем проверку на обфусцированный код
        obfuscation_issues = self._detect_obfuscation(content, 'javascript')
        for issue in obfuscation_issues:
            issue['file'] = file_path
        issues.extend(obfuscation_issues)

        return issues

    def analyze_php_file(self, file_path: str) -> List[Dict]:
        issues = []
        content = self._safe_read_file(file_path)
        if content is None:
            return [{'file': file_path, 'line': 0, 'type': 'file-error', 
                    'message': f"Could not read file: {file_path}", 'severity': 'low'}]
        
        issues.extend(self._analyze_with_regex(file_path, content, 'php'))

        # Добавляем проверку на обфусцированный код
        obfuscation_issues = self._detect_obfuscation(content, 'php')
        for issue in obfuscation_issues:
            issue['file'] = file_path
        issues.extend(obfuscation_issues)

        return issues

    def _collect_files_to_scan(self, path_to_scan: str) -> List[str]:
        files = []
        path = Path(path_to_scan)
        
        if path.is_file():
            if path.suffix in SUPPORTED_EXTENSIONS:
                files.append(str(path))
            else:
                logger.info(f"File {path_to_scan} is not a supported type. Skipping.")
        elif path.is_dir():
            for file_path in path.rglob('*'):
                if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
                    files.append(str(file_path))
        else:
            logger.error(f"Path {path_to_scan} does not exist or is invalid.")
        
        return files

    def _analyze_dependencies(self, file_path: str, file_type: str = None) -> List[Dict]:
        """
        Анализирует файлы зависимостей на наличие потенциально вредоносных пакетов.
        
        Args:
            file_path: Путь к файлу зависимостей
            file_type: Тип файла зависимостей ('requirements', 'package.json', 'composer.json')
        
        Returns:
            Список обнаруженных проблем
        """
        if not os.path.exists(file_path):
            logger.error(f"Dependencies file not found: {file_path}")
            return []
        
        issues = []
        
        # Определяем тип файла, если не указан
        if file_type is None:
            filename = os.path.basename(file_path).lower()
            if 'requirements' in filename and filename.endswith('.txt'):
                file_type = 'requirements'
            elif filename == 'package.json':
                file_type = 'package.json'
            elif filename == 'composer.json':
                file_type = 'composer.json'
            else:
                logger.warning(f"Unknown dependencies file type: {file_path}")
                return []
        
        # Загружаем базу данных вредоносных пакетов
        malicious_packages = self._load_malicious_packages()
        
        try:
            content = self._safe_read_file(file_path)
            if content is None:
                return []
            
            # Анализируем в зависимости от типа файла
            if file_type == 'requirements':
                # Анализ requirements.txt или похожих файлов
                for line_num, line in enumerate(content.splitlines(), 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Извлекаем имя пакета
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('~=')[0].strip()
                    
                    # Проверяем, есть ли пакет в базе вредоносных
                    if package_name.lower() in malicious_packages:
                        info = malicious_packages[package_name.lower()]
                        issues.append({
                            'file': file_path,
                            'line': line_num,
                            'type': 'malicious-package',
                            'message': f"Потенциально вредоносный пакет: {package_name} - {info['reason']}",
                            'severity': info['severity']
                        })
                    
            elif file_type == 'package.json':
                # Анализ package.json для Node.js проектов
                try:
                    package_data = json.loads(content)
                    all_dependencies = {}
                    
                    # Собираем зависимости из разных секций
                    if 'dependencies' in package_data:
                        all_dependencies.update(package_data['dependencies'])
                    if 'devDependencies' in package_data:
                        all_dependencies.update(package_data['devDependencies'])
                    if 'optionalDependencies' in package_data:
                        all_dependencies.update(package_data['optionalDependencies'])
                    
                    # Проверяем каждую зависимость
                    for package_name in all_dependencies:
                        if package_name.lower() in malicious_packages:
                            info = malicious_packages[package_name.lower()]
                            issues.append({
                                'file': file_path,
                                'line': 0,  # JSON не сохраняет информацию о строках
                                'type': 'malicious-package',
                                'message': f"Потенциально вредоносный пакет: {package_name} - {info['reason']}",
                                'severity': info['severity']
                            })
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in package.json: {file_path}")
                    
            elif file_type == 'composer.json':
                # Анализ composer.json для PHP проектов
                try:
                    composer_data = json.loads(content)
                    all_dependencies = {}
                    
                    if 'require' in composer_data:
                        all_dependencies.update(composer_data['require'])
                    if 'require-dev' in composer_data:
                        all_dependencies.update(composer_data['require-dev'])
                    
                    # Проверяем каждую зависимость
                    for package_name in all_dependencies:
                        if package_name.lower() in malicious_packages:
                            info = malicious_packages[package_name.lower()]
                            issues.append({
                                'file': file_path,
                                'line': 0,  # JSON не сохраняет информацию о строках
                                'type': 'malicious-package',
                                'message': f"Потенциально вредоносный пакет: {package_name} - {info['reason']}",
                                'severity': info['severity']
                            })
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in composer.json: {file_path}")
        
        except Exception as e:
            logger.error(f"Error analyzing dependencies file {file_path}: {str(e)}")
        
        return issues

    def _load_malicious_packages(self) -> Dict:
        """
        Загружает базу данных потенциально вредоносных пакетов.
        
        В будущем может быть обновлена для загрузки из внешнего источника 
        или локальной базы данных.
        
        Returns:
            Словарь вредоносных пакетов с информацией о них
        """
        # Список известных вредоносных пакетов или тех, которые имитируют популярные пакеты
        # В реальном приложении это должна быть база данных, регулярно обновляемая
        return {
            # Python пакеты
            "requests3": {
                "reason": "Тайпосквоттинг пакета 'requests'",
                "severity": "medium"
            },
            "django-backend": {
                "reason": "Пакет не связан с официальным Django",
                "severity": "medium"
            },
            "crypt": {
                "reason": "Может содержать вредоносный код, имитирует криптографические библиотеки",
                "severity": "high"
            },
            "flask-email": {
                "reason": "Не является официальным расширением Flask, подозрительная активность",
                "severity": "medium"
            },
            "setup-tools": {
                "reason": "Тайпосквоттинг пакета 'setuptools'",
                "severity": "medium"
            },
            
            # Node.js пакеты
            "crossenv": {
                "reason": "Тайпосквоттинг пакета 'cross-env'",
                "severity": "high"
            },
            "loadyaml": {
                "reason": "Тайпосквоттинг пакета 'js-yaml'",
                "severity": "medium"
            },
            "mongodb": {
                "reason": "Может содержать вредоносный код, не является официальной библиотекой",
                "severity": "high"
            },
            "express-parser": {
                "reason": "Не является официальным пакетом экосистемы Express",
                "severity": "medium"
            },
            
            # PHP пакеты
            "symfony/symfony2": {
                "reason": "Тайпосквоттинг пакета 'symfony/symfony'",
                "severity": "medium"
            },
            "laravel/installer-next": {
                "reason": "Не является официальным пакетом Laravel",
                "severity": "medium"
            }
        }

    def scan(self, path_to_scan: str, use_pylint: bool = False, use_multiprocessing: bool = True, max_workers: int = None, check_dependencies: bool = True) -> List[Dict]:
        """
        Сканирует указанный путь на наличие потенциальных бэкдоров.
        
        Args:
            path_to_scan: Путь к файлу или директории для сканирования
            use_pylint: Использовать pylint для проверки Python-файлов
            use_multiprocessing: Использовать многопоточную обработку
            max_workers: Максимальное количество рабочих потоков
            check_dependencies: Проверять файлы зависимостей
            
        Returns:
            Список обнаруженных проблем
        """
        logger.info(f"Starting scan for: {path_to_scan}")
        all_issues = []
        files_to_process = self._collect_files_to_scan(path_to_scan)
        
        # Отфильтруем игнорируемые файлы
        files_to_process = [f for f in files_to_process if not self.should_ignore_file(f)]

        if not files_to_process:
            if Path(path_to_scan).is_dir():
                logger.info(f"No supported files found in {path_to_scan}")
            return all_issues

        # Проверка файлов зависимостей
        if check_dependencies and Path(path_to_scan).is_dir():
            dependency_files = [
                (os.path.join(path_to_scan, 'requirements.txt'), 'requirements'),
                (os.path.join(path_to_scan, 'package.json'), 'package.json'),
                (os.path.join(path_to_scan, 'composer.json'), 'composer.json')
            ]
            
            for dep_file, file_type in dependency_files:
                if os.path.exists(dep_file):
                    logger.info(f"Analyzing dependencies in {os.path.basename(dep_file)}...")
                    dep_issues = self._analyze_dependencies(dep_file, file_type)
                    all_issues.extend(dep_issues)
                
        try:
            # Обеспечиваем наличие tqdm
            tqdm = tqdm_lib
        except ImportError:
            logger.warning("tqdm library not found. Progress bar will be basic.")
            tqdm = lambda x, **kwargs: x

        if use_multiprocessing and len(files_to_process) > 1:
            # Используем многопоточность для обработки файлов
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for file_path in files_to_process:
                    if file_path.endswith('.py'):
                        futures.append(executor.submit(self.analyze_python_file, file_path, use_pylint))
                    elif file_path.endswith('.js'):
                        futures.append(executor.submit(self.analyze_js_file, file_path))
                    elif file_path.endswith('.php'):
                        futures.append(executor.submit(self.analyze_php_file, file_path))
                
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scanning", unit="file"):
                    all_issues.extend(future.result())
        else:
            # Последовательное сканирование
            for file_path in tqdm(files_to_process, desc="Scanning", unit="file"):
                display_name = Path(file_path).name
                if len(display_name) > MAX_DISPLAY_LENGTH:
                    display_name = "..." + display_name[-(MAX_DISPLAY_LENGTH - 3):]
                logger.info(f"Scanning {display_name}")

                current_issues = []
                if file_path.endswith('.py'):
                    current_issues = self.analyze_python_file(file_path, use_pylint)
                elif file_path.endswith('.js'):
                    current_issues = self.analyze_js_file(file_path)
                elif file_path.endswith('.php'):
                    current_issues = self.analyze_php_file(file_path)

                all_issues.extend(current_issues)

        seen = set()
        final_issues = []
        for issue in all_issues:
            raw_message = re.sub(r'\033\[[0-9;]*m', '', issue['message'])
            key = (issue['file'], issue['line'], issue['type'].split('-')[0], raw_message[:30].lower())
            if key not in seen:
                seen.add(key)
                final_issues.append(issue)

        return final_issues
        
    def export_to_json(self, issues: List[Dict], output_file: str) -> bool:
        """
        Экспортирует результаты сканирования в JSON-файл.
        
        Args:
            issues: Список обнаруженных проблем
            output_file: Путь к файлу для сохранения результатов
            
        Returns:
            True в случае успеха, False в случае ошибки
        """
        try:
            # Подготовим данные, удаляя ANSI-последовательности цветов
            clean_issues = []
            for issue in issues:
                clean_issue = issue.copy()
                if 'message' in clean_issue:
                    clean_issue['message'] = re.sub(r'\033\[[0-9;]*m', '', clean_issue['message'])
                clean_issues.append(clean_issue)
                
            # Создаем структуру отчета
            report = {
                'scan_time': logging.Formatter().converter(),
                'issues_count': len(clean_issues),
                'issues_by_severity': {
                    'critical': len([i for i in clean_issues if i.get('severity') == 'critical']),
                    'high': len([i for i in clean_issues if i.get('severity') == 'high']),
                    'medium': len([i for i in clean_issues if i.get('severity') == 'medium']),
                    'low': len([i for i in clean_issues if i.get('severity') == 'low'])
                },
                'issues': clean_issues
            }
            
            # Записываем в файл
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Results exported to JSON file: {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to export results to JSON: {e}")
            return False

def main():
    if sys.platform == "win32" and sys.stdout.isatty():
        os.system("")

    if not PATTERNS or not any(PATTERNS.values()):
        logger.critical("No patterns were loaded. Ensure 'patterns.json' or 'patterns.py' is correctly placed and readable.")
        sys.exit(3)

    logger.info("--- Backdoor Detector ---")

    parser = argparse.ArgumentParser(
        description="Scans for potential backdoors in Python, JS, and PHP code."
    )
    parser.add_argument('path', help="File or directory path to scan.")
    parser.add_argument('--use-pylint', action='store_true', help="Enable Pylint for Python files (can be slow).")
    parser.add_argument('--min-severity', type=str, default='low',
                       choices=['low', 'medium', 'high', 'critical'],
                       help="Minimum issue severity to display (default: low).")
    # Добавляем новые аргументы
    parser.add_argument('--output-format', type=str, choices=['text', 'json'], default='text',
                      help="Output format (default: text)")
    parser.add_argument('--output-file', type=str, help="Output file path for reports")
    parser.add_argument('--ignore-file', type=str, help=f"Path to ignore file (default: {IGNORE_FILE})")
    parser.add_argument('--no-multiprocessing', action='store_true', help="Disable multiprocessing")
    parser.add_argument('--max-workers', type=int, help="Maximum number of worker threads for multiprocessing")
    parser.add_argument('--no-check-dependencies', action='store_true', 
                      help="Skip checking dependency files like requirements.txt, package.json, composer.json")
    
    args = parser.parse_args()

    try:
        detector = BackdoorDetector()
        
        # Загружаем правила игнорирования
        if args.ignore_file:
            detector.load_ignore_file(args.ignore_file)
            
        # Запускаем сканирование
        issues = detector.scan(
            args.path, 
            use_pylint=args.use_pylint,
            use_multiprocessing=not args.no_multiprocessing,
            max_workers=args.max_workers,
            check_dependencies=not args.no_check_dependencies
        )

        min_sev_level = SEVERITY_ORDER.get(args.min_severity.lower(), 1)
        filtered_issues = [
            iss for iss in issues
            if SEVERITY_ORDER.get(str(iss['severity']).lower(), 0) >= min_sev_level
        ]
        
        filtered_issues.sort(
            key=lambda x: (
                SEVERITY_ORDER.get(str(x['severity']).lower(), 0),
                x['file'],
                x['line']
            ),
            reverse=True
        )

        if not filtered_issues:
            logger.info(f"No issues found (or above severity: {args.min_severity}).")
        else:
            if args.output_format == 'json':
                output_file = args.output_file or f"bac_detect_results_{Path(args.path).name}.json"
                detector.export_to_json(filtered_issues, output_file)
            else:
                logger.info(f"Scan Results ({len(filtered_issues)} issues):")
                for issue in filtered_issues:
                    sev = str(issue['severity'])
                    colored_sev = Colors.format(f"[{sev.upper()}]", sev)

                    file_disp = issue['file']
                    if len(file_disp) > MAX_DISPLAY_LENGTH:
                        file_disp = "..." + file_disp[-(MAX_DISPLAY_LENGTH - 3):]

                    type_str_raw = f"({issue['type']})"
                    colored_type = Colors.format(type_str_raw, 'dim')
                    file_line_str = f"{Colors.format(file_disp, 'bold')}:{Colors.format(str(issue['line']), 'bold')}"

                    print(f"{colored_sev} {file_line_str} {colored_type}: {issue['message']}")

    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {str(e)}")
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()