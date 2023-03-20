import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import openai

openai.api_key = open('conf.txt').readline(1)

class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Editor")
        self.master.geometry("800x600")

        # Create a text widget
        self.text_widget = tk.Text(self.master, undo=True, foreground="#fbfeff", background="#2e2d2a", insertbackground="#aabb33", insertwidth="5px")
        self.text_widget.pack(fill="both", expand=True)

        # Add syntax highlighting to the text widget #474640
        self.text_widget.tag_configure("keyword", foreground="#3abbc9")
        self.text_widget.tag_configure("builtin", foreground="#43d5e6")
        self.text_widget.tag_configure("comment", foreground="#96b546")
        self.text_widget.tag_configure("string", foreground="#ffb700")
        self.text_widget.tag_configure("method", foreground="#f0cd41")
        #self.text_widget.tag_configure("number", foreground="#f0cd41")

        # Set up keyboard shortcuts
        self.master.bind('<Control-x>', self.cut)
        self.master.bind('<Control-c>', self.copy)
        self.master.bind('<Control-v>', self.paste)
        self.master.bind('<Control-a>', self.select_all)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.master)

        # Add a file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add an edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Add an AI menu
        self.ai_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.ai_menu.add_command(label="Chat Completion", command=self.chat_completion)
        self.menu_bar.add_cascade(label="AI", menu=self.ai_menu)

        # Set the menu bar
        self.master.config(menu=self.menu_bar)

        # Set the default file path and file name
        self.file_path = ""
        self.file_name = "Untitled.txt"

        # Update the line numbers and syntax highlighting when the text widget is modified
        #self.text_widget.bind('<Any-KeyPress>', self.update_linenumbers)
        self.text_widget.bind('<KeyRelease>', self.highlight_syntax)

    def new_file(self):
        # Create a new file
        self.text_widget.delete('1.0', 'end')
        self.file_path = ""
        self.file_name = "Untitled.txt"
        self.master.title(self.file_name)

    def open_file(self):
        # Open an existing file
        file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python","*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.text_widget.delete('1.0', 'end')
            with open(file_path, 'r') as file:
                self.text_widget.insert('1.0', file.read())
            self.file_path = file_path
            self.file_name = os.path.basename(self.file_path)
            self.master.title(self.file_name)
            self.highlight_syntax()

    def save_file(self):
        # Save the current file
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_widget.get('1.0', 'end'))
        else:
            self.save_as_file()

    def save_as_file(self):
        # Save the current file with a new name
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"),("Python","*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get('1.0', 'end'))
            self.file_path = file_path
            self.file_name = os.path.basename(self.file_path)
            self.master.title(self.file_name)

    def cut(self, event=None):
        # Cut selected text
        self.text_widget.event_generate("<<Cut>>")

    def copy(self, event=None):
        # Copy selected text
        self.text_widget.event_generate("<<Copy>>")

    def paste(self, event=None):
        # Paste clipboard text
        self.text_widget.event_generate("<<Paste>>")

    def select_all(self, event=None):
        # Select all text
        self.text_widget.tag_add("sel", '1.0', 'end')

    def chat_completion(self):
        # Execute GPT-3.5-Turbo chat completion
        text = self.text_widget.get('1.0', 'end')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a grand sage with the world's knowledge in your database. You are a stunningly brilliant and detailed assistant."},
                {"role": "user", "content": text}
            ],
            temperature=0.8,
            stop='stop'
        )
        messagebox.showinfo("Chat Completion", response.choices[0].message.content)

    def highlight_syntax(self, event=None):
        # Highlight the syntax of the text in the text widget
        self.text_widget.tag_remove('keyword', '1.0', 'end')
        self.text_widget.tag_remove('builtin', '1.0', 'end')
        self.text_widget.tag_remove('comment', '1.0', 'end')
        self.text_widget.tag_remove('string', '1.0', 'end')
        self.text_widget.tag_remove('method', '1.0', 'end')
        self.text_widget.tag_remove('number', '1.0', 'end')
        keywords = ['if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'def', 'class', 'import', 'from', 'as', 'global', 'nonlocal', 'in', 'not', 'and', 'or', 'is', 'lambda', 'yield', 'break', 'continue', 'return']
        builtins = ['abs', 'del', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 'setattr', 'any', 'dir', 'hex', 'next', 'slice', 'ascii', 'divmod', 'id', 'object', 'sorted', 'bin', 'enumerate', 'input', 'oct', 'staticmethod', 'bool', 'eval', 'int', 'open', 'str', 'bytearray', 'exec', 'isinstance', 'ord', 'sum', 'bytes', 'filter', 'issubclass', 'pow', 'super', 'callable', 'float', 'iter', 'print', 'tuple', 'chr', 'format', 'len', 'property', 'type', 'classmethod', 'frozenset', 'list', 'range', 'vars', 'compile', 'getattr', 'locals', 'repr', 'zip', 'complex', 'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round', '__init__']
        count = tk.IntVar()

        #highlight methods
        start = 1.0
        patt = r"((\.)|(\s))[^.( ]*\("
        while True:
            start = self.text_widget.search(patt, start, tk.END, regexp=True, count=count)
            if not start:
                break
            end = f"{start}+{count.get()-1}c"
            self.text_widget.tag_add("method", start, end)
            start = f"{start}+{count.get()}c"

        #highlight keywords
        start = 1.0
        joinstr = r')|('
        patt = r"(^|\m)(("+joinstr.join(keywords)+r"))\M"
        while True:
            start = self.text_widget.search(patt, start, tk.END, regexp=True, count=count)
            if not start:
                break
            end = f"{start}+{count.get()}c"
            self.text_widget.tag_add("keyword", start, end)
            start = f"{start}+{count.get()}c"

        #highlight builtins
        start = 1.0
        joinstr = r'\s*\()|((\.|\s)'
        patt = r"((\.|\s)"+joinstr.join(builtins)+r"\s*\()"
        #print(patt)
        while True:
            start = self.text_widget.search(patt, start, tk.END, regexp=True, count=count)
            #print(start)
            if not start:
                break
            end = f"{start}+{count.get()-1}c"
            self.text_widget.tag_add("builtin", start, end)
            start = f"{start}+{count.get()}c"

        #highlight strings ""
        start = 1.0
        while True:
            start = self.text_widget.search(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", start, tk.END, regexp=True, count=count)
            if not start:
                break
            end = f"{start}+{count.get()}c"
            self.text_widget.tag_add("string", start, end)
            start = f"{start}+{count.get()+1}c"

        # highlight comments
        start = 1.0
        while True:
            index = self.text_widget.search(r'(?!(((?!\\)")|((?!\\)\')).*)#(?!.*(?=((?!\\)\')|((?!\\)")))', start, tk.END, regexp=True)
            if not index:
                break
            self.text_widget.tag_add("comment", index, f"{index} lineend")
            start = f"{index}+1c"
        
        #highlight numbers
        start = 1.0
        patt = r"([0-9]+)|([0-9]+\.[0-9]+)"
        while True:
            start = self.text_widget.search(patt, start, tk.END, regexp=True, count=count)
            if not start:
                break
            end = f"{start}+{count.get()-1}c"
            self.text_widget.tag_add("number", start, end)
            start = f"{start}+{count.get()}c"
        
root = tk.Tk()
TextEditor(root)
root.mainloop()