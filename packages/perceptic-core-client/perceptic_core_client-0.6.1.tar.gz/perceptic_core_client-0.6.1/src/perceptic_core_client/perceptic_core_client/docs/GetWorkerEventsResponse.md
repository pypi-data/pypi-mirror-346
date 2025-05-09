# GetWorkerEventsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[WorkerEvent]**](WorkerEvent.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_worker_events_response import GetWorkerEventsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkerEventsResponse from a JSON string
get_worker_events_response_instance = GetWorkerEventsResponse.from_json(json)
# print the JSON string representation of the object
print(GetWorkerEventsResponse.to_json())

# convert the object into a dict
get_worker_events_response_dict = get_worker_events_response_instance.to_dict()
# create an instance of GetWorkerEventsResponse from a dict
get_worker_events_response_from_dict = GetWorkerEventsResponse.from_dict(get_worker_events_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


