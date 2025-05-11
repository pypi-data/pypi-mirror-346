from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class AdmonitionConverter(Preprocessor):
    BLOCK_RE = re.compile(
        r'^```ad-(\w+)\s*\n'        # opening fence with type
        r'(?:title:[ \t]*(.+?)\n)?'  # optional title line
        r'((?:.*?\n)*?)'              # content
        r'^```\s*$',
        re.MULTILINE
    )

    def run(self, lines):
        text = "\n".join(lines)
        def repl(match):
            ad_type = match.group(1).strip()
            title = match.group(2).strip() if match.group(2) else ""
            content = match.group(3)
            indented = "\n".join("    " + line for line in content.rstrip().splitlines())
            title_str = f' "{title}"' if title else ""
            return f"!!! {ad_type}{title_str}\n{indented}"
        new_text = self.BLOCK_RE.sub(repl, text)
        return new_text.splitlines()

class ObsidianToMaterialExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(AdmonitionConverter(md), 'obsidian_to_material', 25)

def makeExtension(**kwargs):
    return ObsidianToMaterialExtension(**kwargs)