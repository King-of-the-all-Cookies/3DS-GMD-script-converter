import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess

def create_bat_file(command, output_file):
    with open(output_file, 'w') as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'{command}\n')

def run_bat_file(output_file):
    subprocess.run([output_file], creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    os.remove(output_file)

def extract_files(file_list):
    if not file_list:
        return
    try:
        if len(file_list) == 1:
            input_file = file_list[0]
            command = f'gmd -e {input_file}'
            output_file = f'extract_{os.path.splitext(input_file)[0]}.bat'
            create_bat_file(command, output_file)
            run_bat_file(output_file)
            messagebox.showinfo("Success", f"Extracted: {input_file}")
        else:
            input_files = ' '.join(file_list)
            command = f'gmd -e {input_files}'
            output_file = 'extract_multiple.bat'
            create_bat_file(command, output_file)
            run_bat_file(output_file)
            messagebox.showinfo("Success", f"Extracted: {len(file_list)} files.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during extraction: {e}")

def insert_files(file_list):
    if not file_list:
        return
    try:
        if len(file_list) == 1:
            input_file = file_list[0]
            command = f'gmd -i -header=%s {input_file}'
            output_file = f'insert_{os.path.splitext(input_file)[0]}.bat'
            create_bat_file(command, output_file)
            run_bat_file(output_file)
            messagebox.showinfo("Success", f"Inserted: {input_file}")
        else:
            input_files = ' '.join(file_list)
            command = f'gmd -i -header=%s {input_files}'
            output_file = 'insert_multiple.bat'
            create_bat_file(command, output_file)
            run_bat_file(output_file)
            messagebox.showinfo("Success", f"Inserted: {len(file_list)} files.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during insertion: {e}")

def browse_files(entry):
    filenames = filedialog.askopenfilenames(title="Select Files")
    entry.delete(0, tk.END)
    entry.insert(0, ', '.join(filenames))

def extract_button_clicked(entry):
    files = entry.get().split(', ')
    extract_files(files)

def insert_button_clicked(entry):
    files = entry.get().split(', ')
    insert_files(files)


root = tk.Tk()
root.title("GMD Tool GUI (only for GS5 from 3DS)")


tab_control = ttk.Notebook(root)


extract_tab = ttk.Frame(tab_control)
tab_control.add(extract_tab, text='Extract')


insert_tab = ttk.Frame(tab_control)
tab_control.add(insert_tab, text='Insert')

tab_control.pack(expand=1, fill='both')


extract_label = tk.Label(extract_tab, text="Select files to extract:")
extract_label.pack(pady=10)

extract_file_entry = tk.Entry(extract_tab, width=50)
extract_file_entry.pack(pady=10)

extract_browse_button = tk.Button(extract_tab, text="Browse", command=lambda: browse_files(extract_file_entry))
extract_browse_button.pack(pady=5)

extract_button = tk.Button(extract_tab, text="Extract", command=lambda: extract_button_clicked(extract_file_entry))
extract_button.pack(pady=5)


insert_label = tk.Label(insert_tab, text="Select files to insert:")
insert_label.pack(pady=10)

insert_file_entry = tk.Entry(insert_tab, width=50)
insert_file_entry.pack(pady=10)

insert_browse_button = tk.Button(insert_tab, text="Browse", command=lambda: browse_files(insert_file_entry))
insert_browse_button.pack(pady=5)

insert_button = tk.Button(insert_tab, text="Insert", command=lambda: insert_button_clicked(insert_file_entry))
insert_button.pack(pady=5)


root.mainloop()
