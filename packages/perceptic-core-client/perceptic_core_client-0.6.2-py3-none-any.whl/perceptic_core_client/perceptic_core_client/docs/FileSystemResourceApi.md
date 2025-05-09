# perceptic_core_client.FileSystemResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_file_systems_file_system_rid_get**](FileSystemResourceApi.md#api_v1_file_systems_file_system_rid_get) | **GET** /api/v1/file-systems/{fileSystemRid} | Get File System
[**api_v1_file_systems_get**](FileSystemResourceApi.md#api_v1_file_systems_get) | **GET** /api/v1/file-systems | List All File Systems
[**api_v1_file_systems_managed_post**](FileSystemResourceApi.md#api_v1_file_systems_managed_post) | **POST** /api/v1/file-systems/managed | Create Managed File System
[**api_v1_file_systems_remote_post**](FileSystemResourceApi.md#api_v1_file_systems_remote_post) | **POST** /api/v1/file-systems/remote | Create Remote File System


# **api_v1_file_systems_file_system_rid_get**
> FileSystemApiDto api_v1_file_systems_file_system_rid_get(file_system_rid)

Get File System

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.file_system_api_dto import FileSystemApiDto
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
    api_instance = perceptic_core_client.FileSystemResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 

    try:
        # Get File System
        api_response = api_instance.api_v1_file_systems_file_system_rid_get(file_system_rid)
        print("The response of FileSystemResourceApi->api_v1_file_systems_file_system_rid_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemResourceApi->api_v1_file_systems_file_system_rid_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 

### Return type

[**FileSystemApiDto**](FileSystemApiDto.md)

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

# **api_v1_file_systems_get**
> ListAllFileSystemsResponse api_v1_file_systems_get()

List All File Systems

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.list_all_file_systems_response import ListAllFileSystemsResponse
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
    api_instance = perceptic_core_client.FileSystemResourceApi(api_client)

    try:
        # List All File Systems
        api_response = api_instance.api_v1_file_systems_get()
        print("The response of FileSystemResourceApi->api_v1_file_systems_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemResourceApi->api_v1_file_systems_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListAllFileSystemsResponse**](ListAllFileSystemsResponse.md)

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

# **api_v1_file_systems_managed_post**
> CreateFileSystemResponse api_v1_file_systems_managed_post(create_managed_file_system_request)

Create Managed File System

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.create_file_system_response import CreateFileSystemResponse
from perceptic_core_client.models.create_managed_file_system_request import CreateManagedFileSystemRequest
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
    api_instance = perceptic_core_client.FileSystemResourceApi(api_client)
    create_managed_file_system_request = perceptic_core_client.CreateManagedFileSystemRequest() # CreateManagedFileSystemRequest | 

    try:
        # Create Managed File System
        api_response = api_instance.api_v1_file_systems_managed_post(create_managed_file_system_request)
        print("The response of FileSystemResourceApi->api_v1_file_systems_managed_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemResourceApi->api_v1_file_systems_managed_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_managed_file_system_request** | [**CreateManagedFileSystemRequest**](CreateManagedFileSystemRequest.md)|  | 

### Return type

[**CreateFileSystemResponse**](CreateFileSystemResponse.md)

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

# **api_v1_file_systems_remote_post**
> CreateFileSystemResponse api_v1_file_systems_remote_post(create_remote_file_system_request)

Create Remote File System

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.create_file_system_response import CreateFileSystemResponse
from perceptic_core_client.models.create_remote_file_system_request import CreateRemoteFileSystemRequest
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
    api_instance = perceptic_core_client.FileSystemResourceApi(api_client)
    create_remote_file_system_request = perceptic_core_client.CreateRemoteFileSystemRequest() # CreateRemoteFileSystemRequest | 

    try:
        # Create Remote File System
        api_response = api_instance.api_v1_file_systems_remote_post(create_remote_file_system_request)
        print("The response of FileSystemResourceApi->api_v1_file_systems_remote_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemResourceApi->api_v1_file_systems_remote_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_remote_file_system_request** | [**CreateRemoteFileSystemRequest**](CreateRemoteFileSystemRequest.md)|  | 

### Return type

[**CreateFileSystemResponse**](CreateFileSystemResponse.md)

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

