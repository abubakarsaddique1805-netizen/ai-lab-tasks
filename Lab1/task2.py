"""Lab 1 / Task 2: explainable scholarship screening, synthetic data only."""
MIN_SCORE, MIN_ATTENDANCE, MAX_INCOME = 70, 80, 50000

def screen(application):
    checks = [
        (application['documents'], 'Missing required documents'),
        (application['score'] >= MIN_SCORE, 'Academic score below minimum'),
        (application['attendance'] >= MIN_ATTENDANCE, 'Attendance below minimum'),
        (application['income'] <= MAX_INCOME, 'Income exceeds example cap'),
    ]
    failures = [reason for passed, reason in checks if not passed]
    return ('Hold', failures) if failures else ('Review', ['Eligible for human review'])

def threshold(probability):
    if not 0 <= probability <= 1:
        raise ValueError('Probability must be between 0 and 1')
    return 'Review' if probability >= .70 else 'Hold'

if __name__ == '__main__':
    examples = [
        ('Meets all rules', dict(score=76, attendance=84, income=46000, documents=True), .78, 'Review'),
        ('Missing papers', dict(score=91, attendance=95, income=38000, documents=False), .92, 'Hold'),
        ('Low attendance', dict(score=82, attendance=78, income=42000, documents=True), .81, 'Hold'),
        ('Boundary', dict(score=70, attendance=80, income=50000, documents=True), .70, 'Review'),
        ('Score just below', dict(score=69, attendance=90, income=40000, documents=True), .77, 'Hold'),
    ]
    for label, person, probability, expected in examples:
        result, reasons = screen(person)
        comparison = threshold(probability)
        assert result == expected
        print(f'{label}: rules={result}, score-threshold={comparison}, reasons={reasons}')
    print('Passed five sample cases. All figures are invented for teaching.')
