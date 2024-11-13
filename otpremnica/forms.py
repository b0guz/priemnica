from django import forms
from datetime import date
from betterforms.multiform import MultiModelForm
from django.forms import DateField, DateInput

from core import settings
from .models import Supplier, MeatType, DispatchNote, Company


class DateFieldInput(forms.DateInput):
    input_type = 'date'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = []


class MeatTypeForm(forms.ModelForm):
    class Meta:
        model = MeatType
        exclude = []


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = []


class DispatchNoteFormAP(forms.ModelForm):
    class Meta:
        model = DispatchNote
        exclude = ['index', 'company', 'supplier', 'sys_doc_date', 'created_by', 'updated_by']
        widgets = {
            'doc_date': DateFieldInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.initial) < 1:
            year = date.today().year
            company = Company.objects.first()
            if DispatchNote.objects.count() < 1:
                new_item = 1
            else:
                notes = DispatchNote.objects.filter(company=company).order_by('-id')
                if notes.count() < 1:
                    new_item = 1
                else:
                    prev_note = notes.first()

                    if prev_note.doc_date.year != year:
                        new_item = 1
                    else:
                        new_item = prev_note.index + 1

            self.initial['doc_number'] = f'{new_item}/{company.book_number}/{year}'

    def clean(self):
        cleaned_data = self.cleaned_data

        doc_number = cleaned_data['doc_number']

        if doc_number and DispatchNote.objects.filter(doc_number=doc_number, company=Company.objects.first()).exclude(pk=self.instance.pk).count() > 0:
            self._errors['doc_number'] = self.error_class(["Document with this number already exist"])

        return cleaned_data


class DispatchNoteFormSid(forms.ModelForm):
    class Meta:
        model = DispatchNote
        exclude = ['index', 'company', 'supplier', 'sys_doc_date', 'created_by', 'updated_by']
        widgets = {
            'doc_date': DateFieldInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.initial) < 1:
            year = date.today().year
            company = Company.objects.last()
            if DispatchNote.objects.count() < 1:
                new_item = 1
            else:
                notes = DispatchNote.objects.filter(company=company).order_by('-id')
                if notes.count() < 1:
                    new_item = 1
                else:
                    prev_note = notes.first()

                    if prev_note.doc_date.year != year:
                        new_item = 1
                    else:
                        new_item = prev_note.index + 1

            self.initial['doc_number'] = f'{new_item}/{company.book_number}/{year}'

    def clean(self):
        cleaned_data = self.cleaned_data

        doc_number = cleaned_data['doc_number']

        if doc_number and DispatchNote.objects.filter(doc_number=doc_number, company=Company.objects.last()).exclude(pk=self.instance.pk).count() > 0:
            self._errors['doc_number'] = self.error_class(["Document with this number already exist"])

        return cleaned_data


class DispatchNoteMultiFormAP(MultiModelForm):
    form_classes = {
        'supplier': SupplierForm,
        'dispatch_note': DispatchNoteFormAP,
    }


class DispatchNoteMultiFormSid(MultiModelForm):
    form_classes = {
        'supplier': SupplierForm,
        'dispatch_note': DispatchNoteFormSid,
    }
