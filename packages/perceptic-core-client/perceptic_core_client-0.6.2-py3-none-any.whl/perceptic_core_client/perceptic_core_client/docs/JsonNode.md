# JsonNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**empty** | **bool** |  | [optional] 
**value_node** | **bool** |  | [optional] 
**container_node** | **bool** |  | [optional] 
**missing_node** | **bool** |  | [optional] 
**array** | **bool** |  | [optional] 
**object** | **bool** |  | [optional] 
**node_type** | [**JsonNodeType**](JsonNodeType.md) |  | [optional] 
**pojo** | **bool** |  | [optional] 
**number** | **bool** |  | [optional] 
**integral_number** | **bool** |  | [optional] 
**floating_point_number** | **bool** |  | [optional] 
**short** | **bool** |  | [optional] 
**int** | **bool** |  | [optional] 
**long** | **bool** |  | [optional] 
**var_float** | **bool** |  | [optional] 
**double** | **bool** |  | [optional] 
**big_decimal** | **bool** |  | [optional] 
**big_integer** | **bool** |  | [optional] 
**textual** | **bool** |  | [optional] 
**boolean** | **bool** |  | [optional] 
**null** | **bool** |  | [optional] 
**binary** | **bool** |  | [optional] 

## Example

```python
from perceptic_core_client.models.json_node import JsonNode

# TODO update the JSON string below
json = "{}"
# create an instance of JsonNode from a JSON string
json_node_instance = JsonNode.from_json(json)
# print the JSON string representation of the object
print(JsonNode.to_json())

# convert the object into a dict
json_node_dict = json_node_instance.to_dict()
# create an instance of JsonNode from a dict
json_node_from_dict = JsonNode.from_dict(json_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


