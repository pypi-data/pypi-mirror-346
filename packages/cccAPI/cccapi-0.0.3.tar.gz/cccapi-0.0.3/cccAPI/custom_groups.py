# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPICustomGroups:
    def __init__(self, connection):
        """Handles CCC Custom Groups API endpoints."""
        self.connection = connection