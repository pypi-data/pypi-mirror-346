def Return_Value_Of(Value):
  return Value

def Error(Err=Exception):
  raise Err

def Range(Number):
  return range(Number)

def Len(List):
  return len(List)

def Int(Number):
  return int(Number)

def String(Message):
  return str(Message)

def Bool(Boolean):
  return bool(Boolean)

def Float(Decimal):
  return float(Decimal)

def List(Array):
  return list(Array)

def Print(Message):
  print(Message)

def Print_Multiple_Times(Count, Msg):
  For_Loop(Range(Count), lambda Message: Print(Message), Msg)

def Sum_Multiple_Numbers(*Numbers):
  Total = 0
  def Add_To_Total(Number):
    nonlocal Total
    Total += Number
  
  For_Loop(Numbers, Add_To_Total, True)
  return Total

def Multiply_Multiple_Numbers(*Numbers):
  Total = 1
  def Multiply_To_Total(Number):
    nonlocal Total
    Total *= Number
  
  For_Loop(Numbers, Multiply_To_Total, True)
  return Total

def Get_Input_From_User(Message, Type = String):
  return Return_Value_Of(Type(input(Message)))

def For_Loop(List, Code, PassElement, *Arguments):
  for Element in List:
    if PassElement: Code(Element, *Arguments)
    else: Code(*Arguments)

def While_Loop(Condition, Code, *Arguments):
  while Condition():
    Code(*Arguments)

def Open_File(Name, Mode, Code, *Arguments):
  with open(Name, Mode) as File:
    Code(File, *Arguments)