"""Remove solid black background from fanclub logo and save as transparent PNG."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(
    r"C:\Users\rui05\.cursor\projects\c-HIBARI-HIBARI-project\assets"
    r"\c__Users_rui05_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"e270fe27000fbcd9990816d2b88b1170_images_ChatGPT_Image_2026_7_16__"
    r"04_30_30-7fe91a6d-f35f-4dcc-98ab-44412de9645e.png"
)
DST = Path(__file__).resolve().parents[1] / "public" / "images" / "page" / "fanlogo.png"


def is_bg(px: np.ndarray) -> bool:
    px = px.astype(np.float32)
    # pure / near-black canvas
    if float(np.max(px)) <= 18:
        return True
    # soft dark spill next to subject edges
    if float(np.max(px)) <= 42 and float(np.linalg.norm(px)) <= 28:
        return True
    return False


def remove_dark_connected_background(rgb: np.ndarray) -> np.ndarray:
    h, w, _ = rgb.shape
    visited = np.zeros((h, w), dtype=bool)
    bg_mask = np.zeros((h, w), dtype=bool)
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
        visited[y, x] = True
        if not is_bg(rgb[y, x]):
            continue
        bg_mask[y, x] = True
        queue.extend([(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)])

    alpha = np.where(bg_mask, 0, 255).astype(np.uint8)
    return np.dstack([rgb, alpha])


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)

    rgb = np.array(Image.open(SRC).convert("RGB"))
    rgba = remove_dark_connected_background(rgb)
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 0)
    if ys.size == 0:
        raise RuntimeError("No opaque pixels remaining; tolerance too aggressive?")

    pad = 12
    h, w = alpha.shape
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(h, int(ys.max()) + 1 + pad)
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(w, int(xs.max()) + 1 + pad)
    out = Image.fromarray(rgba).crop((x0, y0, x1, y1))

    DST.parent.mkdir(parents=True, exist_ok=True)
    backup = DST.with_suffix(".png.bak")
    if DST.exists() and not backup.exists():
        backup.write_bytes(DST.read_bytes())

    out.save(DST, format="PNG")
    opaque = int((np.array(out)[:, :, 3] > 0).sum())
    print(f"saved -> {DST}")
    print(f"size={out.size} opaque={opaque} crop=({x0},{y0},{x1},{y1})")


if __name__ == "__main__":
    main()
