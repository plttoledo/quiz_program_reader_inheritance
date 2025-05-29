import tkinter as tk
from quiz_viewer import quiz_reader

if __name__ == '__main__':
    window = tk.Tk()
    app = quiz_reader(window)
    window.mainloop()