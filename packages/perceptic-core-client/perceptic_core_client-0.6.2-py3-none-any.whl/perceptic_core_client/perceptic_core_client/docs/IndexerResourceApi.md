# perceptic_core_client.IndexerResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_indexing_indexers_get**](IndexerResourceApi.md#api_v1_indexing_indexers_get) | **GET** /api/v1/indexing/indexers | List Indexers
[**api_v1_indexing_indexers_indexer_rid_get**](IndexerResourceApi.md#api_v1_indexing_indexers_indexer_rid_get) | **GET** /api/v1/indexing/indexers/{indexerRid} | Get Indexer


# **api_v1_indexing_indexers_get**
> ListIndexersResponse api_v1_indexing_indexers_get()

List Indexers

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.list_indexers_response import ListIndexersResponse
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
    api_instance = perceptic_core_client.IndexerResourceApi(api_client)

    try:
        # List Indexers
        api_response = api_instance.api_v1_indexing_indexers_get()
        print("The response of IndexerResourceApi->api_v1_indexing_indexers_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexerResourceApi->api_v1_indexing_indexers_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListIndexersResponse**](ListIndexersResponse.md)

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

# **api_v1_indexing_indexers_indexer_rid_get**
> GetIndexerResponse api_v1_indexing_indexers_indexer_rid_get(indexer_rid)

Get Indexer

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_indexer_response import GetIndexerResponse
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
    api_instance = perceptic_core_client.IndexerResourceApi(api_client)
    indexer_rid = 'indexer_rid_example' # str | 

    try:
        # Get Indexer
        api_response = api_instance.api_v1_indexing_indexers_indexer_rid_get(indexer_rid)
        print("The response of IndexerResourceApi->api_v1_indexing_indexers_indexer_rid_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexerResourceApi->api_v1_indexing_indexers_indexer_rid_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **indexer_rid** | **str**|  | 

### Return type

[**GetIndexerResponse**](GetIndexerResponse.md)

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

