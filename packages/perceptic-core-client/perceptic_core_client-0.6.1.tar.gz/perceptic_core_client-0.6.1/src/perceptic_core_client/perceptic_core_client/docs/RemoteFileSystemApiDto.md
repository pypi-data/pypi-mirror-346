# RemoteFileSystemApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**metadata** | [**FileSystemRootMetadataApiDto**](FileSystemRootMetadataApiDto.md) |  | [optional] 
**connection_rid** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.remote_file_system_api_dto import RemoteFileSystemApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of RemoteFileSystemApiDto from a JSON string
remote_file_system_api_dto_instance = RemoteFileSystemApiDto.from_json(json)
# print the JSON string representation of the object
print(RemoteFileSystemApiDto.to_json())

# convert the object into a dict
remote_file_system_api_dto_dict = remote_file_system_api_dto_instance.to_dict()
# create an instance of RemoteFileSystemApiDto from a dict
remote_file_system_api_dto_from_dict = RemoteFileSystemApiDto.from_dict(remote_file_system_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


