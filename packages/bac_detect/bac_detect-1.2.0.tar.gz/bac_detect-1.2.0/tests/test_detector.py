import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Добавляем путь к исходным файлам
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from bac_detect.backdoor_detector import BackdoorDetector, Colors, load_patterns


class TestBackdoorDetector(unittest.TestCase):
    def setUp(self):
        self.detector = BackdoorDetector()
        
    def test_analyze_with_regex(self):
        # Тестируем обнаружение шаблонов в Python-коде
        content = """
def dangerous_function():
    user_input = input("Enter command: ")
    eval(user_input)  # This is dangerous
    
    # Another dangerous pattern
    exec(f"print({user_input})")
"""
        
        # Мокаем patterns для теста
        test_patterns = {
            "eval_usage": r"eval\s*\(",
            "exec_usage": r"exec\s*\("
        }
        
        with patch.object(self.detector, 'patterns', {'python': test_patterns}):
            issues = self.detector._analyze_with_regex('test.py', content, 'python')
            
            # Проверяем, что обнаружены обе проблемы
            self.assertEqual(len(issues), 2)
            self.assertIn('eval_usage', issues[0]['message'])
            self.assertIn('exec_usage', issues[1]['message'])
    
    def test_detect_obfuscation(self):
        # Тестируем обнаружение обфусцированного кода
        obfuscated_js = """
var _0x1a2b = ['value', 'fromCharCode', 'createElement', 'appendChild'];
function deobfuscate() {
    eval(String.fromCharCode(97, 108, 101, 114, 116, 40, 49, 41));
}
"""
        issues = self.detector._detect_obfuscation(obfuscated_js, 'javascript')
        
        # Проверяем обнаружение обфускации
        self.assertGreater(len(issues), 0)
        
        # Проверяем типы обнаруженных проблем
        for issue in issues:
            self.assertEqual(issue['type'], 'obfuscation')
    
    def test_analyze_dependencies(self):
        # Создаем временный файл requirements.txt с вредоносным пакетом
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp:
            temp.write("""
# Test requirements file
requests>=2.25.0
crypt==1.0.0  # Вредоносный пакет
flask==2.0.0
""")
            temp_path = temp.name
        
        try:
            # Анализируем файл
            issues = self.detector._analyze_dependencies(temp_path, 'requirements')
            
            # Проверяем, найден ли вредоносный пакет
            self.assertEqual(len(issues), 1)
            self.assertIn('crypt', issues[0]['message'])
            self.assertEqual(issues[0]['severity'], 'high')
        finally:
            # Удаляем временный файл
            os.unlink(temp_path)
    
    def test_export_to_json(self):
        # Тестируем экспорт в JSON
        issues = [
            {
                'file': 'test.py',
                'line': 10,
                'type': 'bandit',
                'message': 'Test issue 1',
                'severity': 'high'
            },
            {
                'file': 'test.js',
                'line': 5,
                'type': 'esprima-ast',
                'message': 'Test issue 2',
                'severity': 'medium'
            }
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Экспортируем issues в JSON
            result = self.detector.export_to_json(issues, temp_path)
            self.assertTrue(result)
            
            # Проверяем содержимое экспортированного файла
            with open(temp_path, 'r') as f:
                exported_data = json.load(f)
            
            self.assertEqual(exported_data['issues_count'], 2)
            self.assertEqual(exported_data['issues_by_severity']['high'], 1)
            self.assertEqual(exported_data['issues_by_severity']['medium'], 1)
            self.assertEqual(len(exported_data['issues']), 2)
        finally:
            # Удаляем временный файл
            os.unlink(temp_path)
    
    def test_ignore_file(self):
        # Создаем временный файл .bac_detectignore
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write("""
# Test ignore file
pattern:eval_usage
test_ignored_file.py
*.min.js
""")
            temp_path = temp.name
        
        try:
            # Загружаем правила игнорирования
            detector = BackdoorDetector()
            detector.load_ignore_file(temp_path)
            
            # Проверяем игнорирование шаблона
            self.assertTrue(detector.should_ignore_pattern('eval_usage'))
            self.assertFalse(detector.should_ignore_pattern('exec_usage'))
            
            # Проверяем игнорирование файла
            self.assertTrue(detector.should_ignore_file('test_ignored_file.py'))
            self.assertTrue(detector.should_ignore_file('jquery.min.js'))
            self.assertFalse(detector.should_ignore_file('normal_file.py'))
        finally:
            # Удаляем временный файл
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
