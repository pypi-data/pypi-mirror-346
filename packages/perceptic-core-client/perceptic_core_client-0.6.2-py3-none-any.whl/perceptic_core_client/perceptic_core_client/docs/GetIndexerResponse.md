# GetIndexerResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indexer** | [**IndexerDto**](IndexerDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_indexer_response import GetIndexerResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetIndexerResponse from a JSON string
get_indexer_response_instance = GetIndexerResponse.from_json(json)
# print the JSON string representation of the object
print(GetIndexerResponse.to_json())

# convert the object into a dict
get_indexer_response_dict = get_indexer_response_instance.to_dict()
# create an instance of GetIndexerResponse from a dict
get_indexer_response_from_dict = GetIndexerResponse.from_dict(get_indexer_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


