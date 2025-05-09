# ListFileSystemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resources** | [**Dict[str, ResourceMetadataDto]**](ResourceMetadataDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.list_file_system_response import ListFileSystemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListFileSystemResponse from a JSON string
list_file_system_response_instance = ListFileSystemResponse.from_json(json)
# print the JSON string representation of the object
print(ListFileSystemResponse.to_json())

# convert the object into a dict
list_file_system_response_dict = list_file_system_response_instance.to_dict()
# create an instance of ListFileSystemResponse from a dict
list_file_system_response_from_dict = ListFileSystemResponse.from_dict(list_file_system_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


