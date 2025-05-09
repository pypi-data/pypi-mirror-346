# GetWorkerStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_status** | [**RunStatusDto**](RunStatusDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_worker_status_response import GetWorkerStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkerStatusResponse from a JSON string
get_worker_status_response_instance = GetWorkerStatusResponse.from_json(json)
# print the JSON string representation of the object
print(GetWorkerStatusResponse.to_json())

# convert the object into a dict
get_worker_status_response_dict = get_worker_status_response_instance.to_dict()
# create an instance of GetWorkerStatusResponse from a dict
get_worker_status_response_from_dict = GetWorkerStatusResponse.from_dict(get_worker_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


