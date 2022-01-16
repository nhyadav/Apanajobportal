from django import forms
from django.contrib.auth import authenticate
from django.contrib import auth

from .models import Category, Job, SaveJob, Applicant, UserDetails

class UserDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['description'].label = "User Descriptions :"
        self.fields['age'].label = "User Age :"
        self.fields['contact_no'].label = "User Contact No :"
        self.fields['education'].label = "User Last Education Certificate :"
        self.fields['address'].label = "User Address :"
        self.fields['country'].label = "Country :"
        self.fields['company_name'].label = "Company/organization/School :"

        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'eg : Tell me about yourself',
            }
        )        
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': 'eg : 18 < age',
            }
        )     
        self.fields['contact_no'].widget.attrs.update(
            {
                'placeholder': 'eg : 9193****96',
            }
        )   
        self.fields['education'].widget.attrs.update(
            {
                'placeholder': 'eg : Beachlor of Science',
            }
        )   
        self.fields['address'].widget.attrs.update(
            {
                'placeholder': 'eg : Your Parmanent Addrss',
            }
        )      
        self.fields['country'].widget.attrs.update(
            {
                'placeholder': 'eg : India',
            }
        )           
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'eg : Company/Organization/College/School',
            }
        )  

    class Meta:
        model = UserDetails 
        fields = ['description',
            'age',
            'contact_no',
            'education',
            'address',
            'country',
            'company_name'
        ]                 

    def save(self, commit=True):
        userdetails = super(UserDetailForm, self).save(commit=False)
        if commit:
            userdetails.save()
        return userdetails
        





    

class JobForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['company_url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : India',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$1000 - $2200',
            }
        )                     
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
                
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['company_url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    


    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "company_url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category


    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            job.save()
        return job




class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['resume']

# class JobSaveForm(forms.ModelForm):
#     class Meta:
#         model = SaveJob
#         fields = ['job']




class JobEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['company_url'].label = "Website :"
        self.fields['company_description'].label = "Company Description :"



        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : India',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$1000 - $2200',
            }
        )                      
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['company_url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    
        self.fields['company_description'].widget.attrs.update(
            {
                'placeholder': 'Explain the about company.',
            }
        )    

    
        last_date = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': 'Service Name',
                    'class' : 'datetimepicker1'
                }))

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "company_url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required")
        return category


    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
      
        if commit:
            job.save()
        return job