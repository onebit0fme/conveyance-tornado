import unittest
import jsonschema
from examples import PAYLOAD_GET_EXAMPLE
from spec import PAYLOAD_SCHEMA


class PayloadValidatorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validation(self):
        jsonschema.validate(PAYLOAD_GET_EXAMPLE, PAYLOAD_SCHEMA)

if __name__ == "__main__":
    unittest.main()
