import pandas as pd
import os
import spacy

# Load dataset from Excel or existing CSV file
def load_dataset(file_path):
    csv_file_path = file_path.replace('.xlsx', '.csv')
    
    # Check if CSV already exists, if not, convert Excel to CSV
    if not os.path.exists(csv_file_path):
        df = pd.read_excel(file_path)  # Load Excel file
        df.to_csv(csv_file_path, index=False)  # Convert to CSV
    else:
        df = pd.read_csv(csv_file_path)  # Load existing CSV file
    return df

# Prepare a dictionary of grammar rules based on tense type
def prepare_nlp_rules(df, tense_type):
    rules = {}
    if tense_type == "present":
        for _, row in df.iterrows():
            subject = row['Subject']
            normal_verb = row['Normal verb - Present tense']
            written_verb = row['Written verb - Present tense']
            rules[(subject.lower(), normal_verb.lower())] = written_verb
    elif tense_type == "past":
        for _, row in df.iterrows():
            subject = row['Subject']
            normal_verb = row['Normal verb - Past tense']
            written_verb = row['Written verb - Past tense']
            rules[(subject.lower(), normal_verb.lower())] = written_verb
    else:
        raise ValueError("Invalid tense_type. Use 'present' or 'past'.")
    return rules

# Predict the corrected verbs using NLP rules
def predict_with_rules(paragraph, rules):
    # Split the paragraph into sentences
    sentences = paragraph.split('.')
    results = []

    for sentence in sentences:
        if not sentence.strip():
            continue
        words = sentence.strip().split()
        if len(words) >= 2:
            subject = words[0].lower()  # First word as subject
            last_word = words[-1].lower()  # Last word as normal verb
            
            # Apply rule-based correction
            key = (subject, last_word)
            if key in rules:
                corrected_verb = rules[key]
                words[-1] = corrected_verb

        corrected_sentence = " ".join(words)
        results.append(corrected_sentence)

    return ". ".join(results)

# Main grammar check function
def grammar_check(spell_corrected_paragraph, tense_type):
    # Path to the Excel file containing the rules
    excel_file_path = "verbs.xlsx"

    # Load the dataset
    df = load_dataset(excel_file_path)

    # Prepare rules based on the tense type
    rules = prepare_nlp_rules(df, tense_type)

    # Correct the paragraph using the rules
    corrected_paragraph = predict_with_rules(spell_corrected_paragraph, rules)

    return corrected_paragraph
