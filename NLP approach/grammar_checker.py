import pandas as pd
import spacy
import os

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

# Check if subject ends with "ලා" or has "ඕ" vowel combination
def is_plural_pronoun(subject):
    return subject.endswith("ලා") or (len(subject) > 1 and subject[-1] == "ෝ")

# Load NLP model for better sentence segmentation and tokenization
def nlp_model_loader():
    # Load the Sinhala language model placeholder
    nlp = spacy.blank("si")
    
    # Add the sentence boundary detector to the pipeline
    nlp.add_pipe('sentencizer')
    
    return nlp


# Predict with NLP rules
def predict_with_nlp_rules(paragraph, rules, df, tense_type):
    # Load NLP model
    nlp = nlp_model_loader()

    # Get the default verb for "ඔහු"
    default_subject = "ඔහු"
    default_verb_col = 'Written verb - Present tense' if tense_type == "present" else 'Written verb - Past tense'
    default_verb = df[df['Subject'] == default_subject][default_verb_col].values[0]

    # Get the verb for "ඔවුහු"
    plural_subject = "ඔවුහු"
    plural_verb = df[df['Subject'] == plural_subject][default_verb_col].values[0]

    # Split the paragraph into sentences using the NLP model
    doc = nlp(paragraph)
    sentences = [sent.text.strip() for sent in doc.sents]

    results = []

    for sentence in sentences:
        if not sentence:
            continue

        words = sentence.split()
        if len(words) >= 2:
            subject = words[0].lower()  # First word as subject
            last_word = words[-1].lower()  # Last word as normal verb

            # Check if subject ends with "ලා" or has "ඕ" vowel combination
            if is_plural_pronoun(subject):
                words[-1] = plural_verb  # Replace with "ඔවුහු" verb
            elif (subject, last_word) in rules:
                words[-1] = rules[(subject, last_word)]  # Use rule-based correction
            else:
                words[-1] = default_verb  # Replace with "ඔහු" verb

        corrected_sentence = " ".join(words)
        results.append(corrected_sentence)

    return ". ".join(results)

# Main grammar check function for NLP approach
def grammar_check(spell_corrected_paragraph, tense_type):
    # Path to the Excel file containing the rules
    excel_file_path = "verbs.xlsx"

    # Load the dataset
    df = load_dataset(excel_file_path)

    # Prepare rules based on the tense type
    rules = prepare_nlp_rules(df, tense_type)

    # Correct the paragraph using the rules
    corrected_paragraph = predict_with_nlp_rules(spell_corrected_paragraph, rules, df, tense_type)

    return corrected_paragraph
