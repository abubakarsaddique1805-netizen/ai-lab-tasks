"""Lab 6 / Task 1: compare whitespace, Unicode regex and model tokenization."""
import re
SAMPLES=["AI helps students learn.","I can't sign in!","Unicode: café, لاہور and 2026."]

def whitespace(text):return text.split()
def unicode_regex(text):return re.findall(r"\w+|[^\w\s]",text,flags=re.UNICODE)

def main():
    for sample in SAMPLES:
        print('TEXT:',sample)
        print('Whitespace:',whitespace(sample))
        print('Unicode regex:',unicode_regex(sample))
    print('Loading real MiniLM tokenizer...')
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    for sample in SAMPLES:
        tokens=tokenizer.tokenize(sample)
        print('MODEL:',repr(sample),'tokens:',tokens,'count:',len(tokens))
    print('Word counts and model subword counts are not necessarily equal.')

if __name__=='__main__':main()
