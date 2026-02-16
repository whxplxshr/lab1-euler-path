# Поиск Эйлерова Пути — Руководство Пользователя

## Запуск

```powershell
cd c:\Users\Nikita\Documents\Тестировка\lab1
python -m src.main
```

---

## Главное Меню

```
--- Main Menu ---
  1 — Manual input
  2 — Load from JSON file
  0 — Exit
```

- **1** — Ввести граф вручную через консоль
- **2** — Загрузить граф из JSON-файла
- **0** — Выйти из приложения

После выполнения приложение возвращается в главное меню.

---

## Опция 1: Ручной Ввод (Manual Input)

Приложение запрашивает данные шаг за шагом:

```
Enter the number of vertices: 3
  Vertex 1: 1
  Vertex 2: 2
  Vertex 3: 3
Enter the number of edges: 3
  Edge 1 (u v): 1 2
  Edge 2 (u v): 2 3
  Edge 3 (u v): 3 1
```

**Правила:**
- Вершины — это целые числа, вводятся по одной в строке.
- Рёбра вводятся как два целых числа, разделенных пробелом: `u v`.
- Оба конца каждого ребра должны присутствовать в списке вершин.
- Повторяющиеся вершины не допускаются.

---

## Опция 2: JSON Файл

Введите полный путь к файлу `.json`:

```
Enter JSON file path: C:\Users\Nikita\Documents\Тестировка\lab1\samples\triangle.json
```

**Формат JSON:**
```json
{
  "vertices": [1, 2, 3],
  "edges": [[1, 2], [2, 3], [3, 1]]
}
```

---

## Выбор Алгоритма

```
Choose algorithm:
  1 — Hierholzer
  2 — Fleury
```

- **Hierholzer** — более быстрый, использует итеративный DFS с двумя стеками.
- **Fleury** — медленнее, но интуитивно понятен, избегает мостов на каждом шаге.

Оба алгоритма выдают одинаковый Эйлеров путь для одного и того же графа.

---

## Вывод Результатов

```
==================================================
  Algorithm: hierholzer
  Euler path: [1, 2, 3, 1]
  Path length (edges): 3
==================================================

Save result to JSON file? (y/n):
```

Если вы выберете `y`, введите путь к выходному файлу. Результат сохраняется в следующем виде:
```json
{
  "algorithm": "hierholzer",
  "euler_path": [1, 2, 3, 1],
  "path_length": 3
}
```

---

## Примеры Файлов (`samples/`)

| Файл | Тип | Описание |
|------|-----|----------|
| `single_edge.json` | ✅ Путь | 2 вершины, 1 ребро — минимальный граф |
| `simple_path.json` | ✅ Путь | 3 вершины в линию (1-2-3) |
| `triangle.json` | ✅ Цикл | 3 вершины, все связаны (треугольник) |
| `square_circuit.json` | ✅ Цикл | 4 вершины, кольцо (квадрат) |
| `path_graph.json` | ✅ Путь | 4 вершины, 2 нечетной степени |
| `chain_custom_labels.json` | ✅ Путь | 5 вершин (10,20,30,40,50) в линию |
| `pentagon_with_chords.json` | ✅ Путь | 5-вершинный пятиугольник + 2 хорды |
| `two_triangles_circuit.json` | ✅ Цикл | Два треугольника с общей вершиной 3 |
| `star_cycle_circuit.json` | ✅ Цикл | Центр звезды с внешним кольцом |
| `large_circuit.json` | ✅ Цикл | 7 вершин, кольцо + перекрестные ребра |
| `disconnected_no_path.json` | ❌ Ошибка | 2 отдельных ребра — нет Эйлерова пути |
| `complete_k4_no_path.json` | ❌ Ошибка | K₄ — все вершины нечетной степени |

---

## Случаи Ошибок

- **Нет Эйлерова пути** → `ValueError: Graph does not have an Euler path`
- **Файл не найден** → `FileNotFoundError: File not found: ...`
- **Некорректный JSON** → `ValueError: Invalid JSON syntax: ...`
- **Отсутствуют ключи** → `ValueError: Missing required key: 'vertices'`
- **Неверная вершина** → `ValueError: Each vertex must be an integer`

---

## Запуск Автоматических Тестов

Для запуска тестов используйте `pytest` из корневой директории проекта.

**Важно:** Всегда запускайте тесты как модуль (`python -m pytest`), чтобы пакет `src` был найден корректно.

### 1. Запуск Всех Тестов

```powershell
python -m pytest tests/ -v
```

> **Примечание:** Если `tests/test_branch.py` падает при полном запуске, запустите его отдельно (см. ниже).

### 2. Запуск Конкретных Наборов Тестов

**Анализ Граничных Значений (BVA)**
```powershell
python -m pytest tests/test_bva.py -v
```

**Разбиение на Классы Эквивалентности (EP)**
```powershell
python -m pytest tests/test_equivalence.py -v
```

**Покрытие Операторов (Statement Coverage)**
```powershell
python -m pytest tests/test_statement.py -v
```

**Покрытие Ветвей (Branch Coverage)**
```powershell
python -m pytest tests/test_branch.py -v
```

### 3. Проверка Покрытия Кода

Чтобы увидеть отчет о покрытии (требуется `pytest-cov`):

```powershell
python -m pytest tests/ --cov=src --cov-branch --cov-report=term-missing
```

### Устранение Неполадок

- **`ModuleNotFoundError: No module named 'src'`**:
  Убедитесь, что вы запускаете команду из корневой папки (`lab1`) и используете `python -m pytest ...`, а НЕ просто `pytest ...` и не запускаете файл напрямую.

- **Тесты падают с `Exit code: 1`**:
  Прочитайте вывод, чтобы увидеть, какой тест упал. Если `test_branch` падает при полном запуске, запустите его отдельно.
