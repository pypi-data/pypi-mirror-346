# CreateFileSystemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_system_rid** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_file_system_response import CreateFileSystemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFileSystemResponse from a JSON string
create_file_system_response_instance = CreateFileSystemResponse.from_json(json)
# print the JSON string representation of the object
print(CreateFileSystemResponse.to_json())

# convert the object into a dict
create_file_system_response_dict = create_file_system_response_instance.to_dict()
# create an instance of CreateFileSystemResponse from a dict
create_file_system_response_from_dict = CreateFileSystemResponse.from_dict(create_file_system_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


