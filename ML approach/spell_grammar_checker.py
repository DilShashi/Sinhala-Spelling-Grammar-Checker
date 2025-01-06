import tkinter as tk
from tkinter import ttk, messagebox
from grammar_checker import grammar_check
from spell_checker import get_corrected_paragraph
from sklearn.metrics import accuracy_score  # Example evaluation metric

# Global variable to store the selected tense
tense_type = None

# Function to select tense type
def select_tense(selected_tense):
    global tense_type
    tense_type = selected_tense
    tense_label.config(text=f"Selected Tense: {tense_type.capitalize()}")

# Function to process input and apply spell & grammar correction
def process_paragraph():
    if tense_type not in ["present", "past"]:
        messagebox.showwarning("Tense Selection Error", "Please select a tense (Present or Past).")
        return

    # Get user input
    input_paragraph = input_text.get("1.0", tk.END).strip()

    if not input_paragraph:
        messagebox.showwarning("Input Error", "Please enter a paragraph.")
        return

    # First, get the corrected paragraph from spell checker
    spell_corrected_paragraph = get_corrected_paragraph(input_paragraph)

    # Then, apply grammar correction
    corrected_paragraph = grammar_check(spell_corrected_paragraph, tense_type)

    # Display the corrected paragraph in the GUI
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, corrected_paragraph)

    # Make the true paragraph input box and evaluation button visible
    true_paragraph_label.pack(pady=10)
    true_paragraph_input.pack(pady=5)
    evaluate_button.pack(pady=10)

# Function to evaluate the corrected paragraph with the true paragraph
def evaluate_paragraph():
    true_paragraph = true_paragraph_input.get("1.0", tk.END).strip()
    corrected_paragraph = output_text.get("1.0", tk.END).strip()

    if not true_paragraph:
        messagebox.showwarning("Input Error", "Please enter the true paragraph.")
        return

    # Calculate evaluation metric (e.g., accuracy)
    true_words = true_paragraph.split()
    corrected_words = corrected_paragraph.split()

    accuracy = accuracy_score(true_words, corrected_words)

    # Display evaluation results in the GUI
    evaluation_result.delete(1.0, tk.END)
    evaluation_result.insert(tk.END, f"Evaluation Accuracy: {accuracy:.2f}")

    # Make the evaluation results section visible after clicking the evaluate button
    evaluation_label.pack(pady=10)
    evaluation_result.pack(pady=5)

# Setting up the GUI
root = tk.Tk()
root.title("Sinhala Spell & Grammar Checker")

# Create a canvas and scrollbar for vertical scrolling
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Content inside the scrollable frame
tense_label = tk.Label(scrollable_frame, text="Select Tense:")
tense_label.pack(pady=10)

present_button = tk.Button(scrollable_frame, text="Present Tense", command=lambda: select_tense("present"))
present_button.pack(pady=5)

past_button = tk.Button(scrollable_frame, text="Past Tense", command=lambda: select_tense("past"))
past_button.pack(pady=5)

tense_label = tk.Label(scrollable_frame, text="Selected Tense: None")
tense_label.pack(pady=10)

input_label = tk.Label(scrollable_frame, text="Enter Sinhala Paragraph:")
input_label.pack(pady=10)
input_text = tk.Text(scrollable_frame, height=6, width=50)
input_text.pack(pady=5)

process_button = tk.Button(scrollable_frame, text="Check Spelling and Grammar", command=process_paragraph)
process_button.pack(pady=10)

output_label = tk.Label(scrollable_frame, text="Corrected Paragraph:")
output_label.pack(pady=10)
output_text = tk.Text(scrollable_frame, height=6, width=50)
output_text.pack(pady=5)

true_paragraph_label = tk.Label(scrollable_frame, text="Enter True Paragraph (Without Errors):")
true_paragraph_input = tk.Text(scrollable_frame, height=6, width=50)
evaluate_button = tk.Button(scrollable_frame, text="Evaluate", command=evaluate_paragraph)

evaluation_label = tk.Label(scrollable_frame, text="Evaluation Results:")
evaluation_result = tk.Text(scrollable_frame, height=4, width=50)

true_paragraph_label.pack_forget()
true_paragraph_input.pack_forget()
evaluate_button.pack_forget()
evaluation_label.pack_forget()
evaluation_result.pack_forget()

root.mainloop()
