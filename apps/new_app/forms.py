from dataclasses import fields
from pyexpat import model
from django import forms
from new_app.models import (
     Homework,
     File
)


class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = (
            'title',
            'subject',
            'logo',
        )


    class FileForm(forms.ModelForm):

        class Meta:
            model = File
            fields = (
                'title',
                'obj',
                'is_checked',
            )