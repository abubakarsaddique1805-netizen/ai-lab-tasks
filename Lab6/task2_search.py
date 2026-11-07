"""Lab 6 / Task 2: compare lexical and semantic search over original chunks."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from task2_chunks import DOCS,make_chunks
QUERIES=[
    'May someone with an emergency hand in an assignment after the deadline?',
    'Is a later return possible for a library book recalled for inspection?',
    'What if transport trouble causes me to reach the examination late?',
]

def show(label,scores,records,top=3):
    print('\n',label)
    for index in sorted(range(len(records)),key=lambda i:(-float(scores[i]),i))[:top]:
        r=records[index]
        assert DOCS[r['doc']][r['start']:r['end']]==r['text']
        print(f"{r['id']} | {r['doc']} | {r['start']}:{r['end']} | score={float(scores[index]):.3f}")
        print('Original evidence:',r['text'])

def main():
    records=make_chunks(DOCS,'sentence')
    texts=[r['text'] for r in records]
    tfidf=TfidfVectorizer()
    matrix=tfidf.fit_transform(texts)
    model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',device='cpu')
    for text in texts+QUERIES:
        tokens=model.tokenizer(text,truncation=False)['input_ids']
        if len(tokens)>model.max_seq_length:raise ValueError('Text exceeds encoder limit')
    embeddings=model.encode(texts,normalize_embeddings=True)
    for query in QUERIES:
        print('\n'+'='*60,'\nQUERY:',query)
        lexical=(tfidf.transform([query])@matrix.T).toarray()[0]
        semantic=embeddings@model.encode([query],normalize_embeddings=True)[0]
        show('TF-IDF',lexical,records)
        show('REAL EMBEDDINGS',semantic,records)
    print('Scores from these two methods have different meanings; inspect source evidence.')

if __name__=='__main__':main()
