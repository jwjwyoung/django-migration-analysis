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
            if funcname == 'CreateModel':
                args = node.keywords
                for arg in args:
                    v = arg.value
                    if(type(arg.value) == ast.Str):
                        v = arg.value.s
                    if arg.arg == "name":
                        model_name = (arg.value.value).lower()
                    if arg.arg == "fields":
                        fields = v.elts 
                        field_name = ""
                        for field in fields:
                            if type(field.elts[0]) == ast.Name:
                                field_name = field.elts[0].id
                            else:
                                field_name = field.elts[0].value
                            print("add field", file=f)
                            print("{} {}".format(model_name, field_name), file=f)
                            print(field.elts[1].func.attr, file=f)
            if funcname == "RenameModel":
                print("rename model", file=f)
                args = node.args
                if args != []:
                    print(args[0].value.lower(), file=f)
                    print(args[1].value.lower(), file=f)
                else:
                    args = node.keywords
                    print(args[0].value.value.lower(), file=f)
                    print(args[1].value.value.lower(), file=f)
            if funcname in ['AddField', 'RemoveField']:
                model_name = node.keywords[0].value.value.lower()
                if funcname == 'AddField':
                    c_name = node.keywords[1].value.value.lower()
                    print('add field', file=f)
                    t = node.keywords[2].value.func
                    if type(t) == ast.Name:
                        print("{} {}".format(model_name, c_name), file=f)
                        print(t.id, file=f)
                    else:
                        print("{} {}".format(model_name, c_name), file=f)
                        print(t.attr, file=f)
                else:
                    c_name = node.keywords[1].value.value.lower()
                    print('remove field', file=f)
                    print("{} {}".format(model_name, c_name), file=f)
            if funcname == 'AlterField':
                print("alter field", file=f)
                model_name = node.keywords[0].value.value.lower()
                c_name = node.keywords[1].value.value.lower()
                t = node.keywords[2].value.func
                if type(t) == ast.Name:
                    print("{} {}".format(model_name, c_name), file=f)
                    print(t.id, file=f)
                else:
                    print("{} {}".format(model_name, c_name), file=f)
                    print(t.attr, file=f)
            if funcname == 'RenameField':
                if node.keywords != []:
                    model_name = node.keywords[0].value.value.lower()
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.keywords[1].value.value), file=f)
                    print("{} {}".format(model_name, node.keywords[2].value.value), file=f)
                else:
                    model_name = node.args[0].value.lower()
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.args[1].value), file=f)
                    print("{} {}".format(model_name, node.args[2].value), file=f)
        f.close()

# Getting migration files
m = []
path = "/Users/sophiexie/Downloads/code/dsp/zulip/zerver/migrations"
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

# Type changes
f = open("output.txt", "r")
lst = []
for x in f:
    lst.append(x[:-1])
f.close()

column_types = {}

for j in range(len(lst)):
    name = lst[j]
    if name[0] == "0":
        i = j+1
        while i < len(lst) and lst[i][0] != "0":
            line = lst[i]
            if line == "add field":
                if lst[i+1] in column_types:
                    if column_types[lst[i+1]][-1] != lst[i+2]:
                        column_types[lst[i+1]].append(lst[i+2])
                        print("add field", lst[i+1], column_types[lst[i+1]], name[0:4])
                else:
                    column_types[lst[i+1]] = [lst[i+2]]
            elif line == "alter field":
                if lst[i+1] in column_types:
                    if column_types[lst[i+1]][-1] != lst[i+2]:
                        column_types[lst[i+1]].append(lst[i+2])
                        print("alter field", lst[i+1], column_types[lst[i+1]], name[0:4])
            elif line == "rename field":
                if lst[i+1] in column_types:
                    if lst[i+2] in column_types:
                        if column_types[lst[i+2]][-1] == column_types[lst[i+1]][0]:
                            column_types[lst[i+2]] = column_types[lst[i+2]] + column_types[lst[i+1]][1:]
                        else:
                            column_types[lst[i+2]] = column_types[lst[i+2]] + column_types[lst[i+1]]
                            print(lst[i+2], column_types[lst[i+2]], name[0:4])
                    else:
                        column_types[lst[i+2]] = column_types[lst[i+1]]
                    del column_types[lst[i+1]]
            elif line == "rename model":
                ct = []
                for column in column_types:
                    ct.append(column)
                for column in ct:
                    if lst[i+1] in column:
                        nc = lst[i+2]+column[len(lst[i+1]):]
                        if nc in column_types:
                            if nc[-1] == column_types[column][0]:
                                column_types[nc] = column_types[nc] + column_types[column][1:]
                            else:
                                column_types[nc] = column_types[nc] + column_types[column]
                                print(lst[nc], column_types[lst[nc]], name[0:4])
                        else:
                            column_types[nc] = column_types[column]
                        del column_types[column]
            i+=1

# Print type changes
count=0
for i in column_types:
    if len(column_types[i]) > 1:
        count+=(len(column_types[i])-1)
print("# of type changes = ", count)

# Clear files
file = open("output.txt","r+")
file. truncate(0)
file.close()
