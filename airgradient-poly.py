import udi_interface
from nodes import AirGradientController
import sys

LOGGER = udi_interface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([AirGradientController])
        polyglot.start()

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        polyglot.stop()
        sys.exit(0)
    except Exception as err:
        LOGGER.error('Exception: {0}'.format(err), exc_info = True)
        sys.exit(0)