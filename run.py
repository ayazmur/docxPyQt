import os
import subprocess

def compile_ui(ui_file_path, output_path):
    try:
        command = f"pyuic5 {ui_file_path} -o {output_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"Успешно скомпилирован {ui_file_path} в {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при компиляции {ui_file_path}: {e}")
def run_main_py():
    try:
        subprocess.run("main.py", shell=True, check= True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске main.py: {e}")
if __name__ == "__main__":
    ui_file = "main.ui"
    py_out = "main_ui.py"
    compile_ui(ui_file, py_out)
    run_main_py()
