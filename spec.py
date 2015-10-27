
SCHEMA_REGEX = {
    'var_name': '^(?=[^\d].)([a-zA-Z\d_]{1,255})$',
    'resource_reference': '^(@[a-zA-Z\d_\$\/\.]+)$'
}

PAYLOAD_SCHEMA_RESOURCE = {
    "type": "object",
    "properties": {
        "url": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "protocol": {
                            "oneOf": [
                                {
                                    "enum": ["http", "https"]
                                },
                                {
                                    "type": "string",
                                    "pattern": SCHEMA_REGEX['resource_reference']
                                }
                            ]
                        },
                        "hostname": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    # "format": "hostname"
                                },
                                # {
                                #     "type": "string",
                                #     "pattern": SCHEMA_REGEX['resource_reference']
                                # }
                            ]
                        },
                        "port": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    "pattern": "^(\d+)$"
                                },
                                {
                                    "type": "string",
                                    "pattern": SCHEMA_REGEX['resource_reference']
                                }
                            ]
                        },
                        "path": {
                            "type": "string"
                        }
                    },
                    "required": ["protocol", "hostname"],
                    "additionalProperties": False
                },
                {
                    "type": "string",
                    "pattern": SCHEMA_REGEX['resource_reference']
                }
            ]
        },
        "method": {
            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]
        },
        "parameters": {
            "oneOf": [
                {
                    "type": "object"
                },
                {
                    "type": "string",
                    "pattern": SCHEMA_REGEX['resource_reference']
                }
            ]
        },
        "headers": {
            "oneOf": [
                {
                    "type": "object"
                },
                {
                    "type": "string",
                    "pattern": SCHEMA_REGEX['resource_reference']
                }
            ]
        },
        "body": {}
    },
    "required": ["url", "method"],
    "additionalProperties": False
}

PAYLOAD_SCHEMA = {
    "type": "object",
    "properties": {
        "compose": {
            "type": "object",
            "properties": {
                "body": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                        }
                    },
                    "required": [
                        "type"
                    ]
                },
                "value": {}
            },
            "required": [
                "body"
            ],
            "additionalProperties": False
        },
        "resources": {
            "type": "object",
            "patternProperties": {
                SCHEMA_REGEX['var_name']: {
                    "type": "object",
                    "properties": {
                        "url": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "protocol": {
                                            "oneOf": [
                                                {
                                                    "enum": ["http", "https"]
                                                },
                                                {
                                                    "type": "string",
                                                    "pattern": SCHEMA_REGEX['resource_reference']
                                                }
                                            ]
                                        },
                                        "hostname": {
                                            "oneOf": [
                                                {
                                                    "type": "string",
                                                    # "format": "hostname"
                                                },
                                                # {
                                                #     "type": "string",
                                                #     "pattern": SCHEMA_REGEX['resource_reference']
                                                # }
                                            ]
                                        },
                                        "port": {
                                            "oneOf": [
                                                {
                                                    "type": "string",
                                                    "pattern": "^(\d+)$"
                                                },
                                                {
                                                    "type": "string",
                                                    "pattern": SCHEMA_REGEX['resource_reference']
                                                }
                                            ]
                                        },
                                        "path": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["protocol", "hostname"],
                                    "additionalProperties": False
                                },
                                {
                                    "type": "string",
                                    "pattern": SCHEMA_REGEX['resource_reference']
                                }
                            ]
                        },
                        "method": {
                            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                        },
                        "parameters": {
                            "oneOf": [
                                {
                                    "type": "object"
                                },
                                {
                                    "type": "string",
                                    "pattern": SCHEMA_REGEX['resource_reference']
                                }
                            ]
                        },
                        "headers": {
                            "oneOf": [
                                {
                                    "type": "object"
                                },
                                {
                                    "type": "string",
                                    "pattern": SCHEMA_REGEX['resource_reference']
                                }
                            ]
                        },
                        "body": {}
                    },
                    "required": ["url", "method"],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        },
        "definitions": {
            "type": "object",
            "patternProperties": {
                SCHEMA_REGEX['var_name']: {
                    "type": "object",
                    "properties": {
                        # "type": {
                        #     "enum": ["number", "integer", "string", "boolean", "object", "array", "null", "eval"]
                        # },
                        "schema": {},
                        "value": {},
                        "default": {},
                        "verbatim": {
                            "type": "boolean"
                        }
                    },
                    "required": ["value"],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    }
}
