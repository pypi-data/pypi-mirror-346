from .check_code import combina_cpp_and_py

def select_file(title, filetypes):
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def read_file(file_path):
    if not file_path:
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(content):
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="save the combine code file",
        defaultextension="",
        filetypes=[("Python files", "*.py"),
                   ("Python source files", "*.pyi"),
                   ("Python file (no console)", "*.pyw"),
                   ("C files", "*.c"),
                   ("C++ files", "*.cpp"),                   
                   ("C header files", "*.h"),
                   ("C++ header files", "*.hpp"),
                   ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)        
        return True
    return False

def main(use_double=True):
    """
    Open the file and combine to new file.
    First open cpp then py.
    If the system is not windows, it may doesn't work.
    """
    import tkinter as tk
    from tkinter import messagebox
    
    cpp_path = select_file("Choose cpp file", [("C++ files", "*.c *.cpp *.h *.hpp"), ("All files", "*.*")])
    if not cpp_path:
        return
    
    py_path = select_file("Choose py file", [("Python files", "*.py *.pyw *.pyi"), ("All files", "*.*")])
    if not py_path:
        return
    
    cpp_code = read_file(cpp_path)
    py_code = read_file(py_path)
    
    if cpp_code is None or py_code is None:
        messagebox.showerror("Error", "Cannot read the file.")
        return
    
    combined_code = combina_cpp_and_py(cpp_code, py_code, use_double)
    
    if save_file(combined_code):
        messagebox.showinfo("Success", "The code has been combined！")
    else:
        messagebox.showwarning("Cancel", "Saving has been canceled.")

if __name__ == '__main__':
    while True:
        a = input("Use double?(Y/n)")
        if a == 'Y':
            main(True)
            break
        elif a == 'n':
            main(False)
            break
        else:
            print('Invalid input!')
