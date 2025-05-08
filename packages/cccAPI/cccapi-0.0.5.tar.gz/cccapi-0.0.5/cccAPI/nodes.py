# Configure logging
import logging
logger = logging.getLogger("cccAPI")

class cccAPINodes:
    def __init__(self, connection):
        """Handles CCC Nodes API endpoints."""
        self.connection = connection
        self.allowed_fields = {"name", "id", "uuid", "etag", "links", "network", 
                               "image", "creationTime", "modificationTime", "deletionTime",
                               "links", "links.actions", "links.imagegroup", "links.networkgroup",
                               "network", "network.name", "network.ipAddress", "network.subnetMask", 
                               "network.macAddress", "network.mgmtServerIp", "network.defaultGateway",
                               "image", "image.name", "image.cloningBlockDevice", "image.cloningDate",
                               "platform", "platform.name", "platform.architecture", "platform.serialPort",
                               "platform.serialPortSpeed", "platform.vendorsArgs",
                               "management", "management.cardType", "management.cardIpAddress",
                               "primaryId", "secondaryId", "biosBootMode", "iscsiRoot", 
                               "features",  
                               "features.BIOS", "features.CPU model", "features.Cluster dns domain name",
                               "features.Disk size", "features.Disk type", "features.Logical CPU number",
                               "features.Memory size", "features.Native CPU speed", "features.System model",
                               }  # Define allowed fields
        self.default_fields = "name,id,network.name,network.ipAddress,management.cardType,management.cardIpAddress"  # Default fields if none are specified

    def show_nodes(self, params=None):
        """
        Retrieve currently registered nodes with optional query parameters.

        :param params: Dictionary of query parameters to include in the request.
                       Example: {"fields": "name,id,uuid,etag"}
        :return: API response containing currently registered nodes.
        """
        if params is None:
            params = {}

        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            invalid_fields = requested_fields - self.allowed_fields
            if invalid_fields:
                raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}. Allowed fields are: {', '.join(self.allowed_fields)}")
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = None

        return self.connection.get("nodes", params=params)

    def show_node(self, name, params=None):
        """
        Retrieve details about specific node "name" with optional query parameters.

        :param name: The name of the node to retrieve.
        :param params: Dictionary of query parameters to include in the request.
                       Example: {"fields": "name,id,uuid,etag"}
        :return: API response for the node "name".
        """
        if params is None:
            params = {}

        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            invalid_fields = requested_fields - self.allowed_fields
            if invalid_fields:
                raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}. Allowed fields are: {', '.join(self.allowed_fields)}")
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = None

        return self.connection.get(f"nodes/{name}", params=params)

    def create_nodes(self, nodes):
        """
        Create one or multiple nodes.

        :param nodes: A list of node objects conforming to the Node.json schema.
                      Example:
                      [
                          {
                              "name": "Node1",
                              "network": {...},
                              "image": {...},
                              ...
                          },
                          {
                              "name": "Node2",
                              "network": {...},
                              "image": {...},
                              ...
                          }
                      ]
        :return: API response from the POST /nodes endpoint.
        """


        if not isinstance(nodes, list):
            raise ValueError("The 'nodes' parameter must be a list of node objects.")
        
         # Restricted fields in the 'image' object
        restricted_image_fields = {"name", "cloningBlockDevice", "cloningDate"}

        # Validate each node
        for node in nodes:
            # Check for restricted fields in the 'image' object
            if "image" in node:
                restricted_fields_in_image = restricted_image_fields.intersection(node["image"].keys())
                if restricted_fields_in_image:
                    raise ValueError(
                        f"The following fields are not allowed in the 'image' object: {', '.join(restricted_fields_in_image)}"
                    )

        # Check for readonly field 'network.name'
        if "network" in node and "name" in node["network"]:
            raise ValueError("The 'network.name' field is readonly and cannot be set.")

        # Validate each node against the schema (optional, if needed)
        from jsonschema import RefResolver, validate
        from jsonschema.exceptions import ValidationError
        import json 
        import os

        # Get the absolute path to the definitions directory
        definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))

        # Base URI for resolving references
        base_uri = f"file://{definitions_dir}/"

        # Load the Node.json schema
        node_schema_path = os.path.join(definitions_dir, "Node.json")
        with open(node_schema_path) as schema_file:
            node_schema = json.load(schema_file)

        # Create a resolver for external references
        resolver = RefResolver(base_uri=base_uri, referrer=node_schema)

        for node in nodes:
            try:
                validate(instance=node, schema=node_schema, resolver=resolver)
            except ValidationError as e:
                raise ValueError(f"Node validation failed: {e.message}")
    
        # for node in nodes:
        #     if not isinstance(node, dict):
        #         raise ValueError("Each node must be a dictionary conforming to the Node.json schema.")

        VALID_BIOS_BOOT_MODES = {"UEFI", "PXE", "AUTO"}
        for node in nodes:
            if "biosBootMode" in node and node["biosBootMode"] not in VALID_BIOS_BOOT_MODES:
                raise ValueError(f"Invalid biosBootMode value: {node['biosBootMode']}. Allowed values are: {', '.join(VALID_BIOS_BOOT_MODES)}")

        # Send the POST request to the /nodes endpoint
        response = self.connection.post("nodes", data=nodes)

        return response

    def delete_node(self, identifier):
        """
        Delete an existing node.

        :param identifier: The identifier of the node to delete (String).
        :return: API response indicating the result of the deletion.
        """
        if not isinstance(identifier, str):
            raise ValueError("The 'identifier' parameter must be a string.")

        # Send the DELETE request to the /nodes/{identifier} endpoint
        response = self.connection.delete(f"nodes/{identifier}")

        return response
    

    def update_node(self, identifier, body):
        """
        Update an existing node.

        :param identifier: The identifier of the node to update (String).
        :param body: The updated node definition conforming to the Node.json schema.
        :return: API response indicating the result of the update.
        """
        if not isinstance(identifier, str):
            raise ValueError("The 'identifier' parameter must be a string.")
        
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary conforming to the Node.json schema.")

        # Validate the body against the Node.json schema
        from jsonschema import RefResolver, validate
        from jsonschema.exceptions import ValidationError
        import json
        import os

        # Get the absolute path to the definitions directory
        definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))

        # Base URI for resolving references
        base_uri = f"file://{definitions_dir}/"

        # Load the Node.json schema
        node_schema_path = os.path.join(definitions_dir, "Node.json")
        with open(node_schema_path) as schema_file:
            node_schema = json.load(schema_file)

        # Create a resolver for external references
        resolver = RefResolver(base_uri=base_uri, referrer=node_schema)

        try:
            validate(instance=body, schema=node_schema, resolver=resolver)
        except ValidationError as e:
            raise ValueError(f"Node validation failed: {e.message}")

        # Send the PUT request to the /nodes/{identifier} endpoint
        response = self.connection.put(f"nodes/{identifier}", data=body)

        return response
    

    def show_node_noimggroup(self, params=None):
        """
        Retrieve nodes that are not in any image group with optional query parameters.

        :param params: Dictionary of query parameters to include in the request.
                    Example: {"fields": "name,id,uuid,etag"}
        :return: API response containing nodes not in any image group.
        """
        if params is None:
            params = {}

        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            invalid_fields = requested_fields - self.allowed_fields
            if invalid_fields:
                raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}. Allowed fields are: {', '.join(self.allowed_fields)}")
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = self.default_fields

        # Send the GET request to the /nodes/no_image endpoint
        return self.connection.get("nodes/no_image", params=params)

    def remove_nodes_from_image_group(self, body):
        """
        Remove a set of nodes from their current image group.

        :param body: A dictionary conforming to the MultipleIdentifierDto.json schema.
        :return: API response. If the response status is 200, it returns a response conforming to Node.json schema.
        :raises ValueError: If the body does not conform to the MultipleIdentifierDto.json schema.
        """
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary conforming to the MultipleIdentifierDto.json schema.")

        # Validate the body against the MultipleIdentifierDto.json schema
        from jsonschema import RefResolver, validate
        from jsonschema.exceptions import ValidationError
        import json
        import os

        # Get the absolute path to the definitions directory
        definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))

        # Load the MultipleIdentifierDto.json schema
        multiple_identifier_schema_path = os.path.join(definitions_dir, "MultipleIdentifierDto.json")
        with open(multiple_identifier_schema_path) as schema_file:
            multiple_identifier_schema = json.load(schema_file)

        # Create a resolver for external references
        base_uri = f"file://{definitions_dir}/"
        resolver = RefResolver(base_uri=base_uri, referrer=multiple_identifier_schema)

        try:
            validate(instance=body, schema=multiple_identifier_schema, resolver=resolver)
            logger.debug("Validation of body with MultipleIdentifierDto schema successful")
        except ValidationError as e:
            raise ValueError(f"Request body validation failed: {e.message}")

        # Send the POST request to the /nodes/no_image endpoint
        response = self.connection.post("nodes/no_image", data=body)

        # If the response status is 200, validate it against the Node.json schema
        if response.status_code == 200:
            # Load the Node.json schema
            node_schema_path = os.path.join(definitions_dir, "Node.json")
            with open(node_schema_path) as schema_file:
                node_schema = json.load(schema_file)

            try:
                validate(instance=response.json(), schema=node_schema, resolver=resolver)
                logger.debug("Validation of response with Node schema successful")
            except ValidationError as e:
                raise ValueError(f"Response validation failed: {e.message}")

            return response.json()

        # Return the response as-is for other status codes
        return response
    
    #Section 4.5.11
    def show_node_noNetworkGroup(self, params=None):
        """
        Retrieve nodes that are not in any network group with optional query parameters.
    
        :param params: Dictionary of query parameters to include in the request.
                       Example: {"fields": "name,id,uuid,etag"}
        :return: API response containing nodes not in any network group.
        :raises ValueError: If the response does not conform to the Node.json schema.
        """
        if params is None:
            params = {}
    
        # Validate and process the 'fields' parameter
        if "fields" in params:
            requested_fields = set(params["fields"].split(","))
            invalid_fields = requested_fields - self.allowed_fields
            if invalid_fields:
                raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}. Allowed fields are: {', '.join(self.allowed_fields)}")
            # Use only the valid fields
            params["fields"] = ",".join(requested_fields)
        else:
            # Use default fields if 'fields' is not specified
            params["fields"] = self.default_fields
    
        # Send the GET request to the /nodes/no_network endpoint
        response = self.connection.get("nodes/no_network", params=params)
    
        # If the response status is 200, validate it against the Node.json schema
        if response.status_code == 200:
            from jsonschema import RefResolver, validate
            from jsonschema.exceptions import ValidationError
            import json
            import os
    
            # Get the absolute path to the definitions directory
            definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))
    
            # Load the Node.json schema
            node_schema_path = os.path.join(definitions_dir, "Node.json")
            with open(node_schema_path) as schema_file:
                node_schema = json.load(schema_file)
    
            # Create a resolver for external references
            base_uri = f"file://{definitions_dir}/"
            resolver = RefResolver(base_uri=base_uri, referrer=node_schema)
    
            try:
                validate(instance=response.json(), schema=node_schema, resolver=resolver)
                logger.debug("Validation of response with Node schema successful")
            except ValidationError as e:
                raise ValueError(f"Response validation failed: {e.message}")
    
            return response.json()
    
        # Return the response as-is for other status codes
        return response
    
    #section 4.5.12 
    def remove_nodes_noNetworkGroup(self, body):
        """
        Remove a set of nodes from their current network group.
    
        :param body: A dictionary conforming to the MultipleIdentifierDto.json schema.
        :return: API response. If the response status is 200, it returns a response conforming to Node.json schema.
        :raises ValueError: If the body does not conform to the MultipleIdentifierDto.json schema.
        """
        if not isinstance(body, dict):
            raise ValueError("The 'body' parameter must be a dictionary conforming to the MultipleIdentifierDto.json schema.")
    
        # Validate the body against the MultipleIdentifierDto.json schema
        from jsonschema import RefResolver, validate
        from jsonschema.exceptions import ValidationError
        import json
        import os
    
        # Get the absolute path to the definitions directory
        definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))
    
        # Load the MultipleIdentifierDto.json schema
        multiple_identifier_schema_path = os.path.join(definitions_dir, "MultipleIdentifierDto.json")
        with open(multiple_identifier_schema_path) as schema_file:
            multiple_identifier_schema = json.load(schema_file)
    
        # Create a resolver for external references
        base_uri = f"file://{definitions_dir}/"
        resolver = RefResolver(base_uri=base_uri, referrer=multiple_identifier_schema)
    
        try:
            validate(instance=body, schema=multiple_identifier_schema, resolver=resolver)
            logger.debug("Validation of body with MultipleIdentifierDto schema successful")
        except ValidationError as e:
            raise ValueError(f"Request body validation failed: {e.message}")
    
        # Send the POST request to the /nodes/no_network endpoint
        response = self.connection.post("nodes/no_network", data=body)
    
        # If the response status is 200, validate it against the Node.json schema
        if response.status_code == 200:
            # Load the Node.json schema
            node_schema_path = os.path.join(definitions_dir, "Node.json")
            with open(node_schema_path) as schema_file:
                node_schema = json.load(schema_file)
    
            try:
                validate(instance=response.json(), schema=node_schema, resolver=resolver)
                logger.debug("Validation of response with Node schema successful")
            except ValidationError as e:
                raise ValueError(f"Response validation failed: {e.message}")
    
            return
    
    #Section 4.5.13 
    def show_node_actions(self, identifier):
        """
        Show available actions on an existing node.

        :param identifier: The identifier of the node (String).
        :return: API response containing available actions if status code is 200.
        :raises ValueError: If the identifier is not a valid string or if the response does not conform to the Action.json schema.
        """
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("The 'identifier' parameter must be a non-empty string.")

        # Send the GET request to the /nodes/{identifier}/actions endpoint
        response = self.connection.get(f"nodes/{identifier}/actions")

        return response
        #CMU Rest API documentation does not have Actionable Array schema defined. (Actionable)
        # Handle the response if it's a dictionary or list
        # if isinstance(response, (dict, list)):
        #     from jsonschema import RefResolver, validate
        #     from jsonschema.exceptions import ValidationError
        #     import json
        #     import os

        #     # Get the absolute path to the definitions directory
        #     definitions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../definitions"))

        #     # Load the Action.json schema
        #     action_schema_path = os.path.join(definitions_dir, "Action.json")
        #     with open(action_schema_path) as schema_file:
        #         action_schema = json.load(schema_file)

        #     # Create a resolver for external references
        #     base_uri = f"file://{definitions_dir}/"
        #     resolver = RefResolver(base_uri=base_uri, referrer=action_schema)

        #     try:
        #         validate(instance=response, schema=action_schema, resolver=resolver)
        #         logger.debug("Validation of response with Action schema successful")
        #     except ValidationError as e:
        #         raise ValueError(f"Response validation failed: {e.message}")

        #     return response

        # # If the response is an HTTP response object, handle it as before
        # if response.status_code == 200:
        #     return response.json()

        # # Print the response for other status codes
        # logger.warning(f"Received non-200 response: {response.status_code}")
        # print(f"Response: {response.text}")
        # return response