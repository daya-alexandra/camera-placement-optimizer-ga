import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.map_tools.generator import ROOM_LABELS, load_map


def plot_map(grid, save_path="data/map.png"):
    cmap = ListedColormap(["white", "black", "orange"])
    ticks = range(0, grid.shape[0], 10)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title("0=empty, 1=wall, 2=important point")
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.grid(color="lightgray", linewidth=0.3)

    for name, (r, c) in ROOM_LABELS.items():
        ax.text(
            c, r, name, ha="center", va="center", fontsize=7, color="#444", alpha=0.75
        )

    fig.tight_layout()
    fig.savefig(save_path, dpi=120)
    return fig


if __name__ == "__main__":
    plot_map(load_map())
    plt.show()
