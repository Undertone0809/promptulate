OUTPUT_FORMAT = """## Output format
The output should be formatted as a JSON instance that conforms to the JSON schema below. JSON only, no explanation.

As an example, for the schema {{"properties": {{"foo": {{"description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```
{schema}
```"""  # noqa: E501
