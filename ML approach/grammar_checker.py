import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
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

# Prepare data for ML based on the tense type
def prepare_ml_data(df, tense_type):
    if tense_type == "present":
        X = df[['Subject', 'Normal verb - Present tense']].apply(lambda x: " ".join(x), axis=1)
        y = df['Written verb - Present tense']
    elif tense_type == "past":
        X = df[['Subject', 'Normal verb - Past tense']].apply(lambda x: " ".join(x), axis=1)
        y = df['Written verb - Past tense']
    else:
        raise ValueError("Invalid tense_type. Use 'present' or 'past'.")
    return X, y

# Train a Decision Tree model
def train_model(X, y):
    # Convert text data into numeric format
    vectorizer = CountVectorizer()
    X_transformed = vectorizer.fit_transform(X)

    # Train a Decision Tree Classifier
    model = DecisionTreeClassifier()
    model.fit(X_transformed, y)

    return model, vectorizer

# Check if the subject matches specific conditions
def match_special_rules(subject):
    if subject.endswith("ලා"):
        return "ඔවුහු"
    elif subject[-1] == "ෝ":  # Check if the last letter is combined with the vowel "ඕ"
        return "ඔවුහු"
    else:
        return None

# Predict the corrected verbs using the trained model
def predict_with_model(paragraph, model, vectorizer, tense_type, df):
    # Split the paragraph into sentences
    sentences = paragraph.split('.')
    results = []

    for sentence in sentences:
        if not sentence.strip():
            continue
        words = sentence.strip().split()
        if len(words) >= 2:
            subject = words[0]  # First word as subject
            last_word = words[-1]  # Last word as normal verb

            # Apply special rules
            matched_subject = match_special_rules(subject)
            if matched_subject:
                # Get the correct verb for "ඔවුහු"
                correct_verb = df.loc[df['Subject'] == matched_subject, f'Written verb - {tense_type.title()} tense'].values
                if len(correct_verb) > 0:
                    words[-1] = correct_verb[0]
                else:
                    # Fallback to default if not found
                    words[-1] = last_word
            elif not any(df['Subject'] == subject):  # Subject not in dataset
                # Get the correct verb for "ඔහු"
                correct_verb = df.loc[df['Subject'] == "ඔහු", f'Written verb - {tense_type.title()} tense'].values
                if len(correct_verb) > 0:
                    words[-1] = correct_verb[0]
                else:
                    # Fallback to default if not found
                    words[-1] = last_word
            else:
                # Normal processing with model
                input_text = f"{subject} {last_word}"
                input_vector = vectorizer.transform([input_text])
                predicted_written_verb = model.predict(input_vector)[0]
                words[-1] = predicted_written_verb

            corrected_sentence = " ".join(words)
            results.append(corrected_sentence)

    return ". ".join(results)

# Main grammar check function
def grammar_check(spell_corrected_paragraph, tense_type):
    # Path to the Excel file containing the rules
    excel_file_path = "verbs.xlsx"

    # Load the dataset
    df = load_dataset(excel_file_path)

    # Prepare data based on the tense type
    X, y = prepare_ml_data(df, tense_type)

    # Train the model
    model, vectorizer = train_model(X, y)

    # Correct the paragraph using the trained model
    corrected_paragraph = predict_with_model(spell_corrected_paragraph, model, vectorizer, tense_type, df)

    return corrected_paragraph