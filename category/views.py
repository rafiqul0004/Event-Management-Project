from django.shortcuts import render,redirect
from .import forms
from django.utils.text import slugify

# Create your views here.
def add_category(request):
    if request.method == 'POST':
        category_form=forms.CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.instance.slug = slugify(category_form.cleaned_data['name'])
            category_form.save()
            return redirect('add_category')
    else:
        category_form=forms.CategoryForm()
    return render(request,'add_category.html',{'form':category_form})