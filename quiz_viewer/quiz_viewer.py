import tkinter as tk
from tkinter import ttk, Button, Radiobutton, IntVar, filedialog
import random
import sys

class quiz_reader:
    def __init__(self, window):
        # Parent window
        self.window = window
        self.window.geometry('600x500')
        self.window.title('Quiz Reader')  # Title bar
        self.window.configure(bg='#f1dede')  # Background color

        # Color an Other Variable/Data
        self.header_clr = '#d496a7'  # Dark Pink
        self.main_clr = '#f1dede'  # Light Pink
        self.font_clr = '#542e38'  # Darker Pink
        self.var = tk.IntVar()
        self.question_data = []
        self.current_index = 0

        self.setup_layout()
        self.create_widget()

    def setup_layout(self):
        # Aesthetics
        header = tk.Frame(self.window, bg=self.header_clr, height=100, bd=1, relief='solid')
        header.pack(fill="x")

        header_label = tk.Label(header, text="Quiz Reader", bg=self.header_clr, fg=self.font_clr, font=("trebuchet MS", 45, "bold"))
        header_label.grid(padx=40, sticky="w")

        footer = tk.Frame(self.window, bg=self.header_clr, height=60, bd=1, relief='solid')
        footer.pack(fill="x", side='bottom')

    def create_widget(self):
        # Question Text
        self.question_text = tk.Label(self.window, text='Question:', font=('Trebuchet MS', 25, 'bold'),
                                 fg=self.font_clr, bg=self.main_clr)
        self.question_text.pack(padx=40, pady=10, anchor='w')

        # Question Textbox
        self.question_textbox = tk.Text(self.window, font=('Arial', 15), height=1, bd=1, relief='solid',
                                   state='disabled')
        self.question_textbox.pack(padx=40, anchor='w')

        self.option_a = self.answer_field(1, 'A')
        self.option_b = self.answer_field(2, 'B')
        self.option_c = self.answer_field(3, 'C')
        self.option_d = self.answer_field(4, 'D')

        # Bottom Buttons
        load_btn = Button(self.window, text="Load Quiz", bg=self.header_clr,
                          font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                          width=15, command=self.load_quiz)
        load_btn.pack(side='left', padx=40)

        nextq_btn = Button(self.window, text="Next", bg=self.header_clr,
                           font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                           width=10, command=self.next_question)
        nextq_btn.pack(side='left', padx=0)

        exit_btn = Button(self.window, text="Exit", bg=self.header_clr,
                          font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=self.main_clr,
                          width=10, command=self.exit_btn)
        exit_btn.pack(side='left', padx=40)


    # Functionalities
    def answer_field(self, var_value, option_letter):
        frame = tk.Frame(self.window, bg=self.main_clr)
        frame.pack(padx=40, pady=10, anchor='w')

        ans_textbox = tk.Text(frame, font=('Arial', 10), height=1, width=65, bd=1, relief='solid', state='disabled')
        ans_textbox.pack(side='left')

        radio_btn = Radiobutton(frame, variable=self.var, value=var_value, bg=self.main_clr,
                                selectcolor=self.header_clr)
        radio_btn.pack(side='left', padx=(10, 2))

        # Label Letters
        label = tk.Label(frame, text=option_letter, font=('Arial', 12, 'bold'),
                         fg=self.font_clr, bg=self.main_clr)
        label.pack(side='left', padx=(0, 10))

        return ans_textbox

    # Update textbox
    def update_textbox(self, textbox, text):
        self.textbox.config(state='normal')
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', text)
        self.textbox.config(state='disabled')

    # Show the question
    def show_question(self, index):
        if 0 <= index < len(self.question_data):
            question = self.question_data[index]
            self.update_textbox(self.question_textbox, question['question'])
            self.update_textbox(self.option_a, question['answers'][0])
            self.update_textbox(self.option_b, question['answers'][1])
            self.update_textbox(self.option_c, question['answers'][2])
            self.update_textbox(self.option_d, question['answers'][3])
            self.var.set(0)


    # Button Function
    def load_quiz(self):
        file_path = filedialog.askopenfilename(title='Select quiz file',
                                               filetypes=[('Text Files', "*.txt"), ('All Files', '*.*')])

        if not file_path:
            return

        self.question_data = []
        self.current_index = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                question_block = content.split('\n\n')

                for block in question_block:
                    if not block.strip():
                        continue

                    lines = block.strip().split('\n')

                    if len(lines) < 2:
                        continue

                    question_line = lines[0].strip()
                    question_text = ''

                    if question_line.startswith('Q') and ':' in question_line:
                        question_text = question_line[question_line.find(':') + 1:].strip()
                    else:
                        continue

                    answers = []
                    correct_index = -1

                    for line in lines[1:]:
                        line = line.strip()
                        if not line:
                            continue

                        if len(line) > 2 and line[0] in 'ABCD' and line[1] == '.':
                            option = line[0]

                            answer_text = line[2:].strip()

                            if '(Correct)' in line:
                                correct_index = ord(option) - ord('A')
                                answer_text = answer_text.replace('(Correct)', '').strip()

                            answers.append(answer_text)

                    if question_text and len(answers) == 4 and correct_index >= 0:
                        self.question_data.append({
                            'question': question_text,
                            'answers': answers,
                            'correct': correct_index + 1
                        })

            random.shuffle(self.question_data)

            for q in self.question_data:
                correct_answer = q['answers'][q['correct'] - 1]
                random.shuffle(q['answers'])

                new_index = q['answers'].index(correct_answer) + 1
                q['correct'] = new_index

            if self.question_data:
                self.show_question(0)
            else:
                print('There are no questions found in the file.')

        except Exception as e:
            print(f'Error in loading the quiz file: {e}')


    def next_question(self):
        if self.var.get() == 0 and self.question_data:
            print('Answer first before going to the next question.')
            return

        if self.current_index + 1 < len(self.question_data):
            self.current_index += 1
            self.show_question(self.current_index)
        else:
            print('End of the quiz.')


    def exit_btn(self):
        self.window.destroy()