"""Lab 6 / Task 1: simple TF-IDF FAQ chatbot with suggestions."""
from sklearn.feature_extraction.text import TfidfVectorizer
FAQ=[
 ('How can I reset my password?','Open the account recovery page.'),
 ('Where do I submit assignments?','Upload coursework through the student portal.'),
 ('Can I request extra time?','Contact the tutor with your supporting reason.'),
 ('Where are my grades?','Check the results tab on the portal.'),
 ('How can I message my tutor?','Use the course messaging tool.'),
]

def suggest(question,top=3):
    if not question.strip():return []
    vectorizer=TfidfVectorizer()
    matrix=vectorizer.fit_transform([q+' '+a for q,a in FAQ])
    query=vectorizer.transform([question])
    if query.nnz==0:return []
    scores=(query@matrix.T).toarray()[0]
    ranked=sorted(range(len(FAQ)),key=lambda i:-scores[i])
    return [(FAQ[i][0],FAQ[i][1],round(float(scores[i]),3)) for i in ranked[:top] if scores[i]>0]

if __name__=='__main__':
    for question in ['I forgot my password','How do I hand in my work?','unrelated xyz']:
        print('Question:',question,'\nSuggestions:',suggest(question))
