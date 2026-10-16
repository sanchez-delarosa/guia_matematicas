import json
from pathlib import Path

reactivos_dir = Path("assets/reactivos")
for f in sorted(reactivos_dir.glob("capitulo-*.json"), key=lambda p: int(p.stem.split("-")[1])):
    num = int(f.stem.split("-")[1])
    data = json.loads(f.read_text(encoding="utf-8"))
    meta = data.get("metadata", {})
    version = meta.get("version") or data.get("version")
    total = len(data.get("reactivos", []))
    title = meta.get("titulo") or data.get("titulo", "")
    print(f"Capítulo {num:02d}: {title:<35} | v{version} | {total:3d} reactivos")
