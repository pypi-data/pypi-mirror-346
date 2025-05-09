# Perceptic Core API - Python Client (`perceptic-core-client`)

This package provides a generated Python client for interacting with the Perceptic Core API.

## Installation

Install the package from the configured package registry (ensure `pip` is configured, see parent project documentation if using GitHub Packages):

```bash
pip install perceptic-core-client

# To install a specific version:
# pip install perceptic-core-client==<version>
```

## Basic Usage
You need the URL of your Perceptic Core API instance and a valid authentication token (e.g., a Bearer token from Keycloak) obtained separately.

```python
import os
from perceptic_core_client import ApiClient, Configuration, ApiException
# Import the specific API category you need, e.g., UserResourceApi
from perceptic_core_client.api.user_resource_api import UserResourceApi
from pprint import pprint

# --- Configuration ---

# 1. Get your API host and token (e.g., from environment variables)
api_host = os.environ.get("PERCEPTIC_CORE_HOST", "http://localhost:8080")
access_token = os.environ.get("PERCEPTIC_CORE_TOKEN")

if not access_token:
    raise ValueError("Authentication token not found. Set PERCEPTIC_CORE_TOKEN environment variable.")

# 2. Create a Configuration object
configuration = Configuration(host=api_host)

# 3. Set the access token on the configuration
configuration.access_token = access_token

# 4. Create the main ApiClient
api_client = ApiClient(configuration=configuration)

# --- Making API Calls ---

# 5. Instantiate the specific API resource class you want to use
user_api = UserResourceApi(api_client=api_client)

# 6. Call API methods
try:
    print(f"Fetching user info from {api_host}...")
    me_response = user_api.api_v1_users_me_get()

    print("API Call Successful:")
    # Models often have a .to_dict() method for easy inspection
    pprint(me_response.to_dict())

except ApiException as e:
    print(f"API Error: Status {e.status}, Reason: {e.reason}")
    if e.body:
        print(f"Body: {e.body}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Example of another API (if you need to interact with connections)
# from perceptic_core_client.api.connection_resource_api import ConnectionResourceApi
# connection_api = ConnectionResourceApi(api_client=api_client)
# try:
#     # ... call methods on connection_api ...
# except ApiException as e:
#     # ... handle error ...
```