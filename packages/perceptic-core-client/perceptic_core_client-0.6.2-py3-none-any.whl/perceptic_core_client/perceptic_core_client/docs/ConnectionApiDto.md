# ConnectionApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**user_id** | **str** |  | [optional] 
**settings** | [**ConnectionSettingsApiDto**](ConnectionSettingsApiDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.connection_api_dto import ConnectionApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionApiDto from a JSON string
connection_api_dto_instance = ConnectionApiDto.from_json(json)
# print the JSON string representation of the object
print(ConnectionApiDto.to_json())

# convert the object into a dict
connection_api_dto_dict = connection_api_dto_instance.to_dict()
# create an instance of ConnectionApiDto from a dict
connection_api_dto_from_dict = ConnectionApiDto.from_dict(connection_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


