import datetime

from collections import OrderedDict

from django.conf import settings

from django_remote_jsonschema_forms import logger, widgets

from django.forms.models import ModelChoiceIteratorValue, ModelChoiceIterator


class RemoteField(object):
    """
    A base object for being able to return a Django Form Field as a Python
    dictionary.

    This object also takes into account if there is initial data for the field
    coming in from the form directly, which overrides any initial data
    specified on the field per Django's rules:

    https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    """

    def __init__(self, field, form_initial_data=None, field_name=None):
        self.field_name = field_name
        self.field = field
        self.form_initial_data = form_initial_data

    def as_dict(self):
        field_dict = OrderedDict()

        # if self.field.help_text != '':
        field_dict["description"] = self.field.help_text

        if self.form_initial_data:
            field_dict["default"] = self.form_initial_data

        if self.field.label != "":
            field_dict["title"] = self.field.label

        return field_dict


class RemoteCharField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteCharField, self).as_dict()

        update_fields = {"type": "string"}

        if self.field.max_length:
            update_fields["maxLength"] = self.field.max_length

        if self.field.min_length:
            update_fields["minLength"] = self.field.min_length

        try:
            if self.field.widget.attrs["cols"]:
                #                update_fields["maxLength"] = 750
                update_fields["widget"] = "textarea"
        except:
            pass

        field_dict.update(update_fields)

        return field_dict


class RemoteIntegerField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteIntegerField, self).as_dict()

        field_dict.update(
            {
                "type": "number",
                "max_value": self.field.max_value,
                "min_value": self.field.min_value,
            }
        )

        return field_dict


class RemoteFloatField(RemoteIntegerField):
    def as_dict(self):
        return super(RemoteFloatField, self).as_dict()


class RemoteDecimalField(RemoteIntegerField):
    def as_dict(self):
        field_dict = super(RemoteDecimalField, self).as_dict()

        field_dict.update(
            {
                "max_digits": self.field.max_digits,
                "decimal_places": self.field.decimal_places,
            }
        )

        return field_dict


class RemoteTimeField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteTimeField, self).as_dict()

        try:
            if self.field.__class__.__name__ == "DateField":
                field_dict.update(
                    {"title": self.field.label, "type": "string", "format": "date"}
                )
            elif self.field.__class__.__name__ == "TimeField":
                field_dict.update(
                    {"title": self.field.label, "type": "string", "format": "time"}
                )
            else:
                field_dict.update(
                    {"title": self.field.label, "type": "string", "format": "date-time"}
                )
            if self.field.__class__.__name__ == "DateField":
                input_format = settings.DATE_INPUT_FORMATS[0]
            elif self.field.__class__.__name__ == "TimeField":
                input_format = settings.TIME_INPUT_FORMATS[0]
            else:
                input_format = settings.DATETIME_INPUT_FORMATS[0]

            if "initial" in field_dict:
                field_dict["initial"] = field_dict["initial"].strftime(input_format)
        except Exception as e:
            pass

        return field_dict


class RemoteDateField(RemoteTimeField):
    def as_dict(self):
        return super(RemoteDateField, self).as_dict()


class RemoteDateTimeField(RemoteTimeField):
    def as_dict(self):
        return super(RemoteDateTimeField, self).as_dict()


class RemoteRegexField(RemoteCharField):
    def as_dict(self):
        field_dict = super(RemoteRegexField, self).as_dict()

        # We don't need the pattern object in the frontend
        # field_dict['regex'] = self.field.regex

        return field_dict


class RemoteEmailField(RemoteCharField):
    def as_dict(self):
        return super(RemoteEmailField, self).as_dict()


class RemoteFileField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteFileField, self).as_dict()

        if self.field.max_length:
            field_dict["max_length"] = self.field.max_length

        if "multiple" in self.field.widget.attrs:
            field_dict.update(
                {
                    "type": "array",
                    "items": {
                        "description": "",
                        "title": "",
                        "type": "string",
                        "widget": "file",
                    },
                }
            )
        else:
            field_dict.update(
                {"type": "string", "format": "data-url"},
            )

        return field_dict


class RemoteImageField(RemoteFileField):
    def as_dict(self):
        return super(RemoteImageField, self).as_dict()


class RemoteURLField(RemoteCharField):
    def as_dict(self):
        return super(RemoteURLField, self).as_dict()


class RemoteBooleanField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteBooleanField, self).as_dict()

        update_fields = {"type": "boolean"}

        field_dict.update(update_fields)

        return field_dict


class RemoteNullBooleanField(RemoteBooleanField):
    def as_dict(self):
        return super(RemoteNullBooleanField, self).as_dict()


class RemoteChoiceField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteChoiceField, self).as_dict()

        field_dict["oneOf"] = []
        for key, value in self.field.choices:
            if isinstance(key, ModelChoiceIteratorValue):
                key = key.value
            field_dict["oneOf"].append({"const": key, "title": value})

        return field_dict


class RemoteModelChoiceField(RemoteChoiceField):
    def as_dict(self):
        field_dict = super(RemoteModelChoiceField, self).as_dict()

        serialized_choices = []
        for choice in field_dict.get("oneOf", []):
            if choice["const"] == "":
                continue
            serialized_choices.append(choice["const"])

        field_dict.pop("oneOf", None)
        field_dict["enum"] = serialized_choices

        return field_dict


class RemoteTypedChoiceField(RemoteChoiceField):
    def as_dict(self):
        field_dict = super(RemoteTypedChoiceField, self).as_dict()

        field_dict.update(
            {"coerce": self.field.coerce, "empty_value": self.field.empty_value}
        )

        return field_dict


class RemoteMultipleChoiceField(RemoteChoiceField):
    def as_dict(self):
        return super(RemoteMultipleChoiceField, self).as_dict()


class RemoteModelMultipleChoiceField(RemoteMultipleChoiceField):
    def as_dict(self):
        field_dict = super(RemoteModelMultipleChoiceField, self).as_dict()
        serialized_choices = []
        for choice in field_dict.get("choices", []):
            if isinstance(choice["value"], ModelChoiceIteratorValue):
                serialized_choices.append(choice["display"])

        field_dict.pop("choices", None)
        field_dict["enum"] = serialized_choices

        return field_dict


class RemoteTypedMultipleChoiceField(RemoteMultipleChoiceField):
    def as_dict(self):
        field_dict = super(RemoteTypedMultipleChoiceField, self).as_dict()

        field_dict.update(
            {"coerce": self.field.coerce, "empty_value": self.field.empty_value}
        )

        return field_dict


class RemoteComboField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteComboField, self).as_dict()

        field_dict.update(fields=self.field.fields)

        return field_dict


class RemoteMultiValueField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteMultiValueField, self).as_dict()

        field_dict["fields"] = self.field.fields

        return field_dict


class RemoteFilePathField(RemoteChoiceField):
    def as_dict(self):
        field_dict = super(RemoteFilePathField, self).as_dict()

        field_dict.update(
            {
                "path": self.field.path,
                "match": self.field.match,
                "recursive": self.field.recursive,
            }
        )

        return field_dict


class RemoteSplitDateTimeField(RemoteMultiValueField):
    def as_dict(self):
        field_dict = super(RemoteSplitDateTimeField, self).as_dict()

        field_dict.update(
            {
                "input_date_formats": self.field.input_date_formats,
                "input_time_formats": self.field.input_time_formats,
            }
        )

        return field_dict


class RemoteIPAddressField(RemoteCharField):
    def as_dict(self):
        return super(RemoteIPAddressField, self).as_dict()


class RemoteSlugField(RemoteCharField):
    def as_dict(self):
        return super(RemoteSlugField, self).as_dict()
