"""Remove only connected background pixels. Preserve subject RGB and canvas size."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "public" / "images"
ASSETS = Path(r"C:\Users\tomoa\.cursor\projects\c-HIBARI\assets")

SOURCE_MAP = {
    "misorahibari-logo.png": "*logo-misorahibari-3e9bb5a6*",
    "page/flower-image.png": "*flower-image-4a2864d9*",
    "page/cd-image.png": "*cd-image-034f01ea*",
    "page/misorahibari-chair.png": "*misorahibari-chair-78394acf*",
    "page/fanclub-image.png": "*fanclub-image-1f5b1bed*",
    "page/misorahibari-image.png": "*misorahibari-image-8eb4a693*",
    "page/misorahibari-mike-image.png": "*misorahibari-mike-image-032f2681*",
    "page/benefits-image.png": "*flower-image-4a2864d9*",
    "login/yuri-white.png": "*yuri-white-d4b6dacf*",
    "login/misorahibari-mike-image.png": "*misorahibari-mike-image-032f2681*",
}


def find_asset(pattern: str) -> Path:
    matches = sorted(ASSETS.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Asset not found: {pattern}")
    return matches[0]


def restore_sources() -> None:
    for rel, pattern in SOURCE_MAP.items():
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        source = find_asset(pattern)
        target.write_bytes(source.read_bytes())
        print(f"restored -> {rel}")


def quantize_rgb(rgb: np.ndarray) -> tuple[int, int, int]:
    return tuple(int(round(v / 8) * 8) for v in rgb[:3])


def collect_edge_pixels(arr: np.ndarray, margin_ratio: float = 0.12) -> np.ndarray:
    h, w, _ = arr.shape
    margin = max(8, int(min(h, w) * margin_ratio))
    pixels: list[np.ndarray] = []
    for x in range(margin, w - margin):
        pixels.append(arr[0, x, :3])
        pixels.append(arr[h - 1, x, :3])
    for y in range(margin, h - margin):
        pixels.append(arr[y, 0, :3])
        pixels.append(arr[y, w - 1, :3])
    return np.array(pixels, dtype=np.float32)


def dominant_light_bg_colors(edge_pixels: np.ndarray, max_colors: int = 3) -> list[np.ndarray]:
    """Pick light background colors from border mid-sections (ignore dark subject corners)."""
    light = edge_pixels[np.min(edge_pixels, axis=1) > 120]
    if light.size == 0:
        light = edge_pixels

    buckets: dict[tuple[int, int, int], list[np.ndarray]] = {}
    for px in light:
        key = quantize_rgb(px)
        buckets.setdefault(key, []).append(px)

    ranked = sorted(
        buckets.items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )

    colors: list[np.ndarray] = []
    for key, group in ranked[: max_colors + 2]:
        mean = np.mean(group, axis=0)
        if np.min(mean) < 120:
            continue
        if any(np.linalg.norm(mean - c) < 20 for c in colors):
            continue
        colors.append(mean.astype(np.float32))
        if len(colors) >= max_colors:
            break

    if not colors:
        colors.append(np.array([255.0, 255.0, 255.0], dtype=np.float32))
    return colors


def is_removable_bg(rgb: np.ndarray, bg_colors: list[np.ndarray], tolerance: float) -> bool:
    rgb = rgb.astype(np.float32)
    if np.min(rgb) < 90:
        return False
    return any(np.linalg.norm(rgb - bg) <= tolerance for bg in bg_colors)


def remove_connected_background(img: Image.Image, tolerance: float = 20.0) -> Image.Image:
    rgb = np.array(img.convert("RGB"))
    h, w, _ = rgb.shape
    edge_pixels = collect_edge_pixels(rgb)
    bg_colors = dominant_light_bg_colors(edge_pixels)

    bg_mask = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(w):
        queue.append((0, x))
        queue.append((h - 1, x))
    for y in range(h):
        queue.append((y, 0))
        queue.append((y, w - 1))

    while queue:
        y, x = queue.popleft()
        if y < 0 or y >= h or x < 0 or x >= w or visited[y, x]:
            continue
        if not is_removable_bg(rgb[y, x], bg_colors, tolerance):
            continue
        visited[y, x] = True
        bg_mask[y, x] = True
        queue.extend([(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)])

    rgba = np.dstack([rgb, np.full((h, w), 255, dtype=np.uint8)])
    rgba[bg_mask, 3] = 0
    return Image.fromarray(rgba)


def process_file(rel: str, tolerance: float = 20.0) -> None:
    path = ROOT / rel
    original = Image.open(path)
    size = original.size
    out = remove_connected_background(original, tolerance=tolerance)
    if out.size != size:
        raise ValueError(f"Size changed for {rel}: {size} -> {out.size}")
    out.save(path, format="PNG")
    alpha = out.getchannel("A")
    opaque = sum(1 for px in alpha.getdata() if px > 0)
    print(f"processed -> {rel} {size} opaque={opaque}")


def process_logo(tolerance: float = 18.0) -> None:
    logo_path = ROOT / "misorahibari-logo.png"
    original = Image.open(logo_path)
    size = original.size
    out = remove_connected_background(original, tolerance=tolerance)
    if out.size != size:
        raise ValueError(f"Logo size changed: {size} -> {out.size}")
    out.save(logo_path, format="PNG")
    print(f"processed -> misorahibari-logo.png {size}")


def main() -> None:
    restore_sources()
    tolerances = {
        "misorahibari-logo.png": 18.0,
        "page/flower-image.png": 22.0,
        "page/cd-image.png": 22.0,
        "page/misorahibari-chair.png": 22.0,
        "page/fanclub-image.png": 22.0,
        "page/misorahibari-image.png": 22.0,
        "page/misorahibari-mike-image.png": 14.0,
        "page/benefits-image.png": 22.0,
        "login/yuri-white.png": 18.0,
    }
    skip_login_portrait = "login/misorahibari-mike-image.png"
    for rel in SOURCE_MAP:
        if rel == skip_login_portrait:
            print(f"skipped -> {rel} (use scripts/process-login-portrait.py)")
            continue
        if rel == "misorahibari-logo.png":
            process_logo(tolerance=tolerances.get(rel, 18.0))
            continue
        process_file(rel, tolerance=tolerances.get(rel, 20.0))


if __name__ == "__main__":
    main()
