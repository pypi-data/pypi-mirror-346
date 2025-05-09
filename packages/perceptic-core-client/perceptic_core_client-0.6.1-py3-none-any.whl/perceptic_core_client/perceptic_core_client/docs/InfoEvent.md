# InfoEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sequence** | **int** |  | [optional] 
**type_of** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.info_event import InfoEvent

# TODO update the JSON string below
json = "{}"
# create an instance of InfoEvent from a JSON string
info_event_instance = InfoEvent.from_json(json)
# print the JSON string representation of the object
print(InfoEvent.to_json())

# convert the object into a dict
info_event_dict = info_event_instance.to_dict()
# create an instance of InfoEvent from a dict
info_event_from_dict = InfoEvent.from_dict(info_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


