# SchemaLocation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**root_document_uri** | **str** |  | [optional] 
**pointer_to_location** | **List[str]** |  | [optional] 

## Example

```python
from perceptic_core_client.models.schema_location import SchemaLocation

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaLocation from a JSON string
schema_location_instance = SchemaLocation.from_json(json)
# print the JSON string representation of the object
print(SchemaLocation.to_json())

# convert the object into a dict
schema_location_dict = schema_location_instance.to_dict()
# create an instance of SchemaLocation from a dict
schema_location_from_dict = SchemaLocation.from_dict(schema_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


