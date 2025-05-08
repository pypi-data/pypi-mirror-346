from collections import OrderedDict


class RemoteWidget(object):
    def __init__(self, widget, field_name=None):
        self.field_name = field_name
        self.widget = widget

    def as_dict(self):
        widget_dict = OrderedDict()
        widget_dict["type"] = self.widget.__class__.__name__
        widget_dict["is_hidden"] = self.widget.is_hidden
        widget_dict["needs_multipart_form"] = self.widget.needs_multipart_form
        widget_dict["is_localized"] = self.widget.is_localized
        widget_dict["is_required"] = self.widget.is_required
        widget_dict["attrs"] = self.widget.attrs

        return widget_dict


class RemoteInput(RemoteWidget):
    def as_dict(self):
        widget_dict = super(RemoteInput, self).as_dict()
        widget_dict["input_type"] = self.widget.input_type
        return widget_dict


class RemoteTextInput(RemoteInput):
    def as_dict(self):
        return super(RemoteTextInput, self).as_dict()


class RemotePasswordInput(RemoteInput):
    def as_dict(self):
        return super(RemotePasswordInput, self).as_dict()


class RemoteHiddenInput(RemoteInput):
    def as_dict(self):
        return super(RemoteHiddenInput, self).as_dict()


class RemoteEmailInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteEmailInput, self).as_dict()
        widget_dict["type"] = "TextInput"
        widget_dict["input_type"] = "text"
        return widget_dict


class RemoteNumberInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteNumberInput, self).as_dict()
        widget_dict["type"] = "TextInput"
        widget_dict["input_type"] = "text"
        return widget_dict


class RemoteURLInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteURLInput, self).as_dict()
        widget_dict["type"] = "TextInput"
        widget_dict["input_type"] = "text"
        return widget_dict


class RemoteMultipleHiddenInput(RemoteHiddenInput):
    def as_dict(self):
        widget_dict = super(RemoteMultipleHiddenInput, self).as_dict()
        widget_dict["choices"] = self.widget.choices
        return widget_dict


class RemoteFileInput(RemoteInput):
    def as_dict(self):
        return super(RemoteFileInput, self).as_dict()


class RemoteClearableFileInput(RemoteFileInput):
    def as_dict(self):
        widget_dict = super(RemoteClearableFileInput, self).as_dict()
        widget_dict["initial_text"] = self.widget.initial_text
        widget_dict["input_text"] = self.widget.input_text
        widget_dict["clear_checkbox_label"] = self.widget.clear_checkbox_label
        return widget_dict


class RemoteTextarea(RemoteWidget):
    def as_dict(self):
        widget_dict = super(RemoteTextarea, self).as_dict()
        widget_dict["input_type"] = "textarea"
        return widget_dict


class RemoteTimeInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteTimeInput, self).as_dict()
        widget_dict["input_type"] = "time"
        widget_dict["format"] = self.widget.format
        return widget_dict


class RemoteDateInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteDateInput, self).as_dict()
        widget_dict["input_type"] = "date"
        widget_dict["format"] = self.widget.format
        return widget_dict


class RemoteDateTimeInput(RemoteInput):
    def as_dict(self):
        widget_dict = super(RemoteDateTimeInput, self).as_dict()
        widget_dict["input_type"] = "datetime"
        widget_dict["format"] = self.widget.format
        return widget_dict


class RemoteCheckboxInput(RemoteWidget):
    def as_dict(self):
        return super(RemoteCheckboxInput, self).as_dict()


class RemoteChoiceWidget(RemoteWidget):
    def as_dict(self):
        widget_dict = super(RemoteChoiceWidget, self).as_dict()
        widget_dict["choices"] = [
            {"value": key, "display": value} for key, value in self.widget.choices
        ]
        return widget_dict


class RemoteSelect(RemoteChoiceWidget):
    def as_dict(self):
        return super(RemoteSelect, self).as_dict()


class RemoteNullBooleanSelect(RemoteSelect):
    def as_dict(self):
        return super(RemoteNullBooleanSelect, self).as_dict()


class RemoteSelectMultiple(RemoteSelect):
    def as_dict(self):
        return super(RemoteSelectMultiple, self).as_dict()


class RemoteRadioSelect(RemoteChoiceWidget):
    def as_dict(self):
        return super(RemoteRadioSelect, self).as_dict()


class RemoteCheckboxSelectMultiple(RemoteSelectMultiple):
    def as_dict(self):
        return super(RemoteCheckboxSelectMultiple, self).as_dict()


class RemoteMultiWidget(RemoteWidget):
    def as_dict(self):
        widget_dict = super(RemoteMultiWidget, self).as_dict()
        widget_dict["decompress"] = self.widget.decompress
        widget_dict["widgets"] = [
            RemoteWidget(widget).as_dict() for widget in self.widget.widgets
        ]
        return widget_dict


class RemoteSplitDateTimeWidget(RemoteMultiWidget):
    def as_dict(self):
        return super(RemoteSplitDateTimeWidget, self).as_dict()
