from promptulate.utils.string_template import StringTemplate


def test_f_string():
    data = "Test"
    prompt = """This is a {data}"""
    string_template = StringTemplate(prompt)
    resp = string_template.format(data=data)
    assert resp == "This is a Test"

    resp = string_template.format([data])
    assert resp == "This is a Test"


def test_jinja():
    data = "Test"
    prompt = """This is a {{data}} {fake} {'key':'value'}."""
    string_template = StringTemplate(prompt, template_format="jinja2")
    resp = string_template.format(data=data)
    assert resp == "This is a Test {fake} {'key':'value'}."

    resp = string_template.format([data])
    assert resp == "This is a Test {fake} {'key':'value'}."
