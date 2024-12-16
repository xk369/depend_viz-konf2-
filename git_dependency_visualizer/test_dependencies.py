import unittest
from unittest.mock import patch, MagicMock, mock_open
from main import (
    parse_arguments,
    collect_file_dependencies,
    generate_dot_file,
    generate_graph
)
import subprocess

class TestDependencyVisualizer(unittest.TestCase):
    """Тесты для модуля визуализации зависимостей."""

    def setUp(self):
        """Настройка окружения перед каждым тестом."""
        self.test_args = ["--repo-path", "/fake/repo", "--graphviz-path", "/usr/local/bin/dot"]
        self.mock_dependencies = {"file1": {"file2"}, "file2": {"file1"}}
        self.mock_dot_content = 'digraph G {\n    "file1" -> "file2";\n    "file2" -> "file1";\n}\n'

    def test_parse_arguments(self):
        """Тест: корректный парсинг аргументов командной строки."""
        with patch("argparse._sys.argv", ["main.py"] + self.test_args):
            args = parse_arguments()
            self.assertEqual(args.repo_path, "/fake/repo")
            self.assertEqual(args.graphviz_path, "/usr/local/bin/dot")

    def test_collect_file_dependencies(self):
        """Тест: сбор зависимостей файлов с использованием моков git.Repo."""
        with patch("git.Repo") as MockRepo:
            mock_repo = MockRepo.return_value
            mock_commit = MagicMock()
            mock_commit.tree.traverse.return_value = [
                MagicMock(path="file1", type="blob"),
                MagicMock(path="file2", type="blob")
            ]
            mock_repo.iter_commits.return_value = [mock_commit]

            result = collect_file_dependencies("/fake/repo")
            self.assertEqual(result, self.mock_dependencies)

    def test_generate_dot_file(self):
        """Тест: генерация корректного DOT-файла."""
        with patch("builtins.open", mock_open()) as mock_file:
            generate_dot_file(self.mock_dependencies, "output.dot")
            mock_file.assert_called_once_with("output.dot", "w")
            mock_file().write.assert_any_call('digraph G {\n')
            mock_file().write.assert_any_call('    "file1" -> "file2";\n')
            mock_file().write.assert_any_call('    "file2" -> "file1";\n')
            mock_file().write.assert_any_call('}\n')

    def test_generate_graph(self):
        """Тест: вызов subprocess для генерации графа через Graphviz."""
        with patch("subprocess.run") as mock_run:
            generate_graph("output.dot", "output.png", "/usr/local/bin/dot")
            mock_run.assert_called_once_with(
                ["/usr/local/bin/dot", "-Tpng", "output.dot", "-o", "output.png"]
            )

    def test_collect_file_dependencies_empty_repo(self):
        """Тест: обработка пустого репозитория."""
        with patch("git.Repo") as MockRepo:
            mock_repo = MockRepo.return_value
            mock_repo.iter_commits.return_value = []  # Нет коммитов
            result = collect_file_dependencies("/empty/repo")
            self.assertEqual(result, {})  # Ожидаем пустой словарь

    def tearDown(self):
        """Очистка после тестов (если нужно)."""
        pass


if __name__ == "__main__":
    unittest.main()
