"""Remove checkerboard / flat background from login portrait. Preserves subject RGB and size."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(r"C:\Users\tomoa\.cursor\projects\c-HIBARI\assets")
TARGET = ROOT / "public" / "images" / "login" / "misorahibari-mike-image.png"
SOURCE_PATTERN = "*misorahibari-mike-image-c427fb8e*"


def find_source() -> Path:
    matches = sorted(ASSETS.glob(SOURCE_PATTERN))
    if not matches:
        matches = sorted(ASSETS.glob("*misorahibari-mike-image*"))
    if not matches:
        raise FileNotFoundError("Portrait source not found in assets")
    return matches[0]


def flat_bg_mask(rgb: np.ndarray) -> np.ndarray:
    mn = rgb.min(axis=2).astype(np.int16)
    mx = rgb.max(axis=2).astype(np.int16)
    chroma = mx - mn
    return ((mn >= 200) & (chroma <= 12)) | ((mn >= 235) & (chroma <= 6))


def fringe_mask(rgb: np.ndarray) -> np.ndarray:
    mn = rgb.min(axis=2).astype(np.int16)
    mx = rgb.max(axis=2).astype(np.int16)
    chroma = mx - mn
    return (mn >= 205) & (chroma <= 28)


def flood_core(fg_seed: np.ndarray, removable: np.ndarray) -> np.ndarray:
    h, w = fg_seed.shape
    core = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque(
        (int(y), int(x)) for y, x in zip(*np.where(fg_seed))
    )

    while queue:
        y, x = queue.popleft()
        if y < 0 or y >= h or x < 0 or x >= w or visited[y, x]:
            continue
        if removable[y, x]:
            continue
        visited[y, x] = True
        core[y, x] = True
        queue.extend(((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))

    return core


def mic_column_mask(
    rgb: np.ndarray,
    removable: np.ndarray,
    x_min: int = 48,
    x_max: int = 280,
    margin: int = 12,
    max_up: int = 240,
) -> np.ndarray:
    """Keep microphone columns including bright grill above the dark body."""
    h, w, _ = rgb.shape
    dark = rgb.min(axis=2) < 135
    mask = np.zeros((h, w), dtype=bool)

    for x in range(x_min, min(x_max + 1, w)):
        ys = np.where(dark[:, x])[0]
        if ys.size == 0:
            continue
        y0 = max(0, int(ys.min()) - margin)
        y1 = min(h - 1, int(ys.max()) + margin)
        while y0 > 0 and removable[y0 - 1, x] and (int(ys.min()) - y0) < max_up:
            y0 -= 1
        mask[y0 : y1 + 1, x] = True

    return mask


def flood_border_removable(removable: np.ndarray, blocked: np.ndarray) -> np.ndarray:
    h, w = removable.shape
    border = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(w):
        queue.extend(((0, x), (h - 1, x)))
    for y in range(h):
        queue.extend(((y, 0), (y, w - 1)))

    while queue:
        y, x = queue.popleft()
        if y < 0 or y >= h or x < 0 or x >= w or visited[y, x]:
            continue
        if blocked[y, x] or not removable[y, x]:
            continue
        visited[y, x] = True
        border[y, x] = True
        queue.extend(((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))

    return border


def fill_internal_holes(alpha: np.ndarray) -> np.ndarray:
    """Fill enclosed transparent pixels (e.g. gaps inside hair/kimono silhouette)."""
    h, w = alpha.shape
    bg = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    transparent = alpha == 0
    for x in range(w):
        if transparent[0, x]:
            queue.append((0, x))
        if transparent[h - 1, x]:
            queue.append((h - 1, x))
    for y in range(h):
        if transparent[y, 0]:
            queue.append((y, 0))
        if transparent[y, w - 1]:
            queue.append((y, w - 1))

    while queue:
        y, x = queue.popleft()
        if y < 0 or y >= h or x < 0 or x >= w or visited[y, x]:
            continue
        if not transparent[y, x]:
            continue
        visited[y, x] = True
        bg[y, x] = True
        queue.extend(((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))

    holes = transparent & ~bg
    out = alpha.copy()
    out[holes] = 255
    return out


def peel_outer_fringe(subject: np.ndarray, peelable: np.ndarray, passes: int = 3) -> np.ndarray:
    sub = subject.copy()
    h, w = sub.shape

    for _ in range(passes):
        bg = ~sub
        has_bg_neighbor = np.zeros_like(sub, dtype=bool)
        has_bg_neighbor[1:, :] |= sub[1:, :] & bg[:-1, :]
        has_bg_neighbor[:-1, :] |= sub[:-1, :] & bg[1:, :]
        has_bg_neighbor[:, 1:] |= sub[:, 1:] & bg[:, :-1]
        has_bg_neighbor[:, :-1] |= sub[:, :-1] & bg[:, 1:]

        peel = sub & has_bg_neighbor & peelable
        if not peel.any():
            break
        sub[peel] = False

    return sub


def process_portrait(source: Path, target: Path) -> None:
    original = Image.open(source)
    size = original.size
    rgb = np.array(original.convert("RGB"))
    h, w, _ = rgb.shape

    mn = rgb.min(axis=2).astype(np.int16)
    chroma = rgb.max(axis=2).astype(np.int16) - mn
    removable = flat_bg_mask(rgb)
    peelable = removable
    fg_seed = (mn < 175) | (chroma > 18)

    subject_core = flood_core(fg_seed, removable)
    mic_mask = mic_column_mask(rgb, removable)
    protected = subject_core | mic_mask

    bg = flood_border_removable(removable, protected)
    subject = protected | (~removable & ~bg)
    subject = peel_outer_fringe(subject, peelable, passes=3)

    alpha = np.where(subject, 255, 0).astype(np.uint8)
    alpha = fill_internal_holes(alpha)
    subject = alpha > 0

    rgba = np.dstack([rgb, alpha])
    out = Image.fromarray(rgba)

    if out.size != size:
        raise ValueError(f"Size changed: {size} -> {out.size}")

    target.parent.mkdir(parents=True, exist_ok=True)
    out.save(target, format="PNG")
    print(f"processed -> {target.relative_to(ROOT)} size={size} opaque={int(subject.sum())}")


def main() -> None:
    source = find_source()
    print(f"source -> {source.name}")
    process_portrait(source, TARGET)


if __name__ == "__main__":
    main()
