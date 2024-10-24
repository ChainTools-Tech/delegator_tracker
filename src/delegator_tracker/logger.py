import logging

def setup_logger(level):
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)-8s] %(name)s: (%(module)s, %(funcName)s): %(message)s',
        level=getattr(logging, level.upper())
    )
