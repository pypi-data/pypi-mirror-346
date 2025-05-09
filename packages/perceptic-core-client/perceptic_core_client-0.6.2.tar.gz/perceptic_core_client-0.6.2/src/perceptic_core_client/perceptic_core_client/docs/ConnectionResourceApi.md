# perceptic_core_client.ConnectionResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_connections_connection_rid_get**](ConnectionResourceApi.md#api_v1_connections_connection_rid_get) | **GET** /api/v1/connections/{connectionRid} | Get Connection
[**api_v1_connections_post**](ConnectionResourceApi.md#api_v1_connections_post) | **POST** /api/v1/connections | Create Connection


# **api_v1_connections_connection_rid_get**
> GetConnectionResponse api_v1_connections_connection_rid_get(connection_rid)

Get Connection

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_connection_response import GetConnectionResponse
from perceptic_core_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = perceptic_core_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with perceptic_core_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = perceptic_core_client.ConnectionResourceApi(api_client)
    connection_rid = 'connection_rid_example' # str | 

    try:
        # Get Connection
        api_response = api_instance.api_v1_connections_connection_rid_get(connection_rid)
        print("The response of ConnectionResourceApi->api_v1_connections_connection_rid_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionResourceApi->api_v1_connections_connection_rid_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_rid** | **str**|  | 

### Return type

[**GetConnectionResponse**](GetConnectionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_connections_post**
> CreateConnectionResponse api_v1_connections_post(create_connection_request)

Create Connection

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.create_connection_request import CreateConnectionRequest
from perceptic_core_client.models.create_connection_response import CreateConnectionResponse
from perceptic_core_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = perceptic_core_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with perceptic_core_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = perceptic_core_client.ConnectionResourceApi(api_client)
    create_connection_request = perceptic_core_client.CreateConnectionRequest() # CreateConnectionRequest | 

    try:
        # Create Connection
        api_response = api_instance.api_v1_connections_post(create_connection_request)
        print("The response of ConnectionResourceApi->api_v1_connections_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionResourceApi->api_v1_connections_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_connection_request** | [**CreateConnectionRequest**](CreateConnectionRequest.md)|  | 

### Return type

[**CreateConnectionResponse**](CreateConnectionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

