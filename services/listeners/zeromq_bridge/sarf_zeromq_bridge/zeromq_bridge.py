#!/usr/bin/env python3

import sys
import logging
import json
import threading

import zmq
from awesome_messages.domain.listener import MessageListener
from awesome_messages.domain.handler import MessageHandler
import dependency_injector
from dependency_injector.wiring import Provide, inject


from sarf_listener.containers import Application
from sarf_listener.bootstrap import setup_logging


logger = logging.getLogger("sarf_listener")


class ZeroMQTopicServer:

    def __init__(self, port):
        self.__address = f"tcp://*:{port}"
        self.__context = zmq.Context()
        self.__socket = None

    def connect(self):
        logger.debug(f"Zeromq server starting to listen on {self.__address}")
        self.__socket = self.__context.socket(zmq.PUB)
        self.__socket.bind(self.__address)
        logger.debug(f'ZeroMQ server connected on {self.__address}')

    def disconnect(self):
        logger.debug(f"Terminating zeromq pub server {self.__address}")
        self.__socket.close()
        logger.debug(f"Terminated zeromq server {self.__address} ")

    def send_json(self, topic: str, json_obj: dict):
        self.__socket.send_string(f"{topic} {json.dumps(json_obj)}")


class ZeroMQBridge(MessageHandler):

    def __init__(self, topic: str, zeromq: ZeroMQTopicServer):
        self.__zeromq = zeromq
        self.__topic = topic

    def on_msg(self, message: dict):
        logger.debug(f"Handling message with ZeroMQBridge")
        self.__zeromq.send_json(self.__topic, message)
        logger.debug(f"Message sent to zeromq {self.__topic} topic")


@inject
def start(config: dict=Provide[Application.config],
        tools_listener: MessageListener=Provide[
            Application.listener.messages_tools_subscriber],
        reports_listener: MessageListener=Provide[
            Application.listener.messages_reports_subscriber],
        ):

    setup_logging("sarf_listener", config['listeners']['logfile'], config['listeners']['loglevel'])

    zeroMQ_topic_server = ZeroMQTopicServer(config['listeners']['zeromq_bridge']['port'])
    zeroMQ_topic_server.connect()

    tools_handler = ZeroMQBridge("tools", zeroMQ_topic_server)
    reports_handler =  ZeroMQBridge("reports", zeroMQ_topic_server)

    # Currently listeners are hardcoded because I can't find the way to work with them
    # dinamically with the python-dependency-injector...
    # This should be changed in the future. Help needed here! 🙏
    tools_listener.add_handler(tools_handler)
    reports_listener.add_handler(reports_handler)

    def handle_zeromq_listener_thread(listener):
        try:
            logger.debug("Start listening")
            listener.start_listening()
        except KeyboardInterrupt:
            logger.error("Keyboard interruption")
        except Exception as e:
            logger.error(e)

    try:
        tools_thread = threading.Thread(target=lambda: handle_zeromq_listener_thread(tools_listener))
        reports_thread = threading.Thread(target=lambda: handle_zeromq_listener_thread(reports_listener))
        tools_thread.daemon = True
        reports_thread.daemon = True
        reports_thread.start()
        logger.debug('Start tools listener')
        tools_thread.start()
        logger.debug('Start reports listener')

        tools_thread.join()
        reports_thread.join()

    except KeyboardInterrupt:
        try:
            tools_listener.stop_listening()
            reports_listener.stop_listening()
        except Exception as e:
            logger.warning(f"Exception raised while closing connections {e}")
    except dependency_injector.errors.Error:
        print(
            "Error during dependency injection. Check configuration file")
        print("Configuration file should exist in /etc/sarf/config.yml")
        sys.exit(2)
    finally:
        zeroMQ_topic_server.disconnect()


INTRO = r"""
 _____              __  __  ___    ____       _     _            
|__  /___ _ __ ___ |  \/  |/ _ \  | __ ) _ __(_) __| | __ _  ___ 
  / // _ \ '__/ _ \| |\/| | | | | |  _ \| '__| |/ _` |/ _` |/ _ \
 / /|  __/ | | (_) | |  | | |_| | | |_) | |  | | (_| | (_| |  __/
/____\___|_|  \___/|_|  |_|\__\_\ |____/|_|  |_|\__,_|\__, |\___|
                                                      |___/   
      A SARF utility made with <3 by @elchicodepython
"""

def wire():
    container = Application()
    container.wire(modules=[__name__])


def main():
    print(INTRO)
    wire()
    start()


if __name__ == '__main__':
    main()
