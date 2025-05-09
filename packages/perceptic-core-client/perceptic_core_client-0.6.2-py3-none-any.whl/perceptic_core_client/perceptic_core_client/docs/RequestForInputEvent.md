# RequestForInputEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sequence** | **int** |  | [optional] 
**requested_data** | **object** |  | [optional] 
**provided_data** | **object** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.request_for_input_event import RequestForInputEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RequestForInputEvent from a JSON string
request_for_input_event_instance = RequestForInputEvent.from_json(json)
# print the JSON string representation of the object
print(RequestForInputEvent.to_json())

# convert the object into a dict
request_for_input_event_dict = request_for_input_event_instance.to_dict()
# create an instance of RequestForInputEvent from a dict
request_for_input_event_from_dict = RequestForInputEvent.from_dict(request_for_input_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


