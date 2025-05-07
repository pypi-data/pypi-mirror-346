def main():
    import datetime
    import logging as stdlib_logging

    from loguru import logger as loguru_logger

    from . import logging_setup
    from .tools import install_rich_traceback

    install_rich_traceback()
    logging_setup.setup_logging(log_format='auto', level='trace')

    loguru_logger.trace("Logging messagem from loguru")
    loguru_logger.debug("Logging messagem from loguru")
    loguru_logger.info("Logging messagem from loguru", abc=123, foo=datetime.datetime.now(), bar=[1, 2, 3, 4, 5])
    loguru_logger.warning("Logging messagem from loguru")
    loguru_logger.error("Logging messagem from loguru")
    stdlib_logging.critical("This one is from stdlib", extra=dict(extra_std=1))

    try:
        raise Exception("oh yes exception!")
    except Exception as e:
        loguru_logger.exception("in except loguru")
        stdlib_logging.exception("in except stdlib")
        raise
