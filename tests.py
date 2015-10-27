import unittest
import jsonschema
from examples import PAYLOAD_GET_EXAMPLE, PAYLOAD_GET_EXAMPLE_3
from spec import PAYLOAD_SCHEMA
from conveyance import Conveyance

PAYLOAD_1 = {
    "compose": {
        "body": {
            "type": "object",
            "value": {
                "example": {
                    "one": "$value2",
                    "two": "$another",
                    "three": "Just a string",
                    "four": 35
                }
            }
        }
    },
    "resources": {
        "post": {
            "url": {
                "protocol": "http",
                "hostname": "jsonplaceholder.typicode.com",
                "path": "/posts/{$post_id}"
            },
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        },
        "user": {
            "url": {
                "hostname": "@post.url.hostname",
                "protocol": "@post.url.protocol",
                "path": "/users/{@post.$resp.userId}"
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
            "value": 1
        },
        "value2": {
            "value": "/path/to/{$post_id}"
        },
        "another": {
            "value": "This is plain string with {this}"
        }
    }
}


RESPONSE_1 = {
  "example": {
    "two": "This is plain string with {this}",
    "four": 35,
    "one": "/path/to/1",
    "three": "Just a string"
  }
}


class PayloadValidatorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validation(self):
        jsonschema.validate(PAYLOAD_GET_EXAMPLE, PAYLOAD_SCHEMA)

    def test_payload_processing_example(self):
        # TODO: http_call() should not have been called (use mocks)
        conv = Conveyance(PAYLOAD_1)
        compose = conv.compose()(conv.definitions, conv.resources)

        self.assertEqual(compose, RESPONSE_1)

if __name__ == "__main__":
    unittest.main()
