# perceptic_core_client.UserResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_users_me_get**](UserResourceApi.md#api_v1_users_me_get) | **GET** /api/v1/users/me | Me


# **api_v1_users_me_get**
> MeResponse api_v1_users_me_get()

Me

### Example


```python
import perceptic_core_client
from perceptic_core_client.models.me_response import MeResponse
from perceptic_core_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = perceptic_core_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with perceptic_core_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = perceptic_core_client.UserResourceApi(api_client)

    try:
        # Me
        api_response = api_instance.api_v1_users_me_get()
        print("The response of UserResourceApi->api_v1_users_me_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserResourceApi->api_v1_users_me_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**MeResponse**](MeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

