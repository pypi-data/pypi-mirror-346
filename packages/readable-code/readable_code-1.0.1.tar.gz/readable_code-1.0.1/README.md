
# Overiew

### NO DEPENDENCIES REQUIRED

Joke Python module for making your code *'more readable'*.

Has a weird naming scheme, random abstracted functions for no reason, and anything else that you could ever want!

  

# Functions

  

- **Return_Value_Of(Value)** - Returns Value OFC (useless).

- **Error(Err = Exception)** - Raises an exception (kinda useless).

- **Empty()** - Does nothing (useless).

- **Range(Number) / Len(List) / Int(Number) / String(Message) / Bool(Boolean)  / Float(Decimal) / List(Array) / Print(Message)** - The corresponding function but capitalised.

- **Add(Number_One, Number_Two) / Subtract(Number_One, Number_Two) / Multiply(Number_One, Number_Two) / Divide(Number_One, Number_Two) / Int_Divide(Number_One, Number_Two) / Modulo(Number_One, Number_Two)** - Math operations.

- **Is_Odd(Number) / Is_Even(Number) / Is_Positive(Number) / Is_Negative(Number) / Is_Zero(Number) / Is_Wholly_Divisible(Number_One, Number_Two) / Is_Whole(Number) / Is_Float(Number)** - Math checks.

- **Character_To_Code(Character) / Code_To_Character(Code)** - Character-Code operations.

- **Is_Uppercase(Message) / Is_Lowercase(Message) / Is_Alphabet_Exclusive(Message) / Is_Number_Exclusive(Message) / Is_Alphabet_Number(Message)** - String checks.

- **And(Bool_One, Bool_Two) / Or(Bool_One, Bool_Two) / Not(Bool)** - Bool operations.

- **Print_Multiple_Times(Count, Msg)** - Prints Msg Count amount of times.

- **Sum_Multiple_Numbers(Numbers)** - Sums multiple numbers.

- **Multiply_Multiple_Numbers(Numbers)** - Multiplies multiple numbers.

- **Get_Input_From_User(Message, Type = String)** - Gets an input from the user and applies a function to that input (intended to change the input type which is by default string).

- **If_Selection(Condition, True_Code, False_Code = lambda: Null)** - Creates an if statement that will run the true code if the condition is true, else will run the false code.

- **For_Loop(List, Code, PassElement, Arguments)** - Creates a for loop iterating over a list, where the body code is a function, and the extra arguments (first of which will be the element if PassElement is true) goes into it.

- **While_Loop(Condition, Code, Arguments)** - Creates a while loop which will keep on iterating when the condition *(MUST BE A FUNCTION)* returns true, where the body code is a function and the extra arguments goes into it.

- **Open_File(Name, Mode, Code, Arguments)** - Opens the file with that name in that mode, where the body code is a function *which will always have the file be put into it as the first argument* as well as the extra arguments.

- **Invoke_Function(Function, Arguments)** - Runs the given function with the given arguments.

- **Values_To_List(Values)** - Converts the values given to a list and returns it.

- **Function_Creator(Argument_List, Lambda_List)** - Goes through each lambda function in the lambda list and runs it, feeding in all arguments from the argument list.

There are also 3 values, true, false and none, which are just True, False and None (mimicking how most of python is lowercase except those 3 keywords).



# Challenges



This module could create a few coding challenges such as using its functions as much as possible to make the most 'readable' code, excluding a few functions that could take it out of proportion. If you would like to make reading your code ~~horrible~~ better, this is the perfect opportunity!