import json
import jsonschema
import requests
from spec import PAYLOAD_SCHEMA, PAYLOAD_SCHEMA_RESOURCE


class ValidationError(Exception):
    pass


# VALIDATORS


def value_schema_validator(obj, schema):
    try:
        jsonschema.validate(obj, schema)
    except jsonschema.ValidationError as e:
        raise ValidationError(e)

# MAIN


class ConveyString(str):

    def __iter__(self):
        s_list = self.split(".")
        for s in s_list:
            yield s

    def is_reference(self):
        return self.startswith("$") and not self.is_method()

    def is_resource(self):
        return self.startswith("@")

    def is_method(self):
        return self.startswith("$$")

    def has_method(self):
        return "$$" in self


class ConveyValue(object):

    def __init__(self):
        self.crums = []

    def __set__(self, instance, value):
        self.crums.append(value)

    def __get__(self, instance, owner):
        if self.crums:
            return self.crums[-1]
        return None

    def __delete__(self, instance):
        raise AttributeError("can not delete attribute")


class ConveyObject(object):
    value = ConveyValue()

    def __init__(self, convey_value, value_schema=None, default=None, verbatim=False, http_handler=None):
        self.convey_value = convey_value
        self.value_schema = value_schema
        self.verbatim = verbatim
        self.default = default

        self.http_handler = http_handler

        # self.value = ConveyValue()

    def __call__(self, defs, resources, *args, **kwargs):
        self.value = self._process(self.convey_value, defs, resources)
        self._validate_value()
        return self.value

    def _process(self, convey_value, defs, resources):
        if isinstance(convey_value, ConveyString):
            value = self._process_string(convey_value, defs, resources)
        elif isinstance(convey_value, list):
            value = self._process_array(convey_value)
        elif isinstance(convey_value, dict):
            value = self._process_obj(convey_value, defs, resources)
        elif isinstance(convey_value, (int, float)) or self.convey_value is None:
            value = convey_value
        else:
            raise ValidationError("Type {} is not supported".format(type(convey_value)))
        # self._validate_value()
        return value

    def _process_string(self, cs, defs, resources):
        if self.verbatim:
            return cs
        if cs.is_reference() and not self.verbatim:
            cs_list = [s for s in cs]
            convey_ref_obj = defs.get(cs_list[0][1:])
            if convey_ref_obj is None:
                return self.default   # TODO: either raise ValidationError or implement special type to set default behaviour to
            else:
                value = convey_ref_obj(defs, resources)
                for s in cs_list[1:]:
                    # val = getattr(val, s)
                    try:
                        value = value.get(s, self.default)   # TODO: same here
                    except AttributeError:
                        value = None
                        break
                return value
                # return self.value
        elif cs.is_resource():
            cs_list = [s for s in cs]
            convey_res_obj = resources.get(cs_list[0][1:])
            if convey_res_obj is None:
                return self.default
            else:
                value = convey_res_obj(defs, resources)
                for s in cs_list[1:]:
                    try:
                        if s == "$resp":
                            value = self.http_handler(self._parse_url(value))
                            continue
                        value = value.get(s, self.default)
                    except AttributeError:
                        value = None
                        break
                return value
        else:
            return cs

    def _parse_url(self, url_obj):
        protocol = url_obj.get('url', {}).get('protocol', 'http')
        hostname = url_obj.get('url', {}).get('hostname')
        path = url_obj.get('url', {}).get('path')
        # TODO: clean url parts
        return "{}://{}{}".format(protocol, hostname, path)

    def _validate_value(self):
        if self.value_schema is not None:
            value_schema_validator(self.value, self.value_schema)

    def _process_array(self, arr):
        return arr

    def _process_obj(self, obj, defs, resources):
        value = {}
        for k, v in obj.items():
            if isinstance(v, str):
                v = ConveyString(v)
            value[k] = self._process(v, defs, resources)
        return value

    def __new__(cls, convey_value, *args, **kwargs):
        # if isinstance(convey_value, ConveyString):
        #     if convey_value.is_reference():
        #         return ConveyReferenceObject(convey_value, *args, **kwargs)
        #     elif convey_value.is_resource():
        #         return ConveyResourceObject(convey_value, *args, **kwargs)
        # else:
        # return object.__new__(cls, convey_value, *args, **kwargs)
        obj = super(ConveyObject, cls).__new__(cls)
        return obj


class ConveyDefinitions(dict):

    def get_value(self, name, resources):
        c = self.get(name)
        if c:
            return c(self, resources)


class ConveyResources(ConveyDefinitions):

    def get_response(self, name, definitions):
        r = self.get(name)
        if r:
            return r(definitions, self)   # .http_call()


class Conveyance(object):

    class Meta:
        # define additional definitions here
        # will be used when handling the payload on predefined api request
        pass

    def __init__(self, payload, **kwargs):
        try:
            jsonschema.validate(payload, PAYLOAD_SCHEMA)
        except jsonschema.ValidationError as e:
            raise ValidationError("Payload is not valid:\n{}".format(e))
        self.payload = payload
        self.definitions = self._process_definitions()
        self.resources = self._process_resources()

    def _process_resources(self):
        res_load = self.payload.get('resources')
        if res_load is None or len(res_load) == 0:
            pass

        def consume_res(resource_load):
            # res_value = resource_load['value']
            res_schema = PAYLOAD_SCHEMA_RESOURCE

            value = self._process_value(resource_load, value_schema=res_schema)

            return value

        res = ConveyResources()
        for k, v in res_load.items():
            res[k] = consume_res(v)

        return res

    def _process_definitions(self):
        defs_load = self.payload.get('definitions')
        if defs_load is None or len(defs_load) == 0:
            # TODO: definitions required?
            pass

        # process definitions
        def consume_def(def_load):
            def_value = def_load['value']
            def_schema = def_load.get('schema')
            def_verbatim = def_load.get('verbatim')
            def_default = def_load.get('default')

            value = self._process_value(def_value, value_schema=def_schema, default=def_default, literal=def_verbatim)

            return value

        defs = ConveyDefinitions()
        for k, v in defs_load.items():
            defs[k] = consume_def(v)

        return defs

    def compose(self):
        compose_load = self.payload.get('compose')
        if compose_load is None or len(compose_load) == 0:
            pass

        compose_body = compose_load.get('body').get('value')
        # if compose_body:
        compose = self._process_value(compose_body)
        return compose

    def _process_value(self, the_value, value_schema=None, default=None, literal=False):
        if isinstance(the_value, (int, bool, float, dict, list)) or the_value is None:
            return ConveyObject(the_value, value_schema=value_schema, verbatim=literal, default=default, http_handler=self.http_call)
        if isinstance(the_value, str):
            the_value = ConveyString(the_value)
            return ConveyObject(the_value, value_schema=value_schema, verbatim=literal, default=default, http_handler=self.http_call)
        else:
            raise ValidationError("Type {} is not supported".format(type(the_value)))

    def http_call(self, url):
        r = requests.get(url)
        return r.json()


if __name__ == '__main__':

    from examples import PAYLOAD_GET_EXAMPLE, PAYLOAD_GET_EXAMPLE_v2
    # PAYLOAD_GET_EXAMPLE['compose']['foo'] = 'foo'
    conv = Conveyance(PAYLOAD_GET_EXAMPLE_v2)
    print(conv.definitions)
    # for k, v in conv.definitions.items():
    #     value = conv.definitions.get_value(k, conv.resources)
    #     print(k + ": " + repr(value))
    #
    # for k, v in conv.resources.items():
    #     value = conv.resources.get_response(k, conv.definitions)
    #     print(k + ": " + repr(value))

    from pprint import pprint
    pprint(conv.compose()(conv.definitions, conv.resources))
