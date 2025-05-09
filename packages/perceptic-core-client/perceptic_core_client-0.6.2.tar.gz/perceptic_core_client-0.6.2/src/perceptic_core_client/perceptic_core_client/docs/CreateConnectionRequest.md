# CreateConnectionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**settings** | [**ConnectionSettingsApiDto**](ConnectionSettingsApiDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_connection_request import CreateConnectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequest from a JSON string
create_connection_request_instance = CreateConnectionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequest.to_json())

# convert the object into a dict
create_connection_request_dict = create_connection_request_instance.to_dict()
# create an instance of CreateConnectionRequest from a dict
create_connection_request_from_dict = CreateConnectionRequest.from_dict(create_connection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


