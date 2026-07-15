"""
表紙モックアップ画像から「表紙デザインのみ」の透明PNGを生成する。

- 背表紙・市松模様・外周グレー背景を除去
- 出力: 1024x1536 RGBA PNG
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

SRC_DIR = Path(__file__).resolve().parents[1] / "public" / "images" / "memorybook" / "covers"
OUT_SIZE = (1024, 1536)


def is_background_pixel(r: int, g: int, b: int) -> bool:
    """市松模様・白・ライトグレー背景を判定"""
    if r > 248 and g > 248 and b > 248:
        return True
    if r > 212 and g > 212 and b > 212:
        if max(abs(int(r) - int(g)), abs(int(g) - int(b)), abs(int(r) - int(b))) <= 14:
            return True
    return False


def column_density(mask: np.ndarray, x: int) -> float:
    return float(mask[:, x].sum()) / mask.shape[0]


def find_cover_columns(mask: np.ndarray) -> tuple[int, int]:
    """背表紙を除いた表紙面の左右境界を推定"""
    h, w = mask.shape
    densities = [column_density(mask, x) for x in range(w)]

    # 背表紙は左端で密度が低い → 表紙面は高密度列が続く領域
    threshold = h * 0.55
    left = 0
    for x in range(w):
        if densities[x] >= threshold:
            left = x
            break

    right = w - 1
    for x in range(w - 1, -1, -1):
        if densities[x] >= threshold:
            right = x
            break

    # 左端の背表紙帯をさらに除外（表紙面の左境界はしきい値超え後の安定域）
    stable_left = left
    for x in range(left, min(left + 80, w)):
        if densities[x] >= h * 0.82:
            stable_left = x
            break

    return stable_left, right


def trim_transparent_vertical(img: Image.Image) -> Image.Image:
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rows = np.where(alpha.max(axis=1) > 8)[0]
    if rows.size == 0:
        return img
    top, bottom = int(rows[0]), int(rows[-1])
    return img.crop((0, top, img.width, bottom + 1))


def process_image(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGBA")
    arr = np.array(img.convert("RGB"))
    h, w, _ = arr.shape

    opaque_mask = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            r, g, b = arr[y, x]
            if not is_background_pixel(int(r), int(g), int(b)):
                opaque_mask[y, x] = True

    left, right = find_cover_columns(opaque_mask)

    row_mask = opaque_mask[:, left : right + 1].any(axis=1)
    rows = np.where(row_mask)[0]
    if rows.size == 0:
        top, bottom = 0, h - 1
    else:
        top, bottom = int(rows[0]), int(rows[-1])

    cropped = img.crop((left, top, right + 1, bottom + 1))

    # クロップ後に背景を透明化
    data = np.array(cropped)
    rgb = data[:, :, :3]
    alpha = data[:, :, 3]
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            r, g, b = rgb[y, x]
            if is_background_pixel(int(r), int(g), int(b)):
                alpha[y, x] = 0
    data[:, :, 3] = alpha
    result = Image.fromarray(data, mode="RGBA")
    result = trim_transparent_vertical(result)

    # 表紙比率 2:3 にフィット（余白なし・全体収まる）
    result = result.resize(OUT_SIZE, Image.Resampling.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    result.save(dst, format="PNG", optimize=True)
    print(f"saved {dst.name} {result.size} mode=RGBA")


def main() -> None:
    for i in range(1, 10):
        mockup = SRC_DIR / f"hyousi-design-{i}.mockup.png"
        src = mockup if mockup.exists() else SRC_DIR / f"hyousi-design-{i}.png"
        if not src.exists():
            print(f"skip missing {src}")
            continue
        dst = SRC_DIR / f"hyousi-design-{i}.png"
        process_image(src, dst)


if __name__ == "__main__":
    main()
