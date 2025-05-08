import subprocess
from .registry import register_tool

import re
import html

def unescape_html(input_string: str) -> str:
  """
  将字符串中的 HTML 实体（例如 &amp;）转换回其原始字符（例如 &）。

  Args:
    input_string: 包含 HTML 实体的输入字符串。

  Returns:
    转换后的字符串。
  """
  return html.unescape(input_string)

def get_python_executable(command: str) -> str:
    """
    获取 Python 可执行文件的路径。

    Returns:
        str: Python 可执行文件的路径。
    """
    cmd_parts = command.split(None, 1)
    if cmd_parts:
        executable = cmd_parts[0]
        args_str = cmd_parts[1] if len(cmd_parts) > 1 else ""

        # 检查是否是 python 可执行文件 (如 python, python3, pythonX.Y)
        is_python_exe = False
        if executable == "python" or re.match(r"^python[23]?(\.\d+)?$", executable):
            is_python_exe = True

        if is_python_exe:
            # 检查参数中是否已经有 -u 选项
            args_list = args_str.split()
            has_u_option = "-u" in args_list
            if not has_u_option:
                if args_str:
                    command = f"{executable} -u {args_str}"
    return command

# 执行命令
@register_tool()
def excute_command(command):
    """
执行命令并返回输出结果 (标准输出会实时打印到控制台)
禁止用于查看pdf，禁止使用 pdftotext 命令

参数:
    command: 要执行的命令，可以克隆仓库，安装依赖，运行代码等

返回:
    命令执行的最终状态和收集到的输出/错误信息
    """
    try:
        command = unescape_html(command) # 保留 HTML 解码

        command = get_python_executable(command)


        # 使用 Popen 以便实时处理输出
        # bufsize=1 表示行缓冲, universal_newlines=True 与 text=True 效果类似，用于文本模式
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        stdout_lines = []

        # 实时打印 stdout
        # print(f"--- 开始执行命令: {command} ---")
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                # 对 pip install 命令的输出进行过滤，去除进度条相关的行
                if "pip install" in command and '━━' in line:
                    continue
                print(line, end='', flush=True) # 实时打印到控制台，并刷新缓冲区
                stdout_lines.append(line) # 收集行以供后续返回
            process.stdout.close()
        # print(f"\n--- 命令实时输出结束 ---")

        # 等待命令完成
        process.wait()

        # 获取 stderr (命令完成后一次性读取)
        stderr_output = ""
        if process.stderr:
            stderr_output = process.stderr.read()
            process.stderr.close()

        # 组合最终的 stdout 日志 (已经过 pip install 过滤)
        final_stdout_log = "".join(stdout_lines)

        if process.returncode == 0:
            return f"执行命令成功:\n{final_stdout_log}"
        else:
            return f"执行命令失败 (退出码 {process.returncode}):\n错误: {stderr_output}\n输出: {final_stdout_log}"

    except FileNotFoundError:
        # 当 shell=True 时，命令未找到通常由 shell 处理，并返回非零退出码。
        # 此处捕获 FileNotFoundError 主要用于 Popen 自身无法启动命令的场景 (例如 shell 本身未找到)。
        return f"执行命令失败: 命令或程序未找到 ({command})"
    except Exception as e:
        # 其他未知异常
        return f"执行命令时发生异常: {e}"

if __name__ == "__main__":
    # print(excute_command("ls -l && echo 'Hello, World!'"))
    # print(excute_command("ls -l &amp;&amp; echo 'Hello, World!'"))

#     tqdm_script = """
# import time
# from tqdm import tqdm

# for i in range(10):
#     print(f"TQDM 进度条测试: {i}")
#     time.sleep(1)
# print('\\n-------TQDM 任务完成.')
# """
#     processed_tqdm_script = tqdm_script.replace('"', '\\"')
#     tqdm_command = f"python -u -u -c \"{processed_tqdm_script}\""
#     # print(f"执行: {tqdm_command}")
#     print(excute_command(tqdm_command))


    # long_running_command_unix = "echo '开始长时间任务...' && for i in 1 2 3; do echo \"正在处理步骤 $i/3...\"; sleep 1; done && echo '长时间任务完成!'"
    # print(f"执行: {long_running_command_unix}")
    # print(excute_command(long_running_command_unix))


    # long_running_command_unix = "pip install torch"
    # print(f"执行: {long_running_command_unix}")
    # print(excute_command(long_running_command_unix))


#     python_long_task_command = """
# python -c "import time; print('Python 长时间任务启动...'); [print(f'Python 任务进度: {i+1}/3', flush=True) or time.sleep(1) for i in range(3)]; print('Python 长时间任务完成.')"
# """
#     python_long_task_command = python_long_task_command.strip() # 移除可能的前后空白
#     print(f"执行: {python_long_task_command}")
#     print(excute_command(python_long_task_command))

    print(get_python_executable("python -c 'print(123)'"))
# python -m beswarm.aient.src.aient.plugins.excute_command
