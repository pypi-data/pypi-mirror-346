# django_remote_jsonschema_forms


A package that allows you to serialize django forms, including fields and widgets into Python
dictionary for easy conversion into JSON Schema.

This way one can expose a django form using the [JSON Schema](https://json-schema.org/) standard.

These forms can be then rendered using JS libraries like [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/docs/).


This package is heavily based on [django-remote-forms](https://github.com/WiserTogether/django-remote-forms), which we have used as an example. 

We have changed the output format that `django-remote-forms` provides and return a JSON Schema compatible format.


## Usage

Say you have a django form like this one:

```python
from django.db import models
from django import forms

class Task(models.Model):
    text = models.TextField("Text")
    email = models.TextField("Text")

class MyForm(forms.ModelForm):

    class Meta:
        model =  Task

```

You can create a view to expose it in JSON Schema like this:


```python
from .forms import MyForm
from django_remote_jsonschema_forms.forms import RemoteJSONSChemaForm
from django.http import JsonResponse

def json_schema_form_view(request):
    form = MyForm()
    remote_form = RemoteJSONSChemaForm(form)
    return JsonResponse(remote_form.as_dict())

```

Remember that you will need to register a url in `urls.py` to expose it.
