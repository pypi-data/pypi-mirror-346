# CreateRemoteFileSystemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_rid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**metadata** | [**FileSystemRootMetadataApiDto**](FileSystemRootMetadataApiDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_remote_file_system_request import CreateRemoteFileSystemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateRemoteFileSystemRequest from a JSON string
create_remote_file_system_request_instance = CreateRemoteFileSystemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateRemoteFileSystemRequest.to_json())

# convert the object into a dict
create_remote_file_system_request_dict = create_remote_file_system_request_instance.to_dict()
# create an instance of CreateRemoteFileSystemRequest from a dict
create_remote_file_system_request_from_dict = CreateRemoteFileSystemRequest.from_dict(create_remote_file_system_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


