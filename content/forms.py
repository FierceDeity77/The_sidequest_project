from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Guide, Review, Topic, Game, Comments, Community


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'platforms', 'genre', 'description', 'release_date', 'game_icon', 'cover_image']
        widgets = {
            'release_date': SelectDateWidget(years=range(1980, 2101)), # best practice to store in the db in this format yyyy-mm-dd
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Game Title"
        self.fields['platforms'].label = "Platform"
        self.fields['genre'].label = "Genre"
        self.fields['description'].label = "Description"
        self.fields['release_date'].label = "Release Date"
        self.fields['game_icon'].label = "Game Icon"
        self.fields['cover_image'].label = "Cover Image"


class TopicForm(forms.ModelForm):
    spoiler = forms.TypedChoiceField(
        choices=((True, 'True'), (False, 'False')),
        coerce=lambda x: x == 'True', # converts True string into True boolean
        widget=forms.Select
    )

    class Meta:
        model = Topic
        fields = ['title', 'content', "spoiler"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spoiler'].label = "Does your post contain any spoilers?"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # make it smaller (default is ~10)
                'placeholder': 'Write a comment...',
            })
        }


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'icon', 'banner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Community Name"
        self.fields['description'].label = "Description"
        self.fields['banner'].label = "Banner Image"
        self.fields['icon'].label = "Icon Image"


class BaseForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'content', 'created_at']
        

class GuideForm(BaseForm):
    class Meta:
        model = Guide
        fields = BaseForm.Meta.fields + ["type"] # add this field for this form


class ReviewForm(BaseForm):
    class Meta:
        model = Review
        exclude = ['updated_at']

