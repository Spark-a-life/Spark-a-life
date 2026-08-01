from pathlib import Path
import argparse, zipfile
EXCLUDE={".git",".venv","__pycache__",".pytest_cache",".ruff_cache"}
def main():
 p=argparse.ArgumentParser(); p.add_argument("--output",required=True); a=p.parse_args()
 root=Path(__file__).resolve().parents[1]; target=Path(a.output); target.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as z:
  for f in root.rglob("*"):
   if f.is_file() and not any(x in EXCLUDE for x in f.parts) and f.resolve()!=target.resolve(): z.write(f,f.relative_to(root.parent))
 print(target)
if __name__=="__main__": main()
