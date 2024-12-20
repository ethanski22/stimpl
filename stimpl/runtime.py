from typing import Any, Tuple, Optional


from stimpl.expression import *
from stimpl.types import *
from stimpl.errors import *

"""
Interpreter State
"""


class State(object):
    def __init__(self, variable_name: str, variable_value: Expr, variable_type: Type, next_state: 'State') -> None:
        self.variable_name = variable_name
        self.value = (variable_value, variable_type)
        self.next_state = next_state

    def copy(self) -> 'State':
        variable_value, variable_type = self.value
        return State(self.variable_name, variable_value, variable_type, self.next_state)

    def set_value(self, variable_name, variable_value, variable_type):
        return State(variable_name, variable_value, variable_type, self)

    '''
    Get value gets the value of the variable given

    The paramater is a variable name

    If the variable name given matches the variable name of the
    current instance, return its stored value
    Else call get value on the next state

    Returns the value of the variable if found
    '''
    def get_value(self, variable_name) -> Any:
        """ TODO: Implement. """
        if variable_name == self.variable_name:
            return self.value
        else:
            return self.next_state.get_value(variable_name)

    def __repr__(self) -> str:
        return f"{self.variable_name}: {self.value}, " + repr(self.next_state)


class EmptyState(State):
    def __init__(self):
        pass

    def copy(self) -> 'EmptyState':
        return EmptyState()

    def get_value(self, variable_name) -> None:
        return None
 
    def __repr__(self) -> str:
        return ""


"""
Main evaluation logic!
"""


def evaluate(expression: Expr, state: State) -> Tuple[Optional[Any], Type, State]:
    match expression:
        case Ren():
            return (None, Unit(), state)

        case IntLiteral(literal=l):
            return (l, Integer(), state)

        case FloatingPointLiteral(literal=l):
            return (l, FloatingPoint(), state)

        case StringLiteral(literal=l):
            return (l, String(), state)

        case BooleanLiteral(literal=l):
            return (l, Boolean(), state)

        case Print(to_print=to_print):
            printable_value, printable_type, new_state = evaluate(
                to_print, state)

            match printable_type:
                case Unit():
                    print("Unit")
                case _:
                    print(f"{printable_value}")

            return (printable_value, printable_type, new_state)


            '''
            Handles whether sequence or program is the input

            Iterates through each expression in exprs, evaluating them in sequence
            Updates the current state after each expression evaluation
            Tracks the result value and type of each evaluated expression 
            with the final expression's result being returned

            Returns a tuple containg the result value, type and the current state
            '''
        case Sequence(exprs=exprs) | Program(exprs=exprs):
            """ TODO: Implement. """
            current_state = state
            result_value, result_type = None, Unit()
            for expr in exprs:
                result_value, result_type, current_state = evaluate(expr, current_state)
            return (result_value, result_type, current_state)

        case Variable(variable_name=variable_name):
            value = state.get_value(variable_name)
            if value == None:
                raise InterpSyntaxError(
                    f"Cannot read from {variable_name} before assignment.")
            variable_value, variable_type = value
            return (variable_value, variable_type, state)

        case Assign(variable=variable, value=value):

            value_result, value_type, new_state = evaluate(value, state)

            variable_from_state = new_state.get_value(variable.variable_name)
            _, variable_type = variable_from_state if variable_from_state else (
                None, None)

            if value_type != variable_type and variable_type != None:
                raise InterpTypeError(f"""Mismatched types for Assignment:
            Cannot assign {value_type} to {variable_type}""")

            new_state = new_state.set_value(
                variable.variable_name, value_result, value_type)
            return (value_result, value_type, new_state)

        case Add(left=left, right=right):
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Add:
            Cannot add {left_type} to {right_type}""")

            match left_type:
                case Integer() | String() | FloatingPoint():
                    result = left_result + right_result
                case _:
                    raise InterpTypeError(f"""Cannot add {left_type}s""")

            return (result, left_type, new_state)
        
            '''
            The inputs to the subtract function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is an int or a fp then subtract the right 
            value from the left value
            If not then we throw a type error

            Return the result and the type
            '''
        case Subtract(left=left, right=right):
            """ TODO: Implement. """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Subtract:
            Cannot subtract {left_type} to {right_type}""")

            match left_type:
                case Integer() | FloatingPoint():
                    result = left_result - right_result
                case _:
                    raise InterpTypeError(f"""Cannot subtract {left_type}s""")

            return (result, left_type, new_state)

            '''
            The inputs to the mutiply function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is an int or a fp then multiply the left and
            right values 
            If not then we throw a type error

            Return the result and the type
            '''
        case Multiply(left=left, right=right):
            """ TODO: Implement. """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Multiply:
            Cannot multiply {left_type} to {right_type}""")

            match left_type:
                case Integer() | FloatingPoint():
                    result = left_result * right_result
                case _:
                    raise InterpTypeError(f"""Cannot multiply {left_type}s""")

            return (result, left_type, new_state)

            '''
            The inputs to the divide function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the right value is 0 then throw a divide by zero error

            If the type is an int or a fp then divide the left and
            right values 
            If not then we throw a type error

            Return the result and the type
            '''
        case Divide(left=left, right=right):
            """ TODO: Implement. """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Divide:
            Cannot divide {left_type} to {right_type}""")

            if right_result == 0:
                raise InterpMathError(f"""Cannot Divide by 0""")

            match left_type:
                case Integer():
                    result = left_result // right_result
                case FloatingPoint():
                    result = left_result / right_result
                case _:
                    raise InterpTypeError(f"""Cannot divide {left_type}s""")

            return (result, left_type, new_state)

        case And(left=left, right=right):
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for And:
            Cannot evaluate {left_type} and {right_type}""")
            match left_type:
                case Boolean():
                    result = left_value and right_value
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical and on non-boolean operands.")

            return (result, left_type, new_state)
        
            '''
            The inputs to the or function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the or operation
            If not then throw an error

            Return the result and the type
            '''
        case Or(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Or:
            Cannot evaluate {left_type} or {right_type}""")
            match left_type:
                case Boolean():
                    result = left_value or right_value
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical or on non-boolean operands.")
                
            return (result, left_type, new_state)

            '''
            The input to the not function is an expression

            Define the expression value, type and the new state 
            by evaluating the expression and the state

            If the type is a bool then continue with the not operation
            If not then throw an error

            Return the result and the type
            '''
        case Not(expr=expr):
            """ TODO: Implement. """
            expr_value, expr_type, new_state = evaluate(expr, state)
            
            match expr_type:
                case Boolean():
                    result = not(expr_value)
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical not on non-boolean operands.")
                
            return (result, expr_type, new_state)
        
            '''
            The input to the or function is a condition

            Define the condition value, type and the new state 
            by evaluating the condition and the state

            If the type is a bool then continue with the if expression
            If not then throw an error

            Return true or false based on the condition
            '''
        case If(condition=condition, true=true, false=false):
            """ TODO: Implement. """
            cond_result, cond_type, new_state = evaluate(condition, state)

            match cond_type:
                case Boolean():
                    result = cond_result
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical if on non-boolean operands.")
                
            if result:
                return evaluate(true, new_state)
            return evaluate(false, new_state)

        case Lt(left=left, right=right):
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value < right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform < on {left_type} type.")

            return (result, Boolean(), new_state)

            '''
            The inputs to the lte function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the lte operation
            If not then throw an error

            Return the result and the type
            '''
        case Lte(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lte:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value <= right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform <= on {left_type} type.")
                
            return (result, Boolean(), new_state)

            '''
            The inputs to the gt function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the gt operation
            If not then throw an error

            Return the result and the type
            '''
        case Gt(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Gt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value > right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform > on {left_type} type.")
                
            return (result, Boolean(), new_state)

            '''
            The inputs to the gte function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the gte operation
            If not then throw an error

            Return the result and the type
            '''
        case Gte(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Gte:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value >= right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform >= on {left_type} type.")
                
            return (result, Boolean(), new_state)

            '''
            The inputs to the eq function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the eq operation
            If not then throw an error

            Return the result and the type
            '''
        case Eq(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Gte:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value == right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform == on {left_type} type.")
                
            return (result, Boolean(), new_state)

            '''
            The inputs to the ne function are the
            left and right arguments

            Define the left restult and type as well as the right
            value and type along with their new states

            Check to see if the types of the left and right match

            If the type is a bool then continue with the ne operation
            If not then throw an error

            Return the result and the type
            '''
        case Ne(left=left, right=right):
            """ TODO: Implement. """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = (left_value != right_value)
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform != on {left_type} type.")
                
            return (result, Boolean(), new_state)

            '''
            The inputs to the while function are the
            condition and body

            Define the condition restult and type as well as the new state
            by evaluating the contition and current state

            If the type is a bool then continue with the while operation
            If not then throw an error

            In the while loop define the body result and type and the 
            condition result and type by evaluating the body and condition
            with the new state

            Return the result and the type
            '''
        case While(condition=condition, body=body):
            """ TODO: Implement. """
            cond_result, cond_type, new_state = evaluate(condition, state)

            match cond_type:
                case Boolean():
                    result = cond_result
                case _:
                    raise InterpTypeError("While loop requires a boolean condition.")
                
            while result:
                body_result, body_type, new_state = evaluate(body, new_state)
                cond_result, cond_type, new_state = evaluate(condition, new_state)

                match cond_type:
                    case Boolean():
                        result = cond_result
                    case _:
                        raise InterpTypeError("While loop requires a boolean condition.")
                
            return (result, cond_type, new_state)

        case _:
            raise InterpSyntaxError("Unhandled!")
    pass


def run_stimpl(program, debug=False):
    state = EmptyState()
    program_value, program_type, program_state = evaluate(program, state)

    if debug:
        print(f"program: {program}")
        print(f"final_value: ({program_value}, {program_type})")
        print(f"final_state: {program_state}")

    return program_value, program_type, program_state
