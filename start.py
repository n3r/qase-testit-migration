from src import TestItImporter
from src.support.config_manager import ConfigManager
from src.support.logger import Logger

config = ConfigManager()
try:
    config.load_config()
except Exception as e:
    config.build_config()

prefix = config.get('prefix')
if prefix == None:
    prefix = ''

logger = Logger(config.get('debug'), prefix=prefix)

importer = TestItImporter(config, logger)
importer.start()
