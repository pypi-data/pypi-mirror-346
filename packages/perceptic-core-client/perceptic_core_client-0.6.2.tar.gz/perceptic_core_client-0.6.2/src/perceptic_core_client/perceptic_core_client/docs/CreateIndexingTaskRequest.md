# CreateIndexingTaskRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indexer_rid** | **str** |  | [optional] 
**folder_uri** | **str** |  | [optional] 
**namespace** | **str** |  | [optional] 
**target_minimum_version** | **int** |  | [optional] 
**settings** | **Dict[str, object]** |  | [optional] 

## Example

```python
from perceptic_core_client.models.create_indexing_task_request import CreateIndexingTaskRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIndexingTaskRequest from a JSON string
create_indexing_task_request_instance = CreateIndexingTaskRequest.from_json(json)
# print the JSON string representation of the object
print(CreateIndexingTaskRequest.to_json())

# convert the object into a dict
create_indexing_task_request_dict = create_indexing_task_request_instance.to_dict()
# create an instance of CreateIndexingTaskRequest from a dict
create_indexing_task_request_from_dict = CreateIndexingTaskRequest.from_dict(create_indexing_task_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


