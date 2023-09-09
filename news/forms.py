from django.forms import ModelForm, Textarea, Select, TextInput
from .models import Post

class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categoryType', 'postCategory']
        widgets = {
                    'title': Textarea(attrs={'class': 'title_class'}),
                    'text': Textarea(attrs={'class': 'text_class'}),
  #                  'author': TextInput(attrs={'class': 'author_class'}),
                    'categoryType': Select(attrs={'class': 'category_class'}),
  #                  'postCategory': Select(attrs={'class': 'category_class'})
                }
