from typing import TYPE_CHECKING
from hugo_nbconvert.collapse_preprocessor import CollapsePreprocessor

if TYPE_CHECKING:
    from traitlets.config import Config

    c = Config()

    def get_config():
        return c

# reference: https://racedorsey.com/posts/2024/jupyter-notebook-hugo/

c = get_config()

c.TagRemovePreprocessor.enabled = True
c.TagRemovePreprocessor.remove_cell_tags = ["hide_cell"]
c.TagRemovePreprocessor.remove_input_tags = ["hide_input"]
c.TagRemovePreprocessor.remove_all_outputs_tags = ["hide_output"]
c.MarkdownExporter.preprocessors = [CollapsePreprocessor]
