def readLines(f):
  r = []
  with open(f, 'r') as fr:
    for l in fr:
      r.append(l)
  return r
    

def redundancy(f):
  lines = readLines(f)
  idx = 0
  lastLine = ""
  while idx < len(lines):
    x = lines[idx]
    if len(x.strip()) == 0:
      idx += 1
    elif x != lastLine or x.strip()[0] == ".":
      lastLine = x
      idx += 1
    else:
      lines.pop(idx)
  return lines
  
  
def optimize(f):
  lines = redundancy(f)
  with open(f, "w") as fw:
    for l in lines:
      fw.write(l)