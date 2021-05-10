import re

class Token:
  def __init__(self, T_TYPE, value=None):
    self.T_TYPE = T_TYPE
    self.value = value
  def getTokenType(self):
    return self.T_TYPE
  def getTokenValue(self):
    return self.value
  def __str__(self):
    return '[Token: TokenType: {} TokenValue: {}]'.format(self.T_TYPE, self.value)
  def __repr__(self):
    return '[Token: TokenType: {} TokenValue: {}]'.format(self.T_TYPE, self.value)

def getIndexs(v):
  depth = 0
  values = []
  for i in v:
    if i == "[":
      depth += 1
      if len(values) < depth:
        values.append("")
    elif i == "]":
      continue
    else:
      values[depth - 1] += i 
  #print(values)
  return values

def checkIndexRef(s):
  vn = ""
  n = ""
  idx = -1
  for i in s:
    idx += 1
    if i == "[":
      break
    else:
      vn += i
  ns = s[idx:]
  if re.match(r"^(\[[^\n\]]+\])+$", ns):
    v = getIndexs(ns)
    return True, vn, v

  else:
    return False, None, None

def getNextChar(s, v):
  try:
    return s[v+1]
  except:
    return None

def parseFuncCall(s):
  new = ""
  last = ""
  tmpid = ""
  n = 0
  v = -1
  for i in s:
    v += 1
    if i == " ":
      if tmpid in ["quote", "chr"] or last in ["+", "-", "*", "/", "%"] or getNextChar(s, v) in ["+", "-", "*", "/", "%"]:
        new += i
    else:
      new += i

    if i in [")", "]"] and tmpid in ["paren"]:
      if n == 0:
        tmpid = ""
      else:
        n -= 1
    elif i == "(" and tmpid in ["paren", ""]:
      n += 1
    elif i == "[" and tmpid in ["paren", ""]:
      n += 1
    elif i == "\"" and tmpid in ["quote"]:
      tmpid = ""
    elif i == "\"" and tmpid in [""]:
      tmpid = "quote"
    elif i == "'" and tmpid in ["chr"]:
      tmpid = ""
    elif i == "'" and tmpid in [""]:
      tmpid = "chr"
    else:
      last = i

  return new

def checkFuncCall(s):
  fn = ""
  args = ""
  idx = 0
  for i in s:
    idx += 1
    if i == "(":
      break
    else:
      fn += i
  if is_valid_variable_name(fn):
    args = s[idx:-1]
    args = parseFuncCall(args)
    tmpid = 0
    tmpida = 0
    tmpi = ""
    tmp = ""
    new = []
    #print(args)
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
    if tmpid != 0:
      return False, None, None
    new.append(tmp)
    #print(new)
    return True, fn, new
  else:
    return False, None, None
     

TT_PLUS = "TT_PLUS"
TT_EQUALS = "TT_EQUALS"
TT_DNEQUAL = "TT_DNEQUAL"
TT_GRTHAN = "TT_GRTHAN"
TT_LTHAN = "TT_LTHAN"
TT_MINUS = "TT_MINUS"
TT_KEYWORD = "TT_KEYWORD"
TT_SEMICOLON = "TT_SEMICOLON"
TT_INTEGER = "TT_INTEGER"
TT_HEX = "TT_HEX"
TT_IDENTIFIER = "TT_IDENTIFIER"
TT_LBRACE = "TT_LBRACE"
TT_RBRACE = "TT_RBRACE"
TT_STRING = "TT_STRING"
TT_DEC = "TT_DEC"
TT_AMPOINT = "TT_AMPOINT"
TT_PTR = "TT_PTR"
TT_FUNCCALL = "TT_FUNCCALL"
TT_DEQUAL = "TT_DEQUAL"
TT_MUL = "TT_MUL"
TT_BYTES = "TT_BYTES"
TT_DIV = "TT_DIV"
TT_MOD = "TT_MOD"
TT_CHAR = "TT_CHAR"
TT_COLON = "TT_COLON"
TT_ASM = "TT_ASM"
TT_ARR = "TT_ARR"
TT_AMP = "TT_AMP"
TT_COMMA = "TT_COMMA"
TT_INDEXREF = "TT_INDEXREF"
TT_STRUCTDEF = "TT_STRUCTDEF"

def is_valid_struct_def(s):
  s = s.split(".")
  if len(s) != 2:
    return False
  return is_valid_variable_name(s[0]) and is_valid_variable_name(s[1]) and s[0] not in KEYWORDS.keys() and s[1] not in KEYWORDS.keys()

def findKeyFromValue(dictionary, v):
  for key, val in dictionary.items():
    if val == v:
        return key
  return None
  
KEYWORDS = {
  "INT_DEC": "let",
  "CONST_DEC": "const",
  "FN_DEC": "fn",
  "QUIT": "quit",
  "RETURN": "return",
  "IF": "if",
  "NEW": "new",
  "ASM": "asm",
  "ENDIF": "endif",
  "FREE": "free",
  "BANK": "bank",
  "TRUE": "true",
  "FALSE": "false",
  "CONST": "const",
  "FOR": "for",
  "ELSE": "else",
  "FROM": "from",
  "TO": "to",
  "ENDFOR": "endfor",
  "WHILE": "while",
  "ENDWHILE": "endwhile",
  "BREAK": "break",
  "STRUCT": "struct",
  "NEW": "new",
  "AS": "as",
}

def is_valid_variable_name(name):
    return name.isidentifier() and not name in KEYWORDS.keys()


def lex(s):
  tmp = ""
  tmp2 = ""
  tmpid = ""
  ptmpd = 0
  tokens = []
  for i in s:
    #print(list(tmp))
    #print(tmpid)

    #print(tmpid)

    if tmpid == "multiline":
      if i == "~":
        tmpid = ""
        continue
      continue

    if tmpid == "minus" and i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
      tokens.append(Token(TT_MINUS))
      tmpid = ""
      tmp2 = ""
    elif tmpid == "minus":
      tmp2 += "-"
      tmpid = ""

    if i == "\"" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tmpid = "quote"
      tmp2 += i
    
    elif i == "\"" and tmpid == "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tmpid = ""
      tmp2 += i

    elif i == "(" and tmpid != "quote" and tmpid != "chr" and tmpid != "brac":
      #print(ptmpd)
      tmpid = "paren"
      tmp2 += i
      ptmpd += 1
    
    elif i == ")" and tmpid == "paren" and tmpid != "chr" and tmpid != "quote" and tmpid != "brac":
      tmp2 += i
      ptmpd -= 1
      if ptmpd == 0:
        tmpid = ""

    elif i == "[" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tmpid = "brac"
      tmp2 += i
      ptmpd += 1

    
    elif i == "]" and tmpid == "brac" and tmpid != "chr" and tmpid != "quote" and tmpid != "paren":
      tmp2 += i
      ptmpd -= 1
      if ptmpd == 0:
        tmpid = ""

    elif i == "'" and tmpid != "chr" and tmpid != "quote" and tmpid != "paren" and tmpid != "brac":
      tmpid = "chr"
      tmp2 += i
    
    elif i == "'" and tmpid == "chr" and tmpid != "quote" and tmpid != "paren" and tmpid != "brac":
      tmpid = ""
      tmp2 += i
    
    elif i == " " and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      #print(tmpid)
      tmp = tmp2
      tmp2 = ""
    
    elif i == "\n" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
     # print("hey")
      tmp = tmp2
      tmp2 = ""
      
    elif i == "+" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_PLUS))
      tmpid = ""
      tmp2 = ""

    elif i == "~" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tmpid = "multiline"

    elif i == "&" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_AMP))
      tmpid = ""
      tmp2 = ""

    elif i == "%" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_MOD))
      tmpid = ""
      tmp2 = ""
      
    elif i == ":" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_COLON))
      tmpid = ""
      tmp2 = ""
      
    elif i == "-" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_MINUS))
      tmpid = ""
      tmp2 = ""

    elif i == "*" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_MUL))
      tmpid = ""
      tmp2 = ""

    elif i == "/" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_DIV))
      tmpid = ""
      tmp2 = ""
      
    elif i == "{" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_LBRACE))
      tmpid = ""
      tmp2 = ""
      
    elif i == "}" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_RBRACE))
      tmpid = ""
      tmp2 = ""
      
    elif i == "=" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_EQUALS))
      tmpid = ""
      tmp2 = ""
    
    elif i == "!" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_DNEQUAL))
      tmpid = ""
      tmp2 = ""

    elif i == ">" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_GRTHAN))
      tmpid = ""
      tmp2 = ""
    
    elif i == "<" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      tokens.append(Token(TT_LTHAN))
      tmpid = ""
      tmp2 = ""
    
    elif i == "," and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      #tokens.append(Token(TT_COMMA))
      tmp = tmp2
      tmpid = "comma"
      
    elif i == ";" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren" and tmpid != "brac":
      #print("hi")
      tmp = tmp2
      tmpid = "semi"
      
    else:
      tmp2 += i

    #print(tmp)

    if len(tmp) >= 4 and re.match(r"^(i8:)\d+$", tmp):
          
      tokens.append(Token(TT_BYTES, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^\d+\.\d+$", tmp):
      print("Found double: {}".format(tmp))
      tokens.append(Token(TT_DEC, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif checkIndexRef(tmp)[0]:
      tokens.append(Token(TT_INDEXREF, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^\[(.*)\]\[(.*\,)*(.*)\]$", tmp):
      #print("hello")
      tokens.append(Token(TT_ARR, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^[-]?[0-9]+$", tmp):
      tokens.append(Token(TT_INTEGER, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^(0[xX])[A-Fa-f0-9]+$", tmp):
      tokens.append(Token(TT_HEX, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^['][^\n][']$", tmp):
      tokens.append(Token(TT_CHAR, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r'^["][^\n]*["]$', tmp):
      tokens.append(Token(TT_STRING, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif tmp in KEYWORDS.values():
      tokens.append(Token(TT_KEYWORD, KEYWORDS[findKeyFromValue(KEYWORDS, tmp)]))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif len(tmp) >= 2 and tmp[0] == "@" and is_valid_variable_name(tmp[1:]):
      tokens.append(Token(TT_AMPOINT, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif is_valid_struct_def(tmp):
      tokens.append(Token(TT_STRUCTDEF, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""
      
    elif len(tmp) >= 2 and tmp[0] == "$" and is_valid_variable_name(tmp[1:]):
      tokens.append(Token(TT_PTR, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif is_valid_variable_name(tmp):
      tokens.append(Token(TT_IDENTIFIER, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif len(tmp) >= 3 and checkFuncCall(tmp)[0]:
      tokens.append(Token(TT_FUNCCALL, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      elif tmpid == "comma":
        tokens.append(Token(TT_COMMA))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""
      
      
  return tokens
  