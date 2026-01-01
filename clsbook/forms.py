# # clsbook/forms.py
# from django import forms
# from .models import ClassBook, Student
# from django.contrib.auth import get_user_model
# from allauth.account.forms import SignupForm

# class ClassBookForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, help_text="Set a password for this class book")

#     class Meta:
#         model = ClassBook
#         fields = ['class_name', 'section', 'teacher_name']

#     def save(self, commit=True):
#         classbook = super().save(commit=False)
#         classbook.set_password(self.cleaned_data['password'])
#         if commit:
#             classbook.save()
#         return classbook

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['first_name', 'middle_name', 'last_name', 'phone_number', 'email',
#                   'branch', 'college_regd', 'roll', 'address']
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'First Name'}),
#             'middle_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'Middle Name (optional)'}),
#             'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'Last Name'}),
#             'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': '+91 XXXXX XXXXX'}),
#             'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'student@example.com'}),
#             'branch': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., CSE'}),
#             'college_regd': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'Unique Regd No'}),
#             'roll': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500', 'placeholder': 'Roll Number'}),
#             'address': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-vertical', 'rows': 3, 'placeholder': 'Full Address'}),
#         }
        
# SECRET_KEY = "CLASEBOOK20PB"
# User = get_user_model()

# class TeacherSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=30, label="First Name", required=True)
#     last_name = forms.CharField(max_length=30, label="Last Name", required=True)
#     phone_number = forms.CharField(max_length=15, label="Phone Number", required=True)
#     secret_key = forms.CharField(
#         max_length=50,
#         label="Secret Key (University Provided)",
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter CLASEBOOK20PB'}),
#         help_text="Only authorized teachers can register"
#     )

#     def clean_email(self):
#             email = self.cleaned_data.get('email')
#             if email and User.objects.filter(email__iexact=email).exists():
#                 raise forms.ValidationError(
#                     "This email address is already registered. "
#                     "Please use a different email or sign in instead."
#                 )
#             return email

# def save(self, request=None):
#         # allauth expects request, not commit
#         user = super().save(request)
        
#         # Save extra fields
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         # If you want to save phone_number, you need a profile model or custom user field
        
#         user.save()
#         return user





# clsbook/forms.py
from django import forms
from .models import ClassBook, Student
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm


class ClassBookForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full pl-10 pr-12 py-3 text-sm font-normal text-white bg-gray-700 border border-gray-600 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
            'placeholder': 'Enter a secure password'
        }),
        help_text="Set a password for this class book"
    )

    class Meta:
        model = ClassBook
        fields = ['class_name', 'section', 'teacher_name', 'teacher_email']  # ✅ Added teacher_email
        widgets = {
            'class_name': forms.TextInput(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 text-sm font-normal text-white bg-gray-700 border border-gray-600 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'e.g., Class 10, Grade 5, Year 12'
            }),
            'section': forms.TextInput(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 text-sm font-normal text-white bg-gray-700 border border-gray-600 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'e.g., A, B, C, Alpha, Beta'
            }),
            'teacher_name': forms.TextInput(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 text-sm font-normal text-white bg-gray-700 border border-gray-600 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': "Enter teacher's full name"
            }),
            'teacher_email': forms.EmailInput(attrs={
                'readonly': 'readonly',
                'class': 'block w-full pl-10 pr-4 py-3 text-sm font-normal text-gray-400 bg-gray-900 border border-gray-600 rounded-lg cursor-not-allowed'
            })
        }

    def save(self, commit=True, user=None):
        """Save classbook with password and user"""
        classbook = super().save(commit=False)
        classbook.set_password(self.cleaned_data['password'])
        
        # Set the created_by field if user is provided
        if user:
            classbook.created_by = user
            # Auto-fill teacher_email if not set
            if not classbook.teacher_email:
                classbook.teacher_email = user.email
        
        if commit:
            classbook.save()
        return classbook


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'phone_number', 'email',
                  'branch', 'college_regd', 'roll', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'First Name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Middle Name (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Last Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'student@example.com'
            }),
            'branch': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., CSE'
            }),
            'college_regd': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Unique Regd No'
            }),
            'roll': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Roll Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-vertical',
                'rows': 3,
                'placeholder': 'Full Address'
            }),
        }


# Secret key for teacher registration
SECRET_KEY = "CLASEBOOK20PB"
User = get_user_model()

class TeacherSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name", required=True)
    last_name = forms.CharField(max_length=30, label="Last Name", required=True)
    phone_number = forms.CharField(max_length=15, label="Phone Number", required=True)
    secret_key = forms.CharField(
        max_length=50,
        label="Secret Key (University Provided)",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter CLASEBOOK20PB'}),
        help_text="Only authorized teachers can register"
    )

    def clean_secret_key(self):
        """Validate the secret key"""
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key != SECRET_KEY:
            raise forms.ValidationError(
                "Invalid secret key. Please contact your administrator."
            )
        return secret_key

    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email address is already registered. "
                "Please use a different email or sign in instead."
            )
        return email

    def save(self, request):
        """Save user with extra fields"""
        # Call parent save method (allauth expects request parameter)
        user = super().save(request)
        
        # Save extra fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Note: phone_number needs to be stored in a Profile model or custom User field
        
        user.save()
        return user
