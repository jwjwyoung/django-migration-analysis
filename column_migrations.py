# File is used to find migration files of a specific column

import ast
import os, sys
class VisitCall(ast.NodeVisitor):

    def visit_Call(self, node):
        f = open("output.txt", "a")
        func = node.func
        # Call(expr func, expr* args, keyword* keywords)
        if type(func) == ast.Attribute:
            # Attribute(expr value, identifier attr, expr_context ctx) attr is used for function name
            funcname = func.attr
            args = node.keywords
            if funcname == 'CreateModel':
                print("create model", file=f)
                model_name = ""
                for arg in args:
                    v = arg.value
                    if(type(arg.value) == ast.Str):
                        v = arg.value.s
                    if arg.arg == "name":
                        print("model name {}".format((arg.value.value).lower()), file=f)
                        model_name = (arg.value.value).lower()
                    if arg.arg == "fields":
                        fields = v.elts 
                        field_name = ""
                        for field in fields:
                            if type(field.elts[0]) == ast.Name:
                                field_name = field.elts[0].id
                            else:
                                field_name = field.elts[0].value
                            print("{} {}".format(model_name, field_name), file=f)
            elif funcname in ['DeleteModel', 'RenameModel']:
                for arg in args:
                    if arg.arg == "model_name":
                        print("model name {}".format((arg.value.value).lower()), file=f)
            elif funcname in ['AddField', 'AlterField', 'RemoveField', 'AddConstraint', 'RemoveConstraint']:
                model_name = ""
                for arg in args:
                    if arg.arg == "model_name":
                        n = arg.value.value.lower()
                        print("model name {}".format(n), file=f)
                        model_name = (arg.value.value).lower()
                    if arg.arg == "name":
                        # print("{} {}".format(model_name, arg.value.value))
                        print("{} {}".format(model_name, arg.value.value), file=f)
            elif funcname == 'RenameField':
                if node.keywords != []:
                    model_name = node.keywords[0].value.value.lower()
                    print("model name {}".format(model_name), file=f)
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.keywords[1].value.value), file=f)
                    print("{} {}".format(model_name, node.keywords[2].value.value), file=f)
                else:
                    model_name = node.args[0].value.lower()
                    print("model name {}".format(model_name), file=f)
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.args[1].value), file=f)
                    print("{} {}".format(model_name, node.args[2].value), file=f)
        f.close()

# Getting migration files
m = []
path = "/Users/sophiexie/Downloads/code/dsp/saleor/saleor/order/migrations"
for file in os.listdir(path):
    if file[0] == "0":
        m.append(file)

m.sort()

for i in m:
    f = open("output.txt", "a")
    print(i, file=f)
    f.close()
    contents = open(os.path.join(path,i)).read()
    tree = ast.parse(contents)
    vc = VisitCall()
    vc.visit(tree)

f = open("output.txt", "r")
lst = []
for x in f:
    lst.append(x[:-1])
migration_files = []
for i in range(len(lst)):
    name = lst[i]
    if name[0] == "0":
        j = i+1
        while j < len(lst) and lst[j][0] != "0":
            if lst[j] == "payment customer_ip_address":
                migration_files.append(name)
            j+=1
migration_files.sort()
for x in migration_files:
    print(x)
f.close()

file = open("output.txt","r+")
file. truncate(0)
file.close()