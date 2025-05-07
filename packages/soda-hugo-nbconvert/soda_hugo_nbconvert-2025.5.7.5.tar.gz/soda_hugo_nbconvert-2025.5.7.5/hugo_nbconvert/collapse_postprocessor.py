import sys


class CollapsePostprocessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def process(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                content = file.read()

                # collapsed inputs/outputs
                content = content.replace(
                    "```python\n{{< detailsInput >}}",
                    '{{< details summary="Input collapsed:" altSummary="Input expanded:" >}}',
                )
                content = content.replace(
                    "{{< /detailsInput >}}\n```", "{{< /details >}}\n"
                )
                content = content.replace(
                    "    {{< detailsOutput >}}",
                    '{{< details summary="Output collapsed:" altSummary="Output expanded:" >}}',
                )
                content = content.replace(
                    "    {{< /detailsOutput >}}", "{{< /details >}}\n"
                )

            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write(content)
        except FileNotFoundError:
            sys.exit(f"Could not locate {self.filepath}")
