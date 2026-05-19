import os
import re

def remove_emojis(text):
    # Use a simpler regex for emoji removal that avoids unicode decode errors
    # Range covering common emojis
    return re.sub(r'[^\x00-\x7F\u4e00-\u9fa5\n\r\t]+', '', text)

def tone_down_language(text):
    replacements = [
        (r'(?i)\benterprise-grade\b', 'standard'),
        (r'(?i)\belegantly\b', 'simply'),
        (r'(?i)\belegant\b', 'simple'),
        (r'(?i)\bincredibly\b', 'very'),
        (r'(?i)\bincredible\b', 'great'),
        (r'(?i)\bhighly\b', 'very'),
        (r'(?i)\bperfectly\b', 'accurately'),
        (r'(?i)\bperfect\b', 'exact'),
        (r'(?i)\bseamlessly\b', 'easily'),
        (r'(?i)\bseamless\b', 'smooth'),
        (r'(?i)\bextremely\b', 'very'),
        (r'(?i)\bbeautiful\b', 'clear'),
        (r'(?i)\bamazing\b', 'good'),
        (r'(?i)\brobust\b', 'stable'),
        (r'(?i)\bpowerful\b', 'capable')
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    
    # Fix double spaces caused by removing words if repl was empty
    text = text.replace('  ', ' ')
    return text

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Don't remove emojis indiscriminately because it might strip formatting characters or quotes.
        # Just use the word replacer. We can manually fix the emojis if there are any.
        new_content = tone_down_language(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk('./automated-rag-evaluator'):
        if '.venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py') or file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
