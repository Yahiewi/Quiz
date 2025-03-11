# quiz/models.py
from django.db import models

SUBJECT_CHOICES = [
    ('Vue', 'Vue'),
    ('Django', 'Django'),
    ('HTML_CSS', 'HTML & CSS'),
    ('JS', 'JavaScript'),
    ('TS', 'TypeScript'),
    ('Algorithms', 'Algorithms and Data Structures'),
]

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    answers = models.JSONField()
    correct_answer = models.IntegerField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)

    def __str__(self):
        return self.question_text
