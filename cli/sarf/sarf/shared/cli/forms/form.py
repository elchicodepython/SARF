from .fields import (
    BooleanField,
    InputField,
    TextField,
    SelectField,
    ForeignSelectField,
)
from ...forms.form import FieldsRegistry


cli_fields = FieldsRegistry()
cli_input_field = InputField()
cli_text_field = TextField()
cli_select_field = SelectField()
cli_boolean_field = BooleanField()
cli_foreign_select: ForeignSelectField = ForeignSelectField()

cli_fields.add(cli_input_field, "input")
cli_fields.add(cli_boolean_field, "boolean")
cli_fields.add(cli_text_field, "text")
cli_fields.add(cli_select_field, "select")
cli_fields.add(cli_foreign_select, "foreign_search")
