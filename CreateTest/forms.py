from django.forms import ModelForm, PasswordInput, DateTimeField ,DateTimeInput
from Test.models import TestPackage
from utils.generate_id import generate_numeric_code
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.core.exceptions import ValidationError

class CreateTestForm(ModelForm):
    def clean_testCode(self):
        code = self.cleaned_data['testCode']
        if not code:
            return generate_numeric_code(TestPackage,'testCode',6)
        if TestPackage.objects.filter(testCode=code).exists():
            raise ValidationError("testCode can't be used")
        return code

    class Meta:
        model = TestPackage
        fields = ['testTitle','testAuthor','testCode','testScheduleOpen','testScheduleClose','timeLimit','passwordAdminTest','passwordTest']

    testScheduleOpen = DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': True,
            }
        )
    )
    testScheduleClose = DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': True,
            }
        )
    )
    def __init__(self, *args, **kwargs):
        super(CreateTestForm, self).__init__(*args, **kwargs)
        self.fields['testScheduleOpen'].required = False
        self.fields['testScheduleClose'].required = False
        self.fields['timeLimit'].required = False
        self.fields['testCode'].required = False
        self.fields['passwordTest'].required = False
        self.fields['passwordTest'].widget = PasswordInput(render_value = True)
        self.fields['passwordAdminTest'].widget = PasswordInput()
