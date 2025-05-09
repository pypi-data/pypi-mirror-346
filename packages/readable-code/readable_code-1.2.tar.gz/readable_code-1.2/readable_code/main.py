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

def Uppercase(Message):
  return Message.upper()

def Lowercase(Message):
  return Message.lower()

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

def Equal(Bool_One, Bool_Two):
  return Bool_One == Bool_Two

def Not_Equal(Bool_One, Bool_Two):
  return Bool_One != Bool_Two

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

def If_Selection(Condition, True_Code, True_Argument_List = [], False_Code = lambda: none, False_Argument_List = []):
  if Condition:
    True_Code(*True_Argument_List)
  else:
    False_Code(*False_Argument_List)

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

def Lambda_Creator(Argument_List, Return_Value):
  return eval(f"lambda {', '.join(Argument_List)}: {Return_Value}")

def Function_Creator(Lambda_List, Return_Value = lambda: null):
  def Function(*Argument_List):
    For_Loop(Lambda_List, Invoke_Function, true, *Argument_List)
    return Return_Value(*Argument_List)
  
  return Function

def Class_Creator(Class_Property_List, Class_Values_List, Instance_Property_List, String_Representation):
  class Class:
    @classmethod
    def Set_Class_Properties(Cls):
      nonlocal Class_Property_List, Class_Values_List
      
      for Position in Range(Len(Class_Property_List)):
        setattr(Cls, Class_Property_List[Position], Class_Values_List[Position])
    
    def __init__(Self, *Properties):
      nonlocal Instance_Property_List
      
      for Position in Range(Len(Instance_Property_List)):
        setattr(Self, Instance_Property_List[Position], Properties[Position])
    
    def __str__(Self):
      nonlocal String_Representation
      
      return eval("f'" + String_Representation + "'")
  
  Class.Set_Class_Properties()
  return Class