# File is used to count indexes of application

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
            print(funcname, file=f)
        f.close()

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

m = []
path = "/Users/sophiexie/Downloads/code/dsp/awx/awx"
for f in os.listdir(path):
    f_path = os.path.join(path, f)
    if os.path.isdir(f_path):
        for f2 in os.listdir(f_path):
            if f2 == "migrations":
                f2_path = os.path.join(f_path, f2)
                for file in os.listdir(f2_path):
                    if file[0] == "0":
                        m.append((file, f2_path, f))
m.sort()

for i in m:
    f = open("output.txt", "a")
    print(i[0], i[2], file=f)
    f.close()
    contents = open(os.path.join(i[1],i[0])).read()
    tree = ast.parse(contents)
    vc = VisitCall()
    vc.visit(tree)

f = open("output.txt", "r")
lst = []
for x in f:
    lst.append(x[:-1])
migration_files = []
migration_files2 = []
for i in range(len(lst)):
    name = lst[i]
    if name[0] == "0":
        j = i+1
        while j < len(lst) and lst[j][0] != "0":
            #print(lst[j])
            if lst[j] == "AddIndex":
                migration_files.append(name)
            elif lst[j] == 'RemoveIndex':
                migration_files2.append(name)
            j+=1
migration_files.sort()
migration_files2.sort()

print("AddIndex")
for x in migration_files:
    print(x)

print("RemoveIndex")
for x in migration_files2:
    print(x)
f.close()


"""# Getting Results
f = open("output.txt", "r")
c0 = 0
c1 = 0

for x in f:
    if "AddIndex" in x:
        c0+=1
    elif "RemoveIndex" in x:
        c1+=1

print("add index", c0)
print("remove index", c1)

f.close()"""

file = open("output.txt","r+")
file. truncate(0)
file.close()