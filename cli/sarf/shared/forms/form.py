class FieldsRegistry:
    def __init__(self):
        self.__fields = {}

    def add(self, field, field_type):
        self.__fields[field_type] = field

    def get(self, field_type):
        return self.__fields[field_type]


class Form:
    def __init__(self, fields_registry: FieldsRegistry):
        self.__fields_registry = fields_registry

    def process_form(self, form_fields):
        data = {}
        for field_key in form_fields:
            field = form_fields[field_key]
            value = self.__fields_registry.get(field["type"]).parse_data(field["name"], field.get('conf'))
            data[field_key] = value
        return data
