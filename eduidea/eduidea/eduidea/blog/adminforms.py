
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from dal import autocomplete

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):

    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)
    # 这里自动补全tag和category。
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='部门',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    desc = forms.CharField(widget=forms.Textarea, label='摘要（可选）', required=False)
    is_top = forms.BooleanField(label="是否置顶",required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag','title' ,'desc',
            'is_md', 'content', 'content_md', 'content_ck',
            'status','is_top',
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js', )
