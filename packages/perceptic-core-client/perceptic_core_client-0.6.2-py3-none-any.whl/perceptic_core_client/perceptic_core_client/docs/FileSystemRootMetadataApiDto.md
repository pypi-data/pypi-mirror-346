# FileSystemRootMetadataApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**container_name** | **str** |  | [optional] 
**bucket_name** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.file_system_root_metadata_api_dto import FileSystemRootMetadataApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of FileSystemRootMetadataApiDto from a JSON string
file_system_root_metadata_api_dto_instance = FileSystemRootMetadataApiDto.from_json(json)
# print the JSON string representation of the object
print(FileSystemRootMetadataApiDto.to_json())

# convert the object into a dict
file_system_root_metadata_api_dto_dict = file_system_root_metadata_api_dto_instance.to_dict()
# create an instance of FileSystemRootMetadataApiDto from a dict
file_system_root_metadata_api_dto_from_dict = FileSystemRootMetadataApiDto.from_dict(file_system_root_metadata_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


