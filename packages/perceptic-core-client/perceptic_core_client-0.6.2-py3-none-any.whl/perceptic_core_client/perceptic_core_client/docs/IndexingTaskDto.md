# IndexingTaskDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task_rid** | **str** |  | [optional] 
**indexer_rid** | **str** |  | [optional] 
**folder_uri** | **str** |  | [optional] 
**namespace** | **str** |  | [optional] 
**target_minimum_version** | **int** |  | [optional] 
**settings** | **Dict[str, object]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**status** | [**IndexingTaskStatus**](IndexingTaskStatus.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.indexing_task_dto import IndexingTaskDto

# TODO update the JSON string below
json = "{}"
# create an instance of IndexingTaskDto from a JSON string
indexing_task_dto_instance = IndexingTaskDto.from_json(json)
# print the JSON string representation of the object
print(IndexingTaskDto.to_json())

# convert the object into a dict
indexing_task_dto_dict = indexing_task_dto_instance.to_dict()
# create an instance of IndexingTaskDto from a dict
indexing_task_dto_from_dict = IndexingTaskDto.from_dict(indexing_task_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


