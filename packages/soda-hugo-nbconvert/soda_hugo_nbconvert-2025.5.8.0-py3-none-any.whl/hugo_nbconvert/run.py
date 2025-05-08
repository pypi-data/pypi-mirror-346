from .glob_hugo_ipynb import must_find_hugo_root
import subprocess
from sodatools import CD


def run():
    root = must_find_hugo_root()
    print(f"using hugo root at {root}")
    with CD(root):
        try:
            subprocess.run("hugo serve -OD --baseURL=http://localhost", shell=True)
        except KeyboardInterrupt:
            return
