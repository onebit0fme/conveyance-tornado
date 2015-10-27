# Conveyance API 0.1 Specification


## Introduction

Conveynace API specification is a project used to describe RESTful API definition to use as an API middleware
  by any tool that can process such specification.
  
## Specification

Current version describes only RESTful APIs that use JSON as input/output.

### Convey Payload Object

Convey Payload Object is a JSON object (file) that complies with the current specification.

### <a name="rootFields"></a>Root fields

Field Name | Type | Description
---|:---|:---
[definitions](#definitions) | `object` | Object is used to define any "variable" for later use
[resources](#resources) | `object` | Object is used to define any API url that can be used to retrieve data
[compose](#compose) | `object` | The final part that describes the final output.

#### <a name="definitions"></a>Definitions

This would be a place to define any value for later use.

Field Name | Type | Description
---|:---|:---
(Any latin alphanumeric symbol and `_`, can not start with a number) | `object` | Definition name. RegEx: `^(?=[^\d].)([a-zA-Z\d_]{1,255})$`
 
#### <a name="definitionFields"></a>Definition Fields
 
 Field Name | Type | Description
 ---|:---|:---
 value | any | Definition value
 schema | `object` | JSON schema Draft 3,4 used for value validation. Optional
 default | any | Default value used in case `value` evaluates to `null`. Optional. Default to `null`
 verbatim | `boolean` | If set to `true` the value object will be defined as is (syntax strings will not be processed). Optional. Defaults to `false`.

Basic example:

```js
{
    "post_id": {
        "value": 1
    },
    "author_name": {
        "value": "John"
    }
}
```

All definitions can be reused in any part of the Payload Object. The syntax to reuse definition is to prepend 
`$` at the beginning of the string, followed by the definition's name (ex. `$post_id`). Also note that definition reference can be
nested inside object or array, on any level.

Additionally, any reference any be used to insert value inside a string, for example `/path/to/{$resource_id}`.
Following types can be inserted: `string`, `integer`, `number`, `boolean`, `null`. Note, that type describes
the final value type. One more example: `My name is {@user.$resp.username}`

```js
{
    "post_id": {
        "value": 1,
        "schema": {
            "type": "integer"
        }
    },
    "post": {
        "value": {
            "id": "$post_id",
            "name": "First Post"
        }
    }
}
```

Please note that while this specification claims that the reference to the definition can be used in any part of the
Payload Object, please use your own judgement to avoid self-referenced and other impossible reference combinations.

#### <a name="resources"></a> Resources

Resources object describes the url that has to be used in order to retrieve data for later usage.


Field Name | Type | Description
---|:---|:---
(Any latin alphanumeric symbol and `_`, can not start with a number) | `object` | Resource name. RegEx: `^(?=[^\d].)([a-zA-Z\d_]{1,255})$`
 
 
Same as definitions, resources can be reused in any part of the Payload Object. The syntax to reuse resource is to prepend 
`@` at the beginning of the string, followed by the definition's name (ex. `@comments`).
Resource reference works the same way as definition reference. In addition, resource has a special attribute `$resp`, used to
access response object.

Please note that this specification does not describe how to retrieve the response object, however resource `$resp`
attribute should be able to access the response JSON object regardless of the implementation. For further description,
see [Response Object](#responseObject)
 
 
#### <a name="resourceObject"></a> Resource Object

 Field Name | Type | Required | Description
 ---|:---|:---|:---
 [url](#resourceUrlObject) | `object` or `string` | Yes | Resource url parameters used to parse a valid url. Note that if `string` type is not used to define url directly (INVALID: "http://example.com/posts"). Instead, `string` type is used only to reference another resource url (ex. `@name.url`)
 method | `string` | Yes | Method that is used. Supported: GET, POST, PUT, PATCH, DELETE
 parameters | `object` or `string` | No | Url parameters that should be used when making a call. Note, `string` is used to reference another defined resource.
 headers | `object` or `string` | No | Headers that need to be set when making a call. `string` is used when referencing another defined resource.
 body | any | No | Body of the request that needs to be passed along.
 
#### <a name="resourceUrlObject"></a> Resource Url Object

 Field Name | Type | Required | Description
 ---|:---|:---|:---
 protocol | `string` | Yes | HTTP protocol ("HTTP" or "HTTPS")
 hostname | `string` | Yes | Hostname (ex. "api.example.com")
 path | `string` | No | Url path (ex. "/posts/1")
 port | `integer` | No | In case IP is used as hostname

#### <a name="compose"></a> Compose Object

Compose object describes the shape of the output data and takes into consideration all definitions and resources,
as well as resource responses.

Field Name | Type | Description
---|:---|:---
[body](#composeBody) | `object` | Body object.

#### <a name="composeBody"></a> Compose Body Object

Field Name | Type | Description
---|:---|:---
value | any | Output data.
schema | `object` | JSON schema Draft 3,4 used to validate the output
 
Example:

```js
{
    "body": {
        "value": {
            "POST": "$post",
            "COMMENTS": "@comments.$resp"
        },
        "schema": {
            "type": "object",
            "properties": {
                "POST": {
                    "type": "object",
                },
                "COMMENTS": {
                    "type": "array"
                }
            },
            "additionalProperties": false
        }
    }
}
```
 
### Implementation
 
#### <a name="responseObject"></a> Response Object
 
Response object is an object that describes the http response of the RESTful API.
 
currently under construction...

### Example

```js
{
    "compose": {
        "body": {
            "type": "object",
            "value": {
                "POST": "$post",
                "COMMENTS": "$comments"
            }
        }
    },
    "resources": {
        "post": {
            "url": {
                "protocol": "http",
                "hostname": "jsonplaceholder.typicode.com",
                "path": "/posts/1"
            },
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        },
        "comments": {
            "url": {
                "hostname": "@post.url.hostname",
                "protocol": "@post.url.protocol",
                "path": "/posts/1/comments"
            },
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        }
    },
    "definitions": {
        "post": {
            "value": "@post.$resp"
        },
        "comments": {
            "value": "@comments.$resp"
        }
    }
}
```