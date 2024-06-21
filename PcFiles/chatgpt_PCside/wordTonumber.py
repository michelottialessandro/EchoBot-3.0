import word2number
import word2number.w2n

#print(word2number.w2n.word_to_num("seventy five"))


### TODO: all numbers written like numbers must be converted into words

class InvalidExpressionError(Exception):
    def __init__(self, message):
        super().__init__(message)


def check_if_number_is_splitted(original_string,numbers,expression,litteral_operator):
    
    print(numbers)
    print(expression)
    print(litteral_operator)
    operator_counter=0
    
    new_splitted_string=[]
    
    correct_numbers=[]
    
    for el in expression:
        
        if(type(el)==str):
            if(operator_counter<1):
                operator_position=expression.index(el)
                operator_counter=operator_counter+1
            else:
                raise InvalidExpressionError("More than one operator")
    
    
    
    new_splitted_string=original_string.split(litteral_operator)
    
    print(new_splitted_string)
    
    correct_numbers.append(word2number.w2n.word_to_num(new_splitted_string[0]))
    
    correct_numbers.append(word2number.w2n.word_to_num(new_splitted_string[1]))
    
    return correct_numbers
    
    
        
def create_expression(string):
    
    string=string.replace("?", "")

    
    parts=string.split()
    
    numbers=[]
    
    operator=""
    
    expression=[]
    
    litteral_operator=""
    
    
    for el in parts:
        try:
            number=(word2number.w2n.word_to_num(el))
            expression.append(number)
            numbers.append(number)
           
        except ValueError:
            print(operator)
            
            if(el=="plus"):
                operator="+"
                expression.append(operator)
                litteral_operator=el
            elif(el=="minus"):
                operator="-"
                expression.append(operator)
                litteral_operator=el
            elif(el=="times"):
                operator="*"
                expression.append(operator)
                litteral_operator=el
            elif(el=="divided"):
                operator="/"
                expression.append(operator)
                litteral_operator=el
            elif(el=="power"):
                operator="**"
                expression.append(operator)
                litteral_operator=el

    
    if (len(numbers)<2):
        raise InvalidExpressionError("Invalid numbers")
    
    if(len(numbers)>2):
        print("i think a correction is needed")
        corrected_numbers=check_if_number_is_splitted(original_string=string,numbers=numbers,expression=expression,litteral_operator=litteral_operator)
    
        if(len(corrected_numbers)==2):
            print(f"list numbers before correction: {numbers}")
            numbers[0]=corrected_numbers[0]
            numbers[1]=corrected_numbers[1]
            print(f"list numbers after correction: {numbers}")

    
    if(operator==""):
        raise InvalidExpressionError("The operator is missing or unknown")
    
    if(operator=="+"):
        result=numbers[0]+numbers[1]
    elif(operator=="-"):
        result=numbers[0]-numbers[1]
    elif(operator=="*"):
        result=numbers[0]*numbers[1]
    elif(operator=="**"):
        result=numbers[0]**numbers[1]
    elif(operator=="/"):
        if(numbers[1]!=0):
            result=numbers[0]/numbers[1]
        else:
            result="Math Error division by zero"
    
    return result
    
# while True:
#     string=input("Insert an expression: ")

#     result=create_expression(string)

#     print(result)


