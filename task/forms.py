from django import forms
from django.contrib.auth.models import User


u = User.objects.all()
full_name_t = [("", "")]

for f in u:
    full_name_t.append((f"{f.first_name} {f.last_name}", f"{f.first_name} {f.last_name}"))

status_t = [
    ("", ""),
    ("Отдано в разработку", "Отдано в разработку"),
    ("Выполняется", "Выполняется"),
    ("Выполнено", "Выполнено")
]
type_t = [
    ("", ""),
    ("Гарантийные работы", "Гарантийные работы"),
    ("Ежемесячное ТО", "Ежемесячное ТО"),
    ("Офис", "Офис")
]
business_t = [
    ("", ""),
    ("Не командировка", "Не командировка"),
    ("Командировка", "Командировка")
]


class TaskFilter(forms.Form):
    employee_task = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        choices=full_name_t,
    )

    status_task = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        choices=status_t
    )

    type_task = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        choices=type_t
    )

    business_trip = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            },
        ),
        choices=business_t
    )
