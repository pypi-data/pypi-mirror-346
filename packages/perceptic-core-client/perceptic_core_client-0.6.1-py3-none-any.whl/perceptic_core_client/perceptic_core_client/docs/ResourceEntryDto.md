# ResourceEntryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | [optional] 
**metadata** | [**ResourceMetadataDto**](ResourceMetadataDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.resource_entry_dto import ResourceEntryDto

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceEntryDto from a JSON string
resource_entry_dto_instance = ResourceEntryDto.from_json(json)
# print the JSON string representation of the object
print(ResourceEntryDto.to_json())

# convert the object into a dict
resource_entry_dto_dict = resource_entry_dto_instance.to_dict()
# create an instance of ResourceEntryDto from a dict
resource_entry_dto_from_dict = ResourceEntryDto.from_dict(resource_entry_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


