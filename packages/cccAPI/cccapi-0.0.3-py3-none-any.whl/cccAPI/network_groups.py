# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPINetworkGroups:
    def __init__(self, connection):
        """Handles CCC Network Groups Deployment API endpoints."""
        self.connection = connection