import ast
class VisitCall(ast.NodeVisitor):

    def visit_Call(self, node):
        functions = ['CreateModel', 'DeleteModel', 'RenameModel', 'AddField', 'RemoveField', 'AlterField', 'RenameField']
        func = node.func
        # Call(expr func, expr* args, keyword* keywords)
        if type(func) == ast.Attribute:
            # Attribute(expr value, identifier attr, expr_context ctx) attr is used for function name
            funcname = func.attr
            if funcname in functions:
                # args and keywords are used for args. keywords are more like hash 
                args = node.keywords
                print(funcname)
                for arg in args:
                    v = arg.value
                    if(type(arg.value) == ast.Str):
                        v = arg.value.s
                    # print("{} {}".format(arg.arg, v))
                    if arg.arg == "model_name":
                        print("{}: {}".format(arg.arg, arg.value.value))
                    if arg.arg == "name":
                        print("{}: {}".format(arg.arg, arg.value.value))
                    if arg.arg == "field":
                        lst = []
                        constraints = v.keywords 
                        for constraint in constraints:
                            if type(constraint.value.value) != ast.Name:
                                lst.append("{}: {}".format(constraint.arg, constraint.value.value))
                            else:
                                lst.append("{}: {}.{}".format(constraint.arg, constraint.value.value.id, constraint.value.attr))    
                        print("field type:", v.func.attr) 
                        print("field constraints:", lst)

                    if arg.arg == "fields":
                        fields = v.elts 
                        field_name = ""
                        for field in fields:
                            if type(field.elts[0]) == ast.Name:
                                field_name = field.elts[0].id
                            else:
                                field_name = field.elts[0].value
                            lst = []
                            constraints = field.elts[1].keywords 
                            for constraint in constraints:
                                if type(constraint.value.value) != ast.Name:
                                    lst.append("{} = {}".format(constraint.arg, constraint.value.value))
                                else:
                                    lst.append("{} = {}.{}".format(constraint.arg, constraint.value.value.id, constraint.value.attr))    
                            print("field name:", field_name)
                            print("field type:", field.elts[1].func.attr) 
                            print("field constraints:", lst)

                print("*"*30)

file = "test.py"
contents = open(file).read()
tree = ast.parse(contents)

vc = VisitCall()
vc.visit(tree)