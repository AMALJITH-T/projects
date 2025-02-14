import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

def compile_c_program():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    c_file_path = os.path.join(script_dir, 'backend.c')
    executable_path = os.path.join(script_dir, 'backend')

    # Escape paths with spaces
    c_file_path_escaped = f'"{c_file_path}"'
    executable_path_escaped = f'"{executable_path}"'

    # Compile the C program
    compile_command = f'gcc -o {executable_path_escaped} {c_file_path_escaped}'
    subprocess.run(compile_command, shell=True, text=True)

compile_c_program()  # Compile the C program when the script is run

def run_c_program(choice, temperature):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    executable_path = os.path.join(script_dir, 'backend')

    # Use a list for the command to avoid issues with spaces
    command = [executable_path, str(choice), str(temperature)]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=script_dir)

    # Print the command and result for debugging
    print("Command:", ' '.join(command))
    print("C Program Output:", result.stdout)
    print("C Program Error:", result.stderr)

    if result.returncode != 0:
        print(f"Error: C program exited with code {result.returncode}")

    return result.stdout.strip()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    choice = int(request.form['choice'])
    temperature = float(request.form['temperature'])
    converted_temperature = run_c_program(choice, temperature)

    return render_template('result.html', choice=choice, temperature=temperature, converted_temperature=converted_temperature)

if __name__ == '__main__':
    app.run(debug=True)
