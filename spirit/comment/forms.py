# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..core import utils
from ..core.utils.markdown import Markdown
from .models import Comment
from ..topic.models import Topic


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', ]

    def __init__(self, user=None, topic=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        self.topic = topic
        self.mentions = None  # {username: User, }
        self.fields['comment'].widget.attrs['placeholder'] = _("Write comment...")

    def _get_comment_html(self):
        markdown = Markdown(escape=True, hard_wrap=True)
        comment_html = markdown.render(self.cleaned_data['comment'])
        self.mentions = markdown.get_mentions()
        return comment_html

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.topic = self.topic

        self.instance.comment_html = self._get_comment_html()
        return super(CommentForm, self).save(commit)


class CommentMoveForm(forms.Form):

    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.TextInput)

    def __init__(self, topic, *args, **kwargs):
        super(CommentMoveForm, self).__init__(*args, **kwargs)
        self.fields['comments'] = forms.ModelMultipleChoiceField(queryset=Comment.objects.filter(topic=topic),
                                                                 widget=forms.CheckboxSelectMultiple)

    def save(self):
        comments = self.cleaned_data['comments']
        comments_list = list(comments)
        topic = self.cleaned_data['topic']
        comments.update(topic=topic)

        # Update topic in comment instance
        for c in comments_list:
            c.topic = topic

        return comments_list


class CommentImageForm(forms.Form):

    image = forms.ImageField()

    def __init__(self, user=None, *args, **kwargs):
        super(CommentImageForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_image(self):
        file = self.cleaned_data['image']

        if file.image.format.lower() not in settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT:
            raise forms.ValidationError(
                _("Unsupported file format. Supported formats are %s."
                  % ", ".join(settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT))
            )

        return file

    def save(self):
        file = self.cleaned_data['image']
        file_hash = utils.get_hash(file)
        file.name = ''.join((file_hash, '.', file.image.format.lower()))
        upload_to = os.path.join('spirit', 'images', str(self.user.pk))
        file.url = os.path.join(settings.MEDIA_URL, upload_to, file.name).replace("\\", "/")
        media_path = os.path.join(settings.MEDIA_ROOT, upload_to)
        utils.mkdir_p(media_path)

        with open(os.path.join(media_path, file.name), 'wb') as fh:
            for c in file.chunks():
                fh.write(c)

            file.close()

        return file
