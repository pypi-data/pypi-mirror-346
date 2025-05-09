# PagedListFileSystemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ResourceEntryDto]**](ResourceEntryDto.md) |  | [optional] 
**next_token** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.paged_list_file_system_response import PagedListFileSystemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PagedListFileSystemResponse from a JSON string
paged_list_file_system_response_instance = PagedListFileSystemResponse.from_json(json)
# print the JSON string representation of the object
print(PagedListFileSystemResponse.to_json())

# convert the object into a dict
paged_list_file_system_response_dict = paged_list_file_system_response_instance.to_dict()
# create an instance of PagedListFileSystemResponse from a dict
paged_list_file_system_response_from_dict = PagedListFileSystemResponse.from_dict(paged_list_file_system_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


