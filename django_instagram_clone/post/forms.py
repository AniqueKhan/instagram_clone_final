from django import forms 
from .models import Post

class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected':True}),required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'data-role':'tagsinput'}))

    class Meta:
        model = Post
        fields = ('content','caption','tags')
    
