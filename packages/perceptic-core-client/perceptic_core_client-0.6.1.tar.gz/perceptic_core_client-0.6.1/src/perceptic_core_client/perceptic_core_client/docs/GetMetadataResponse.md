# GetMetadataResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**ResourceMetadataDto**](ResourceMetadataDto.md) |  | [optional] 

## Example

```python
from perceptic_core_client.models.get_metadata_response import GetMetadataResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetMetadataResponse from a JSON string
get_metadata_response_instance = GetMetadataResponse.from_json(json)
# print the JSON string representation of the object
print(GetMetadataResponse.to_json())

# convert the object into a dict
get_metadata_response_dict = get_metadata_response_instance.to_dict()
# create an instance of GetMetadataResponse from a dict
get_metadata_response_from_dict = GetMetadataResponse.from_dict(get_metadata_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


