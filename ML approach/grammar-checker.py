# Inside grammar-checker.py

import re
import sys
sys.path.append(r'c:\Users\dilan\Desktop\Sinhala-Spelling-Grammar-Checker\Rule-based approach')

from spell_checker import get_corrected_paragraph



# Function to apply grammar correction rules
def grammar_check(paragraph):
    # Define the rules for verb modification based on subject
    def apply_rules(sentence):
        # Remove extra spaces before processing
        sentence = sentence.strip()
        if not sentence:  # Check if the sentence is empty
            return sentence

        words = sentence.split()  # Tokenize sentence into words
        subject = words[0]        # First word is the subject
        verb = words[-1]          # Last word is the verb
        
        # Rule 1: If subject is "මම", modify verb ending
        if subject == "මම" and verb.endswith("නවා"):
            verb = verb[:-3] + "මි"
        
        # Rule 2: If subject is "අපි", modify verb ending
        elif subject == "අපි" and verb.endswith("නවා"):
            verb = verb[:-3] + "මු"
        
        # Rule 3: If subject is "ඔහු" or singular pronoun, modify verb ending
        elif subject in ["ඔහු", "ඇය"] and verb.endswith("නවා"):
            verb = verb[:-3] + "යි"
        
        # Rule 4: If subject is plural pronoun, modify verb ending
        elif any(subject.endswith(plural) for plural in ["ලා", "ඔබලා", "නුබලා"]) and verb.endswith("නවා"):
            verb = verb[:-3] + "ති"
        
        # Rule 5: If subject ends with a consonant + "o" vowel sign (e.g., "බල්ලෝ"), modify verb ending
        elif re.search(r'[ක-෴]ෝ$', subject) and verb.endswith("නවා"):
            verb = verb[:-3] + "ති"
        
        # Rule 6: If no rule is satisfied, modify verb ending to "යි"
        else:
            verb = verb[:-3] + "යි"
        
        # Reassemble sentence with the corrected verb
        words[-1] = verb
        return " ".join(words)

    # Split paragraph into sentences using punctuation marks
    sentences = re.split(r'[.!?]\s*', paragraph.strip())  # Split by punctuation marks: period, exclamation mark, or question mark
    corrected_sentences = [apply_rules(sentence) for sentence in sentences if sentence]

    # Reassemble the paragraph
    corrected_paragraph = ". ".join(corrected_sentences) + "."
    return corrected_paragraph

# Sample Input Paragraph
from spell_checker import get_corrected_paragraph

input_paragraph = get_corrected_paragraph("මම දෙඩම් කනවා. අමාලි පාසැලට යනව. අපි කෑම කනවා. කුරුල්ලෝ පියාඹනවා.")
print("Input Paragraph:")
print(input_paragraph)

# Apply the grammar check function
corrected_paragraph = grammar_check(input_paragraph)

# Display the modified paragraph
print("\nModified Paragraph:")
print(corrected_paragraph)
