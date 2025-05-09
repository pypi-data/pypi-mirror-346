# CreateIndexingTaskResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task_rid** | **str** |  | [optional] 
**task** | [**IndexingTaskDto**](IndexingTaskDto.md) |  | [optional] 
**created** | **bool** |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_indexing_task_response import CreateIndexingTaskResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIndexingTaskResponse from a JSON string
create_indexing_task_response_instance = CreateIndexingTaskResponse.from_json(json)
# print the JSON string representation of the object
print(CreateIndexingTaskResponse.to_json())

# convert the object into a dict
create_indexing_task_response_dict = create_indexing_task_response_instance.to_dict()
# create an instance of CreateIndexingTaskResponse from a dict
create_indexing_task_response_from_dict = CreateIndexingTaskResponse.from_dict(create_indexing_task_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


