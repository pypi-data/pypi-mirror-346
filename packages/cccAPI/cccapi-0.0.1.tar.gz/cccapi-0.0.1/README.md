# ccc_client

This package provides a simple, modular SDK for the CCC REST API.

## Features

* Automatically handles authentication and renewal
* Graceful error management
* Logically organized modules
* Easily maintained

## Installation

**Install using `pip`:**

```bash
pip install cccAPI 
```

**Install from source:**

```bash
git clone https://github.hpe.com/hpe/cccAPI.git
cd cccAPI
pip install -e .
```

## Quick Start

### Initialize the Client

```python
import json
from cccAPI import cccAPIClient
client = cccAPIClient("https://localhost:8000/cmu/v1", "root", "your-password")
```

### Example Usage

#### Get Nodes

```python
nodes = client.nodes.show_nodes()
print(json.dumps(nodes, indent=4))
```

#### Get specific Node

```python
#Specific node named BartC01n1-091
node = client.nodes.show_node("BartC01n1-091")
print(json.dumps(node, indent=4))
```

#### Get specific Node/fields 
- Allowed fields are: 

```python 
query_params = {"fields": "name,id,uuid,network.name,network.ipAddress,network.macAddress"}
specific_nodes=client.nodes.show_nodes(query_params)
print(json.dumps(specific_nodes, indent=4))
```

## API Modules

| Module                | Description |
|----------------------|-------------|
| `nodes`           | Query history, top clients/domains, DNS stats |
| `image_groups`       | Enable/disable blocking |
| `network_groups`  | Create, update, and delete groups |
| `custom_groups` | Allow/block domains (exact & regex) |
| `resource_features` | Manage client-specific rules |
| `image_capture_deployment`   | Manage blocklists (Adlists) |
| `power_operation`            | Modify CCC configuration |
| `application`          | Get CCC core process (FTL) info |
| `architecture`              | Manage DHCP leases |
| `management_cards`      | View network devices, interfaces, routes |
| `tasks`           | Flush logs, restart services |

## License

This project is license under the [MIT license](LICENSE).
