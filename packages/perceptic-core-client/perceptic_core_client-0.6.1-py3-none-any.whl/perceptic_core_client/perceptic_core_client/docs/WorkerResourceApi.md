# perceptic_core_client.WorkerResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_workers_get**](WorkerResourceApi.md#api_v1_workers_get) | **GET** /api/v1/workers | Get Workers
[**api_v1_workers_worker_id_get**](WorkerResourceApi.md#api_v1_workers_worker_id_get) | **GET** /api/v1/workers/{workerId} | Get Worker Metadata
[**api_v1_workers_worker_id_runs_post**](WorkerResourceApi.md#api_v1_workers_worker_id_runs_post) | **POST** /api/v1/workers/{workerId}/runs | Post Worker Run
[**api_v1_workers_worker_id_runs_run_rid_events_get**](WorkerResourceApi.md#api_v1_workers_worker_id_runs_run_rid_events_get) | **GET** /api/v1/workers/{workerId}/runs/{runRid}/events | Get Worker Run Events
[**api_v1_workers_worker_id_runs_run_rid_resume_post**](WorkerResourceApi.md#api_v1_workers_worker_id_runs_run_rid_resume_post) | **POST** /api/v1/workers/{workerId}/runs/{runRid}/resume | Post Resume Run
[**api_v1_workers_worker_id_runs_run_rid_status_get**](WorkerResourceApi.md#api_v1_workers_worker_id_runs_run_rid_status_get) | **GET** /api/v1/workers/{workerId}/runs/{runRid}/status | Get Worker Run Status


# **api_v1_workers_get**
> GetWorkersResponse api_v1_workers_get()

Get Workers

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_workers_response import GetWorkersResponse
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)

    try:
        # Get Workers
        api_response = api_instance.api_v1_workers_get()
        print("The response of WorkerResourceApi->api_v1_workers_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetWorkersResponse**](GetWorkersResponse.md)

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

# **api_v1_workers_worker_id_get**
> GetWorkerMetadataResponse api_v1_workers_worker_id_get(worker_id, version=version)

Get Worker Metadata

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_worker_metadata_response import GetWorkerMetadataResponse
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)
    worker_id = 'worker_id_example' # str | 
    version = 'version_example' # str |  (optional)

    try:
        # Get Worker Metadata
        api_response = api_instance.api_v1_workers_worker_id_get(worker_id, version=version)
        print("The response of WorkerResourceApi->api_v1_workers_worker_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_worker_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **worker_id** | **str**|  | 
 **version** | **str**|  | [optional] 

### Return type

[**GetWorkerMetadataResponse**](GetWorkerMetadataResponse.md)

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

# **api_v1_workers_worker_id_runs_post**
> PostWorkerRunResponse api_v1_workers_worker_id_runs_post(worker_id, post_worker_run_request, version=version)

Post Worker Run

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.post_worker_run_request import PostWorkerRunRequest
from perceptic_core_client.models.post_worker_run_response import PostWorkerRunResponse
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)
    worker_id = 'worker_id_example' # str | 
    post_worker_run_request = perceptic_core_client.PostWorkerRunRequest() # PostWorkerRunRequest | 
    version = 'version_example' # str |  (optional)

    try:
        # Post Worker Run
        api_response = api_instance.api_v1_workers_worker_id_runs_post(worker_id, post_worker_run_request, version=version)
        print("The response of WorkerResourceApi->api_v1_workers_worker_id_runs_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_worker_id_runs_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **worker_id** | **str**|  | 
 **post_worker_run_request** | [**PostWorkerRunRequest**](PostWorkerRunRequest.md)|  | 
 **version** | **str**|  | [optional] 

### Return type

[**PostWorkerRunResponse**](PostWorkerRunResponse.md)

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

# **api_v1_workers_worker_id_runs_run_rid_events_get**
> GetWorkerEventsResponse api_v1_workers_worker_id_runs_run_rid_events_get(run_rid, worker_id, limit=limit, offset=offset)

Get Worker Run Events

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_worker_events_response import GetWorkerEventsResponse
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)
    run_rid = 'run_rid_example' # str | 
    worker_id = 'worker_id_example' # str | 
    limit = 50 # int |  (optional) (default to 50)
    offset = 0 # int |  (optional) (default to 0)

    try:
        # Get Worker Run Events
        api_response = api_instance.api_v1_workers_worker_id_runs_run_rid_events_get(run_rid, worker_id, limit=limit, offset=offset)
        print("The response of WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_events_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_events_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_rid** | **str**|  | 
 **worker_id** | **str**|  | 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**GetWorkerEventsResponse**](GetWorkerEventsResponse.md)

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

# **api_v1_workers_worker_id_runs_run_rid_resume_post**
> object api_v1_workers_worker_id_runs_run_rid_resume_post(run_rid, worker_id, post_worker_run_request)

Post Resume Run

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.post_worker_run_request import PostWorkerRunRequest
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)
    run_rid = 'run_rid_example' # str | 
    worker_id = 'worker_id_example' # str | 
    post_worker_run_request = perceptic_core_client.PostWorkerRunRequest() # PostWorkerRunRequest | 

    try:
        # Post Resume Run
        api_response = api_instance.api_v1_workers_worker_id_runs_run_rid_resume_post(run_rid, worker_id, post_worker_run_request)
        print("The response of WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_resume_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_resume_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_rid** | **str**|  | 
 **worker_id** | **str**|  | 
 **post_worker_run_request** | [**PostWorkerRunRequest**](PostWorkerRunRequest.md)|  | 

### Return type

**object**

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

# **api_v1_workers_worker_id_runs_run_rid_status_get**
> GetWorkerStatusResponse api_v1_workers_worker_id_runs_run_rid_status_get(run_rid, worker_id)

Get Worker Run Status

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_worker_status_response import GetWorkerStatusResponse
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
    api_instance = perceptic_core_client.WorkerResourceApi(api_client)
    run_rid = 'run_rid_example' # str | 
    worker_id = 'worker_id_example' # str | 

    try:
        # Get Worker Run Status
        api_response = api_instance.api_v1_workers_worker_id_runs_run_rid_status_get(run_rid, worker_id)
        print("The response of WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_status_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkerResourceApi->api_v1_workers_worker_id_runs_run_rid_status_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_rid** | **str**|  | 
 **worker_id** | **str**|  | 

### Return type

[**GetWorkerStatusResponse**](GetWorkerStatusResponse.md)

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

