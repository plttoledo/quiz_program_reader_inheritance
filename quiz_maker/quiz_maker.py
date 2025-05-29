import tkinter as tk
from tkinter import ttk, Button, Radiobutton, IntVar

class quiz_creator:
    def __init__(self,window):
        # The parent window and its contents
        self.window = window
        self.window.geometry('600x500')
        self.window.title('Quiz Creator')  # Title bar
        self.window.configure(bg='#f1dede')  # Background color

        # Color and Other Variables
        self.header_clr = '#d496a7' # Dark Pink
        self.main_clr = '#f1dede' # Light Pink
        self.font_clr = '#542e38' # Darker Pink
        self.var = IntVar()
        self.qstn_data = []

        self.setup_layout()
        self.create_widget()

    def setup_layout(self):
        # Aesthetics
        header = tk.Frame(self.window, bg="#c48c9f", height=100, bd=1, relief='solid')
        header.pack(fill="x")

        header_label = tk.Label(header, text="Quiz Creator", bg="#c48c9f",
                                fg=self.font_clr, font=("Trebuchet MS", 45, "bold"))
        header_label.grid(padx=40, sticky="w")

        footer = tk.Frame(self.window, bg="#c48c9f", height=60, bd=1, relief='solid')
        footer.pack(fill="x", side='bottom')

    def create_widget(self):
        # Question Text
        question = tk.Label(self.window, text='Question:', font=('Trebuchet MS', 25, 'bold'),
                            fg=self.font_clr, bg=self.main_clr)
        question.pack(padx=40, pady=10, anchor='w')

        # Question textbox
        self.textbox_q = tk.Text(self.window, font=('Arial', 15), height=1, bd=1, relief='solid')
        self.textbox_q.pack(padx=40, anchor='w')

        self.textbox_a = self.answer_button(1, 'A')
        self.textbox_b = self.answer_button(2, 'B')
        self.textbox_c = self.answer_button(3, 'C')
        self.textbox_d = self.answer_button(4, 'D')

        btn_one = Button(self.window, text="Next Question", bg=self.header_clr,
                         font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                         width=15, command=self.next_question)
        btn_one.pack(side='left', padx=40)

        btn_two = Button(self.window, text="Save", bg=self.header_clr,
                         font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                         width=10, command=self.save_button)
        btn_two.pack(side='left', padx=0)

        btn_three = Button(self.window, text="Exit", bg=self.header_clr,
                           font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                           width=10, command=self.exit_prog)
        btn_three.pack(side='left', padx=40)

    # Radio Buttons, placed beside the text boxes
    def answer_button(self, var_value, option_letter):
        frame = tk.Frame(self.window, bg=self.main_clr)
        frame.pack(padx=40, pady=10, anchor='w')

        textbox = tk.Text(frame, font=('Arial', 10), height=1, width=65, bd=1, relief='solid')
        textbox.pack(side="left")

        radiobtn = Radiobutton(frame, variable=self.var, value=var_value, bg=self.main_clr,
                               selectcolor=self.header_clr)
        radiobtn.pack(side="left", padx=(10, 2))

       # Label letters at the right side
        label = tk.Label(frame, text=option_letter, font=('Arial', 12, 'bold'),
                         fg=self.font_clr, bg=self.main_clr)
        label.pack(side="left", padx=(0, 10))

        return textbox

    # Functionalities
    def next_question(self):
        question_text = self.textbox_q.get('1.0', 'end').strip()
        answers = [
            self.textbox_a.get('1.0', 'end').strip(),
            self.textbox_b.get('1.0', 'end').strip(),
            self.textbox_c.get('1.0', 'end').strip(),
            self.textbox_d.get('1.0', 'end').strip()
        ]
        correct = self.var.get()

        if question_text and all(answers) and correct:
            self.qstn_data.append({
                'question': question_text,
                'answers': answers,
                'correct': correct
            })

            # Clear inputs when next question
            self.textbox_q.delete('1.0', 'end')
            self.textbox_a.delete('1.0', 'end')
            self.textbox_b.delete('1.0', 'end')
            self.textbox_c.delete('1.0', 'end')
            self.textbox_d.delete('1.0', 'end')
            self.var.set(0)
        else:
            print("Please input all fields and select the correct answer before going to the next question.")

    def save_button(self):
        with open('quiz_data.txt', 'w', encoding='utf-8') as file:
            for i, q in enumerate(self.qstn_data, 1):
                file.write(f"Q{i}: {q['question']}\n")
                for idx, ans in enumerate(q['answers']):
                    letter = chr(65 + idx)
                    correct_mark = " (Correct)" if (idx + 1) == q['correct'] else ""
                    file.write(f"   {letter}. {ans}{correct_mark}\n")
                file.write("\n")
        print("Quiz saved to quiz_data.txt")

    def exit_prog(self):
        self.window.destroy()