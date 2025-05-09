# AzureBlobFileSystemRootMetadataApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_name** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.azure_blob_file_system_root_metadata_api_dto import AzureBlobFileSystemRootMetadataApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of AzureBlobFileSystemRootMetadataApiDto from a JSON string
azure_blob_file_system_root_metadata_api_dto_instance = AzureBlobFileSystemRootMetadataApiDto.from_json(json)
# print the JSON string representation of the object
print(AzureBlobFileSystemRootMetadataApiDto.to_json())

# convert the object into a dict
azure_blob_file_system_root_metadata_api_dto_dict = azure_blob_file_system_root_metadata_api_dto_instance.to_dict()
# create an instance of AzureBlobFileSystemRootMetadataApiDto from a dict
azure_blob_file_system_root_metadata_api_dto_from_dict = AzureBlobFileSystemRootMetadataApiDto.from_dict(azure_blob_file_system_root_metadata_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


