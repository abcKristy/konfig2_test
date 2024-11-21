import tkinter as tk
from tkinter import ttk
import subprocess

class ShellEmulator:
    def __init__(self, master):
        self.master = master
        master.title("Shell Эмулятор")
        master.configure(bg="black")  # Устанавливаем черный фон

        # Фрейм для вывода команд и результатов
        self.output_frame = tk.Frame(master, bg="black")  # Черный фон для фрейма
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        # Текстовое поле для вывода
        self.output_text = tk.Text(self.output_frame, state=tk.DISABLED, wrap=tk.WORD, bg="black", fg="white")  # Черный фон, белый текст
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Фрейм для ввода команд
        self.input_frame = tk.Frame(master, bg="black")  # Черный фон для фрейма
        self.input_frame.pack(fill=tk.X)

        # Поле ввода
        self.input_entry = tk.Entry(self.input_frame, bg="black", fg="white")  # Черный фон, белый текст
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Кнопка "Выполнить"
        self.run_button = tk.Button(self.input_frame, text="Выполнить", command=self.run_command, bg="black", fg="white")  # Черный фон, белый текст
        self.run_button.pack(side=tk.LEFT)

        # Начальный текст в выводе
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "$ ")
        self.output_text.config(state=tk.DISABLED)

        # Фокус на поле ввода
        self.input_entry.focus()

    def run_command(self):
        # Получение команды из поля ввода
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        # Вывод команды в текстовое поле
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, command + "\n")
        self.output_text.config(state=tk.DISABLED)

            # Выполнение команды
        try:
            process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            output = process.stdout
            error = process.stderr

            # Вывод результата в текстовое поле
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, output)
            if error:
                self.output_text.insert(tk.END, error)
            self.output_text.insert(tk.END, "$ ")
            self.output_text.config(state=tk.DISABLED)
        except FileNotFoundError:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Команда не найдена\n$ ")
            self.output_text.config(state=tk.DISABLED)

root = tk.Tk()
app = ShellEmulator(root)
root.mainloop()