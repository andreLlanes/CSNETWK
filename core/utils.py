import logging

def setup_logging(verbose=False):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
        logging.debug("Verbose mode enabled.")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info("Verbose mode not enabled.")

def log_message(message):
    logging.info(message)

def log_debug_message(message):
    logging.debug(message)
