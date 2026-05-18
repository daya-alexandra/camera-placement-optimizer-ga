import numpy as np

W_COV, W_OVERLAP, W_INVALID = 100, 20, 1000
WALL, IMPORTANT = 1, 2


def has_los(grid, r1, c1, r2, c2) -> bool:
    """True, если от (r1, c1) до (r2, c2) нет стены на линии обзора."""
    steps = int(max(abs(r2 - r1), abs(c2 - c1)) * 2) + 1
    rows = np.rint(np.linspace(r1, r2, steps)).astype(int)
    cols = np.rint(np.linspace(c1, c2, steps)).astype(int)
    return not np.any(grid[rows, cols] == WALL)


def visible_cells(grid, camera_r, camera_c, R):
    """Клетки, которые видит одна камера."""
    n = grid.shape[0]
    visible = []

    for r in range(max(0, camera_r - R), min(n, camera_r + R + 1)):
        for c in range(max(0, camera_c - R), min(n, camera_c + R + 1)):
            in_range = (r - camera_r) ** 2 + (c - camera_c) ** 2 <= R**2
            if in_range and has_los(grid, camera_r, camera_c, r, c):
                visible.append((r, c))

    return visible


def compute_score(cameras, grid, R=10):
    """Оценить расстановку камер: чем выше score, тем лучше."""
    n = grid.shape[0]
    coverage = np.zeros((n, n), dtype=np.int32)
    invalid = 0

    for camera_r, camera_c in cameras:
        camera_r, camera_c = int(camera_r), int(camera_c)
        camera_inside = 0 <= camera_r < n and 0 <= camera_c < n

        if not camera_inside or grid[camera_r, camera_c] == WALL:
            invalid += 1
            continue

        for r, c in visible_cells(grid, camera_r, camera_c, R):
            coverage[r, c] += 1

    important_points = np.argwhere(grid == IMPORTANT)
    covered_points = int(np.sum(coverage[important_points[:, 0], important_points[:, 1]] >= 1))
    overlap = int(np.sum(coverage >= 2))
    score = W_COV * covered_points - W_OVERLAP * overlap - W_INVALID * invalid

    return score, {
        "cov": covered_points,
        "overlap": overlap,
        "invalid": invalid,
        "score": score,
    }
