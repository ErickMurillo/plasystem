#! /usr/bin/env python
# -*- coding: utf-8 -*-

# l = ["hola", "jaja", "lol"]

# l1 = [1,2,3]

# t = (4,5,6)

# d = {"primero" : l1,"segundo" : l, "tercero" : t}

# print d["primero"][2]
# print d["segundo"][1]
# print d["tercero"]


def max(x,y):

	if x > y:
		print str(x) + " Es mayor a " + str(y)
	else:
		print str(y) + " Es mayor a " + str(x)


def max_de_tres(x,y,z):
	if x > y and x > z:
		print "X es el mayor= " + str(x)
	elif y > x and y > z:
		print "Y es el mayor= " + str(y)
	else: 
		print "Z es el mayor= " + str(z)



def leng(l):
	c=0
	for elemento in l:
		c = c + 1
	print c



def letra(letra):
	if letra ==  "a" or letra ==  "e" or letra ==  "i" or letra ==  "o" or letra ==  "u":
		print  "True"
	else:
		print "False" 
	



def sum(l):
	r = 0 
	for i in l:
		r += i
	print str(r)



def mult(l):
	r = 1 
	for i in l:
		r *= i
	print str(r)



def inversa(l):
	invertida = ""
	count = len(l)
	i = -1
	while count>=1:
		invertida += l[i]
		i += -1
		count -= 1
	print invertida



def es_palindromo(l):
	invertida = ""
	count = len(l)
	i = -1
	while count>=1:
		invertida += l[i]
		i += -1
		count -= 1
	if invertida == l:
		print "True"
	else:
		print "False"



def generar_n_caracteres(x):
	letra = "x"
	print letra*x



def procedimiento(l):
	letra = "x"
	count = len(l)
	elem = 0 
	if count>=1:
		for i in l:
			print str(letra*l[elem])
			elem += 1


def superposicion(x,y):
    for i in x:
        for j in y:
            if i == j:
                print "true"
    print "false"

superposicion([8,12,8],[8,1,3])

