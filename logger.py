import logging
import logging.config

import yaml

# load the logger
with open("log-config.yaml", "r") as f:
    logging.config.dictConfig(yaml.load(f, yaml.SafeLoader))
basic_logger = logging.getLogger("basic")
basic_logger.setLevel(logging.DEBUG)
