import sys
sys.path.append(r'c:\Users\dilan\Desktop\Sinhala-Spelling-Grammar-Checker\Rule-based approach')
sys.path.append(r'c:\Users\dilan\Desktop\Sinhala-Spelling-Grammar-Checker')

from spell_checker import get_corrected_paragraph
from paragraphs import get_paragraphs  # Importing the function from paragraphs.py
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from jiwer import wer
from IPython.display import display, Markdown

# Function to tokenize text into words for comparison
def tokenize(text):
    return text.split()

# Function to evaluate the corrected paragraph
def evaluate_paragraph(true_paragraph, corrected_paragraph, input_paragraph):
    # Tokenize true and corrected paragraphs
    true_tokens = tokenize(true_paragraph)
    corrected_tokens = tokenize(corrected_paragraph)

    # Ensure lengths match for accuracy
    max_len = max(len(true_tokens), len(corrected_tokens))
    true_tokens.extend([""] * (max_len - len(true_tokens)))
    corrected_tokens.extend([""] * (max_len - len(corrected_tokens)))

    # Calculate metrics
    accuracy = accuracy_score(true_tokens, corrected_tokens)
    precision = precision_score(true_tokens, corrected_tokens, average='micro', zero_division=0)
    recall = recall_score(true_tokens, corrected_tokens, average='micro', zero_division=0)
    f1 = f1_score(true_tokens, corrected_tokens, average='micro', zero_division=0)
    word_error_rate = wer(true_paragraph, corrected_paragraph)

    # Display paragraphs
    print("\n### Input Paragraph ###")
    print(input_paragraph)
    print("\n### True Paragraph ###")
    print(true_paragraph)
    print("\n### Corrected Paragraph ###")
    print(corrected_paragraph)

    # Display results
    metrics = {
        "Accuracy": accuracy * 100,
        "Precision": precision * 100,
        "Recall": recall * 100,
        "F1-Score": f1 * 100,
        "WER": word_error_rate * 100,
    }

    # Print results in text format
    print("\nEvaluation Results:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}%")

    return metrics

if __name__ == "__main__":
    # Get paragraphs from paragraphs.py
    paragraphs = get_paragraphs()

    # Use the paragraph
    input_paragraph = paragraphs[0]["input_paragraph"]
    true_paragraph = paragraphs[0]["true_paragraph"]

    # Corrected paragraph (output from your grammar checker)
    corrected_paragraph = get_corrected_paragraph(input_paragraph)

    # Evaluate the corrected paragraph
    evaluation_results = evaluate_paragraph(true_paragraph, corrected_paragraph, input_paragraph)
