from spellchecker import SpellChecker

def correct_grammar(sentence):
    spell = SpellChecker()
    
    # Split the sentence into words
    words = sentence.split()
    
    # Find misspelled words
    misspelled = spell.unknown(words)
    
    # Correct misspelled words
    corrected_sentence = []
    for word in words:
        if word in misspelled:
            # Replace misspelled word with the most likely correction
            corrected_sentence.append(spell.correction(word))
        else:
            corrected_sentence.append(word)
    
    return ' '.join(corrected_sentence)

# Example sentence with grammar errors
sentence = "As i dont knw the Doutput of the sytsem"

# Correct the grammar
corrected_sentence = correct_grammar(sentence)

# Print the corrected sentence
print("Original Sentence:", sentence)
print("Corrected Sentence:", corrected_sentence)
