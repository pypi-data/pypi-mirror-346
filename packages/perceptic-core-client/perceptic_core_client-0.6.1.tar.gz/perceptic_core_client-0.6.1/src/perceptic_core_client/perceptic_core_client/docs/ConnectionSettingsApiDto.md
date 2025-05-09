# ConnectionSettingsApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**region** | **str** |  | 
**access_key** | **str** |  | 
**secret_key** | **str** |  | 
**url** | **str** |  | 
**container** | **str** |  | 
**credential_name** | **str** |  | 
**credential_key** | **str** |  | 

## Example

```python
from perceptic_core_client.models.connection_settings_api_dto import ConnectionSettingsApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionSettingsApiDto from a JSON string
connection_settings_api_dto_instance = ConnectionSettingsApiDto.from_json(json)
# print the JSON string representation of the object
print(ConnectionSettingsApiDto.to_json())

# convert the object into a dict
connection_settings_api_dto_dict = connection_settings_api_dto_instance.to_dict()
# create an instance of ConnectionSettingsApiDto from a dict
connection_settings_api_dto_from_dict = ConnectionSettingsApiDto.from_dict(connection_settings_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


