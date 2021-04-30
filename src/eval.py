from src.parse import *
from src.lex import *
import re

functionProlouge = [
  "\tpushl %ebp\n",
  "\tmovl %esp, %ebp\n"
]

breaker = []

functionEpilouge = [
  "\tmovl %ebp, %esp\n",
  "\tpopl %ebp\n",
  "\tret\n"
]

funcleaves = {

}

funcnums = {
  
}

funcs = {
  "_start":["call main", "movl %eax, %ebx", "movl $1, %eax", "int $0x80"],
}

currentFunc = None
vvalue = False

tmpid = ""
valueStack = []
ints = []
varias = {
  
}

data = {
  
}

data["clearBuffer"] = ".asciz \"[semble] clearing output buffer. IF you see this message, you're program has encountered an error in the stdout buffer\\n\""

globalss = {

}

strings = {
  
}

splaces = 4

structbeenptrs = {
  
}

funcargs = {}
bss = [
]

constglobals = [

]

fstructs = {

}

def Reverse(lst):
    return [ele for ele in reversed(lst)]

def checkStructDef(s):
  return s.split(".")

def getstype(variz):
  for i in structs:
    if variz == structs[i]:
      return i

class Struct:
  def __init__(self, name, variz, starting, rev=False):
    self.name = name
    self.variz = variz
    self.stype = getstype(self.variz)
    #print(self.variz)
    '''if rev:
      #print("eho")
      v = self.variz[1:]
      self.variz = Reverse(self.variz)
      self.variz = [self.variz[0]] + [self.variz[1]] + self.variz[2:]
      print(self.variz)'''
    self.starting = starting
  def getvalue(self, s):
    if s in self.variz:
      return str(self.variz.index(s) * 4) + "(" + self.starting + ")"
    else:
      return False

n = 0
nextAdd = 0

def asm(s):
  funcs[currentFunc].append(s)
  
def divver(x, y):
  x = int(x)
  y = int(y)
  z = 0
  while True:
    if x >= y:
      x -= y
      z += 1
    else:
      break
  return z
    

def getPrefix(v):
  v = str(v)
  if v[0] == "-" and v[-1] == ")":
    return ''
  elif re.match(r"[0-9]+$", v):
    return '$'
  else:
    return '%'

def mov(s, v):
  asm("movl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def add(s, v):
  asm("addl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def cmp(s, v):
  asm("cmpl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def sub(s, v):
  asm("subl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def mul(s, v):
  asm("imull " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def push(s):
  asm("pushl " + getPrefix(s) + str(s))

def pop(s):
  asm("popl " + getPrefix(s) + str(s))

structs = {}

def rndz(i):
  i = i - 1
  if i < 0:
    return 0
  else:
    return i

def div(s, v):
  asm("xorl %edx, %edx")
  mov(s, "eax")
  mov(v, "edi")
  asm("idiv %edi")

def divl(s, v):
  asm("xorl %edx, %edx")
  mov(s, "eax")
  mov(v, "edi")
  asm("div %edi")

def seval(name, node):
  v = []
  if node.left != None:
    if node.left.right == None:
      x = seval(name, node.left)
      v = v + x
      return v
    v.append(node.left.right)
    x = seval(name, node.left)
    v = v + x
  return v

automakeStruct = False

def addGlobal(g, val):
  #print(val)
  #print(g)
  globalss[g] = val

class Console:
  def __init__(self, file):
    self.file = file
    with open(self.file, "w") as fw:
      fw.write("")
  def log(self, s):
    with open(self.file, "a") as fw:
      fw.write(str(s) + "\n")
  def clear(self):
    with open(self.file, "w") as fw:
      fw.write("")

console = Console("console.txt")

def cmpl(node):
  global vvalue, automakeStruct, splaces, n, currentFunc, funcs, varias, funcnums, funcargs, nextAdd, breaker, fstructs, funcleaves, consts, constglobals, globalss
  #print(varias)
  #print("Entered cmpl()")
  #print("node.left: {}".format(node.left))
  #print(node.type)
  #ngl = globalss
  #print(globalss)
  ngl = dict(globalss)
  for i in globalss:
    for ni in globalss[i]:
      if ni == "%":
        varias[i] = globalss[i]
        console.log(varias)
        del ngl[i]
        console.log(varias)
        break
    #print(len(globalss) - len(ngl))
  globalss = ngl
  #print(globalss)
  #globalss = ngl
  if node == None:
    return None

  #print(varias)
  
  if currentFunc == None:
    if node != None and node.left != None and node.left.type == "fdef1":
      #print(node.left.right.left.right)
      fname = node.left.right.left.right.getTokenValue()
      args = node.left.right.right
      if fname in funcs.keys():
        quit("Cannot redefine function <" + str(fname) + ">!")
      else:
        fname = checkFuncCall(fname)[1]
        currentFunc = fname
        funcs[fname] =[]
        funcargs[fname] = []
        funcnums[fname] = 0
        n = n + 1
        funcleaves[fname] = ".leaver" + str(n)
        fstructs = {}
        consts = []
        varias = globalss
        #print(globalss)
        idx = 4
        for arg in args:
          idx += 4
          if arg == "":
            break
          elif is_valid_variable_name(arg):
            varias[arg] = str(idx) + "(%ebp)"
            #print(varias[arg])
            funcargs[currentFunc].append(args)

          else:
            quit("Invalid argument <" + arg + ">!")
        
        cmpl(node.left.right.left)
        #print(varias)
        currentFunc = None
        cmpl(node.left)
    elif node != None and node.left != None and node.left.type == "gdec":
      vname = node.left.right.right
      n = n + 1
      v = "globalLOCK" + str(n)
      data["globalLOCK" + str(n)] = ".long 0"
      gh = funcs["_start"]
      currentFunc = "_start"
      varias = globalss
      funcs["_start"] = []
      cmpl(node.left.right.left)
      asm("movl %ecx, " + v)
      if automakeStruct != False:
        cmpl(fparse(lex("{} as struct {};".format(node.left.left.right, automakeStruct)), "tmp"))
        automakeStruct = False
      funcs["_start"] = funcs["_start"] + gh
      currentFunc = None
      if vname in globalss:
        quit("Global <{}> already defined!".format(vname))
      else:
        addGlobal(vname, v)
        cmpl(node.left)
        return None
      varias = {}
    elif node != None and node.left != None and node.left.type == "cgdec":
      vname = node.left.right.right
      n = n + 1
      v = "globalLOCK" + str(n)
      data["globalLOCK" + str(n)] = ".long 0"
      gh = funcs["_start"]
      currentFunc = "_start"
      varias = globalss
      constglobals.append(vname)
      funcs["_start"] = []
      cmpl(node.left.right.left)
      asm("movl %ecx, " + v)
      if automakeStruct != False:
        cmpl(fparse(lex("{} as struct {};".format(node.left.left.right, automakeStruct)), "tmp"))
        automakeStruct = False
      funcs["_start"] = funcs["_start"] + gh
      currentFunc = None
      if vname in globalss:
        quit("Global <{}> already defined!".format(vname))
      else:
        addGlobal(vname, v)
        cmpl(node.left)
        return None
      varias = {}
    elif node != None and node.left != None and node.left.type == "sdef":
      # struct
      sname = node.left.right.right
      v = seval(sname, node.left.right)
      if v == []:
        print("Semble: Warning: Empty struct '{}', due to this being a waste of memory, it will not be generated.".format(sname))
        cmpl(node.left)
        return None
      else:
        structs[sname] = v
        #print(sname)
        cmpl(node.left)
        return None

    elif node == None or node.left == None:
      pass

  elif node.left != None and node.left.type == "srdef":
    #print("he")
    sname = node.left.right[0]
    vname = node.left.right[1]
    stuffs = node.left.right[2]
    # you're to have a place in memory
    asm("pushl $" + str(len(stuffs) * 4))
    asm("call malloc")
    funcnums[currentFunc] += 4
    v = "-" + str(funcnums[currentFunc]) + "(%ebp)"
    asm("movl %eax, " + v)
    if vname in varias:
      quit("Predefined variable {}!".format(vname))
    varias[vname] = v
    idx = -1
    #print(structs[sname])
    for i in structs[sname]:
      idx += 1
      try:
        x = stuffs[idx]
      except:
        x = False
      if x == False:
        asm("xorl %ecx, %ecx")
      else:
        cmpl(checkExpr(stuffs[idx])[2])
      asm("movl " + v + ", %ebx")
      if idx == 0:
        prefix = ""
      else:
        prefix = "" + str(idx * 4)
      asm("movl %ecx, " + prefix + "(%ebx)")
    sva = Struct(sname, structs[sname], v)
    fstructs[vname] = sva
    cmpl(node.left)
    
      

  elif node.left != None and node.left.type == "asstruct":
    if node.left.right[0] in varias:
      try:
        #print(structs.keys())
        #print(structs)
        x = Struct("" + str(node.left.right[0]) + "", structs[node.left.right[1]], varias[node.left.right[0]], rev=True)
        #print(str(x))
      except IndexError:
        quit("No struct '{}' or no variable '{}'!".format(node.left.right[1], node.left.right[0]))
      fstructs[node.left.right[0]] = x
      cmpl(node.left)
      return None
    else:
      quit("Value <{}> not a variable!".format(node.left.right[1]))
  elif node.left != None and node.left.type == "free":
    cmpl(node.left.right)
    asm("pushl $ecx")
    asm("call free")
    cmpl(node.left.left)
  elif node.left != None and node.left.type == "break":
    br = breaker[-1]
    #print(br)
    asm("jmp " + br)
    cmpl(node.left)
    return None

  elif node.left != None and node.left.type == "funccall":
    #print("juud")
    val = node.left.right
    b, fn, args = checkFuncCall(val)
    #print(args)
    for arg in reversed(args):
      if arg == "":
        break
      else:
        try:
          bo, ty, no = checkExpr(lex(arg + "\n"))
        except:
          quit("Invalid expression '" + arg + "'!")
        if bo:
          cmpl(no)
          push("ecx")
        else:
          quit("Invalid expression <" + arg + ">!")
    asm("call " + fn)
    pop("ebx")
    cmpl(node.left)
    return None
  
  elif node.left != None and node.left.type == "forloop":
    fordetails = node.left.right
    fromv = fordetails.right[1]
    tov = fordetails.right[2]
    vname = fordetails.right[0]
    nexts = Node("nonode", left=fordetails.left)
    if vname not in varias:
      cmpl(fromv)
      funcnums[currentFunc] += 4
      varias[vname] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      asm("movl %ecx, " + varias[vname])
      cmpl(tov)
      mov("ecx", "esi")
      n += 1
      mov(varias[vname], "ebx")
      cmp("esi", "ebx")
      nname = "LF" + str(n)
      nname2 = "LD" + str(n)
      asm("jg ." + nname)
      asm("." + nname2 + ":")
      breaker.append("." + nname)
      cmpl(nexts)
      breaker.pop(-1)
      asm("incl " + varias[vname])
      cmpl(tov)
      mov("ecx", "esi")
      mov(varias[vname], "ebx")
      cmp("esi", "ebx")
      asm("jle ." + nname2)
      asm("." + nname + ":")
      #asm("pushl $clearBuffer")
      #asm("call printf")
      cmpl(node.left)
    else:
      quit("Prenamed variable <{}>!".format(vname))
  elif node.left != None and node.left.type == "if_statement":
    things = node.left.right.right
    #print("\n\n#################\n\n" + str(node.left) + "\n\n")
    #print(node.left.left)
    ins = Node("nonode", left=node.left.right.left)
    cmpl(things[0])
    push("ecx")
    cmpl(things[1])
    pop("edx")
    cmp("ecx", "edx")
    prefix = None
    if things[2] == "TT_EQUALS":
      prefix = "ne"
    elif things[2] == "TT_DNEQUAL":
      prefix = "e"
      cmpl(node.left.left)
    elif things[2] == "TT_GRTHAN":
      prefix = "le"
    elif things[2] == "TT_LTHAN":
      prefix = "ge"
    elif things[2] == "TT_GRTHANET":
      prefix = "l"
    elif things[2] == "TT_LTHANET":
      prefix = "g"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    name = prefix + str(n)
    n += 1
    asm("j" + prefix + " ." + name)
    cmpl(ins)
    #print(ins)
    asm("." + name + ":")
    #print(node.left)
    cmpl(node.left)
  elif node.left != None and node.left.type == "while_loop":
    #print(fstructs)
    things = node.left.right.right
    #print("\n\n#################\n\n" + str(node.left) + "\n\n")
    #print(node.left.left)
    ins = Node("nonode", left=node.left.right.left)
    cmpl(things[0])
    push("ecx")    
    #print(node.right.right)
    cmpl(things[1])
    pop("edx")
    cmp("ecx", "edx")
    prefix = None
    if things[2] == "TT_EQUALS":
      prefix = "ne"
    elif things[2] == "TT_DNEQUAL":
      prefix = "e"
      cmpl(node.left.left)
    elif things[2] == "TT_GRTHAN":
      prefix = "le"
    elif things[2] == "TT_LTHAN":
      prefix = "ge"
    elif things[2] == "TT_GRTHANET":
      prefix = "l"
    elif things[2] == "TT_LTHANET":
      prefix = "g"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    name = prefix + str(n)
    n += 1
    asm("j" + prefix + " ." + name)
    abc = "LFB" + str(n)
    asm("." + abc + ":")
    breaker.append("." + name)
    cmpl(ins)
    breaker.pop(-1)
    
    cmpl(things[0])
    push("ecx")
    cmpl(things[1])
    pop("edx")
    cmp("ecx", "edx")
    prefix = None
    if things[2] == "TT_EQUALS":
      prefix = "ne"
    elif things[2] == "TT_DNEQUAL":
      prefix = "e"
      cmpl(node.left.left)
    elif things[2] == "TT_GRTHAN":
      prefix = "le"
    elif things[2] == "TT_LTHAN":
      prefix = "ge"
    elif things[2] == "TT_GRTHANET":
      prefix = "l"
    elif things[2] == "TT_LTHANET":
      prefix = "g"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    asm("j" + prefix + " ." + abc)

    #print(ins)
    asm("." + name + ":")
    #breaker = "." + name
    cmpl(node.left)
    return None
    
  elif node.left != None and node.left.type == "int_dec":
    #print("Entered cmpl.int_dec()")
    if node.left.left.right not in varias.keys():
      cmpl(node.left.right)
      ints.append(node.left.left.right)
      funcnums[currentFunc] += 4
      varias[node.left.left.right] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      v = False
      if nextAdd > 0 and currentFunc != None:
        funcnums[currentFunc] += nextAdd
        nextAdd = 0
        v = True
      if not v:
        asm("movl %ecx, " + varias[node.left.left.right])
      ss = []
      if automakeStruct != False:
        cmpl(fparse(lex("{} as struct {};".format(node.left.left.right, automakeStruct)), "tmp"))
        automakeStruct = False
      cmpl(node.left.left)
      return None
    else:
      #print(node.left.left.right)
      quit("{}: Prenamed variable <".format(node.left) + str(node.left.left.right) + ">!")
  
  elif node.left != None and node.left.type == "const_dec":
    #print("Entered cmpl.int_dec()")
    if node.left.left.right not in varias.keys():
      cmpl(node.left.right)
      ints.append(node.left.left.right)
      funcnums[currentFunc] += 4
      varias[node.left.left.right] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      consts.append(node.left.left.right)
      v = False
      if nextAdd > 0 and currentFunc != None:
        funcnums[currentFunc] += nextAdd
        nextAdd = 0
        v = True
      if not v:
        asm("movl %ecx, " + varias[node.left.left.right])
      if automakeStruct != False:
        cmpl(fparse(lex("{} as struct {};".format(node.left.left.right, automakeStruct)), "tmp"))
        automakeStruct = False
      cmpl(node.left.left)
      return None
    else:
      quit("Prenamed variable <" + str(node.left.left.right) + ">!")

  elif node.left != None and node.left.type == "asm_line":
    v = node.left.right
    cmpl(node.left.left)
    v = v[1:-1]
    for var in varias:
      v = v.replace("~~" + var, varias[var])
    asm(v)
    cmpl(node.left)
    return None
  
  elif node.left != None and node.left.type == "set_mov_equals":
    if node.left.left.right in consts or node.left.left.right in constglobals:
      #print(constglobals)
      quit("Variable <" + str(node.left.left.right) + "> is a constant!")
    #print(is_valid_struct_def(node.left.left.right))
    if node.left.left.right in globalss.keys():
      cmpl(node.left.right)
      asm("movl %ecx, " + globalss[node.left.left.right])
      cmpl(node.left.left)
      return None 
    elif node.left.left.right[0] == "$" and node.left.left.right[1:] in varias.keys():
      cmpl(node.left.right)
      asm("movl " + varias[node.left.left.right[1:]] + ", %ebx")
      asm("movl %ecx, (%ebx)")
      cmpl(node.left.left)
      return None
    elif node.left.left.right in varias.keys():
      #print("ui")
      cmpl(node.left.right)
      asm("movl %ecx, " + varias[node.left.left.right])
      cmpl(node.left.left)
      return None

    elif is_valid_struct_def(node.left.left.right):
      val = node.left.left.right
      #cmpl(node.left.left)
      cmpl(node.left.right)
      #print(node.left.right)
      x = checkStructDef(val)
      if x[0] in fstructs:
        #print(x[0])
        fstructs[x[0]].getvalue(x[1])
        asm("movl " + varias[x[0]] + ", %ebx")
        if x[1] in fstructs[x[0]].variz:
          if str(fstructs[x[0]].variz.index(x[1]) * 4) == "0":
            prefix = ""
          else:
            prefix = "" + str(fstructs[x[0]].variz.index(x[1]) * 4)
          asm("movl %ecx, " + prefix + "(%ebx)")
          cmpl(node.left.left)

          return None
        else:
          quit("Unknown variable '{}'!".format(x[0]))

    elif checkIndexRef(node.left.left.right)[0]:
      val = node.left.left.right
      b, fn, indexs = checkIndexRef(val)
      # b = if it worked
      # fn = object referenced
      # index = index referenced
      
      idx = 0
      for index in indexs:
        #print(index)
        if index[0] == "_":
          ati = 1
          index = index[1:]
          #print(index)
        else:
          ati = 4
        if idx == 0:
          if is_valid_struct_def(fn):
            x = checkStructDef(fn)
            #print(x[0])
            #print(fstructs)
            if x[0] in fstructs:
              #print(x[0])
              fstructs[x[0]].getvalue(x[1])
              asm("movl " + varias[x[0]] + ", %ebx")
              if x[1] in fstructs[x[0]].variz:
                if str(fstructs[x[0]].variz.index(x[1]) * 4) == "0":
                  prefix = ""
                else:
                  prefix = "" + str(fstructs[x[0]].variz.index(x[1]) * 4)
                asm("movl " + prefix + "(%ebx), %ecx")
                ptr = "%ecx"
                #print("movl " + prefix + "(%ebx), %ecx")
              else:
                quit("Semble: Error: Data structure '{}' has no type '{}'!".format(x[0], x[1]))
            else:
              #print(x)
              quit("Unknown type '{}'!".format(x[0]))
          else:
            ptr = varias[fn]
        else:
          ptr = "%ecx"
        asm("movl " + ptr + ", %ebx")
        bo, ty, no = checkExpr(lex(str(index) + "\n"))
        if not bo:
          quit("Invalid expression '{}'".format(str(index)))
        cmpl(no)
        mul(ati, "ecx")
        asm("addl %ecx, %ebx")
        asm("movl (%ebx), %ecx")
        idx += 1
      
      cmpl(node.left.right)
      asm("movl %ecx, (%ebx)")
      cmpl(node.left.left)
      return None
    
    else:
      quit("Unknown variable <" + node.left.left.right +">!")
    

  elif node.left != None and node.left.type == "quit_statement":
    cmpl(node.left.right)
    mov("ecx", "ebx")
    mov(1, "eax")
    asm("int $0x80")

  elif node.left != None and node.left.type == "return_statement":
    cmpl(node.left.right)
    mov("ecx", "eax")
    asm("jmp " + funcleaves[currentFunc])

  elif node.left == None and node.type == "int_val":
    val = node.right
    g = None
    #print(val)
    
    if val in ["true", "false"]:
      if val == "true":
        asm("movl $1, %ecx")
      else:
        asm("movl $0, %ecx") 
        
    elif val == "new":
      n += 1
      x = "newLOCK" + str(n)
      data[x] = ".long 0"
      n += 1
      asm("movl ${}, %ecx".format(x))

    elif re.match(r"^\d+\.\d+$", val):
      n += 1
      x = "doubleLOCK" + str(n)
      data[x] = ".double {}".format(val)
      n += 1
      asm("movl ${}, %ecx".format(x))

    elif re.match(r"^\[(.*)\]\[(.*\,)*(.*)\]$", val):
      x = re.match(r"^\[(.*)\]\[(.*\,)*(.*)\]$", val)
      length = x.group(1)
      try:
        values = x.group(2) + x.group(3)
        args = parseFuncCall(values)
      except:
        args = None
      tmpid = 0
      tmpida = 0
      tmpi = ""
      tmp = ""
      new = []
      if args == None:
        new = []
      else:
        for i in args:
          if i == "(" and tmpi == "":
            tmp += i
            tmpid += 1
          elif i == ")" and tmpi == "":
            tmp += i
            tmpid -= 1
          elif i == "[" and tmpi == "":
            tmp += i
            tmpida += 1
          elif i == "]" and tmpi == "":
            tmp += i
            tmpida -= 1
          elif i == "\"" and tmpi == "":
            tmp += i
            tmpi = "quote"
          elif i == "\"" and tmpi == "quote":
            tmp += i
            tmpi = ""
          elif i == "'" and tmpi == "":
            tmp += i
            tmpi = "char"
          elif i == "'" and tmpi == "char":
            tmp += i
            tmpi = ""
          elif tmpid == 0 and tmpida == 0 and i == "," and tmpi == "":
            new.append(tmp)
            tmp = ""
          else:
            tmp += i
        new.append(tmp)
      #print(new)
      idx = 0
      if length[0] == "_":
        ati = 1
        length = length[1:]
      else:
        ati = 4
      bo, ty, no = checkExpr(lex(length + "\n"))
      if not bo:
        quit("Invalid expression '{}'!".format(length))
      cmpl(no)
      mul(ati, "ecx")
      asm("pushl %ecx")
      asm("call malloc")
      funcnums[currentFunc] += 4
      v = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      asm("movl %eax, " + v)
      for arg in new:
        #print(lex(arg + " "))
        #print(list(arg + " "))
        if arg != "":
          if idx == 0:
            prefix = ""
          else:
            prefix = "" + str(idx * 4)
          try:
            bo, ty, no = checkExpr(lex(arg + "\n"))
          except:
            quit("Invalid expression '{}'".format(arg))
          if not bo:
            quit("Invalid expression '{}'".format(arg))
          cmpl(no)
          asm("movl " + v + ", %ebx")
          asm("movl %ecx, " + prefix + "(%ebx)")
          idx += 1
        else:
          break
      asm("movl " + v + ", %ecx")

    elif checkIndexRef(val)[0]:
      b, fn, indexs = checkIndexRef(val)
      # b = if it worked
      # fn = object referenced
      # index = index referenced

      #print(checkIndexRef(val))
      
      idx = 0
      for index in indexs:
        if index[0] == "_":
          ati = 1
          index = index[1:]
          #print(index)
        else:
          ati = 4
        #print(index)
        if idx == 0:
          #print(fn)
          if is_valid_struct_def(fn):
            x = checkStructDef(fn)
            #print(x[0])
            #print(fstructs)
            if x[0] in fstructs:
              #print(x[0])
              fstructs[x[0]].getvalue(x[1])
              asm("movl " + varias[x[0]] + ", %ebx")
              if x[1] in fstructs[x[0]].variz:
                if str(fstructs[x[0]].variz.index(x[1]) * 4) == "0":
                  prefix = ""
                else:
                  prefix = "" + str(fstructs[x[0]].variz.index(x[1]) * 4)
                asm("movl " + prefix + "(%ebx), %ecx")
                ptr = "%ecx"
                #print("movl " + prefix + "(%ebx), %ecx")
              else:
                quit("Semble: Error: Data structure '{}' has no type '{}'!".format(x[0], x[1]))
            else:
              #print(x)
              quit("Unknown type '{}'!".format(x[0]))
          else:
            ptr = varias[fn]
        else:
          ptr = "%ecx"
        asm("movl " + ptr + ", %ebx")
        bo, ty, no = checkExpr(lex(str(index) + "\n"))
        if not bo:
          quit("Invalid expression '{}'".format(str(index)))
        cmpl(no)
        mul(ati, "ecx")
        asm("addl %ecx, %ebx")
        asm("movl (%ebx), %ecx")
        idx += 1
      
    elif is_valid_struct_def(val):
      x = checkStructDef(val)
      #print(x[0])
      #print(fstructs)
      if x[0] in fstructs:
        #print(x[0])
        fstructs[x[0]].getvalue(x[1])
        asm("movl " + varias[x[0]] + ", %ebx")
        if x[1] in fstructs[x[0]].variz:
          if str(fstructs[x[0]].variz.index(x[1]) * 4) == "0":
            prefix = ""
          else:
            prefix = "" + str(fstructs[x[0]].variz.index(x[1]) * 4)
          asm("movl " + prefix + "(%ebx), %ecx")
          #print("movl " + prefix + "(%ebx), %ecx")
        else:
          print(x)
          print(val)
          quit("Semble: Error: Data structure '{}' has no type '{}'!".format(x[0], x[1]))
      else:
        #print(x)
        quit("Unknown type '{}'!".format(x[0]))

    elif re.match(r"^(i8:)\d+$", val):
      v = val[3:]
      asm("pushl $" + str(v))
      asm("call malloc")
      asm("movl %eax, %ecx")
      n += 1
        
    elif re.match(r'^["][^\n]*["]$', val):
      if val not in strings.keys():
        x ="strLOCK" + str(n)
        n += 1
        data[x] = ".asciz " + val
        strings[val] = x
        asm("movl $" + x + ", %ecx")
        return ["str", val]
      else:
        asm("movl $" + strings[val] + ", %ecx")

    elif is_valid_variable_name(val):
      try:
        g = varias[val]
      except Exception as er:
        #print(varias)
        quit(": Unknown variable <" + val +">!")
      asm("movl " + g + ", %ecx")

    elif len(val) >= 2 and val[0] == "@" and is_valid_variable_name(val[1:]):
      x = val[1:]
      if x in varias:
        asm("leal " + varias[x] + ", %ecx")
      else:
        quit("Unknown variable <" + str(x) + ">!")
    
    elif len(val) >= 2 and val[0] == "$" and is_valid_variable_name(val[1:]):
      x = val[1:]
      if x in varias:
        asm("movl " + varias[x] + ", %edi")
        asm("movl (%edi), %ecx")
      else:
        quit("Unknown variable <" + str(x) + ">!")

    elif checkFuncCall(val)[0]:
      b, fn, args = checkFuncCall(val)
      #print(args)
      #print(args)
      for arg in reversed(args):
        if arg == "":
          break
        else:    
          #print(arg)
          bo, ty, node = checkExpr(lex(arg + "\n"))
          if bo:
            cmpl(node)
            push("ecx")
          else:
            quit("Invalid expression <" + arg + ">!")
      if fn in structs.keys():
        automakeStruct = fn
      asm("call " + fn)
      mov("eax", "ecx")


      #pop("ebx")
    else:
      if val == "0":
        asm("xorl %ecx, %ecx")
      else:
        asm("movl $" + val + ", %ecx")
      return val



  elif node.type == "add":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    if is_valid_variable_name(node.left.right):
  
      if node.left.right in fstructs and node.left.right in varias:
        fsn = fstructs[node.left.right]
        if fsn.stype + "__add__" in funcs.keys():
          vvalue = fsn.stype
          push("ecx")
          y = cmpl(node.left)
          push("ecx")
          asm('call ' + fsn.stype + "__add__")
          asm("movl %eax, %ecx")
          automakeStruct = fsn.stype
          return None
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    add("edx", "ecx")

  elif node.type == "minus":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    if is_valid_variable_name(node.left.right):
      if node.left.right in fstructs and node.left.right in varias:
        fsn = fstructs[node.left.right]
        if fsn.stype + "__sub__" in funcs.keys():
          vvalue = fsn.stype
          push("ecx")
          y = cmpl(node.left)
          push("ecx")
          asm('call ' + fsn.stype + "__sub__")
          asm("movl %eax, %ecx")
          automakeStruct = fsn.stype
          return None
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    sub("edx", "ecx")

    
  
  elif node.type == "mul":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    if is_valid_variable_name(node.left.right):
      if node.left.right in fstructs and node.left.right in varias:
        fsn = fstructs[node.left.right]
        if fsn.stype + "__mul__" in funcs.keys():
          vvalue = fsn.stype
          push("ecx")
          y = cmpl(node.left)
          push("ecx")
          asm('call ' + fsn.stype + "__mul__")
          asm("movl %eax, %ecx")
          automakeStruct = fsn.stype
          return None
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    mul("edx", "ecx")

  
  elif node.type == "div":
    #push("eax")
    x = cmpl(node.left)
    if is_valid_variable_name(node.left.right):
      if node.left.right in fstructs and node.left.right in varias:
        fsn = fstructs[node.left.right]
        if fsn.stype + "__div__" in funcs.keys():
          vvalue = fsn.stype
          push("ecx")
          y = cmpl(node.left)
          push("ecx")
          asm('call ' + fsn.stype + "__div__")
          asm("movl %eax, %ecx")
          automakeStruct = fsn.stype
          return None
    push("ecx")
    y = cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    div("eax", "ecx")
    mov("eax", "ecx")
    #pop("eax")

  elif node.type == "mod":
    #push("eax")
    y = cmpl(node.left)
    if is_valid_variable_name(node.left.right):
      if node.left.right in fstructs and node.left.right in varias:
        fsn = fstructs[node.left.right]
        if fsn.stype + "__mod__" in funcs.keys():
          vvalue = fsn.stype
          push("ecx")
          y = cmpl(node.left)
          push("ecx")
          asm('call ' + fsn.stype + "__mod__")
          asm("movl %eax, %ecx")
          automakeStruct = fsn.stype
          return None
    push("ecx")
    x = cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    divl("eax", "ecx")
    mov("edx", "ecx")
    #pop("eax")

  


def cmpf(ast, f):
  global funcnums, funcs, currentFunc, tmpid, valueStack, ints, varias, data, strings, n, bss
  funcnums = {
    
  }

  funcs = {
    "_start":["call main", "movl %eax, %ebx", "movl $1, %eax", "int $0x80"],
  }

  currentFunc = None

  tmpid = ""
  valueStack = []
  ints = []
  varias = {
    
  }

  data = {
    #"clearBuffer": ".asciz \"[semble] clearing output buffer. IF you see this message, you're program has encountered an error in the stdout buffer\\n\"" 
  }

  strings = {
    
  }

  n = 0
  cmpl(ast)
  with open(f, "w") as fw:
    fw.write("\t.section .data\n")
    for d in data:
      fw.write("\n" + d + ":\n")
      di = data[d]
      fi = di.split("\n")
      for i in fi:
        #print(i)
        fw.write("\t" + i + "\n")
    #fw.write("\n\nL45SDEF:\n\n")
    # fw.write("\t.section .bss\n")
    fw.write("\t.section .bss\n")
    for b in bss:
      fw.write("\n.lcomm " + b + ", " + str(bss[b]) + "\n")
    fw.write("\t.section .text\n")
    fw.write("\t.globl _start\n")
    for func in funcs:
      if func != "_start":
        fw.write("\n\t.type " + func + ", @function")
      fw.write("\n" + func + ":\n")
      if func != "_start":
        for pl in functionProlouge:
          fw.write(pl)
        if funcnums[func] > 0:
          # print(func)
          fw.write("\n\tsubl $" + str(funcnums[func]) + ", %esp\n")

      for fl in funcs[func]:
        fw.write("\t"+ fl + "\n")

      if func != "_start":
        fw.write("\t" + funcleaves[func] + ":\n")
        for el in functionEpilouge:
          fw.write(el)


'''
-> "hello.txt"
-> 
'''