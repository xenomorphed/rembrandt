import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    sys.exit("Missing dependency. Run: pip install -r requirements.txt")

if len(sys.argv) != 2:
    sys.exit("usage: python svg2png.py <file.svg>")

src = Path(sys.argv[1])
dst = src.with_suffix(".png")  # тот же путь и имя, только .png

cairosvg.svg2png(url=str(src), write_to=str(dst))
print(f"saved: {dst}")