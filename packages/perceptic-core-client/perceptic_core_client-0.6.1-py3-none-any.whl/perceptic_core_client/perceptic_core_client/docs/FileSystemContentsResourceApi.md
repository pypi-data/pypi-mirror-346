# perceptic_core_client.FileSystemContentsResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_file_systems_file_system_rid_contents_download_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_download_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/download | Download
[**api_v1_file_systems_file_system_rid_contents_files_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_files_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/files | List Files Flattened
[**api_v1_file_systems_file_system_rid_contents_folders_post**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_folders_post) | **POST** /api/v1/file-systems/{fileSystemRid}/contents/folders | Create Folder
[**api_v1_file_systems_file_system_rid_contents_list_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_list_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/list | List
[**api_v1_file_systems_file_system_rid_contents_metadata_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_metadata_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/metadata | Get Metadata
[**api_v1_file_systems_file_system_rid_contents_parent_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_parent_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/parent | Get Parent
[**api_v1_file_systems_file_system_rid_contents_signed_url_get**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_signed_url_get) | **GET** /api/v1/file-systems/{fileSystemRid}/contents/signed-url | Signed Url
[**api_v1_file_systems_file_system_rid_contents_upload_post**](FileSystemContentsResourceApi.md#api_v1_file_systems_file_system_rid_contents_upload_post) | **POST** /api/v1/file-systems/{fileSystemRid}/contents/upload | Upload File


# **api_v1_file_systems_file_system_rid_contents_download_get**
> bytearray api_v1_file_systems_file_system_rid_contents_download_get(file_system_rid, file=file)

Download

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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    file = 'file_example' # str |  (optional)

    try:
        # Download
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_download_get(file_system_rid, file=file)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_download_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_download_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **file** | **str**|  | [optional] 

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

# **api_v1_file_systems_file_system_rid_contents_files_get**
> PagedListFileSystemResponse api_v1_file_systems_file_system_rid_contents_files_get(file_system_rid, folder=folder, page_size=page_size, resume_token=resume_token)

List Files Flattened

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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    folder = 'folder_example' # str |  (optional)
    page_size = 1000 # int |  (optional) (default to 1000)
    resume_token = 'resume_token_example' # str |  (optional)

    try:
        # List Files Flattened
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_files_get(file_system_rid, folder=folder, page_size=page_size, resume_token=resume_token)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_files_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_files_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **folder** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] [default to 1000]
 **resume_token** | **str**|  | [optional] 

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

# **api_v1_file_systems_file_system_rid_contents_folders_post**
> CreateFolderResponse api_v1_file_systems_file_system_rid_contents_folders_post(file_system_rid, create_folder_request, parent=parent)

Create Folder

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.create_folder_request import CreateFolderRequest
from perceptic_core_client.models.create_folder_response import CreateFolderResponse
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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    create_folder_request = perceptic_core_client.CreateFolderRequest() # CreateFolderRequest | 
    parent = 'parent_example' # str |  (optional)

    try:
        # Create Folder
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_folders_post(file_system_rid, create_folder_request, parent=parent)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_folders_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_folders_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **create_folder_request** | [**CreateFolderRequest**](CreateFolderRequest.md)|  | 
 **parent** | **str**|  | [optional] 

### Return type

[**CreateFolderResponse**](CreateFolderResponse.md)

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

# **api_v1_file_systems_file_system_rid_contents_list_get**
> ListFileSystemResponse api_v1_file_systems_file_system_rid_contents_list_get(file_system_rid, folder=folder)

List

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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    folder = 'folder_example' # str |  (optional)

    try:
        # List
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_list_get(file_system_rid, folder=folder)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_list_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_list_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **folder** | **str**|  | [optional] 

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

# **api_v1_file_systems_file_system_rid_contents_metadata_get**
> GetMetadataResponse api_v1_file_systems_file_system_rid_contents_metadata_get(file_system_rid, id=id)

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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    id = 'id_example' # str |  (optional)

    try:
        # Get Metadata
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_metadata_get(file_system_rid, id=id)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_metadata_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_metadata_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **id** | **str**|  | [optional] 

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

# **api_v1_file_systems_file_system_rid_contents_parent_get**
> GetParentResponse api_v1_file_systems_file_system_rid_contents_parent_get(file_system_rid, id=id)

Get Parent

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_parent_response import GetParentResponse
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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    id = 'id_example' # str |  (optional)

    try:
        # Get Parent
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_parent_get(file_system_rid, id=id)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_parent_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_parent_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **id** | **str**|  | [optional] 

### Return type

[**GetParentResponse**](GetParentResponse.md)

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

# **api_v1_file_systems_file_system_rid_contents_signed_url_get**
> GetSignedUrlResponse api_v1_file_systems_file_system_rid_contents_signed_url_get(file_system_rid, file=file)

Signed Url

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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    file = 'file_example' # str |  (optional)

    try:
        # Signed Url
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_signed_url_get(file_system_rid, file=file)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_signed_url_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_signed_url_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **file** | **str**|  | [optional] 

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

# **api_v1_file_systems_file_system_rid_contents_upload_post**
> UploadFileToManagedFileSystemResponse api_v1_file_systems_file_system_rid_contents_upload_post(file_system_rid, file, filename, overwrite=overwrite, parent=parent)

Upload File

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.upload_file_to_managed_file_system_response import UploadFileToManagedFileSystemResponse
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
    api_instance = perceptic_core_client.FileSystemContentsResourceApi(api_client)
    file_system_rid = 'file_system_rid_example' # str | 
    file = None # bytearray | 
    filename = 'filename_example' # str | 
    overwrite = None # object |  (optional)
    parent = 'parent_example' # str |  (optional)

    try:
        # Upload File
        api_response = api_instance.api_v1_file_systems_file_system_rid_contents_upload_post(file_system_rid, file, filename, overwrite=overwrite, parent=parent)
        print("The response of FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_upload_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileSystemContentsResourceApi->api_v1_file_systems_file_system_rid_contents_upload_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_system_rid** | **str**|  | 
 **file** | **bytearray**|  | 
 **filename** | **str**|  | 
 **overwrite** | [**object**](.md)|  | [optional] 
 **parent** | **str**|  | [optional] 

### Return type

[**UploadFileToManagedFileSystemResponse**](UploadFileToManagedFileSystemResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

