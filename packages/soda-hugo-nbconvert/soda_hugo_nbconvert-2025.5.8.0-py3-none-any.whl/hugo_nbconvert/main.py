import subprocess
from hugo_nbconvert.glob_hugo_ipynb import get_files
from pathlib import Path
from hugo_nbconvert.collapse_postprocessor import CollapsePostprocessor

conf_path = Path(__file__).resolve().parent.joinpath("nbconvert_config.py")


def main():
    files = get_files()
    for i in files:
        subprocess.run(
            ["jupyter", "nbconvert", "--config", conf_path, "--to", "markdown", i]
        )
        output_filepath = i.parent.joinpath("index.md")
        if output_filepath.exists():
            postprocessor = CollapsePostprocessor(output_filepath)
            postprocessor.process()


if __name__ == "__main__":
    main()
