from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, TeacherProfile, Subject, Group

class StudentCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Ad", widget=forms.TextInput(attrs={'placeholder': 'Ad'}))
    last_name = forms.CharField(required=True, label="Soyad", widget=forms.TextInput(attrs={'placeholder': 'Soyad'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Qrup", empty_label="Qrup seçin")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(user=user, group=self.cleaned_data['group'])
        return user

class TeacherCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Ad", widget=forms.TextInput(attrs={'placeholder': 'Ad'}))
    last_name = forms.CharField(required=True, label="Soyad", widget=forms.TextInput(attrs={'placeholder': 'Soyad'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
            TeacherProfile.objects.create(user=user)
        return user

class SubjectForm(forms.ModelForm):
    name = forms.CharField(label="Fənn adı", widget=forms.TextInput(attrs={'placeholder': 'Fənn adı'}))
    class Meta:
        model = Subject
        fields = ['name']

class GroupForm(forms.ModelForm):
    name = forms.CharField(label="Qrup adı", widget=forms.TextInput(attrs={'placeholder': 'Qrup adı'}))
    class Meta:
        model = Group
        fields = ['name']

class TeacherAssignmentForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False, 
        label="Fənlər"
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False, 
        label="Qruplar"
    )

    class Meta:
        model = TeacherProfile
        fields = ['subjects', 'groups']
