import os
import json
from pdfminer.high_level import extract_text

from .registry import register_tool

# 读取文件内容
@register_tool()
def read_file(file_path):
    """
Description: Request to read the contents of a file at the specified path. Use this when you need to examine the contents of an existing file you do not know the contents of, for example to analyze code, review text files, or extract information from configuration files. Automatically extracts raw text from PDF and DOCX files. May not be suitable for other types of binary files, as it returns the raw content as a string.

注意：
1. pdf 文件 必须使用 read_file 读取，可以使用 read_file 直接读取 PDF。

参数:
    file_path: 要读取的文件路径，(required) The path of the file to read (relative to the current working directory)

返回:
    文件内容的字符串

Usage:
<read_file>
<file_path>File path here</file_path>
</read_file>

Examples:

1. Reading an entire file:
<read_file>
<file_path>frontend.pdf</file_path>
</read_file>

2. Reading multiple files:

<read_file>
<file_path>frontend-config.json</file_path>
</read_file>

<read_file>
<file_path>backend-config.txt</file_path>
</read_file>

...

<read_file>
<file_path>README.md</file_path>
</read_file>
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"<read_file error>文件 '{file_path}' 不存在</read_file error>"

        # 检查是否为文件
        if not os.path.isfile(file_path):
            return f"<read_file error>'{file_path}' 不是一个文件</read_file error>"

        # 检查文件扩展名
        if file_path.lower().endswith('.pdf'):
            # 提取PDF文本
            text_content = extract_text(file_path)

            # 如果提取结果为空
            if not text_content:
                return f"<read_file error>无法从 '{file_path}' 提取文本内容</read_file error>"
        elif file_path.lower().endswith('.ipynb'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    notebook_content = json.load(file)

                for cell in notebook_content.get('cells', []):
                    if cell.get('cell_type') == 'code' and 'outputs' in cell:
                        filtered_outputs = []
                        for output in cell.get('outputs', []):
                            new_output = output.copy()
                            if 'data' in new_output:
                                original_data = new_output['data']
                                filtered_data = {}
                                for key, value in original_data.items():
                                    if key.startswith('image/'):
                                        continue
                                    if key == 'text/html':
                                        html_content = "".join(value) if isinstance(value, list) else value
                                        if isinstance(html_content, str) and '<table class="show_videos"' in html_content:
                                            continue
                                    filtered_data[key] = value
                                if filtered_data:
                                    new_output['data'] = filtered_data
                                    filtered_outputs.append(new_output)
                            elif 'output_type' in new_output and new_output['output_type'] in ['stream', 'error']:
                                filtered_outputs.append(new_output)

                        cell['outputs'] = filtered_outputs

                text_content = json.dumps(notebook_content, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                return f"<read_file error>文件 '{file_path}' 不是有效的JSON格式 (IPython Notebook)。</read_file error>"
            except Exception as e:
                return f"<read_file error>处理IPython Notebook文件 '{file_path}' 时发生错误: {e}</read_file error>"
        else:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

        # 返回文件内容
        return text_content

    except PermissionError:
        return f"<read_file error>没有权限访问文件 '{file_path}'</read_file error>"
    except UnicodeDecodeError:
        return f"<read_file error>文件 '{file_path}' 不是文本文件或编码不是UTF-8</read_file error>"
    except Exception as e:
        return f"<read_file error>读取文件时发生错误: {e}</read_file error>"

if __name__ == "__main__":
    # python -m beswarm.aient.src.aient.plugins.read_file
    result = read_file("./work/cax/Lenia Notebook.ipynb")
    print(result)
    print(len(result))
