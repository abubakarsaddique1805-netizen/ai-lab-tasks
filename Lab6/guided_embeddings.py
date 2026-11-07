"""Lab 6: semantic retrieval using genuine pretrained model vectors."""
import numpy as np
from sentence_transformers import SentenceTransformer

def main():
    passages=[
        'Use the account recovery page to change a forgotten password.',
        'Upload your completed coursework through the student portal.',
        'A printer with pale pages may need a new ink cartridge.',
    ]
    question='What should I do when I cannot remember my login password?'
    encoder=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',device='cpu')
    vectors=encoder.encode(passages,normalize_embeddings=True)
    query_vector=encoder.encode([question],normalize_embeddings=True)
    scores=(query_vector@vectors.T)[0]
    print('Embedding matrix shape:',vectors.shape)
    for index in np.argsort(-scores):
        print(f'{float(scores[index]):.3f}',passages[index])
    assert np.allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-5)

if __name__=='__main__':main()
