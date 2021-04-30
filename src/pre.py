import src.linkmain
import os

inimports = []

num = 0

def process(code, n="semble.out"):
  global num
  # include
  # define
  newcode = ""
  code = code.split("\n")
  name = n
  idx = -1
  #newcode += importf("base.smb", newcode)
  for line in code:
    idx += 1
    #print(line)
    if line.strip().startswith("//"):
      newcode += "\n"
    elif line.startswith("#include"):
      l = line.replace("#include ", "")
      l = l.split(", ")
      for f in l:
        newcode += importf(f, newcode)
    elif line.startswith("#program"):
      l = line.replace("#program ", "")
      name = l
    elif line.startswith("#file"):
      l = line.replace("#file ", "")
      try:
        lines = '\n'.join(code[idx+1:])
      except:
        pass
      with open("ppfcf.smb", "w") as fw:
        fw.write(lines)
      src.linkmain.compilefile("ppfcf.smb", l)
      try:
        os.system("rm ppfcf.smb")
      except:
        pass
      break
    else:
      newcode += "\n" + line
  return newcode, name
  
def importf(f, code):
  new = ""
  #print(list(f))
  if f in inimports:
    return "\n"
  else:
    #print(inimports)   
    inimports.append(f)
    try:
      with open("libs/" + f, "r") as file:
        for l in file:
          new += "\n" + l
        #print()
        return process(new)[0]
    except Exception as e:
      #print(e)
      quit("Unkown file '{}'!".format(f))