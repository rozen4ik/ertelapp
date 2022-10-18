from django import forms
from django.contrib.auth.models import User
from counterparty.models import Counterparty
from task.models import TypeWork

u = User.objects.all()
ty = TypeWork.objects.all()
ct = Counterparty.objects.all()
full_name_t = [("", "")]
type_t = [("", "")]
counterparty_t = [("", "")]

for f in u:
    full_name_t.append((f"{f.first_name} {f.last_name}", f"{f.first_name} {f.last_name}"))

for t in ty:
    type_t.append((f"{t.name}", f"{t.name}"))

for c in ct:
    counterparty_t.append((f"{c.name} / ({c.work_name})", f"{c.name} / ({c.work_name})"))

status_t = [
    ("", ""),
    ("Отдано в разработку", "Отдано в разработку"),
    ("Выполняется", "Выполняется"),
    ("Выполнено", "Выполнено")
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

    object_task = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        choices=counterparty_t
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

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "type": "date"
            },
        )
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "type": "date"
            },
        )
    )


class ReportsContFilter(forms.Form):
    object_task = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        choices=counterparty_t
    )
