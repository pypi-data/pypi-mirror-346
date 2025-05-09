# WorkerMetadataDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**input_schema** | **object** |  | [optional] 
**response_schema** | **object** |  | [optional] 

## Example

```python
from perceptic_core_client.models.worker_metadata_dto import WorkerMetadataDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerMetadataDto from a JSON string
worker_metadata_dto_instance = WorkerMetadataDto.from_json(json)
# print the JSON string representation of the object
print(WorkerMetadataDto.to_json())

# convert the object into a dict
worker_metadata_dto_dict = worker_metadata_dto_instance.to_dict()
# create an instance of WorkerMetadataDto from a dict
worker_metadata_dto_from_dict = WorkerMetadataDto.from_dict(worker_metadata_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


