# CreateManagedFileSystemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_managed_file_system_request import CreateManagedFileSystemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateManagedFileSystemRequest from a JSON string
create_managed_file_system_request_instance = CreateManagedFileSystemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateManagedFileSystemRequest.to_json())

# convert the object into a dict
create_managed_file_system_request_dict = create_managed_file_system_request_instance.to_dict()
# create an instance of CreateManagedFileSystemRequest from a dict
create_managed_file_system_request_from_dict = CreateManagedFileSystemRequest.from_dict(create_managed_file_system_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


