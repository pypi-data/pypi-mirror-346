from collections import OrderedDict

from django import forms
from django_remote_jsonschema_forms import fields, logger
from django_remote_jsonschema_forms.utils import resolve_promise

import json


class RemoteJSONSChemaForm(object):
    def __init__(self, form, *args, **kwargs):
        self.form = form

        self.all_fields = set(self.form.fields.keys())

        self.excluded_fields = set(kwargs.pop("exclude", []))
        self.included_fields = set(kwargs.pop("include", []))
        self.readonly_fields = set(kwargs.pop("readonly", []))
        self.ordered_fields = kwargs.pop("ordering", [])

        self.fieldsets = kwargs.pop("fieldsets", {})

        # Make sure all passed field lists are valid
        if self.excluded_fields and not (self.all_fields >= self.excluded_fields):
            logger.warning(
                "Excluded fields %s are not present in form fields"
                % (self.excluded_fields - self.all_fields)
            )
            self.excluded_fields = set()

        if self.included_fields and not (self.all_fields >= self.included_fields):
            logger.warning(
                "Included fields %s are not present in form fields"
                % (self.included_fields - self.all_fields)
            )
            self.included_fields = set()

        if self.readonly_fields and not (self.all_fields >= self.readonly_fields):
            logger.warning(
                "Readonly fields %s are not present in form fields"
                % (self.readonly_fields - self.all_fields)
            )
            self.readonly_fields = set()

        if self.ordered_fields and not (self.all_fields >= set(self.ordered_fields)):
            logger.warning(
                "Readonly fields %s are not present in form fields"
                % (set(self.ordered_fields) - self.all_fields)
            )
            self.ordered_fields = []

        if self.included_fields | self.excluded_fields:
            logger.warning(
                "Included and excluded fields have following fields %s in common"
                % (set(self.ordered_fields) - self.all_fields)
            )
            self.excluded_fields = set()
            self.included_fields = set()

        # Extend exclude list from include list
        self.excluded_fields |= self.included_fields - self.all_fields

        if not self.ordered_fields:
            if hasattr(self.form.fields, "keyOrder"):
                self.ordered_fields = self.form.fields.keyOrder
            else:
                self.ordered_fields = self.form.fields.keys()

        self.fields = []

        # Construct ordered field list considering exclusions
        for field_name in self.ordered_fields:
            if (
                field_name in self.excluded_fields
                or field_name == "question"
                or field_name == "response"
            ):
                continue

            self.fields.append(field_name)

        # Validate fieldset
        fieldset_fields = set()
        if self.fieldsets:
            for fieldset_name, fieldsets_data in self.fieldsets:
                if "fields" in fieldsets_data:
                    fieldset_fields |= set(fieldsets_data["fields"])

        if not (self.all_fields >= fieldset_fields):
            logger.warning(
                "Following fieldset fields are invalid %s"
                % (fieldset_fields - self.all_fields)
            )
            self.fieldsets = {}

        if not (set(self.fields) >= fieldset_fields):
            logger.warning(
                "Following fieldset fields are excluded %s"
                % (fieldset_fields - set(self.fields))
            )
            self.fieldsets = {}

    def as_dict(self):
        """
        Returns a form as a dictionary that looks like the following:

        form = {
            "title": "Abisuak, kexak eta iradokizunak",
            "description": {
                "data": "Eibarko Udalaren app edo webgunetik, 010 telefonora deituta edo Pegorara etorrita (Herritarren Zerbitzurako bulegoa), udalariaren elkarlanean aritzeko aukera eskaintzen dizugu nahi dituzun edo bidezko irizten zaizkizun iradokizunak, kexak edo abisuak emanda. Benetan eskertuko dizugu zure laguntza."
            },
            "properties": {
                "personaNombre": {
                    "description": "",
                    "title": "Izena",
                    "type": "string"
                },
                    "personaApellido1": {
                    "description": "",
                    "title": "Abizenak",
                    "type": "string"
                },
                ...
            },
            "required": [
                "erantzuteko-modua",
                "asunto",
                "extracto",
                "baldintzak-onartzen-ditut"
            ],
            "fieldsets": [
                {
                "fields": [
                    "personaNombre",
                    "personaApellido1",
                    "dni",
                    "erantzuteko-modua",
                    "telefonoa",
                    "helbidea",
                    "email",
                    "asunto",
                    "extracto",
                    "baldintzak-onartzen-ditut"
                ]
                }
            ]
            }
        """
        # Create result base structure
        form_dict = OrderedDict()

        try:
            form_dict["title"] = self.form.title
        except:
            form_dict["title"] = ""
        try:
            form_dict["description"] = self.form.description
        except:
            form_dict["description"] = ""
        form_dict["properties"] = OrderedDict()
        form_dict["required"] = []
        form_dict["fieldsets"] = self.fields

        # Get required fields
        for field in self.form.fields:
            if self.form.fields[field].required and field != "response":
                form_dict["required"].append(field)

        # Get properties' values
        initial_data = {}
        for name, field in [(x, self.form.fields[x]) for x in self.fields]:
            # Retrieve the initial data from the form itself if it exists so
            # that we properly handle which initial data should be returned in
            # the dictionary.

            # Please refer to the Django Form API documentation for details on
            # why this is necessary:
            # https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
            form_initial_field_data = self.form.initial.get(name)

            # Instantiate the Remote Forms equivalent of the field if possible
            # in order to retrieve the field contents as a dictionary.
            remote_field_class_name = "Remote%s" % field.__class__.__name__
            try:
                remote_field_class = getattr(fields, remote_field_class_name)
                remote_field = remote_field_class(
                    field, form_initial_field_data, field_name=name
                )
            except Exception(e):
                logger.warning(
                    "Error serializing field %s: %s", remote_field_class_name, str(e)
                )
                field_dict = {}
            else:
                field_dict = remote_field.as_dict()

            if name in self.readonly_fields:
                field_dict["readonly"] = True

            if name != "question" and name != "response":
                form_dict["properties"][name] = field_dict

        return resolve_promise(form_dict)

    def uiSchema_as_dict(self):
        uiSchema = {}

        for name in self.fields:
            field = self.form.fields[name]
            uiSchema[name] = {}

            # Configurar widgets basados en el tipo de campo
            field_type = type(field).__name__
            if hasattr(field, "widget"):
                widget_type = type(field.widget).__name__
            else:
                widget_type = None

            if field_type == "CharField" and widget_type:
                if widget_type == "Textarea":
                    uiSchema[name]["ui:widget"] = "tinymce"
                elif widget_type == "PasswordInput":
                    uiSchema[name]["ui:widget"] = "password"

            elif field_type == "BooleanField":
                uiSchema[name]["ui:widget"] = "checkbox"

            elif field_type == "ChoiceField":
                uiSchema[name]["ui:widget"] = "select"

            elif field_type == "FileField":
                uiSchema[name]["ui:options"] = {
                    "accept": getattr(field.widget, "attrs", {}).get("accept", "*")
                }

                uiSchema[name]["items"] = {"ui:widget": "file"}

            elif field_type == "ModelChoiceField":
                uiSchema[name]["ui:enumNames"] = [q.__str__() for q in field.queryset]

            if widget_type == "HiddenInput":
                uiSchema[name]["ui:widget"] = "hidden"

            if name in self.readonly_fields:
                uiSchema[name]["ui:disabled"] = True

            if name in self.excluded_fields:
                continue

        return resolve_promise(uiSchema)


class BaseJSONSChemaForm(forms.ModelForm):

    @classmethod
    def remotejson2form(cls, data):
        return cls(json.loads(data))

    def get_json_schema(self):
        remote_form = RemoteJSONSChemaForm(self)
        form_schema = remote_form.as_dict()
        return json.dumps(form_schema)

    def get_ui_schema(self):
        remote_form = RemoteJSONSChemaForm(self)
        ui_schema = remote_form.uiSchema_as_dict()
        return json.dumps(ui_schema)
