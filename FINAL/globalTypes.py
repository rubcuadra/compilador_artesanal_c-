#Todo lo importante se encuentra en cMinusLexer, esto solo es un archivo requisito de la tarea
from enum import Enum
from .cMinusLexer import eof_symbol

programa = None  #Aqui meteran el programa, tambien requisito del profesor

class TokenType(Enum):
	ENDFILE = eof_symbol