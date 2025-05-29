import tkinter as tk
from tkinter import ttk, Button, Radiobutton, IntVar

# Color
header_clr = '#d496a7' # Dark Pink
main_clr = '#f1dede' # Light Pink
font_clr = '#542e38' # Darker Pink

# The parent window and its contents
window = tk.Tk()

window.geometry('600x500')
window.title('Quiz Creator') #Title bar

# Aesthetics
window.configure(bg=main_clr) # Background color

header = tk.Frame(window, bg="#c48c9f", height=100, bd=1, relief='solid')
header.pack(fill="x")

header_label = tk.Label(header, text="Quiz Creator", bg="#c48c9f",
                        fg=font_clr, font=("Trebuchet MS", 45, "bold"))
header_label.grid(padx=40, sticky="w")

footer = tk.Frame(window, bg="#c48c9f", height=60, bd=1, relief='solid')
footer.pack(fill="x", side='bottom')

# Question Text
question = tk.Label(window, text='Question:', font=('Trebuchet MS', 25, 'bold'),
                    fg=font_clr, bg=main_clr)
question.pack(padx=40, pady=10, anchor='w')

# Question textbox
textbox_q = tk.Text(window, font=('Arial', 15), height=1, bd=1, relief='solid')
textbox_q.pack(padx=40, anchor='w')

# Radio Buttons, placed beside the text boxes
var = IntVar()
qstn_data = []

def answer_button(window, var_value, option_letter):
    frame = tk.Frame(window, bg=main_clr)
    frame.pack(padx=40, pady=10, anchor='w')

    textbox = tk.Text(frame, font=('Arial', 10), height=1, width=65, bd=1, relief='solid')
    textbox.pack(side="left")

    radiobtn = Radiobutton(frame, variable=var, value=var_value, bg=main_clr,
                           selectcolor=header_clr)
    radiobtn.pack(side="left", padx=(10, 2))

   # Label letters at the right side
    label = tk.Label(frame, text=option_letter, font=('Arial', 12, 'bold'),
                     fg=font_clr, bg=main_clr)
    label.pack(side="left", padx=(0, 10))

    return textbox

textbox_a = answer_button(window,1, 'A')
textbox_b = answer_button(window,2, 'B')
textbox_c = answer_button(window,3, 'C')
textbox_d = answer_button(window,4, 'D')

# Functionalities
def next_question():
    question_text = textbox_q.get('1.0', 'end').strip()
    answers = [
        textbox_a.get('1.0', 'end').strip(),
        textbox_b.get('1.0', 'end').strip(),
        textbox_c.get('1.0', 'end').strip(),
        textbox_d.get('1.0', 'end').strip()
    ]
    correct = var.get()

    if question_text and all(answers) and correct:
        qstn_data.append({
            'question': question_text,
            'answers': answers,
            'correct': correct
        })

        # Clear inputs when next question
        textbox_q.delete('1.0', 'end')
        textbox_a.delete('1.0', 'end')
        textbox_b.delete('1.0', 'end')
        textbox_c.delete('1.0', 'end')
        textbox_d.delete('1.0', 'end')
        var.set(0)
    else:
        print("Please input all fields and select the correct answer before going to the next question.")

def save_button():
    with open('quiz_data.txt', 'w', encoding='utf-8') as file:
        for i, q in enumerate(qstn_data, 1):
            file.write(f"Q{i}: {q['question']}\n")
            for idx, ans in enumerate(q['answers']):
                letter = chr(65 + idx)
                correct_mark = " (Correct)" if (idx + 1) == q['correct'] else ""
                file.write(f"   {letter}. {ans}{correct_mark}\n")
            file.write("\n")
    print("Quiz saved to quiz_data.txt")

def exit_prog():
    window.destroy()

# Buttons, placed at the bottom
btn_one = Button(window, text="Next Question", bg=header_clr,
                 font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                 width=15, command=next_question)
btn_one.pack(side='left', padx=40)

btn_two = Button(window, text="Save", bg=header_clr,
                 font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                 width=10, command=save_button)
btn_two.pack(side='left', padx=0)

btn_three = Button(window, text="Exit", bg=header_clr,
                   font=('Trebuchet MS', 15, 'bold'), bd=1, relief='solid', activebackground=main_clr,
                   width=10, command=exit_prog)
btn_three.pack(side='left', padx=40)

window.mainloop()