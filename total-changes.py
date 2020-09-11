# This file is used to find the number of tables or columns that were changed out of the total number of tables or columns

import ast
import os, sys
class VisitCall(ast.NodeVisitor):

    def visit_Call(self, node):
        f = open("output.txt", "a")
        f2 = open("output2.txt", "a")
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
                        print("add model", file=f)
                        print("model name {}".format(model_name), file=f)
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
                            print("add field", file=f2)
                            print("{} {}".format(model_name, field_name), file=f2)
                            print(field.elts[1].func.attr, file=f2)
            if funcname == "RenameModel":
                print("rename model", file=f)
                print("rename model", file=f2)
                args = node.args
                if args != []:
                    print("model name {}".format(args[0].value.lower()), file=f)
                    print("model name {}".format(args[1].value.lower()), file=f)
                    print(args[0].value.lower(), file=f2)
                    print(args[1].value.lower(), file=f2)
                else:
                    args = node.keywords
                    print("model name {}".format(args[0].value.value.lower()), file=f)
                    print("model name {}".format(args[1].value.value.lower()), file=f)
                    print(args[0].value.value.lower(), file=f2)
                    print(args[1].value.value.lower(), file=f2)
            if funcname == 'DeleteModel':
                print("delete model", file=f)
                print("model name {}".format(node.keywords[0].value.value.lower()), file=f)
            if funcname in ['AddField', 'RemoveField']:
                model_name = node.keywords[0].value.value.lower()
                print("change model", file=f)
                print("model name {}". format(model_name), file=f)
                if funcname == 'AddField':
                    c_name = node.keywords[1].value.value.lower()
                    print("add field", file=f)
                    print("{} {}".format(model_name, c_name), file=f)
                    print('add field', file=f2)
                    t = node.keywords[2].value.func
                    if type(t) == ast.Name:
                        print("{} {}".format(model_name, c_name), file=f2)
                        print(t.id, file=f2)
                    else:
                        print("{} {}".format(model_name, c_name), file=f2)
                        print(t.attr, file=f2)
                else:
                    c_name = node.keywords[1].value.value.lower()
                    print('remove field', file=f)
                    print("{} {}".format(model_name, c_name), file=f)
                    print('remove field', file=f2)
                    print("{} {}".format(model_name, c_name), file=f2)
            if funcname == 'AlterField':
                print("alter field", file=f2)
                model_name = node.keywords[0].value.value.lower()
                c_name = node.keywords[1].value.value.lower()
                t = node.keywords[2].value.func
                if type(t) == ast.Name:
                    print("{} {}".format(model_name, c_name), file=f2)
                    print(t.id, file=f2)
                else:
                    print("{} {}".format(model_name, c_name), file=f2)
                    print(t.attr, file=f2)
            if funcname == 'RenameField':
                if node.keywords != []:
                    model_name = node.keywords[0].value.value.lower()
                    print("change model", file=f)
                    print("model name {}".format(model_name), file=f)
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.keywords[1].value.value), file=f)
                    print("{} {}".format(model_name, node.keywords[2].value.value), file=f)
                    print("rename field", file=f2)
                    print("{} {}".format(model_name, node.keywords[1].value.value), file=f2)
                    print("{} {}".format(model_name, node.keywords[2].value.value), file=f2)
                else:
                    model_name = node.args[0].value.lower()
                    print("change model", file=f)
                    print("model name {}".format(model_name), file=f)
                    print("rename field", file=f)
                    print("{} {}".format(model_name, node.args[1].value), file=f)
                    print("{} {}".format(model_name, node.args[2].value), file=f)
                    print("rename field", file=f2)
                    print("{} {}".format(model_name, node.args[1].value), file=f2)
                    print("{} {}".format(model_name, node.args[2].value), file=f2)
        f.close()
        f2.close()

# Getting migration files
m = []
path = "/Users/sophiexie/Downloads/code/dsp/saleor/saleor/account/migrations"
for file in os.listdir(path):
    if file[0] == "0":
        m.append(os.path.join(path,file))

m.sort()
for i in m:
    contents = open(i).read()
    tree = ast.parse(contents)
    vc = VisitCall()
    vc.visit(tree)

"""m = []
path = "/Users/sophiexie/Downloads/code/dsp/zulip"
for f in os.listdir(path):
    f_path = os.path.join(path, f)
    if os.path.isdir(f_path):
        for f2 in os.listdir(f_path):
            if f2 == "migrations":
                f2_path = os.path.join(f_path, f2)
                for f3 in os.listdir(f2_path):
                    if f3[0] == "0":
                        m.append(os.path.join(f2_path, f3))
m.sort()
for i in m:
    contents = open(i).read()
    tree = ast.parse(contents)
    vc = VisitCall()
    vc.visit(tree)"""

# Make list of file outputs
f = open("output.txt", "r")
lst = []
for x in f:
    lst.append(x[:-1])
f.close()

# Parse through list
tac = {}
for i in range(len(lst)):
    line = lst[i]
    if line in ["add model", "add field", "remove field", "delete model", "change model"]:
        n_line = lst[i+1]
        if n_line in tac:
            tac[n_line].append(line)
        else:
            tac[n_line] = [line]
    elif line == "rename field":
        n_line = lst[i+1]
        if n_line in tac:
            if lst[i+2] in tac:
                tac[lst[i+2]] = tac[lst[i+2]] + tac[n_line] + ["rename field"]
                del tac[n_line]
            else:
                tac[lst[i+2]] = tac[n_line] + ["rename field"]
                del tac[n_line]
    elif line == "rename model":
        n_line = lst[i+1]
        l_tac = []
        for toc in tac:
            l_tac.append(toc)
        for toc in l_tac:
            if n_line[11:]+" " in toc:
                nc = lst[i+2][11:]+toc[len(n_line[11:]):]
                if nc in tac:
                    tac[nc] = tac[nc] + tac[toc]
                    del tac[toc]
                else:
                    tac[nc] = tac[toc]
                    del tac[toc]
            elif n_line == toc:
                if lst[i+2] in tac:
                    tac[lst[i+2]] = tac[lst[i+2]] + tac[n_line] + ["rename model"]
                    del tac[n_line]
                else:
                    tac[lst[i+2]] = tac[n_line] + ["rename model"]
                    del tac[n_line]

# Type changes
f2 = open("output2.txt", "r")
lst = []
for x in f2:
    lst.append(x[:-1])
f2.close()

column_types = {}
for i in range(len(lst)):
    line = lst[i]
    if line == "add field":
        if lst[i+1] in column_types:
            if column_types[lst[i+1]][-1] != lst[i+2]:
                column_types[lst[i+1]].append(lst[i+2])
        else:
            column_types[lst[i+1]] = [lst[i+2]]
    elif line == "alter field":
        if lst[i+1] in column_types:
            if column_types[lst[i+1]][-1] != lst[i+2]:
                column_types[lst[i+1]].append(lst[i+2])
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
                else:
                    column_types[nc] = column_types[column]
                del column_types[column]
                
# Adding two dicts together
lst_tac = []
for i in tac:
    lst_tac.append(i)
lst_ct = []
for i in column_types:
    if len(column_types[i]) > 1:
        #print(column_types[i])
        lst_ct.append(i)

for i in lst_ct:
    tac[i]+=column_types[i][1:]

for i in lst_tac:
    if "model name" in i:
        for j in lst_ct:
            if i[11:]+" " in j:
                tac[i]+=column_types[j][1:]

# Number of type changes
type_change = 0
for i in column_types:
    type_change+=len(column_types[i][1:])

# Results
columns_changed = 0
columns_changed_gt1 = 0
columns_total = 0
tables_changed = 0
tables_total = 0

for i in tac:
    if "model name" in i:
        if len(tac[i]) > 1:
            tables_changed+=1
        tables_total+=1
    else:
        if len(tac[i]) > 2:
            columns_changed_gt1+=1
        if len(tac[i]) > 1:
            columns_changed+=1
        columns_total+=1

print(tables_changed, "/", tables_total)
print(columns_changed, "/", columns_total)
# number of columns changed more than once
print(columns_changed_gt1, "/", columns_total)
print("type changes", type_change)

# Clear files
file = open("output.txt","r+")
file. truncate(0)
file.close()

file = open("output2.txt","r+")
file. truncate(0)
file.close()