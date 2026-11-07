"""Lab 6: rank FAQ suggestions using the embedding backend."""
from sentence_transformers import SentenceTransformer
QUESTIONS=[
    ('How can I upload coursework?','Submit the file using the learning portal.'),
    ('How do I recover an account?','Use the account recovery form.'),
    ('Where are course grades displayed?','Open the results section.'),
    ('Can a deadline be extended?','Ask for documented approval.'),
    ('How can I contact the instructor?','Use the course messages page.'),
]

def main():
    encoder=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',device='cpu')
    passages=[question+' '+answer for question,answer in QUESTIONS]
    vectors=encoder.encode(passages,normalize_embeddings=True)
    query='Where should I turn in my class assignment?'
    vector=encoder.encode([query],normalize_embeddings=True)[0]
    scores=vectors@vector
    print('Suggestions for:',query)
    for i in sorted(range(len(QUESTIONS)),key=lambda j:-float(scores[j]))[:3]:
        print(f'{float(scores[i]):.3f}',QUESTIONS[i][0],'-',QUESTIONS[i][1])

if __name__=='__main__':main()
