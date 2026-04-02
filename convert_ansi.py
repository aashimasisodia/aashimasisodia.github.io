#!/usr/bin/env python3
import re

def ansi_to_html(ansi_file, output_file):
    with open(ansi_file, 'r') as f:
        content = f.read()

    # Pattern to match ANSI escape codes
    # [48;2;R;G;Bm = background color
    # [38;2;R;G;Bm = foreground color
    # [0m = reset

    html_lines = []
    lines = content.split('\n')

    for line in lines:
        if not line:
            html_lines.append('')
            continue

        html_line = ''
        current_fg = None
        current_bg = None
        i = 0

        while i < len(line):
            # Check for escape sequence
            if line[i] == '\x1b' or (line[i] == '[' and (i == 0 or line[i-1] != '\x1b')):
                # Find the end of the escape sequence
                if line[i] == '[':
                    start = i
                else:
                    start = i + 1
                    if start < len(line) and line[start] == '[':
                        start += 1

                end = start
                while end < len(line) and line[end] != 'm':
                    end += 1

                if end < len(line):
                    code = line[start:end]
                    # Parse the code
                    if code == '0':
                        current_fg = None
                        current_bg = None
                    elif code.startswith('48;2;'):
                        # Background color
                        parts = code.split(';')
                        if len(parts) >= 5:
                            current_bg = f"rgb({parts[2]},{parts[3]},{parts[4]})"
                    elif code.startswith('38;2;'):
                        # Foreground color
                        parts = code.split(';')
                        if len(parts) >= 5:
                            current_fg = f"rgb({parts[2]},{parts[3]},{parts[4]})"

                    i = end + 1
                    continue

            # Regular character
            char = line[i]
            if char not in ['\x1b', '['] or (char == '[' and i > 0 and line[i-1] == '\x1b'):
                if current_fg or current_bg:
                    style = ''
                    if current_fg:
                        style += f'color:{current_fg};'
                    if current_bg:
                        style += f'background:{current_bg};'
                    html_line += f'<span style="{style}">{char}</span>'
                else:
                    html_line += char
            i += 1

        html_lines.append(html_line)

    # Write output
    html_content = '<pre style="font-size:3px;line-height:1;letter-spacing:0;font-family:monospace;background:#0e0e16;display:inline-block;padding:4px;border-radius:4px;">' + '\n'.join(html_lines) + '</pre>'

    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"Converted {len(lines)} lines to HTML")

if __name__ == '__main__':
    ansi_to_html('ansi.txt', 'ansi_html.txt')
