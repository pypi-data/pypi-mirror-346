# IndexingActionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action_type** | [**ActionType**](ActionType.md) |  | [optional] 
**target_uri** | **str** |  | [optional] 
**target_minimum_version** | **int** |  | [optional] 
**status** | [**IndexingActionStatus**](IndexingActionStatus.md) |  | [optional] 
**error_message** | **str** |  | [optional] 
**executed_at** | **datetime** |  | [optional] 
**reason** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.indexing_action_dto import IndexingActionDto

# TODO update the JSON string below
json = "{}"
# create an instance of IndexingActionDto from a JSON string
indexing_action_dto_instance = IndexingActionDto.from_json(json)
# print the JSON string representation of the object
print(IndexingActionDto.to_json())

# convert the object into a dict
indexing_action_dto_dict = indexing_action_dto_instance.to_dict()
# create an instance of IndexingActionDto from a dict
indexing_action_dto_from_dict = IndexingActionDto.from_dict(indexing_action_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


