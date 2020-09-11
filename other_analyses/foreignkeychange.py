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
                            if field.elts[1].func.attr == 'ForeignKey':
                                for c in field.elts[1].keywords:
                                    if c.arg == 'to':
                                        print("{} {}".format(model_name, field_name), file=f)
                                        t = c.value.value
                                        if type(t) == ast.Name:
                                            print(t.id+"."+c.value.attr, file=f)
                                        else:
                                            print(t, file=f)
            if funcname in ['AddField', 'AlterField']:
                model_name = node.keywords[0].value.value.lower()
                c_name = node.keywords[1].value.value.lower()
                for c in node.keywords[2].value.keywords:
                    if c.arg == 'to':
                        print("{} {}".format(model_name, c_name), file=f)
                        t = c.value.value
                        if type(t) == ast.Name:
                            if t.id == 'settings':
                                print(t.id+"."+c.value.attr, file=f)
                            else:
                                print(t.id, file=f)
                        else:
                            print(t, file=f)
        f.close()

# Getting migration files
m = []
path = "/Users/sophiexie/Downloads/code/dsp/onlinejudge/group/migrations"
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

# Getting results

f = open("output.txt", "r")
lst = []
for x in f:
    lst.append(x[:-1])

i=0
fks = {}
while i < len(lst) -1:
    name = lst[i]
    if name[0] == "0":
        j = i+1
        while j < len(lst) and lst[j][0] != "0":
            line = lst[j]
            if line in fks and fks[line][-1] != lst[j+1]:
                print(name)
                fks[line].append(lst[j+1])
            elif line not in fks:
                fks[line] = [lst[j+1]]
            j+=2
    i+=1        

count=0
for i in fks:
    if len(fks[i]) > 1:
        count+=1 
        print(i, fks[i])
print(count)

file = open("output.txt","r+")
file. truncate(0)
file.close()