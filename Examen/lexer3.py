#RUBEN CUADRA A01019102 - 4/sep/2018
#Lexer for all base 3 numbers, it allows real numbers but it is necessary to have a guarism before the '.'
#The function recieves a string with numbers separated by \s
from re import split,compile
lexer3 = lambda _string, numRegex=compile(r"^(0|1|2)+\.?(0|1|2)*$"): [ n for n in filter(None, split(r"[\s]+",_string)) if numRegex.match(n)]

if __name__ == '__main__':
	res = lexer3("2110.011\t112021 11.\n12.12.32\t13.12\t21.11A .211 0 1. 2 3.")
	print(res)