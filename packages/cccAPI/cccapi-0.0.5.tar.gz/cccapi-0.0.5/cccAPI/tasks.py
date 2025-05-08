# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPITasks:
    def __init__(self, connection):
        """Handles CCC Tasks API endpoints."""
        self.connection = connection
