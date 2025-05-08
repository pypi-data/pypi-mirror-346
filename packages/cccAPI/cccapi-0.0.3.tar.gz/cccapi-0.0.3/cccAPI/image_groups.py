# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPIImageGroups:
    def __init__(self, connection):
        """Handles CCC Image Group API endpoints."""
        self.connection = connection