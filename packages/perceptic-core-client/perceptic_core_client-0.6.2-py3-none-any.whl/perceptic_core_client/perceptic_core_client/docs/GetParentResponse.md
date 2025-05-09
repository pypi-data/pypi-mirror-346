# GetParentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parent** | [**ResourceId**](ResourceId.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_parent_response import GetParentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetParentResponse from a JSON string
get_parent_response_instance = GetParentResponse.from_json(json)
# print the JSON string representation of the object
print(GetParentResponse.to_json())

# convert the object into a dict
get_parent_response_dict = get_parent_response_instance.to_dict()
# create an instance of GetParentResponse from a dict
get_parent_response_from_dict = GetParentResponse.from_dict(get_parent_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


