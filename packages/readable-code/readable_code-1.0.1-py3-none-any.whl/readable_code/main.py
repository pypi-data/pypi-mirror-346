true = True
false = False
none = None

def Return_Value_Of(Value):
  return Value

def Error(Err=Exception):
  raise Err

def Empty():
  pass

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

def Add(Number_One, Number_Two):
  return Number_One + Number_Two

def Subtract(Number_One, Number_Two):
  return Number_One - Number_Two

def Multiply(Number_One, Number_Two):
  return Number_One * Number_Two

def Divide(Number_One, Number_Two):
  return Number_One / Number_Two

def Int_Divide(Number_One, Number_Two):
  return Number_One // Number_Two

def Modulo(Number_One, Number_Two):
  return Number_One % Number_Two

def Is_Odd(Number):
  return Number % 2 == 1

def Is_Even(Number):
  return Number % 2 == 0

def Is_Positive(Number):
  return Number > 0

def Is_Negative(Number):
  return Number < 0

def Is_Zero(Number):
  return Number == 0

def Is_Wholly_Divisible(Number_One, Number_Two):
  return Number_One % Number_Two == 0

def Is_Whole(Number):
  return Number % 1 == 0

def Is_Float(Number):
  return Number % 1 != 0

def Character_To_Code(Character):
  return ord(Character)

def Code_To_Character(Code):
  return chr(Code)

def Is_Uppercase(Message):
  return Message.isupper()

def Is_Lowercase(Message):
  return Message.islower()

def Is_Alphabet_Exclusive(Message):
  return Message.isalpha()

def Is_Number_Exclusive(Message):
  return Message.isdigit()

def Is_Alphabet_Number(Message):
  return Message.isalnum()

def And(Bool_One, Bool_Two):
  return Bool_One and Bool_Two

def Or(Bool_One, Bool_Two):
  return Bool_One or Bool_Two

def Not(Bool):
  return not Bool

def Print_Multiple_Times(Count, Msg):
  For_Loop(Range(Count), lambda Message: Print(Message), Msg)

def Sum_Multiple_Numbers(*Numbers):
  Total = 0
  def Add_To_Total(Number):
    nonlocal Total
    Total += Number
  
  For_Loop(Numbers, Add_To_Total, true)
  return Total

def Multiply_Multiple_Numbers(*Numbers):
  Total = 1
  def Multiply_To_Total(Number):
    nonlocal Total
    Total *= Number
  
  For_Loop(Numbers, Multiply_To_Total, true)
  return Total

def Get_Input_From_User(Message, Type = String):
  return Return_Value_Of(Type(input(Message)))

def If_Selection(Condition, True_Code, False_Code = lambda: none):
  if Condition:
    True_Code()
  else:
    False_Code()

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

def Invoke_Function(Function, *Arguments):
  return Function(*Arguments)

def Values_To_List(*Values):
  return List(Values)

def Function_Creator(Argument_List, Lambda_List):
  For_Loop(Lambda_List, Invoke_Function, true, *Argument_List)