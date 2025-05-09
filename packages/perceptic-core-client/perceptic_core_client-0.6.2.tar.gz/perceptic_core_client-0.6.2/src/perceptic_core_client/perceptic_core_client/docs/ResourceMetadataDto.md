# ResourceMetadataDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**files_system_rid** | **str** |  | [optional] 
**resource_id** | **str** |  | [optional] 
**uri** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | [**ResourceTypeDto**](ResourceTypeDto.md) |  | [optional] 
**path** | **str** |  | [optional] 
**extension** | **str** |  | [optional] 
**size_in_bytes** | **int** |  | [optional] 
**last_modified** | **datetime** |  | [optional] 
**etag** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.resource_metadata_dto import ResourceMetadataDto

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceMetadataDto from a JSON string
resource_metadata_dto_instance = ResourceMetadataDto.from_json(json)
# print the JSON string representation of the object
print(ResourceMetadataDto.to_json())

# convert the object into a dict
resource_metadata_dto_dict = resource_metadata_dto_instance.to_dict()
# create an instance of ResourceMetadataDto from a dict
resource_metadata_dto_from_dict = ResourceMetadataDto.from_dict(resource_metadata_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


