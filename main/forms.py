from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class ItemEntryForm(forms.Form):
    item_name = forms.CharField(label = '제목 (64자 이하)', max_length=64)
    expire_date = forms.DateField(label = '만료 날짜')
