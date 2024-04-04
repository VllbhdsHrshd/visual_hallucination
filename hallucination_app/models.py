from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

hallucination_type = (
    ('not_hallucination', 'No Hallucination'),
    ('hallucination', 'Hallucination')
    # ('extrinsic_hallucination', 'Extrinsic')
)

degree = (
    ('noHallucination', 'No Hallucination'),
    ('alarming', 'Alarming'),
    ('mild', 'Mild'),
    ('low', 'Low')
)

nature = (
    ('noHallucination', 'No Hallucination'),
    ('contextualGuessing', 'Contextual Guessing'),
    ('geographicErratum', 'Geographic Erratum'),
    ('identityIncongruity', 'Identity Incongruity'),
    ('visualIllusion','Visual Illusion'),
    ('vlmasClassifier', 'VLM as Classifier'),
    ('genderAnomaly','Gender Anomaly'),
    ('numericDiscrepancy', 'Numeric Discrepancy'),
    ('wrongReading', 'Wrong Reading')
)


class SubmitText(models.Model):
    txt_type = models.CharField(
        choices=hallucination_type, null=False, max_length=50)
    txt_degree = models.CharField(choices=degree, null=False, max_length=20)
    txt_nature = models.CharField(choices=nature, null=False, max_length=40)
    idx = models.IntegerField()
    tweet = models.TextField()
    image_id = models.TextField()
    description = models.TextField()
    user_ids = models.CharField(max_length=30)

    def __str__(self):
        return str(self.text)


class UserTxt(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    annoted_txt = models.IntegerField()

    def __str__(self):
        return str(self.userid)


class AnnotateCode(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.userid)
