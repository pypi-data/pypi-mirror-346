# StartExecutionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task** | [**IndexingTaskDto**](IndexingTaskDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.start_execution_response import StartExecutionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StartExecutionResponse from a JSON string
start_execution_response_instance = StartExecutionResponse.from_json(json)
# print the JSON string representation of the object
print(StartExecutionResponse.to_json())

# convert the object into a dict
start_execution_response_dict = start_execution_response_instance.to_dict()
# create an instance of StartExecutionResponse from a dict
start_execution_response_from_dict = StartExecutionResponse.from_dict(start_execution_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


