# Задание 2 (Вариант 13)

Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя. Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление Graphviz. Визуализатор должен выводить результат на экран в виде графического изображения графа. Построить граф зависимостей для коммитов, в узлах которого находятся связи с файлами и папками, представленными уникальными узлами.
Ключами командной строки задаются:
 1)Путь к программе для визуализации графов.
 2)Путь к анализируемому репозиторию.
Все функции визуализатора зависимостей должны быть покрыты тестами.

# Команда для запуска визуализации графа:
``` python3 main.py --repo-path /Users/a1/Desktop/"ВСЕ ПАПКИ ВУЗ"/konfig/git_dependency_visualizer --graphviz-path /usr/local/bin/dot ```

# Результаты запуска:
<img width="1010" alt="image" src="https://github.com/user-attachments/assets/aa1519bc-dc6e-4c4d-a1d1-ffa51af90c79" />


<img width="487" alt="image" src="https://github.com/user-attachments/assets/1687242a-2005-4dca-a388-89a5156fed87" />

# Тестирование


```python3 -m unittest discover -v tests```

# Результат тестирования

<img width="1361" alt="image" src="https://github.com/user-attachments/assets/de3728bc-fcff-4a85-b97b-818125f468e3" />















