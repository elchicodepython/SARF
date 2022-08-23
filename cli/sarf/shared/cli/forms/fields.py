from PyInquirer import prompt


class InputField:
    def __init__(self, style=None):
        self.__style = style

    def parse_data(self, name, conf=None):
        conf = conf or {}
        inquirer_field_structure = {
            'type': 'input',
            'name': name,
            'message': name,
            'default': conf.get('default', '')
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]


class TextField:
    def __init__(self, style=None, editor='vim'):
        self.__editor = editor
        self.__style = style

    def parse_data(self, name, conf=None):
        print(f'Press enter to write "{name}" in a text editor')
        input()
        conf = conf or {}
        inquirer_field_structure = {
            'type': 'editor',
            'name': name,
            'eargs': {
                'editor': self.__editor
            },
            'message': name,
            'default': conf.get('default', '')
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]


class SelectField:
    def __init__(self, style=None):
        self.__style = style

    def parse_data(self, name, conf=None):
        conf = conf or {}
        inquirer_field_structure = {
            'type': 'list',
            'name': name,
            'message': name,
            'choices': conf.get('choices', []),
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]
