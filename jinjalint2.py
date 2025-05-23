import re
import sys

class JinjaLinter:
    def __init__(self):
        self.patterns = {
            'if': re.compile(r'{%\s*if\b'),
            'endif': re.compile(r'{%\s*endif\s*%}'),
            'for': re.compile(r'{%\s*for\b'),
            'endfor': re.compile(r'{%\s*endfor\s*%}'),
        }

    def lint(self, lines):
        stack = []
        issues = []

        for lineno, line in enumerate(lines, start=1):
            if self.patterns['if'].search(line):
                stack.append(('if', lineno))
            elif self.patterns['for'].search(line):
                stack.append(('for', lineno))
            elif self.patterns['endif'].search(line):
                if not stack or stack[-1][0] != 'if':
                    issues.append(f"Line {lineno}: Unexpected 'endif'")
                else:
                    stack.pop()
            elif self.patterns['endfor'].search(line):
                if not stack or stack[-1][0] != 'for':
                    issues.append(f"Line {lineno}: Unexpected 'endfor'")
                else:
                    stack.pop()

        # Report unclosed blocks
        for block_type, lineno in stack:
            issues.append(f"Line {lineno}: Unclosed '{block_type}' block")

        return issues


def main(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return

    linter = JinjaLinter()
    issues = linter.lint(lines)

    if issues:
        print("Lint Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No issues found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python jinja_linter.py <template_file>")
    else:
        main(sys.argv[1])
