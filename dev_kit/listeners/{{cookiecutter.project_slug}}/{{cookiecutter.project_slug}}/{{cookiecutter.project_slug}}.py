#!/usr/bin/env python3

import sys
import logging

from awesome_messages.domain.listener import MessageListener
from awesome_messages.domain.handler import MessageHandler
import dependency_injector
from dependency_injector.wiring import Provide, inject

from sarf_listener.containers import Application
from sarf_listener.bootstrap import setup_logging


logger = logging.getLogger("sarf_listener")


class {{cookiecutter.handler_class_name}}(MessageHandler):


    def on_msg(self, message: dict):
        logger.debug("Handling message")
        # Do your stuff here
        # ...


@inject
def start(config: dict=Provide[Application.config],
        msg_listener: MessageListener=Provide[
            Application.listener.messages_tools_subscriber]
        ):

    setup_logging("sarf_listener", config['listeners']['logfile'], config['listeners']['loglevel'])

    postgres_handler = {{cookiecutter.handler_class_name}}(**config['listeners']['{{cookiecutter.project_slug}}'])
    msg_listener.add_handler(postgres_handler)

    logger.info("Listening messages")
    try:
        msg_listener.start_listening()
    except KeyboardInterrupt:
        logger.error("Keyboard interruption")
        msg_listener.stop_listening()
    except dependency_injector.errors.Error:
        print(
            "Error during dependency injection. Check configuration file")
        print("Configuration file should exist in /etc/sarf/config.yml")
        sys.exit(2)


def wire():
    container = Application()
    container.wire(modules=[__name__])


def main():
    wire()
    start()


if __name__ == '__main__':
    main()
