#JSON schema spec

`$alias_name` - response alias "alias_name". Points to the response body for the corresponding request.

`$$method` - special methods invoked on the response object. 

###Methods:
- `$$status_code` - Response code
- `$$values` - Used on the array object. Converts array of objects into array of values. 
For example `$alias.$$values.text`: 

        $alias response body:
        [
            {
                "id": 1,
                "text": "some text"
            },
            {
                "id": 2,
                "text": "another text"
            }
        ]
        
        evaluates into:
        [
            "some text",
            "another text"
        ]
        
####Requirements:

- array methods:
    - array of objects:
        - objects to values
        - concatenate object attribute into string
        - use attributes to make other calls (ex. answer ids >> call /answers/{ids})
        - index array by position
    - array of strings:
        - index
        - concatenate
    - arrays of integers:
        - to array of strings (by defining "type" as string???)
- special "alias" methods:
    - response code
    - response headers
    - response time?
- special "value" methods:
    - follow uri/url (optionally set as new alias?) - ex. `$$url.follow`/`$$uri.follow.new_alias`