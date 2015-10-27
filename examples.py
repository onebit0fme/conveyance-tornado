

PAYLOAD_GET_EXAMPLE = {
    "compose": {
        "body": {
            "type": "object",
            "value": {
                "response_code": {
                    "type": "integer",
                    "value": "@question.$resp.$$status_code",
                },
                "answer_ids": {
                    "type": "array",
                    "value": "@answers",
                },
                "public": {
                    "type": "boolean",
                    "value": "@question.$resp.is_public",
                },
                "id": {
                    "type": "integer",
                    "value": "@question.$resp.id"
                }
            }
        }
    },
    "resources": {
        "post": {
            "url": {
                "protocol": "http",
                "hostname": "jsonplaceholder.typicode.com",
                # "path": "/posts/{$post_id}" # TODO: handle references inside strings
                "path": "/posts/1"
            },
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            },
        },
        "comments": {
            "url": {
                "hostname": "@post.url.hostname",
                "protocol": "@post.url.protocol",
                "path": "/comments"
            },
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            },
            "parameters": {
                "post_id": "$post_id"
            }
        }
    },
    "definitions": {
        "post_id": {
            # "type": 'integer',
            "value": 1,
            "schema": {
                "type": "integer"
            }
        },
        "text_obj": {
            # "type": 'object',
            "value": {
                "id": 1,
                "name": "Jeronimo"
            }
        },
        "how_to": {
            # "type": 'string',
            "value": '$this.$do.$$that',
            "verbatim": False,
            "default": "This is default value"
        },
        "test": {
            # "type": 'object',
            "value": '$text_obj.name',
            "schema": {
                "type": "string"
            }
        },
        "object": {
            "value": {
                "id": "$post_id",
                "name": "$how_to"
            },
            "schema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            }
        }
    }
}


PAYLOAD_GET_EXAMPLE_v2 = {
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
            },
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
            },
            "parameters": {
                "post_id": "$post_id"
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
