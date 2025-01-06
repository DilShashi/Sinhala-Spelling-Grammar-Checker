# Sinhala Spell and Grammar Checker

## Features

### 1. **Spelling Correction**
- Detects and corrects misspelled words in Sinhala sentences.
- Uses a predefined dictionary of correct Sinhala words.
- Implements a word similarity algorithm (e.g., Levenshtein distance) to suggest the most accurate correction for misspelled words.

### 2. **Grammar Correction**
- Identifies grammatical inconsistencies in sentences by focusing on the relationship between the subject and verb.
- Corrects verbs to match the subject in both present and past tenses.
- Converts informal or incorrect verb forms to their formal equivalents.

### 3. **Support for Multiple Tenses**
- Present Tense: Converts verbs in the **Normal Verb - Present Tense** form to **Written Verb - Present Tense**.
- Past Tense: Converts verbs in the **Normal Verb - Past Tense** form to **Written Verb - Past Tense**.

### 4. **Sentence-Level Analysis**
- Splits input paragraphs into sentences for individual processing.
- Identifies the first word (subject) and the last word (verb) in each sentence for grammar correction.

### 5. **Integration with Machine Learning (Optional)**
- Uses NLP techniques like word embeddings and n-grams for advanced text analysis.
- Optionally employs machine learning models to predict correct spellings and grammatical structures based on context.

## Workflow

### Spelling Correction Workflow
1. Tokenizes the input text into words.
2. Compares each word against a predefined dictionary.
3. Identifies misspelled words and suggests corrections based on:
   - Word similarity (e.g., edit distance).
   - Frequency of occurrence in the dataset.

### Grammar Correction Workflow
1. Splits the paragraph into sentences.
2. For each sentence:
   - Identifies the first word (subject) and last word (verb).
   - Matches the last word with the dataset to find its corresponding row.
   - Replaces the verb with its correct written form based on the subject and tense.

## Example

### Input
මම සෙල්ලම් කරනවා. ඔහු තරග පරදිනවා. අපි වැරදි වළක්වනවා.

### Processing
1. **Spelling Check**:
   - Verifies each word against the dictionary to ensure correct spelling.
   - Corrects misspelled words (if any).

2. **Grammar Check**:
   - Identifies:
     - Subject: `"මම"`, `"ඔහු"`, `"අපි"`
     - Verb: `"කරනවා"`, `"පරදිනවා"`, `"වළක්වනවා"`
   - Corrects verbs based on subject:
     - `"කරනවා"` → `"කරමි"`
     - `"පරදිනවා"` → `"පරදියි"`
     - `"වළක්වනවා"` → `"වළකමු"`

### Output
මම සෙල්ලම් කරමි. ඔහු තරග පරදියි. අපි වැරදි වළකමු.

## Dataset Structure

The tool uses a CSV dataset (`verbs.csv`) for grammar correction and a data file (`data-spell-checker.xlsx`) for spelling correction.

### CSV Dataset for Grammar Correction
- **Columns**:
  - **Subject**: The subject of the sentence (e.g., "මම", "ඔහු", "අපි").
  - **Normal Verb - Present Tense**: The informal present tense verb form.
  - **Written Verb - Present Tense**: The formal present tense verb form.
  - **Normal Verb - Past Tense**: The informal past tense verb form.
  - **Written Verb - Past Tense**: The formal past tense verb form.

### Dictionary for Spelling Correction
- A list of correctly spelled Sinhala words.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sinhala-spell-grammar-checker.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the required files in the project directory:
   - `verbs.csv`: Dataset for grammar correction.
   - `sinhala_words.txt`: Dictionary for spelling correction.
4. Run the program:
   ```bash
   python sinhala_spell_grammar_checker.py
   ```
5. Input your Sinhala paragraph when prompted, and view the corrected output.

---

## Future Enhancements

1. **Dynamic Dictionary Expansion**:
   - Allow users to add new words to the dictionary for improved spelling correction.

2. **Support for Complex Sentences**:
   - Extend grammar rules to handle complex and compound sentences.

3. **Spell Error Suggestions**:
   - Provide alternative suggestions for misspelled words.

4. **Integration with Deep Learning**:
   - Use transformer models (e.g., BERT) for context-aware corrections.

## Contribution

Feel free to contribute to this project by:
- Expanding the dataset for better accuracy.
- Improving algorithms for faster and more reliable processing.
- Adding features like a GUI for user-friendly interaction.
