import tkinter as tk
from tkinter import ttk, Button, Radiobutton, IntVar, filedialog
import random
import sys

# Color
header_clr = '#d496a7'  # Dark Pink
main_clr = '#f1dede'  # Light Pink
font_clr = '#542e38'  # Darker Pink

# Parent window
window = tk.Tk()

window.geometry('600x500')
window.title('Quiz Reader')  # Title bar

# Aesthetics
window.configure(bg=main_clr)  # Background color

header = tk.Frame(window, bg=header_clr, height=100, bd=1, relief='solid')
header.pack(fill="x")

header_label = tk.Label(header, text="Quiz Reader", bg=header_clr, fg=font_clr, font=("trebuchet MS", 45, "bold"))
header_label.grid(padx=40, sticky="w")

footer = tk.Frame(window, bg=header_clr, height=60, bd=1, relief='solid')
footer.pack(fill="x", side='bottom')

# Question Text
question_text = tk.Label(window, text='Question:', font=('Trebuchet MS', 25, 'bold'),
                         fg=font_clr, bg=main_clr)
question_text.pack(padx=40, pady=10, anchor='w')

# Question Textbox
question_textbox = tk.Text(window, font=('Arial', 15), height=1, bd=1, relief='solid',
                           state='disabled')
question_textbox.pack(padx=40, anchor='w')

# Functionalities
var = tk.IntVar()


def answer_field(window, var_value, option_letter):
    frame = tk.Frame(window, bg=main_clr)
    frame.pack(padx=40, pady=10, anchor='w')

    ans_textbox = tk.Text(frame, font=('Arial', 10), height=1, width=65, bd=1, relief='solid', state='disabled')
    ans_textbox.pack(side='left')

    radio_btn = Radiobutton(frame, variable=var, value=var_value, bg=main_clr,
                            selectcolor=header_clr)
    radio_btn.pack(side='left', padx=(10, 2))

    # Label Letters
    label = tk.Label(frame, text=option_letter, font=('Arial', 12, 'bold'),
                     fg=font_clr, bg=main_clr)
    label.pack(side='left', padx=(0, 10))

    return ans_textbox


option_a = answer_field(window, 1, 'A')
option_b = answer_field(window, 2, 'B')
option_c = answer_field(window, 3, 'C')
option_d = answer_field(window, 4, 'D')

# Quiz Data
question_data = []
current_index = 0


# Update textbox
def update_textbox(textbox, text):
    textbox.config(state='normal')
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', text)
    textbox.config(state='disabled')


# Show the question
def show_question(index):
    if 0 <= index < len(question_data):
        question = question_data[index]
        update_textbox(question_textbox, question['question'])
        update_textbox(option_a, question['answers'][0])
        update_textbox(option_b, question['answers'][1])
        update_textbox(option_c, question['answers'][2])
        update_textbox(option_d, question['answers'][3])
        var.set(0)


# Button Function
def load_quiz():
    global question_data, current_index
    file_path = filedialog.askopenfilename(title='Select quiz file',
                                           filetypes=[('Text Files', "*.txt"), ('All Files', '*.*')])

    if not file_path:
        return

    question_data = []
    current_index = 0

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
                    question_data.append({
                        'question': question_text,
                        'answers': answers,
                        'correct': correct_index + 1
                    })

        random.shuffle(question_data)

        for q in question_data:
            correct_answer = q['answers'][q['correct'] - 1]
            random.shuffle(q['answers'])

            new_index = q['answers'].index(correct_answer) + 1
            q['correct'] = new_index

        if question_data:
            show_question(0)
        else:
            print('There are no questions found in the file.')

    except Exception as e:
        print(f'Error in loading the quiz file: {e}')


def next_question():
    global current_index
    if var.get() == 0 and question_data:
        print('Answer first before going to the next question.')
        return

    if current_index + 1 < len(question_data):
        current_index += 1
        show_question(current_index)
    else:
        print('End of the quiz.')


def exit_btn():
    window.destroy()


# Bottom Buttons
load_btn = Button(window, text="Load Quiz", bg=header_clr,
                  font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                  width=15, command=load_quiz)
load_btn.pack(side='left', padx=40)

nextq_btn = Button(window, text="Next", bg=header_clr,
                   font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                   width=10, command=next_question)
nextq_btn.pack(side='left', padx=0)

exit_btn = Button(window, text="Exit", bg=header_clr,
                  font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                  width=10, command=exit_btn)
exit_btn.pack(side='left', padx=40)

window.mainloop()