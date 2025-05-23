import re

def find_unclosed_endifs(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    stack = []
    for i, line in enumerate(lines, 1):
        if_match = re.search(r'{%\s*if\b', line)
        elif_match = re.search(r'{%\s*elif\b', line)
        else_match = re.search(r'{%\s*else\s*%}', line)
        endif_match = re.search(r'{%\s*endif\s*%}', line)

        if if_match:
            stack.append(('if', i))
        elif elif_match or else_match:
            continue  # doesn't affect stack
        elif endif_match:
            if stack and stack[-1][0] == 'if':
                stack.pop()
            else:
                print(f"Unmatched 'endif' at line {i}")

    for block in stack:
        print(f"Missing 'endif' for 'if' started at line {block[1]}")

# Example usage
find_unclosed_endifs("your_template.json")
