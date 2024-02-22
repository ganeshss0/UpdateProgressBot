import logging

#####################
### LOGGING FILE ####
#####################

logging.basicConfig(
        format='[%(asctime)s] | %(levelname)s | %(lineno)d | %(message)s',
        level=logging.INFO
    )