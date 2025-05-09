# S3ConnectionSettingsApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**region** | **str** |  | 
**access_key** | **str** |  | 
**secret_key** | **str** |  | 
**url** | **str** |  | 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.s3_connection_settings_api_dto import S3ConnectionSettingsApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of S3ConnectionSettingsApiDto from a JSON string
s3_connection_settings_api_dto_instance = S3ConnectionSettingsApiDto.from_json(json)
# print the JSON string representation of the object
print(S3ConnectionSettingsApiDto.to_json())

# convert the object into a dict
s3_connection_settings_api_dto_dict = s3_connection_settings_api_dto_instance.to_dict()
# create an instance of S3ConnectionSettingsApiDto from a dict
s3_connection_settings_api_dto_from_dict = S3ConnectionSettingsApiDto.from_dict(s3_connection_settings_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


