from django import forms
from . models import SubmitText


hallucination_type = (
    ('not_hallucination', 'No Hallucination'),
    ('hallucination', 'Hallucination')
    # ('extrinsic_hallucination', 'Extrinsic')
)

degree = (
    ('noHallucination', 'No Hallucination'),
    ('alarming', 'Alarming'),
    ('mild', 'Mild'),
    ('low', 'Low'),
    
)

nature = (
    ('noHallucination', 'No Hallucination'),
    ('contextualGuessing', 'Contextual Guessing'),
    ('geographicErratum', 'Geographic Erratum'),
    ('identityIncongruity', 'Identity Incongruity'),
    ('visualIllusion', 'Visual Illusion'),
    ('vlmasClassifier','VLM as Classifier'),
    ('genderAnomaly','Gender Anomaly'),
    ('numericDiscrepancy', 'Numeric Discrepancy'),
    ('wrongReading', 'Wrong Reading')
)


class textform(forms.ModelForm):

    idx = forms.IntegerField(widget=forms.NumberInput(
        attrs={'readonly': 'readonly'}))
    tweet = forms.CharField(widget=forms.Textarea(
        attrs={'readonly': 'readonly', 'style': 'width: 40vw; height: 20vh; font-weight: 500;'}))
    image_id = forms.CharField(widget=forms.Textarea(
        attrs={'readonly': 'readonly', 'hidden': 'hidden'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'readonly': 'readonly', 'style': 'width: 40vw; height: 20vh; font-weight: 500;'}))
    txt_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=hallucination_type)
    txt_degree = forms.ChoiceField(widget=forms.RadioSelect, choices=degree)
    txt_nature = forms.ChoiceField(widget=forms.RadioSelect, choices=nature)

    class Meta:
        model = SubmitText
        fields = ('idx', 'tweet', 'image_id', 'description', 'txt_type',
                  'txt_degree', 'txt_nature')
