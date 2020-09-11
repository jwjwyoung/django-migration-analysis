import ast
class VisitCall(ast.NodeVisitor):

    def visit_Call(self, node):
        functions = ['CreateModel', 'DeleteModel', 'RenameModel', 'AddField', 'RemoveField', 'AlterField', 'RenameField']
        func = node.func
        print(ast.dump(node))
        # Call(expr func, expr* args, keyword* keywords)
        if type(func) == ast.Attribute:
            # Attribute(expr value, identifier attr, expr_context ctx) attr is used for function name
            funcname = func.attr
            if funcname in functions:
                #args and keywords are used for args. keywords are more like hash 
                args = node.keywords
                print("function name is {}".format(funcname))
                for arg in args:
                    v = arg.value
                    if(type(arg.value) == ast.Str):
                        v = arg.value.s
                    #print("{} {}".format(arg.arg, arg.value.value))
file = "test.py"
contents = open(file).read()
tree = ast.parse(contents)

vc = VisitCall()
vc.visit(tree)