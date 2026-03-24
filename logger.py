import logging
import sys


def get_logger(name):

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        # 🔥 IMPORTANTE: evita logs duplicados
        logger.propagate = False

    return logger


def setup_root_logger():
    """
    Configure root logger so ALL logs go to stdout (ECS / CloudWatch)
    """

    root = logging.getLogger()

    if not root.handlers:

        root.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        root.addHandler(handler)
