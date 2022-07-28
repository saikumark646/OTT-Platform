from django import forms

class RatingForm(forms.Form):
    
    rating_choices = (
    (0,'Zero'),
    (1,'ONE'),
    (2,'TWO'),
    (3,'THREE'),
    (4,'FOUR'),
    (5,'FIVE')
)   
    rating = forms.ChoiceField(label='Rate',choices = rating_choices)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type_id = forms.IntegerField(widget=forms.HiddenInput)
    next = forms.CharField(widget=forms.HiddenInput)
        