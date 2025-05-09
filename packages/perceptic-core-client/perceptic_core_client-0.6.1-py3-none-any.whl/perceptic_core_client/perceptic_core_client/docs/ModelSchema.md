# ModelSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**schema_location** | **str** |  | [optional] 
**location** | [**SchemaLocation**](SchemaLocation.md) |  | [optional] 
**default_value** | **object** |  | [optional] 
**nullable** | **bool** |  | [optional] 
**read_only** | **bool** |  | [optional] 
**write_only** | **bool** |  | [optional] 
**unprocessed_properties** | **Dict[str, object]** |  | [optional] 

## Example

```python
from perceptic_core_client.models.model_schema import ModelSchema

# TODO update the JSON string below
json = "{}"
# create an instance of ModelSchema from a JSON string
model_schema_instance = ModelSchema.from_json(json)
# print the JSON string representation of the object
print(ModelSchema.to_json())

# convert the object into a dict
model_schema_dict = model_schema_instance.to_dict()
# create an instance of ModelSchema from a dict
model_schema_from_dict = ModelSchema.from_dict(model_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


