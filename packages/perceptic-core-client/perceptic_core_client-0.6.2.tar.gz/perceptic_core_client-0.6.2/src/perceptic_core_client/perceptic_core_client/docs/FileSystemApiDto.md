# FileSystemApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**rid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**metadata** | [**FileSystemRootMetadataApiDto**](FileSystemRootMetadataApiDto.md) |  | [optional] 
**connection_rid** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.file_system_api_dto import FileSystemApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of FileSystemApiDto from a JSON string
file_system_api_dto_instance = FileSystemApiDto.from_json(json)
# print the JSON string representation of the object
print(FileSystemApiDto.to_json())

# convert the object into a dict
file_system_api_dto_dict = file_system_api_dto_instance.to_dict()
# create an instance of FileSystemApiDto from a dict
file_system_api_dto_from_dict = FileSystemApiDto.from_dict(file_system_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


