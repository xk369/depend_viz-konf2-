import os
import sys
import git
import subprocess
from typing import Dict, Set

def parse_arguments():
    """Парсинг аргументов командной строки."""
    import argparse
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей git репозитория")
    parser.add_argument("--repo-path", type=str, help="Путь к анализируемому git репозиторию")
    parser.add_argument("--graphviz-path", type=str, help="Путь к утилите Graphviz (dot)")
    return parser.parse_args()

def collect_file_dependencies(repo_path: str) -> Dict[str, Set[str]]:
    """Собирает зависимости файлов на основе истории коммитов."""
    dependencies = {}
    repo = git.Repo(repo_path)
    
    for commit in repo.iter_commits():
        tree = commit.tree
        files = set()
        for blob in tree.traverse():
            if blob.type == 'blob':
                files.add(blob.path)
        for file in files:
            if file not in dependencies:
                dependencies[file] = set()
            dependencies[file].update(files - {file})
    return dependencies

def generate_dot_file(dependencies: Dict[str, Set[str]], output_file: str):
    """Создаёт DOT-файл для Graphviz."""
    with open(output_file, 'w') as f:
        f.write("digraph G {\n")
        for file, deps in dependencies.items():
            for dep in deps:
                f.write(f'    "{file}" -> "{dep}";\n')
        f.write("}\n")

def generate_graph(dot_file: str, output_image: str, graphviz_path: str):
    """Генерирует изображение графа с помощью Graphviz."""
    subprocess.run([graphviz_path, '-Tpng', dot_file, '-o', output_image])

def main():
    args = parse_arguments()
    if not os.path.exists(args.repo_path):
        print("Ошибка: Указанный путь к репозиторию не существует.")
        sys.exit(1)

    dot_file = "dependencies.dot"
    output_image = "dependencies.png"

    print("Сбор зависимостей...")
    dependencies = collect_file_dependencies(args.repo_path)

    print("Генерация DOT-файла...")
    generate_dot_file(dependencies, dot_file)

    print("Генерация графа зависимостей...")
    generate_graph(dot_file, output_image, args.graphviz_path)

    print(f"Граф зависимостей сохранён в файл: {output_image}")

if __name__ == "__main__":
    main()
