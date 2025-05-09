# perceptic_core_client.IndexingTaskResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_indexing_tasks_post**](IndexingTaskResourceApi.md#api_v1_indexing_tasks_post) | **POST** /api/v1/indexing/tasks | Create Indexing Task
[**api_v1_indexing_tasks_task_rid_actions_get**](IndexingTaskResourceApi.md#api_v1_indexing_tasks_task_rid_actions_get) | **GET** /api/v1/indexing/tasks/{taskRid}/actions | List Indexing Actions
[**api_v1_indexing_tasks_task_rid_execute_post**](IndexingTaskResourceApi.md#api_v1_indexing_tasks_task_rid_execute_post) | **POST** /api/v1/indexing/tasks/{taskRid}/execute | Start Execution
[**api_v1_indexing_tasks_task_rid_get**](IndexingTaskResourceApi.md#api_v1_indexing_tasks_task_rid_get) | **GET** /api/v1/indexing/tasks/{taskRid} | Get Indexing Task


# **api_v1_indexing_tasks_post**
> CreateIndexingTaskResponse api_v1_indexing_tasks_post(create_indexing_task_request, dry_run=dry_run, freshness_minutes=freshness_minutes)

Create Indexing Task

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.create_indexing_task_request import CreateIndexingTaskRequest
from perceptic_core_client.models.create_indexing_task_response import CreateIndexingTaskResponse
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
    api_instance = perceptic_core_client.IndexingTaskResourceApi(api_client)
    create_indexing_task_request = perceptic_core_client.CreateIndexingTaskRequest() # CreateIndexingTaskRequest | 
    dry_run = False # bool |  (optional) (default to False)
    freshness_minutes = 30 # int |  (optional) (default to 30)

    try:
        # Create Indexing Task
        api_response = api_instance.api_v1_indexing_tasks_post(create_indexing_task_request, dry_run=dry_run, freshness_minutes=freshness_minutes)
        print("The response of IndexingTaskResourceApi->api_v1_indexing_tasks_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexingTaskResourceApi->api_v1_indexing_tasks_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_indexing_task_request** | [**CreateIndexingTaskRequest**](CreateIndexingTaskRequest.md)|  | 
 **dry_run** | **bool**|  | [optional] [default to False]
 **freshness_minutes** | **int**|  | [optional] [default to 30]

### Return type

[**CreateIndexingTaskResponse**](CreateIndexingTaskResponse.md)

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

# **api_v1_indexing_tasks_task_rid_actions_get**
> ListIndexingActionsResponse api_v1_indexing_tasks_task_rid_actions_get(task_rid, limit=limit, offset=offset, status=status)

List Indexing Actions

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.indexing_action_status import IndexingActionStatus
from perceptic_core_client.models.list_indexing_actions_response import ListIndexingActionsResponse
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
    api_instance = perceptic_core_client.IndexingTaskResourceApi(api_client)
    task_rid = 'task_rid_example' # str | 
    limit = 100 # int |  (optional) (default to 100)
    offset = 0 # int |  (optional) (default to 0)
    status = [perceptic_core_client.IndexingActionStatus()] # List[IndexingActionStatus] |  (optional)

    try:
        # List Indexing Actions
        api_response = api_instance.api_v1_indexing_tasks_task_rid_actions_get(task_rid, limit=limit, offset=offset, status=status)
        print("The response of IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_actions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_actions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_rid** | **str**|  | 
 **limit** | **int**|  | [optional] [default to 100]
 **offset** | **int**|  | [optional] [default to 0]
 **status** | [**List[IndexingActionStatus]**](IndexingActionStatus.md)|  | [optional] 

### Return type

[**ListIndexingActionsResponse**](ListIndexingActionsResponse.md)

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

# **api_v1_indexing_tasks_task_rid_execute_post**
> StartExecutionResponse api_v1_indexing_tasks_task_rid_execute_post(task_rid)

Start Execution

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.start_execution_response import StartExecutionResponse
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
    api_instance = perceptic_core_client.IndexingTaskResourceApi(api_client)
    task_rid = 'task_rid_example' # str | 

    try:
        # Start Execution
        api_response = api_instance.api_v1_indexing_tasks_task_rid_execute_post(task_rid)
        print("The response of IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_execute_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_execute_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_rid** | **str**|  | 

### Return type

[**StartExecutionResponse**](StartExecutionResponse.md)

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

# **api_v1_indexing_tasks_task_rid_get**
> GetIndexingTaskResponse api_v1_indexing_tasks_task_rid_get(task_rid)

Get Indexing Task

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.get_indexing_task_response import GetIndexingTaskResponse
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
    api_instance = perceptic_core_client.IndexingTaskResourceApi(api_client)
    task_rid = 'task_rid_example' # str | 

    try:
        # Get Indexing Task
        api_response = api_instance.api_v1_indexing_tasks_task_rid_get(task_rid)
        print("The response of IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IndexingTaskResourceApi->api_v1_indexing_tasks_task_rid_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_rid** | **str**|  | 

### Return type

[**GetIndexingTaskResponse**](GetIndexingTaskResponse.md)

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

