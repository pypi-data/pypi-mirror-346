# ListIndexersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indexers** | [**Dict[str, IndexerDto]**](IndexerDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.list_indexers_response import ListIndexersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListIndexersResponse from a JSON string
list_indexers_response_instance = ListIndexersResponse.from_json(json)
# print the JSON string representation of the object
print(ListIndexersResponse.to_json())

# convert the object into a dict
list_indexers_response_dict = list_indexers_response_instance.to_dict()
# create an instance of ListIndexersResponse from a dict
list_indexers_response_from_dict = ListIndexersResponse.from_dict(list_indexers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


