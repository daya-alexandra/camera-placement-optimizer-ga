import json
from pathlib import Path

import numpy as np

GRID_SIZE = 100
WALL = 1
FREE = 0
IMPORTANT = 2
K = 10
R = 12
N_POINTS = 150
SEED = 42

ROOMS = [
    ("Кабинет 1", 0, 0, 28, 24),
    ("Кабинет 2", 0, 24, 28, 48),
    ("Кабинет 3", 0, 51, 28, 75),
    ("Кабинет 4", 0, 75, 28, 99),
    ("Большой зал", 35, 0, 65, 48),
    ("Переговорная", 35, 51, 65, 75),
    ("Открытый офис", 35, 75, 65, 99),
    ("Склад А", 71, 0, 99, 24),
    ("Склад Б", 71, 24, 99, 48),
    ("Серверная", 71, 51, 99, 75),
    ("Техпомещение", 71, 75, 99, 99),
]

ROOM_LABELS = {name: ((r1 + r2) // 2, (c1 + c2) // 2) for name, r1, c1, r2, c2 in ROOMS}

DOORWAYS = [
    ("h", 28, 10),
    ("h", 28, 35),
    ("h", 28, 60),
    ("h", 28, 85),
    ("h", 35, 15),
    ("h", 35, 35),
    ("h", 35, 60),
    ("h", 35, 85),
    ("h", 65, 20),
    ("h", 65, 35),
    ("h", 65, 60),
    ("h", 65, 85),
    ("h", 71, 10),
    ("h", 71, 35),
    ("h", 71, 60),
    ("h", 71, 85),
    ("v", 48, 13),
    ("v", 51, 13),
    ("v", 48, 50),
    ("v", 51, 50),
    ("v", 48, 83),
    ("v", 51, 83),
]

IMPORTANT_AREAS = [
    (0, 0, 28, 99),
    (35, 51, 65, 99),
    (71, 51, 99, 75),
]


def _in_important_area(r, c) -> bool:
    return any(r1 <= r <= r2 and c1 <= c <= c2 for r1, c1, r2, c2 in IMPORTANT_AREAS)


def generate_map() -> np.ndarray:
    g = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int8)

    for _, r1, c1, r2, c2 in ROOMS:
        g[r1, c1 : c2 + 1] = WALL
        g[r2, c1 : c2 + 1] = WALL
        g[r1 : r2 + 1, c1] = WALL
        g[r1 : r2 + 1, c2] = WALL

    for kind, pos, start in DOORWAYS:
        if kind == "h":
            g[pos, start : start + 4] = FREE
        else:
            g[start : start + 4, pos] = FREE

    rng = np.random.default_rng(SEED)
    free = np.argwhere(g == FREE)
    important_free = np.array([(r, c) for r, c in free if _in_important_area(r, c)])
    other_free = np.array([(r, c) for r, c in free if not _in_important_area(r, c)])
    n_priority = int(N_POINTS * 0.7)

    priority_idx = rng.choice(len(important_free), size=n_priority, replace=False)
    other_idx = rng.choice(len(other_free), size=N_POINTS - n_priority, replace=False)
    points = np.vstack([important_free[priority_idx], other_free[other_idx]])

    for r, c in points:
        g[r, c] = IMPORTANT

    return g


def save_map(path="data/map.json") -> np.ndarray:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    grid = generate_map()
    n_wall = int((grid == WALL).sum())
    n_imp = int((grid == IMPORTANT).sum())
    payload = {
        "grid_size": GRID_SIZE,
        "K": K,
        "R": R,
        "n_walls": n_wall,
        "n_points": n_imp,
        "legend": "0=пустота, 1=стена, 2=важная точка",
        "grid": ["".join(map(str, row)) for row in grid],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Карта → {path}  K={K}  R={R}  стен={n_wall}  важных точек={n_imp}")
    return grid


def load_map(path="data/map.json") -> np.ndarray:
    if not Path(path).exists():
        return save_map(path)
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    rows = d["grid"]
    if rows and isinstance(rows[0], str):
        return np.array([[int(ch) for ch in row] for row in rows], dtype=np.int8)
    return np.array(rows, dtype=np.int8)


if __name__ == "__main__":
    save_map("data/map.json")
