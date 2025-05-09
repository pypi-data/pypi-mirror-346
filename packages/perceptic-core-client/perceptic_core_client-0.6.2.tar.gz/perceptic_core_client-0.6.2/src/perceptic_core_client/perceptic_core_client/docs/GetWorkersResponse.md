# GetWorkersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**worker_identifiers** | **Dict[str, List[str]]** |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_workers_response import GetWorkersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkersResponse from a JSON string
get_workers_response_instance = GetWorkersResponse.from_json(json)
# print the JSON string representation of the object
print(GetWorkersResponse.to_json())

# convert the object into a dict
get_workers_response_dict = get_workers_response_instance.to_dict()
# create an instance of GetWorkersResponse from a dict
get_workers_response_from_dict = GetWorkersResponse.from_dict(get_workers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


