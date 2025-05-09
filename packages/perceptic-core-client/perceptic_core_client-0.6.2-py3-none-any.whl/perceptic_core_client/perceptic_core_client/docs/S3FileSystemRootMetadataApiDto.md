# S3FileSystemRootMetadataApiDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bucket_name** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from perceptic_core_client.models.s3_file_system_root_metadata_api_dto import S3FileSystemRootMetadataApiDto

# TODO update the JSON string below
json = "{}"
# create an instance of S3FileSystemRootMetadataApiDto from a JSON string
s3_file_system_root_metadata_api_dto_instance = S3FileSystemRootMetadataApiDto.from_json(json)
# print the JSON string representation of the object
print(S3FileSystemRootMetadataApiDto.to_json())

# convert the object into a dict
s3_file_system_root_metadata_api_dto_dict = s3_file_system_root_metadata_api_dto_instance.to_dict()
# create an instance of S3FileSystemRootMetadataApiDto from a dict
s3_file_system_root_metadata_api_dto_from_dict = S3FileSystemRootMetadataApiDto.from_dict(s3_file_system_root_metadata_api_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


