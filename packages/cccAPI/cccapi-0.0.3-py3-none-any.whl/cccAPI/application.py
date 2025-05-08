import os
import json
from jsonschema import validate, RefResolver
from jsonschema.exceptions import ValidationError

# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPIApplication:
    def __init__(self, connection):
        """Handles CCC Application API endpoints."""
        self.connection = connection

    def list_application_entry_points(self):
        """
        List application entry points.

        :return: API response containing application entry points.
        :raises ValueError: If the response does not conform to the ApplicationDescriptionDTO.json schema.
        """
        # Send the GET request to the root endpoint
        response = self.connection.get("")

        # Load the ApplicationDescriptionDTO.json schema
        definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))
        schema_path = os.path.join(definitions_dir, "ApplicationDescriptionDTO.json")
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        # Create a resolver for external references
        base_uri = f"file://{definitions_dir}/"
        resolver = RefResolver(base_uri=base_uri, referrer=schema)

        # Validate the response against the schema
        try:
            validate(instance=response, schema=schema, resolver=resolver)
            logger.debug("Validation successful")
        except ValidationError as e:
            raise ValueError(f"Response validation failed: {e.message}")

        return response

    def list_application_settings(self):
        """
        List application current settings.

        :return: API response containing application settings.
        """
        # Send the GET request to the /settings endpoint
        response = self.connection.get("settings")

        # Return the response as-is
        return response