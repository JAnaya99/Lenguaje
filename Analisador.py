#Autor: Jesus Anaya A00823445
import ply.lex as lex
import ply.yacc as yacc
import sys

#Tabla de Simbolos.
sim_tab = {}

#Arreglo de erroes.
errores = []

#Palabras reservadas
reserved = {
	'var'		: 'VAR',
	'func'		: 'FUNC',
	'int'		: 'INT',
	'or'		: 'ORT',
	'and'       : 'ANDT',
	'double'	: 'DOUBLE',
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
	'STRING',
	'NUMERO',
	'DNUMERO',
	'SUMRES',
	'MULTDIV',
	'OPREL',
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
t_SUMRES 	= r'\+|\-'
t_MULTDIV	= r'\*|\/|\%|\^'
t_OPREL		= r'\<|\>|\=\=|\<\=|\>\='

def t_DNUMERO(t):
	r'\-?\d+\.\d+'
	return t

def t_NUMERO(t):
	r'\-?\d+'
	return t

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

#Funciones auxiliares.
#Funcion que permite transformar una lista de ID y guardarlas en la tabla de simbolos.
def ToSimbolTable(ids, tipo):
	lista_ids = ids.split(',')
	for x in lista_ids:
		if x in sim_tab:
			return False
		sim_tab[x] = tipo
	return True

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
			 | VARIABLE X ID TIPO ARRAY ENDINS
			 |
	'''
	if len(p) > 2:
		#Adjuntar , + id.
		if len(p[2]) > 0:
			p[2] = str(p[2]) + ',' + p[3]
		else: #Adjuntar solo id.
			p[2] =  p[3]
		#Ver si es un arreglo o una variable normal.
		if len(p) == 6:
			if not ToSimbolTable(str(p[2]), str(p[4])):
				errores.append("Error variable repetida en linea: " + str(p.lexer.lineno - 1))

def p_X(p):
	'''
	X : X ID COMA
	  |
	'''
	#Recursivamente buscar todos los id en una misma linea.
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
	PUTS : PUTST LPAR Z EXPAR RPAR ENDINS
	     | PUTST LPAR Z STRING RPAR ENDINS
	'''
def p_Z(p):
	'''
	Z : Z STRING COMA
	  | Z EXPAR COMA 
	  |
	'''
# Expresion aritmetica.
def p_EXPAR(p):
	'''
	EXPAR : EXPAR SUMRES T
          | T
	'''

def p_T(P):
	'''
	T : T MULTDIV F
	T : F
	'''

def p_F(p):
	'''
	F : CTE
      | LPAR EXPAR RPAR 
	'''


def p_CTE(p):
	'''
	CTE : ID
	    | ID ARRAY
	    | DNUMERO
		| NUMERO
	'''

def p_EXPLOG(p):
	'''
	EXPLOG : EXPLOG ORT TL
	       | TL
	'''

def p_TL(p):
	'''
	TL : TL ANDT FL
	   | FL 
	'''

def p_FL(p):
	'''
	FL : LPAR EXPLOG RPAR
	   | CTE OPREL CTE
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
			if(len(errores) > 0):
				print("Syntaxis Incorrecta")
				#Lista de errores
				for x in errores:
					print(x)
				sys.exit()
			else:
				print("Syntaxis Correcta")
		#Imprimir variables
		print("Variables declaradas:")
		for x,y in sim_tab.items():
			print(x, " -> ", y)
	except EOFError:
		print(EOFError)