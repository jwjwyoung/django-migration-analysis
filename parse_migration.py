import ast

file = "test.py"
contents = open(file).read()
tree = ast.parse(contents)

body = tree.body

print(body)
# the last is a class def type get it
class_definition = body[-1]

# print class_definition
class_body = class_definition.body
print(class_definition.body)

assign2 = class_body[-1]

value = assign2.value

# the assignment stmt has targets and value, which can be mapped as `targets = value`
for item in value.elts:
    print(item.func.attr) # get the function name, which could be createModel, addField, etc.
    for keyword in item.keywords:
        print("{} {}".format(keyword.arg, keyword.value))
