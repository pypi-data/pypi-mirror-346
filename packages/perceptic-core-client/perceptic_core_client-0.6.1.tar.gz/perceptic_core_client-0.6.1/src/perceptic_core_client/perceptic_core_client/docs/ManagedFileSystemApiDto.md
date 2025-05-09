# ManagedFileSystemApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.managed_file_system_api_dto import ManagedFileSystemApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedFileSystemApiDto from a JSON string
managed_file_system_api_dto_instance = ManagedFileSystemApiDto.from_json(json)
# print the JSON string representation of the object
print(ManagedFileSystemApiDto.to_json())

# convert the object into a dict
managed_file_system_api_dto_dict = managed_file_system_api_dto_instance.to_dict()
# create an instance of ManagedFileSystemApiDto from a dict
managed_file_system_api_dto_from_dict = ManagedFileSystemApiDto.from_dict(managed_file_system_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


