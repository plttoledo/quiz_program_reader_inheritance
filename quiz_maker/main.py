import tkinter as tk
from quiz_maker import quiz_creator

if __name__ == '__main__':
    window = tk.Tk()
    app = quiz_creator(window)
    window.mainloop()