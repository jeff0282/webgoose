from jinja2 import Environment, FileSystemLoader, pass_context

@pass_context
def test(context, value):
	print(context.parent)
	return(f"Modified: {value}")


env = Environment(loader=FileSystemLoader("."))
env.filters['test'] = test

test_str = """
this is some text

{{"modify this text" | test}}
"""

input = env.from_string(test_str)
print(input.render({'the': 1}))
