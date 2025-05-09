# perceptic_core_client.UriResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_resources_download_get**](UriResourceApi.md#api_v1_resources_download_get) | **GET** /api/v1/resources/download | Download Resource
[**api_v1_resources_files_get**](UriResourceApi.md#api_v1_resources_files_get) | **GET** /api/v1/resources/files | List Files
[**api_v1_resources_list_get**](UriResourceApi.md#api_v1_resources_list_get) | **GET** /api/v1/resources/list | List Resources
[**api_v1_resources_metadata_get**](UriResourceApi.md#api_v1_resources_metadata_get) | **GET** /api/v1/resources/metadata | Get Metadata
[**api_v1_resources_parent_get**](UriResourceApi.md#api_v1_resources_parent_get) | **GET** /api/v1/resources/parent | Get Parent
[**api_v1_resources_signed_url_get**](UriResourceApi.md#api_v1_resources_signed_url_get) | **GET** /api/v1/resources/signed-url | Get Signed Url


# **api_v1_resources_download_get**
> bytearray api_v1_resources_download_get(uri=uri)

Download Resource

### Example


```python
import perceptic_core_client
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    uri = 'uri_example' # str |  (optional)

    try:
        # Download Resource
        api_response = api_instance.api_v1_resources_download_get(uri=uri)
        print("The response of UriResourceApi->api_v1_resources_download_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_download_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uri** | **str**|  | [optional] 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_resources_files_get**
> PagedListFileSystemResponse api_v1_resources_files_get(page_size=page_size, resume_token=resume_token, uri=uri)

List Files

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.paged_list_file_system_response import PagedListFileSystemResponse
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    page_size = 500 # int |  (optional) (default to 500)
    resume_token = 'resume_token_example' # str |  (optional)
    uri = 'uri_example' # str |  (optional)

    try:
        # List Files
        api_response = api_instance.api_v1_resources_files_get(page_size=page_size, resume_token=resume_token, uri=uri)
        print("The response of UriResourceApi->api_v1_resources_files_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_files_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**|  | [optional] [default to 500]
 **resume_token** | **str**|  | [optional] 
 **uri** | **str**|  | [optional] 

### Return type

[**PagedListFileSystemResponse**](PagedListFileSystemResponse.md)

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

# **api_v1_resources_list_get**
> ListFileSystemResponse api_v1_resources_list_get(uri=uri)

List Resources

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.list_file_system_response import ListFileSystemResponse
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    uri = 'uri_example' # str |  (optional)

    try:
        # List Resources
        api_response = api_instance.api_v1_resources_list_get(uri=uri)
        print("The response of UriResourceApi->api_v1_resources_list_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_list_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uri** | **str**|  | [optional] 

### Return type

[**ListFileSystemResponse**](ListFileSystemResponse.md)

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

# **api_v1_resources_metadata_get**
> GetMetadataResponse api_v1_resources_metadata_get(uri=uri)

Get Metadata

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_metadata_response import GetMetadataResponse
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    uri = 'uri_example' # str |  (optional)

    try:
        # Get Metadata
        api_response = api_instance.api_v1_resources_metadata_get(uri=uri)
        print("The response of UriResourceApi->api_v1_resources_metadata_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_metadata_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uri** | **str**|  | [optional] 

### Return type

[**GetMetadataResponse**](GetMetadataResponse.md)

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

# **api_v1_resources_parent_get**
> GetParentUriResponse api_v1_resources_parent_get(uri=uri)

Get Parent

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_parent_uri_response import GetParentUriResponse
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    uri = 'uri_example' # str |  (optional)

    try:
        # Get Parent
        api_response = api_instance.api_v1_resources_parent_get(uri=uri)
        print("The response of UriResourceApi->api_v1_resources_parent_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_parent_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uri** | **str**|  | [optional] 

### Return type

[**GetParentUriResponse**](GetParentUriResponse.md)

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

# **api_v1_resources_signed_url_get**
> GetSignedUrlResponse api_v1_resources_signed_url_get(uri=uri)

Get Signed Url

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_signed_url_response import GetSignedUrlResponse
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
    api_instance = perceptic_core_client.UriResourceApi(api_client)
    uri = 'uri_example' # str |  (optional)

    try:
        # Get Signed Url
        api_response = api_instance.api_v1_resources_signed_url_get(uri=uri)
        print("The response of UriResourceApi->api_v1_resources_signed_url_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UriResourceApi->api_v1_resources_signed_url_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uri** | **str**|  | [optional] 

### Return type

[**GetSignedUrlResponse**](GetSignedUrlResponse.md)

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

