import src.lex
import src.parse
import src.eval
import src.tools
import src.optimize
import src.pre
import re
import sys

def main(file, n=None, first=False):

  import os
  debug = False

  version = "Beta 2.5"

  l = src.tools.readSembleFile(file)

  #if first:
  #  l += src.pre.importf("base.smb", l)[0]

  l, fname = src.pre.process(l)

  with open("newcode.smb", "w") as newcode:
    newcode.write(l)

  x = src.lex.lex(l)

  with open("lexout.txt", "w") as fw:
    fw.write(str(x).replace("[", "[\n").replace("]", "]\n"))

  v = src.parse.parse(x)

  with open("parseout.txt", "w") as fw:
    fw.write(str(v).replace("[", "[\n").replace("]", "]\n"))

  src.eval.cmpf(v, "semble.asm")
  
  src.optimize.optimize("semble.asm")

  os.system("as --32 semble.asm -o semble.o")
  if n != None:
    fname = n
  os.system("ld -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 -o " + fname + " semble.o -lc")
  if not debug:
    os.system("rm semble.o parseout.txt lexout.txt newcode.smb console.txt")
  

if __name__ == '__main__':
  #print(src.lex.checkFuncCall("hello(helo,hello, h)"))
  #if re.match(r"^\[\d+\]\[(.*\,)*(.*)\]$", "[7][6, 6,]"):
  #  print("hello")
  #print(src.lex.checkIndexRef("hello[5]"))
  #print(re.match(r"^(\[[^\n\]]+\])+$", "[56][65][67]"))
  #src.lex.getIndexs("[56][65][67]")
  #print(src.lex.checkIndexRef("people.names[3]"))
  #print(src.lex.lex("5 + 5 * 5\n"))
  #print("\n")
  #print(src.parse.organizeEquation(src.lex.lex("5 + 5 * 5 + 5 + 5\n")))
  main(sys.argv[1])
  print("Compiled Succesfully")