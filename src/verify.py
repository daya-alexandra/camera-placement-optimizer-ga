import numpy as np

from src.map_tools.generator import FREE, IMPORTANT, K, R, load_map
from src.scoring import compute_score, has_los


def random_baseline(grid, n_runs=100, seed=7):
    rng = np.random.default_rng(seed)
    free = np.argwhere(grid == FREE)
    scores = []

    for _ in range(n_runs):
        idx = rng.choice(len(free), size=K, replace=False)
        cameras = [(int(r), int(c)) for r, c in free[idx]]
        score, _ = compute_score(cameras, grid, R=R)
        scores.append(score)

    return float(np.mean(scores)), int(np.max(scores))


def greedy_by_coverage(grid):
    free = np.argwhere(grid == FREE)
    points = np.argwhere(grid == IMPORTANT)
    visible = []

    for cr, cc in free:
        seen = set()
        for i, (pr, pc) in enumerate(points):
            in_range = (pr - cr) ** 2 + (pc - cc) ** 2 <= R**2
            if in_range and has_los(grid, cr, cc, pr, pc):
                seen.add(i)
        visible.append(seen)

    chosen = []
    covered = set()
    available = set(range(len(free)))

    for _ in range(K):
        best_i = max(available, key=lambda i: len(visible[i] - covered))
        chosen.append((int(free[best_i][0]), int(free[best_i][1])))
        covered.update(visible[best_i])
        available.remove(best_i)

    score, _ = compute_score(chosen, grid, R=R)
    return score


def main():
    grid = load_map("data/map.json")
    random_avg, random_max = random_baseline(grid)
    greedy_score = greedy_by_coverage(grid)

    print("Verification")
    print(f"random_avg={random_avg:.2f}")
    print(f"random_max={random_max}")
    print(f"greedy={greedy_score}")
    print(f"gap={greedy_score - random_avg:.2f}")


if __name__ == "__main__":
    main()
