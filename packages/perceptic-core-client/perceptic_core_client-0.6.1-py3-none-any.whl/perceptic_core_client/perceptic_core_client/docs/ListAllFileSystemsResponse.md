# ListAllFileSystemsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_systems** | [**Dict[str, FileSystemApiDto]**](FileSystemApiDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.list_all_file_systems_response import ListAllFileSystemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListAllFileSystemsResponse from a JSON string
list_all_file_systems_response_instance = ListAllFileSystemsResponse.from_json(json)
# print the JSON string representation of the object
print(ListAllFileSystemsResponse.to_json())

# convert the object into a dict
list_all_file_systems_response_dict = list_all_file_systems_response_instance.to_dict()
# create an instance of ListAllFileSystemsResponse from a dict
list_all_file_systems_response_from_dict = ListAllFileSystemsResponse.from_dict(list_all_file_systems_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


