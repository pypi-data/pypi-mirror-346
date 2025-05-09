# IndexerDto

Indexer service details, including supported index version range and capabilities.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**indexer_rid** | **str** |  | [optional] 
**target_index_version** | **int** |  | [optional] 
**minimum_supported_index_version** | **int** |  | [optional] 

## Example

```python
from perceptic_core_client.models.indexer_dto import IndexerDto

# TODO update the JSON string below
json = "{}"
# create an instance of IndexerDto from a JSON string
indexer_dto_instance = IndexerDto.from_json(json)
# print the JSON string representation of the object
print(IndexerDto.to_json())

# convert the object into a dict
indexer_dto_dict = indexer_dto_instance.to_dict()
# create an instance of IndexerDto from a dict
indexer_dto_from_dict = IndexerDto.from_dict(indexer_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


