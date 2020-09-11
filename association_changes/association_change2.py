# Same thing as other association change file but it includes migration files that the association relationships were deleted in.

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
            if funcname == 'DeleteModel':
                print("delete model", file=f)
                print(node.keywords[0].value.value.lower(), file=f)
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
                    print('add field', file=f)
                    c_name = node.keywords[1].value.value.lower()
                    t = node.keywords[2].value.func
                    if type(t) == ast.Name:
                        print("{} {}".format(model_name, c_name), file=f)
                        print(t.id, file=f)
                    else:
                        print("{} {}".format(model_name, c_name), file=f)
                        print(t.attr, file=f)
                else:
                    print('remove field', file=f)
                    c_name = node.keywords[1].value.value.lower()
                    print("{} {}".format(model_name, c_name), file=f)
            if funcname == 'AlterField':
                model_name = node.keywords[0].value.value.lower()
                c_name = node.keywords[1].value.value.lower()
                t = node.keywords[2].value.func
                print("alter field", file=f)
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
path = "/Users/sophiexie/Downloads/code/dsp/onlinejudge/contest/migrations"
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

# counting add and delete association columns
column_types = {}
a_fk = 0
d_fk = 0
dm_fk = 0
r_fk = 0
rm_fk = 0

for j in range(len(lst)):
    name = lst[j]
    if name[0] == "0":
        i = j+1
        while i < len(lst) and lst[i][0] != "0":
            line = lst[i]
            if line == "add field":
                if lst[i+1] in column_types:
                    if column_types[lst[i+1]][-1] != lst[i+2]:
                        if lst[i+2] == 'ForeignKey':
                            column_types[lst[i+1]].append(lst[i+2])
                        else:
                            column_types[lst[i+1]].append((lst[i+2], name))
                else:
                    column_types[lst[i+1]] = [lst[i+2]]
            elif line == "alter field":
                if lst[i+1] in column_types:
                    if column_types[lst[i+1]][-1] != lst[i+2]:
                        if lst[i+2] == 'ForeignKey':
                            column_types[lst[i+1]].append(lst[i+2])
                        else:
                            column_types[lst[i+1]].append((lst[i+2], name))
            elif line == "remove field":
                if lst[i+1] in column_types:
                    column_types[lst[i+1]].append((line, name))
            elif line == "delete model":
                d = False
                for column in column_types:
                    if lst[i+1]+" " in column and column[0:len(lst[i+1])] == lst[i+1]:
                        if column_types[column][-1] == "ForeignKey":
                            d = True
                        column_types[column].append((line, name))
                if d:
                    dm_fk+=1
            elif line == "rename field":
                if lst[i+1] in column_types:
                    if lst[i+2] in column_types:
                        if column_types[lst[i+2]][-1] == column_types[lst[i+1]][0]:
                            column_types[lst[i+2]] = column_types[lst[i+2]] + column_types[lst[i+1]][1:]
                        else:
                            column_types[lst[i+2]] = column_types[lst[i+2]] + column_types[lst[i+1]]
                    else:
                        column_types[lst[i+2]] = column_types[lst[i+1]]
                    del column_types[lst[i+1]]
                    if column_types[lst[i+2]][-1] == "ForeignKey":
                        r_fk+=1
            elif line == "rename model":
                r = False
                ct = []
                for column in column_types:
                    ct.append(column)
                for column in ct:
                    if lst[i+1] in column:
                        nc = lst[i+2]+column[len(lst[i+1]):]
                        if nc in column_types:
                            if nc[-1] != column_types[column][0]:
                                column_types[nc] = column_types[nc] + column_types[column][1:]
                            else:
                                column_types[nc] = column_types[nc] + column_types[column]
                        else:
                            column_types[nc] = column_types[column]
                        del column_types[column]
                        if column_types[nc][-1] == "ForeignKey":
                            r = True
                if r:
                    rm_fk+=1
            i+=1

"""for i in column_types:
    if len(column_types[i]) > 1:
        print(i,column_types[i])"""

# count add foreign key, delete foreign key, and rename foreign key
for i in column_types:
    types = column_types[i]
    for j in range(len(types)):
        t = types[j]
        if t == 'ForeignKey' and j == len(types) - 1:
            #print(i, types)
            a_fk+=1
        elif t == 'ForeignKey' and types[j+1] != 'ForeignKey':
            print(i, types)
            a_fk+=1
            d_fk+=1

print("-"*50)
print("add fk {} delete fk {} rename fk {}".format(a_fk, d_fk, r_fk))
print("delete model that had fk {} rename model that had fk {}".format(dm_fk, rm_fk))

file = open("output.txt","r+")
file. truncate(0)
file.close()