import logging
import sys

import structlog


class Logger:
    instances = []

    def __init__(self, name: str = __file__):
        self.LOG = structlog.get_logger(name)
        self.name = name

        Logger.instances.append(self)

    def get_logger(self):
        return self.LOG


def setup_structlog():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            request_id_processor,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        wrapper_class=structlog.stdlib.BoundLogger,
    )


def request_id_processor(_, __, event_dict):
    event_dict["request_id"] = structlog.contextvars.get_contextvars().get("request_id")
    return event_dict


setup_structlog()
