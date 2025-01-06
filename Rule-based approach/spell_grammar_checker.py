import tkinter as tk
from tkinter import messagebox
from grammar_checker import grammar_check
from spell_checker import get_corrected_paragraph
from sklearn.metrics import accuracy_score  # Example evaluation metric

# Function to process input and apply spell & grammar correction
def process_paragraph():
    # Get user input
    input_paragraph = input_text.get("1.0", tk.END).strip()

    if not input_paragraph:
        messagebox.showwarning("Input Error", "Please enter a paragraph.")
        return

    # First, get the corrected paragraph from spell checker
    spell_corrected_paragraph, words_to_underline = get_corrected_paragraph(input_paragraph)
    
    # Then, apply grammar correction
    corrected_paragraph = grammar_check(spell_corrected_paragraph)

    # Remove any existing tags
    output_text.tag_remove("blue", "1.0", tk.END)

    # Display the corrected paragraph in the GUI
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, corrected_paragraph)

    # Highlight words to be displayed in blue without underlining
    for word in words_to_underline:
        start_index = "1.0"
        while True:
            start_index = output_text.search(word, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(word)}c"
            output_text.tag_add("blue", start_index, end_index)
            start_index = end_index

    # Configure the blue color tag
    output_text.tag_configure("blue", foreground="blue")

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

# Create text box for user input
input_label = tk.Label(root, text="Enter Sinhala Paragraph:")
input_label.pack(pady=10)
input_text = tk.Text(root, height=6, width=50)
input_text.pack(pady=5)

# Create a button to process the input
process_button = tk.Button(root, text="Check Spelling and Grammar", command=process_paragraph)
process_button.pack(pady=10)

# Create a text box to display the corrected paragraph
output_label = tk.Label(root, text="Corrected Paragraph:")
output_label.pack(pady=10)
output_text = tk.Text(root, height=6, width=50)
output_text.pack(pady=5)

# New Section for True Paragraph input and evaluation
true_paragraph_label = tk.Label(root, text="Enter True Paragraph (Without Errors):")
true_paragraph_input = tk.Text(root, height=6, width=50)
evaluate_button = tk.Button(root, text="Evaluate", command=evaluate_paragraph)

# Create a text box to display evaluation results
evaluation_label = tk.Label(root, text="Evaluation Results:")
evaluation_result = tk.Text(root, height=4, width=50)

# Hide true paragraph input and evaluation button initially
true_paragraph_label.pack_forget()
true_paragraph_input.pack_forget()
evaluate_button.pack_forget()

# Hide evaluation results initially
evaluation_label.pack_forget()
evaluation_result.pack_forget()

# Start the GUI
root.mainloop()
