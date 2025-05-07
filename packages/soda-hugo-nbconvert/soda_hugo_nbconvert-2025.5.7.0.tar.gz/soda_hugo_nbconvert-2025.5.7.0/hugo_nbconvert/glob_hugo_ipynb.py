import glob
from pathlib import Path
import os


def get_files() -> list[Path]:
    cwd = Path(os.getcwd())
    files = glob.glob("**/hugo.yaml", recursive=True, root_dir=cwd)
    if len(files) == 0:
        print("cannot find a hugo site")
        return []
    hugo_basedir = cwd.joinpath(files[0]).parent

    hugo_ipynbs = glob.glob("**/*.ipynb", recursive=True, root_dir=hugo_basedir)

    hugo_ipynbs = list(
        map(
            hugo_basedir.joinpath,
            filter(lambda x: not x.startswith("public"), hugo_ipynbs),
        )
    )
    return hugo_ipynbs
