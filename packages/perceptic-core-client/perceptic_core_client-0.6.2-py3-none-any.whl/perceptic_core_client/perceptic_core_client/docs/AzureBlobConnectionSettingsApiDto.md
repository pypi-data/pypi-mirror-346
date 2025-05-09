# AzureBlobConnectionSettingsApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container** | **str** |  | 
**credential_name** | **str** |  | 
**credential_key** | **str** |  | 
**url** | **str** |  | 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.azure_blob_connection_settings_api_dto import AzureBlobConnectionSettingsApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of AzureBlobConnectionSettingsApiDto from a JSON string
azure_blob_connection_settings_api_dto_instance = AzureBlobConnectionSettingsApiDto.from_json(json)
# print the JSON string representation of the object
print(AzureBlobConnectionSettingsApiDto.to_json())

# convert the object into a dict
azure_blob_connection_settings_api_dto_dict = azure_blob_connection_settings_api_dto_instance.to_dict()
# create an instance of AzureBlobConnectionSettingsApiDto from a dict
azure_blob_connection_settings_api_dto_from_dict = AzureBlobConnectionSettingsApiDto.from_dict(azure_blob_connection_settings_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


