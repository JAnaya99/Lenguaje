#Autor: Jesus Anaya A00823445
import ply.lex as lex
import ply.yacc as yacc
import sys

#Palabras reservadas
reserved = {
	'var'		: 'VAR',
	'func'		: 'FUNC',
	'int'		: 'INT',
	'double'	: 'DOUBLE',
	'expar'		: 'EXPAR',
	'explog'	: 'EXPLOG',
	'main'		: 'MAINT',
	'call'		: 'CALL',
	'if'		: 'IFT',
	'elif'		: 'ELIFT',
	'else'		: 'ELST',
	'for'		: 'FORT',
	'while'		: 'WHILET',
	'do'		: 'DOT',
	'scan'		: 'SCANT',
	'puts'		: 'PUTST'
}

#Tokens
tokens = [
	'ID',
	'LLLAV',
	'RLLAV',
	'LCOR',
	'RCOR',
	'LPAR',
	'RPAR',
	'COMA',
	'ENDINS',
	'IGUAL',
	'STRING'
] + list(reserved.values())

#Expresiones regulares para tokenizar las entradas.
t_LLLAV		= r'\{'
t_RLLAV		= r'\}'
t_LCOR		= r'\['
t_RCOR		= r'\]'
t_LPAR		= r'\('
t_RPAR		= r'\)'
t_COMA		= r'\,'
t_ENDINS	= r'\;'
t_IGUAL		= r'\='
t_STRING	= r'\".*\"'

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'ID')
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

#Caracteres a ignorar.
t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

#Manejador de errores.
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

#Estructura General.
def p_S(p):
	'''
	S : DEFVAR FUNCIONES MAIN FUNCIONES
	'''
	p[0] = 'CORRECTO'

#Definicion de variables.
def p_DEFVAR(p):
	'''
	DEFVAR : VAR LLLAV VARIABLE RLLAV 
		   | 
	'''
def p_VARIABLE(p):
	'''
	VARIABLE : VARIABLE X ID TIPO ENDINS
			 |
	'''
	print('...................................')
	if(len(p) > 2):
		print("Entre1")
		print("nombre ?", p[0])
		print("Otras variables", p[2])
		print(p[3], " -> ", p[4])

def p_X(p):
	'''
	X : X ID COMA
	  |
	'''
	if len(p) == 1:
		p[0] = ""
	if len(p) > 2:
		if len(p[1]) > 0:
			p[0] = str(p[1]) + ',' + p[2]
		else:
			p[0] = p[2]

#Diferentes tipos de variables.
def p_TIPO(p):
	'''
	TIPO : INT 
	     | DOUBLE
	     | INT ARRAY
	     | DOUBLE ARRAY
	'''
	p[0] = p[1]

def p_ARRAY(p):
	'''
	ARRAY : LCOR EXPAR RCOR 
	      | LCOR EXPAR RCOR LCOR EXPAR RCOR
	      | LCOR EXPAR RCOR LCOR EXPAR RCOR LCOR EXPAR RCOR
	'''

#Definicion de funciones.
def p_FUNCIONES(p):
	'''
	FUNCIONES : FUNCIONES FUNC ID LLLAV ESTATUTOS RLLAV
			  |
	'''
# #Definicion del MAIN.
def p_MAIN(p):
	'''
	MAIN : FUNC MAINT LLLAV ESTATUTOS RLLAV
	'''

#Definicion de Estatutos.
def p_ESTATUTOS(p):
	'''
	ESTATUTOS : ESTATUTOS ASIGNACION
			  | ESTATUTOS LLAMADAS
			  | ESTATUTOS IF
			  | ESTATUTOS FOR
			  | ESTATUTOS WHILE
			  | ESTATUTOS SCAN
			  | ESTATUTOS PUTS
			  |
	'''

#Asignacion a variables.
def p_ASIGNACION(p):
	'''
	ASIGNACION : ID IGUAL EXPAR ENDINS
	           | ID ARRAY IGUAL EXPAR ENDINS
	'''

#Llamada a funciones
def p_LLAMADAS(p):
	'''
	LLAMADAS : CALL ID ENDINS
	'''

# Estructura IF
def p_IF(p):
	'''
	IF : IFT EXPLOG LLLAV ESTATUTOS RLLAV ELIF ELSE
	'''
def p_ELIF(p):
	'''
	ELIF : ELIF ELIFT EXPLOG LLLAV ESTATUTOS RLLAV 
	     |
	'''
def p_ELSE(p):
	'''
	ELSE : ELST LLLAV ESTATUTOS RLLAV
	     | 
	'''

# Estructura ciclo for.
def p_FOR(p):
	'''
	FOR : FORT EXPLOG LLLAV ESTATUTOS RLLAV
	'''
# Estructura ciclo while.
def p_WHILE(p):
	'''
	WHILE : WHILET EXPLOG LLLAV ESTATUTOS RLLAV
	      | DOT LLLAV ESTATUTOS RLLAV WHILET EXPLOG ENDINS
	'''

# Leer de consola.
def p_SCAN(p):
	'''
	SCAN : SCANT LPAR Y ID RPAR ENDINS
	     | SCANT LPAR Y ID ARRAY RPAR ENDINS
	'''
def p_Y(p):
	'''
	Y : Y ID COMA
	  |
	'''

# Imprimir a consola.
def p_PUTS(p):
	'''
	PUTS : PUTST LPAR Z LINE RPAR ENDINS
	'''
def p_Z(p):
	'''
	Z : Z LINE COMA
	  |
	'''
def p_LINE(p):
	'''
	LINE : ID
	     | ID ARRAY
	     | EXPAR
		 | STRING
	'''

def p_error(p):
	if p is not None:
		print("Error en la linea: ", p.lineno)
	else:
		print('Final de archivo no esperado.')
	print('Syntaxis Incorrecta')
	sys.exit()

parser = yacc.yacc()

if __name__ == '__main__':
	try:
		print("Ingrese el nombre del archivo: ")
		nombre = input()
		archivo = open(nombre, 'r')
		codigo = archivo.read()
		if(parser.parse(codigo, tracking=True) == 'CORRECTO'):
			print("Syntaxis Correcta")
	except EOFError:
		print(EOFError)