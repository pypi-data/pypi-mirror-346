# WorkerEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**sequence** | **int** |  | [optional] 
**type_of** | **str** |  | [optional] 
**payload** | **object** |  | [optional] 
**requested_data** | **object** |  | [optional] 
**provided_data** | **object** |  | [optional] 

## Example

```python
from perceptic_core_client.models.worker_event import WorkerEvent

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerEvent from a JSON string
worker_event_instance = WorkerEvent.from_json(json)
# print the JSON string representation of the object
print(WorkerEvent.to_json())

# convert the object into a dict
worker_event_dict = worker_event_instance.to_dict()
# create an instance of WorkerEvent from a dict
worker_event_from_dict = WorkerEvent.from_dict(worker_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


