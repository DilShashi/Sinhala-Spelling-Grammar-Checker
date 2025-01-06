import re
import pandas as pd
from difflib import get_close_matches

# Load dataset with correct words
excel_file = r"C:\\Users\\dilan\\Desktop\\Sinhala-Spelling-Grammar-Checker\\data-spell-checker.xlsx"
df = pd.read_excel(excel_file, engine='openpyxl')
correct_words = set(df['word'])

def tokenize_sinhala_text(paragraph):
    """Tokenize Sinhala text by matching Unicode characters."""
    sinhala_pattern = r'[\u0D80-\u0DFF]+'  # Match Sinhala Unicode range
    words = re.findall(sinhala_pattern, paragraph)
    return words

def is_vowel_modifier_difference(word1, word2):
    """Check if the difference between two words is only in vowel modifiers."""
    base_word1 = re.sub(r'[\u0DCF-\u0DFF]', '', word1)  # Remove vowel modifiers from word1
    base_word2 = re.sub(r'[\u0DCF-\u0DFF]', '', word2)  # Remove vowel modifiers from word2
    return base_word1 == base_word2

def matches_custom_rules(word, correct_words):
    """Check if the word matches any of the custom rules."""
    rules = [
        lambda w: w[:-1] in correct_words if w.endswith("\u0D9A") else False,  # Ends with "\u0D9A"
        lambda w: w[:-1] in correct_words if w.endswith("\u0DA7") else False,  # Ends with "\u0DA7"
        lambda w: w[:-1] in correct_words if w.endswith("\u0DB6") else False,  # Ends with "\u0DB6"
        lambda w: w[:-2] in correct_words if w.endswith("\u0D9A\u0DA7") else False,  # Ends with "\u0D9A\u0DA7"
        lambda w: w[:-1] in correct_words if w.endswith("\u0DB2\u0DCA") else False,  # Ends with "\u0DB2\u0DCA"
        lambda w: re.sub(r'[\u0DCF-\u0DFF]', '', w[:-1]) + "\u0DCF" in correct_words  # Replace vowel signs
    ]

    for rule in rules:
        if rule(word):
            return True

    return False

def suggest_corrections(word, correct_words, n=3):
    """Suggest the closest matching words from the dataset."""
    suggestions = get_close_matches(word, correct_words, n=n, cutoff=0.6)
    return suggestions

def correct_sinhala_text(paragraph):
    """Correct spelling mistakes in a Sinhala paragraph."""
    sentences = re.split(r'[.!?]\s*', paragraph.strip())  # Split into sentences
    corrected_paragraph = paragraph
    corrections = []
    corrected_words = {}  # Track already corrected words

    for sentence in sentences:
        tokens = tokenize_sinhala_text(sentence)
        if not tokens:
            continue

        # Keep the first word (subject) and the last word (verb) unchanged
        for i, word in enumerate(tokens):
            if i == 0 or i == len(tokens) - 1:  # Skip first (subject) and last (verb) words
                corrected_words[word] = word
                continue

            if word in corrected_words:
                continue  # Skip if the word has already been corrected

            if word not in correct_words:
                # Check if the word satisfies any of the custom rules
                if matches_custom_rules(word, correct_words):
                    corrected_words[word] = word  # No correction needed, keep the original
                    continue

                # Otherwise, suggest corrections
                suggestions = suggest_corrections(word, correct_words)
                if suggestions:
                    # Check if any suggestion differs only by vowel modifiers
                    for suggestion in suggestions:
                        if is_vowel_modifier_difference(word, suggestion):
                            corrected_paragraph = corrected_paragraph.replace(word, suggestion)
                            corrections.append((word, suggestion))
                            corrected_words[word] = suggestion  # Mark this word as corrected
                            break
                    else:
                        # No suggestion satisfies the vowel modifier rule
                        corrections.append((word, suggestions))
                        corrected_words[word] = None  # Track as not replaceable

    return corrected_paragraph, corrections

# Return corrected paragraph
def get_corrected_paragraph(input_paragraph):
    spell_corrected_paragraph, corrections = correct_sinhala_text(input_paragraph)
    return spell_corrected_paragraph
