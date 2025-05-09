# ListIndexingActionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actions** | [**List[IndexingActionDto]**](IndexingActionDto.md) |  | [optional] 
**total_actions** | **int** |  | [optional] 
**next_offset** | **int** |  | [optional] 
**pending_count** | **int** |  | [optional] 
**executing_count** | **int** |  | [optional] 
**succeeded_count** | **int** |  | [optional] 
**failed_count** | **int** |  | [optional] 
**index_count** | **int** |  | [optional] 
**delete_count** | **int** |  | [optional] 

## Example

```python
from perceptic_core_client.models.list_indexing_actions_response import ListIndexingActionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListIndexingActionsResponse from a JSON string
list_indexing_actions_response_instance = ListIndexingActionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListIndexingActionsResponse.to_json())

# convert the object into a dict
list_indexing_actions_response_dict = list_indexing_actions_response_instance.to_dict()
# create an instance of ListIndexingActionsResponse from a dict
list_indexing_actions_response_from_dict = ListIndexingActionsResponse.from_dict(list_indexing_actions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


