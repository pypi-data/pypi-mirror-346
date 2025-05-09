# ResourceIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_identifier** | **str** |  | [optional] 
**service_index** | **int** |  | [optional] 
**instance_index** | **int** |  | [optional] 
**type_index** | **int** |  | [optional] 
**service** | **str** |  | [optional] 
**instance** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**locator** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.resource_identifier import ResourceIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceIdentifier from a JSON string
resource_identifier_instance = ResourceIdentifier.from_json(json)
# print the JSON string representation of the object
print(ResourceIdentifier.to_json())

# convert the object into a dict
resource_identifier_dict = resource_identifier_instance.to_dict()
# create an instance of ResourceIdentifier from a dict
resource_identifier_from_dict = ResourceIdentifier.from_dict(resource_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


