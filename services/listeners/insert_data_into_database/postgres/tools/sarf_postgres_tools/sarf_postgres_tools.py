#!/usr/bin/env python3

import sys
import logging
from collections import OrderedDict

import psycopg2
from awesome_messages.domain.listener import MessageListener
from awesome_messages.domain.handler import MessageHandler
import dependency_injector
from dependency_injector.wiring import Provide, inject

from sarf_listener.containers import Application
from sarf_listener.bootstrap import setup_logging


logger = logging.getLogger("sarf_listener")


"""This listener retrieve data from SARF tools messages and store it in
a Postgresql database. The postgresql database should have a table
to store this data.

The table can be created using the following code:

CREATE TABLE tools (
	pk serial PRIMARY KEY,
	tags VARCHAR ( 200 ) NOT NULL,
	storage_type VARCHAR ( 50 ) NOT NULL,
	path VARCHAR ( 255 ) NOT NULL,
    emitter VARCHAR ( 255 ) NOT NULL,
	report_id INTEGER NOT NULL
);

"""

class PostgreSQLHandler(MessageHandler):
    def __init__(self, host: str, port: int, user: str, password: str, database: str, table: str, datamap: dict):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.__table = table
        self.__datamap = datamap

    def on_msg(self, message: dict):
        logger.debug("Handling message")

        connection = psycopg2.connect(
            host=self.__host,
            database=self.__database,
            user=self.__user,
            password=self.__password,
            port=self.__port
        )
        logger.debug("Connection stablished to postgres")
        cursor = connection.cursor()

        columns_data = OrderedDict()

        for key in self.__datamap:
            columns_data[self.__datamap[key]] = message[key]

        # Quick example
        columns_data[self.__datamap['tags']] = ','.join(
            columns_data[self.__datamap['tags']]
        )

        columns = ','.join(columns_data.keys())
        values = tuple(columns_data.values())
        safe_values = ','.join(['%s']*(len(values)))
        query = f"INSERT INTO {self.__table} ({columns}) VALUES ({safe_values})"

        logger.debug(f"Executing query {query}")
        cursor.execute(
            query,
            (values)
        )
        logger.debug(f'Postgresql row inserted in {self.__database} with the following data {values}')
        connection.commit()
        logger.debug("Postgresql commit made")

        cursor.close()
        connection.close()


@inject
def start(config: dict=Provide[Application.config],
        msg_listener: MessageListener=Provide[
            Application.listener.messages_tools_subscriber]
        ):

    setup_logging("sarf_listener", config['listeners']['logfile'], config['listeners']['loglevel'])

    postgres_handler = PostgreSQLHandler(**config['listeners']['postgres_tools'])
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
