# GetIndexingTaskResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task** | [**IndexingTaskDto**](IndexingTaskDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_indexing_task_response import GetIndexingTaskResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetIndexingTaskResponse from a JSON string
get_indexing_task_response_instance = GetIndexingTaskResponse.from_json(json)
# print the JSON string representation of the object
print(GetIndexingTaskResponse.to_json())

# convert the object into a dict
get_indexing_task_response_dict = get_indexing_task_response_instance.to_dict()
# create an instance of GetIndexingTaskResponse from a dict
get_indexing_task_response_from_dict = GetIndexingTaskResponse.from_dict(get_indexing_task_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


