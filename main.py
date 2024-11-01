import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import argparse
import time

parser = argparse.ArgumentParser(description='GMD converter')
parser.add_argument('debug', nargs='?', default=False, help='Enable debug mode (pass "debug" to enable).')
args = parser.parse_args()


debug = args.debug == 'debug'  
def create_bat_file(command, output_file):
    with open(output_file, 'w') as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'{command}\n')

def run_bat_file(output_file):
    subprocess.run([output_file], creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    if not debug:
        os.remove(output_file)
    time.sleep(0.5)

def show_progress_bar(total_files):
    progress_window = tk.Toplevel()
    progress_window.title("Progress")
    progress_window.geometry("600x600")

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="determinate")
    progress_bar.pack(pady=20)

    progress_label = tk.Label(progress_window, text="Processing files...")
    progress_label.pack()

    progress_bar["maximum"] = total_files

    return progress_window, progress_bar

def extract_files():
    file_paths = file_path_extract.get().split(',')
    if not file_paths or all(path.strip() == '' for path in file_paths):
        messagebox.showwarning('Warning', 'Please select at least one GMD file.')
        return

    progress_window, progress_bar = show_progress_bar(len(file_paths))
    progress_window.update_idletasks()  

    for file_path in file_paths:
        file_path = file_path.strip()
        command = f'gmd -e "{file_path}"'
        output_file = f'extract_{os.path.splitext(os.path.basename(file_path))[0]}.bat'
        create_bat_file(command, output_file)
        run_bat_file(output_file)
        progress_bar["value"] += 1  

    progress_window.destroy()
    messagebox.showinfo('Completed', 'Extraction completed successfully!')

def insert_files():
    file_paths = file_path_insert.get().split(',')
    if not file_paths or all(path.strip() == '' for path in file_paths):
        messagebox.showwarning('Warning', 'Please select at least one TXT file.')
        return

    progress_window, progress_bar = show_progress_bar(len(file_paths))
    progress_window.update_idletasks() 

    for file_path in file_paths:
        file_path = file_path.strip()
        command = f'gmd -i -header=%s "{file_path}"'
        output_file = f'insert_{os.path.splitext(os.path.basename(file_path))[0]}.bat'
        create_bat_file(command, output_file)
        run_bat_file(output_file)
        progress_bar["value"] += 1  

    progress_window.destroy()
    messagebox.showinfo('Completed', 'Insertion completed successfully!')

def choose_extract_files():
    files = filedialog.askopenfilenames(title='Select GMD Files', filetypes=[('GMD Files', '*.gmd')])
    if files:
        file_path_extract.set(', '.join(files))  

def choose_insert_files():
    files = filedialog.askopenfilenames(title='Select TXT Files', filetypes=[('Text Files', '*.txt')])
    if files:
        file_path_insert.set(', '.join(files)) 


root = tk.Tk()
root.title('GMD converter')


file_path_extract = tk.StringVar()
file_path_insert = tk.StringVar()


extract_button = tk.Button(root, text='Choose GMD Files', command=choose_extract_files)
extract_button.pack(pady=5)


manual_input_extract = tk.Entry(root, textvariable=file_path_extract, width=50)
manual_input_extract.pack(pady=5)


extract_execute_button = tk.Button(root, text='Extract from GMD', command=extract_files)
extract_execute_button.pack(pady=5)


insert_button = tk.Button(root, text='Choose TXT Files', command=choose_insert_files)
insert_button.pack(pady=5)


manual_input_insert = tk.Entry(root, textvariable=file_path_insert, width=50)
manual_input_insert.pack(pady=5)


insert_execute_button = tk.Button(root, text='Insert into GMD', command=insert_files)
insert_execute_button.pack(pady=5)


root.mainloop()
