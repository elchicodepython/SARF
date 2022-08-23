from .fields import InputField, TextField, SelectField
from ...forms.form import Form, FieldsRegistry


cli_fields = FieldsRegistry()
cli_input_field = InputField()
cli_text_field = TextField()
cli_select_field = SelectField()

cli_fields.add(cli_input_field, "input")
cli_fields.add(cli_text_field, "text")
cli_fields.add(cli_select_field, "select")

cli_form = Form(cli_fields)
