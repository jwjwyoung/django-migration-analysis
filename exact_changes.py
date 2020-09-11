# File is used to find the exact number of times tables and columns were added, renamed, deleted, and altered.

import random
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
            if funcname in ["AlterField", "AddField"]:
                if funcname == "AlterField":
                    print("AlterField", file=f)
                else:
                    print("AddField", file=f)
                model_name = node.keywords[0].value.value.lower()
                c_name = node.keywords[1].value.value.lower()
                t = node.keywords[2].value.func
                if type(t) == ast.Name:
                    print("model name {}".format(model_name), file=f2)
                    print("{} {}".format(model_name, c_name), file=f2)
                    print(t.id, file=f2)
                else:
                    print("model name {}".format(model_name), file=f2)
                    print("{} {}".format(model_name, c_name), file=f2)
                    print(t.attr, file=f2)
            elif funcname == "CreateModel":
                print(funcname, file=f)
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
                            print("model name {}".format(model_name), file=f2)
                            print("{} {}".format(model_name, field_name), file=f2)
                            print(field.elts[1].func.attr, file=f2)
            elif funcname in ["RemoveField", "RenameField"]:
                if node.keywords:
                    model_name = node.keywords[0].value.value.lower()
                    c_name = node.keywords[1].value.value.lower()
                    print(funcname, file=f)
                    print("{} {}".format(model_name, c_name), file=f)
            elif funcname in ["DeleteModel", "RenameModel"]:
                print(funcname, file=f)
                if node.keywords:
                    print(node.keywords[0].value.value.lower(), file=f)
            else:
                print(funcname, file=f)
        f.close()
        f2.close()

# Getting migration files

"""m = []
path = "/Users/sophiexie/Downloads/code/dsp/posthog/posthog/migrations"
for file in os.listdir(path):
    if file[0] == "0":
        m.append(os.path.join(path,file))

m.sort()
for i in m:
    contents = open(i).read()
    tree = ast.parse(contents)
    vc = VisitCall()
    vc.visit(tree)"""

path = "/Users/sophiexie/Downloads/code/dsp/zulip"
for f in os.listdir(path):
    f_path = os.path.join(path, f)
    if os.path.isdir(f_path):
        for f2 in os.listdir(f_path):
            if f2 == "migrations":
                f2_path = os.path.join(f_path, f2)
                for f3 in os.listdir(f2_path):
                    if f3[0] == "0":
                        f4 = open("output.txt", "a")
                        print(f3+" "+f, file=f4)
                        f4.close()
                        contents = open(os.path.join(f2_path,f3)).read()
                        tree = ast.parse(contents)
                        vc = VisitCall()
                        vc.visit(tree)

f = open("output.txt", "r")
c0 = 0
c1 = 0
c2 = 0
c3 = 0
c4 = 0
c5 = 0
c6 = 0
c7 = 0

for x in f:
    if "CreateModel" in x:
        c0+=1
    elif "DeleteModel" in x:
        c2+=1
    elif "RenameModel" in x:
        c3+=1
    elif "AddField" in x:
        c4+=1
    elif "AlterField" in x or "AddConstraint" in x or "RemoveConstraint" in x:
        c5+=1
    elif "RemoveField" in x:
        c6+=1
    elif "RenameField" in x:
        c7+=1

print("create table", c0)
print("change table", c4+c5+c6+c7)
print("delete table", c2)
print("rename table", c3)
print("add column", c4)
print("alter field", c5)
print("delete column", c6)
print("rename column", c7)

# Getting specific migration files that had RenameField instances
"""lst = []
for x in f:
    lst.append(x[:-1])

removed = []
for i in range(len(lst)):
    line = lst[i]
    if line[0] == "0":
        j=i+1
        n_line = lst[j]
        while n_line[0] != "0" and j < len(lst):
            n_line = lst[j]
            if n_line == "RenameField":
                removed.append(line+" "+lst[j+1])
            j+=1

rand_lst = []

i=0
while i < 11 and i < len(removed):
    rand = random.randint(0, len(removed)-1)
    if rand not in rand_lst:
        print(removed[rand])
        i+=1
    rand_lst.append(rand)

for i in removed:
    print(i)"""

# Clear files
file = open("output.txt","r+")
file. truncate(0)
file.close()

file = open("output2.txt","r+")
file. truncate(0)
file.close()