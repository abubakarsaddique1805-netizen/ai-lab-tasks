"""Lab 6 / Task 2: reproducible chunking study with source evidence."""
import re

DOCS = {
    "assignment": """
A training institute operates a demonstration assignment portal for students who are learning how to manage digital coursework. Each learner receives a demonstration account and a calendar showing suggested submission dates. The portal accepts Python programs, project notes, and short reports. Students are encouraged to check their file names before uploading work. The system displays a confirmation message after each successful upload. Students can review their previous submissions from the activity page. A tutor may leave comments to help learners improve their next attempt. The practice portal does not issue real university grades.
Rule: Learners must upload their practice assignments before Wednesday at three in the afternoon. Exception: Learners with an approved emergency extension may upload the assignment on Friday without a penalty.
Learners should keep a local copy of every file they submit. A clear folder structure makes it easier to find earlier work. When students prepare a complicated programming project with several modules and supporting images and explanatory notes and test results and different versions of their source code and screenshots of program output and written reflections about their approach, they should carefully review the complete folder before creating the final upload package so that no important supporting file is accidentally left behind during submission. The help page includes examples of acceptable filenames. Students can also ask a tutor to explain confusing instructions. These instructions are fictional examples for a classroom experiment.
""".strip(),
    "library": """
The training library is a fictional service created for testing a document search program. Readers can browse printed books, reserve quiet tables, and use a computer for research exercises. The library catalogue lists each book by title, author, and subject. A visitor can search the catalogue before arriving. Staff members explain how to use the self service borrowing station. Borrowed items appear in a personal account along with their expected return dates. The library also offers reading workshops for students who want to improve their study habits. None of these instructions describe an actual library.
Rule: Readers must return borrowed books within eleven days of checkout. Exception: Readers whose books are recalled for a safety inspection may return them within sixteen days after receiving written permission.
Readers are encouraged to keep borrowed books away from food and liquids. A damaged book should be reported promptly to the desk. The fictional catalogue also includes journals, maps, and beginner programming guides. When a reader borrows several books for a group project and moves between classrooms and study halls and shared workspaces and outdoor meeting places while carrying notebooks and electronic devices and printed research materials and reference sheets and carefully prepared outlines, the reader should use a protective bag and keep a simple checklist to prevent important library materials from being misplaced during a busy week. Staff can demonstrate how to renew a book online. A short orientation video explains common account features. Visitors may suggest new titles through a feedback form.
""".strip(),
    "exam": """
The learning institute uses a fictional examination schedule to teach students how to search policy documents. Each learner can see practice examination dates on a dashboard. The academy provides sample questions for revision and encourages students to plan their study sessions early. Practice examinations contain multiple choice questions, short answers, and programming exercises. Students can review their scores after the marking process is complete. A coordinator can explain the instructions for a particular practice examination. These rules are not connected to any real academic institution.
Rule: Learners must arrive at the practice examination room ten minutes before the scheduled start. Exception: Learners with documented transport disruption may enter up to eight minutes after the start when the coordinator approves their request.
Learners should bring a pencil, a notebook, and any permitted reference materials. Phones should remain switched off during the practice session. The supervisor announces the remaining time at regular intervals. Students may ask for clarification if an instruction is difficult to understand. When a participant prepares for a lengthy assessment involving algorithm design and database questions and basic programming concepts and written explanations and careful calculations and debugging exercises and interpretation of sample outputs and comparisons between different solutions and discussion of possible errors and thoughtful review of earlier mistakes, the participant should organize revision notes into clear sections and practise under realistic time limits rather than relying only on memorized answers. After the session, students receive feedback. This fictional document tests chunking and retrieval.
""".strip(),
}

# Exact passages to track: each pair must appear together in a chunk.
LABELS = {
    "assignment": (
        "Rule: Learners must upload their practice assignments before Wednesday at three in the afternoon.",
        "Exception: Learners with an approved emergency extension may upload the assignment on Friday without a penalty.",
    ),
    "library": (
        "Rule: Readers must return borrowed books within eleven days of checkout.",
        "Exception: Readers whose books are recalled for a safety inspection may return them within sixteen days after receiving written permission.",
    ),
    "exam": (
        "Rule: Learners must arrive at the practice examination room ten minutes before the scheduled start.",
        "Exception: Learners with documented transport disruption may enter up to eight minutes after the start when the coordinator approves their request.",
    ),
}


def words_with_offsets(text):
    return [(match.start(), match.end()) for match in re.finditer(r"\S+",text)]

def fixed_windows(text, budget=40, overlap=0, base=0):
    if budget<1 or overlap<0 or overlap>=budget:
        raise ValueError('Budget must be positive and overlap smaller than budget')
    spans=words_with_offsets(text)
    output=[]
    for first in range(0,len(spans),budget-overlap):
        last=min(first+budget,len(spans))
        output.append((base+spans[first][0],base+spans[last-1][1]))
        if last==len(spans):break
    return output

def sentence_windows(text,budget=40):
    if budget<1:raise ValueError('Budget must be positive')
    boundaries=[0]+[m.end() for m in re.finditer(r'[.!?]\s+',text)]+[len(text)]
    result=[];pending=None;used=0
    for start,end in zip(boundaries,boundaries[1:]):
        part=text[start:end];length=len(part.split())
        if not length:continue
        if length>budget:
            if pending is not None:result.append(pending)
            result.extend(fixed_windows(part,budget,base=start))
            pending=None;used=0
        elif pending is not None and used+length<=budget:
            pending=(pending[0],end);used+=length
        else:
            if pending is not None:result.append(pending)
            pending=(start,end);used=length
    if pending is not None:result.append(pending)
    return result

def make_chunks(documents,strategy):
    records=[]
    for document,text in documents.items():
        offsets=(sentence_windows(text) if strategy=='sentence'
                 else fixed_windows(text,40,int(strategy)) if strategy in ('0','10')
                 else None)
        if offsets is None:raise ValueError('Unknown chunking strategy')
        for index,(start,end) in enumerate(offsets):
            records.append(dict(id=f'{document}:{strategy}:{index}',doc=document,
                                strategy=strategy,start=start,end=end,text=text[start:end]))
    return records

def preserved(records,document):
    rule,exception=LABELS[document]
    return any(c['doc']==document and rule in c['text'] and exception in c['text'] for c in records)

def run_tests():
    assert fixed_windows('')==[] and sentence_windows('')==[]
    assert len(fixed_windows('small text'))==1
    assert len(sentence_windows('small text'))==1
    for overlap in (-1,40,50):
        try:fixed_windows('hello world',40,overlap)
        except ValueError:pass
        else:raise AssertionError('Invalid overlap accepted')
    long_text=' '.join(['word']*95)+'.'
    assert [len(long_text[a:b].split()) for a,b in sentence_windows(long_text)]==[40,40,15]
    for strategy in ('0','10','sentence'):
        for c in make_chunks(DOCS,strategy):
            assert c['text']==DOCS[c['doc']][c['start']:c['end']]
            assert 0<len(c['text'].split())<=40
    print('PASS: empty, short, invalid overlap, oversized sentence, offsets')

def main():
    print('Lab 6 Task 2: source-preserving chunking')
    for key,document in DOCS.items():
        count=len(document.split());print(key,count,'words')
        assert 150<=count<=250
        assert all(label in document for label in LABELS[key])
    run_tests()
    original=sum(len(text.split()) for text in DOCS.values())
    for strategy in ('0','10','sentence'):
        records=make_chunks(DOCS,strategy)
        lengths=[len(r['text'].split()) for r in records]
        print('\nSTRATEGY:',strategy,'chunks:',len(records),'sizes:',lengths)
        print('Repeated word positions:',sum(lengths)-original)
        for doc in DOCS:print('Rule and exception together',doc,preserved(records,doc))
        for r in records:
            print(r['id'],f"offsets {r['start']}:{r['end']}",repr(r['text']))
    sample='Dr. Amina works here. She teaches, e.g. Python basics.'
    print('\nNaive sentence split:',re.split(r'(?<=[.!?])\s+',sample))
    print('Regex may wrongly split Dr. and e.g.; abbreviations need more careful tokenization.')

if __name__=='__main__':main()
