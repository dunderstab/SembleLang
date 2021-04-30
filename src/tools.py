def readSembleFile(filename):
  x = None
  with open(filename, "r") as fd:
    x = ''.join(fd.readlines()) + "\n"
  return x