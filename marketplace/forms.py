from django import forms
from .models import FreelancerProfile, Project
from .models import Bid
from .models import Review

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        exclude = ["user"]

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "budget",
            "skills_required",
            "deadline",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        exclude = ["project", "freelancer"]

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.Select(
                choices=[
                    (1, "⭐ 1"),
                    (2, "⭐⭐ 2"),
                    (3, "⭐⭐⭐ 3"),
                    (4, "⭐⭐⭐⭐ 4"),
                    (5, "⭐⭐⭐⭐⭐ 5"),
                ]
            ),

            "comment": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write your review..."
                }
            ),
        }