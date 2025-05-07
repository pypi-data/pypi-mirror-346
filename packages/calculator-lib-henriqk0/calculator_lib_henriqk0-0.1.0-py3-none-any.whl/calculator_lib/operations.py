def sum_to_api(first_value, second_value):
    return first_value + second_value;

def subtract_to_api(first_value, second_value):
    return first_value - second_value;

def multiply_to_api(first_value, second_value):
    return first_value * second_value;

def divide_to_api(first_value, second_value):
    if (second_value == 0 and first_value == 0): raise ValueError("ERRO: Indefinição (0/0)");
    if (second_value == 0): raise ValueError('ERRO: Não é possível dividir por 0.');
    return first_value / second_value;     
    
def sqrt_to_api(first_value, second_value):
    if (second_value == 0): raise ValueError("ERRO: Raiz indefinida com índice 0");
    return (first_value ** (1/second_value));

def pow_to_api(first_value, second_value):
    if (second_value == 0 and first_value == 0): raise ValueError("ERRO: Indefinição (0 elevado a 0)") ;
    if (second_value == 0): return 1;
    return first_value ** second_value;
    