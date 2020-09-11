import ast
import os, sys
class VisitCall(ast.NodeVisitor):

    def visit_Call(self, node):
        f = open("output.txt", "a")
        functions = ['CreateModel', 'DeleteModel', 'RenameModel', 'AddField', 'RemoveField', 'AlterField', 'RenameField']
        func = node.func
        # Call(expr func, expr* args, keyword* keywords)
        if type(func) == ast.Attribute:
            # Attribute(expr value, identifier attr, expr_context ctx) attr is used for function name
            funcname = func.attr
            if funcname in functions:
                #args and keywords are used for args. keywords are more like hash 
                args = node.keywords
                for arg in args:
                    v = arg.value
                    if(type(arg.value) == ast.Str):
                        v = arg.value.s
                    if arg.arg == "field":
                        constraints = v.keywords
                        for constraint in constraints:
                            if constraint.arg == "on_delete":
                                print("on_delete", file=f) 
                    
                    if arg.arg == "fields":
                        columns = v.elts 
                        for column in columns:
                            constraints = column.elts[1].keywords
                            for constraint in constraints:
                                if constraint.arg == "on_delete":
                                    print("on_delete", file=f) 
        f.close()




"""file = "test.py"
contents = open(file).read()
tree = ast.parse(contents)

vc = VisitCall()
vc.visit(tree)"""

path = "/Users/sophiexie/Downloads/code/dsp/zulip/zilencer/migrations"
for file in os.listdir(path):
    if file[0] == "0":
        contents = open(os.path.join(path,file)).read()
        tree = ast.parse(contents)
        vc = VisitCall()
        vc.visit(tree)

f = open("output.txt", "r")
count = 0
for x in f:
    if "on_delete" in x:
        count+=1
f.close()
print(count)
file = open("output.txt","r+")
file. truncate(0)
file.close()

"""c_total = 0
t_changed = 0
t_total = 0

type_changes = 0

column_type_changed = {}
sc_changed = {}
st_changed = {}

c = 0
change = 0
discovered = []
while c < len(lst):
    line = lst[c]

    # Parsing 
    if line in ["rename model", "rename field"]:
        c+=2
    if line == "delete model":
        c+=1
    if line not in discovered and line not in ["rename model", "rename field", "delete model"]:
        j = c+1
        while j < len(lst):
            n_line = lst[j]
            if n_line == "rename model":
                if lst[j+1] == line:
                    line = lst[j+2]
                    change+=1
                    if j == c+1:
                        i-=1
                    del lst[j+1]
                elif lst[j+1][11:] == line[:len(lst[j+1][11:])]:
                    line = lst[j+2][11:] + line[len(lst[j+1][11:]):]
                j+=2
            if n_line == "rename field":
                if lst[j+1] == line:
                    #print(line)
                    old_line.append(line)
                    line = lst[j+2]
                    change+=1
                j+=2
            """if n_line == "delete model":
                if lst[j+1] == line:
                    change+=1
                    j+=1000000000000000000000000000"""
            if n_line == line:
                change+=1     
            j+=1
        for l in old_line:
            discovered.append(l)
        discovered.append(line)
        if "model name" in line and change > 0:
            t_changed+=1
            st_changed[line] = change
        if "model name" in line:
            t_total+=1
        elif "model name" not in line and change > 0:
            c_total+=1
            sc_changed[line] = change
        elif "model name" not in line and "rename model" not in line and "rename field" not in line:
            c_total+=1   
    change = 0
    c+=1"""