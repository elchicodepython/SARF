import tempfile, os
from subprocess import call

from .base import Input, Output


class ConsoleOutput(Output):
    def __init__(self, endchar=""):
        self.__endchar = endchar

    def write(self, content: bytes):
        print(content.encode(), end=self.__endchar)

    def writeText(self, content: str):
        print(content, end=self.__endchar)


class ConsoleInput(Input):
    def __init__(self, message: str=">> "):
        self.__mesage = message

    def retrieve(self) -> str:
        data = input(self.__mesage)
        return data


class EditorInput(Input):

    def __init__(self, initial_msg="", tmp_suffix=".tmp", editor=None):
        self.__initial = initial_msg.encode()
        self.__tmp_suffix = tmp_suffix
        self.__editor = editor or os.environ.get("EDITOR", "vim")

    def retrieve(self) -> str:
        with tempfile.NamedTemporaryFile(suffix=self.__tmp_suffix) as tf:
            tf.write(self.__initial)
            tf.flush()
            call([self.__editor, tf.name])
            tf.seek(0)
            edited_message = tf.read()
        return edited_message.decode()
