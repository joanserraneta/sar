#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin
# AUTOR JOAN VIDAL CARBO 
#@JOAVICAR

import re
import sys
from typing import Optional, Text
from os.path import isfile

class Translator():

    def __init__(self, punt:Optional[Text]=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word:Text) -> Text:
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        new_word = word 

        #VOCALES
        patronMinus = r'^[aeiouy]\w*' #empiezan por minuscula
        patSoloMayus = r'^[AEIOUY][a-z]+$' #empiezan por mayuscula
        patMayus = r'^[AEIOUY].*' #toda la palabra en mayuscula
        
        matchmayus = re.match(patMayus, new_word)
        matchminus = re.match(patronMinus, new_word)
        matchSoloMayus = re.match(patSoloMayus, new_word)

        if matchminus:  #empiezan por minuscula
            new_word = new_word + "yay"
        elif matchSoloMayus: #empiezan por mayuscula
             new_word = new_word + "yay"
        elif matchmayus: #toda la palabra en mayuscula
            new_word = new_word + "YAY"
       
        #CONSONANTES

        
        patCon = r'^([^aeiouyAEIOUY]+)(.*)$'
        
        matchCon = re.match(patCon, new_word)

        
        if matchCon:
            consonantes = matchCon.group(1) #primeras consonantes
            resto =matchCon.group(2) #hasta la primera vocal
            
            if consonantes.isupper() and resto.isupper(): #todas mayuscula
                new_word = resto + consonantes + "AY"
                return new_word
            elif consonantes[0].isupper(): #solo la primera es mayuscula
                consonantes = consonantes.lower()
                resto = resto.capitalize()
                new_word = resto + consonantes + "ay"
            elif consonantes.islower(): # son minusculas
                new_word = resto + consonantes + "ay"



        
        return new_word

    def translate_sentence(self, sentence:Text) -> Text:
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """
        puntuaciones = [",", ".", ";", "!", "?"]
        new_sentence = sentence 
        frase = new_sentence.split()
        frase_nueva = ""
        palabra_trad= ""
        for palabra in frase:
            signo_puntuacion = ""
            if palabra[-1] in puntuaciones: #si la palabra tiene un signo de puntuación al final este se separa
                signo_puntuacion= palabra[-1]
                palabra = palabra[:-1]

            palabra_trad = t.translate_word(palabra) #se traduce
            palabra_trad += signo_puntuacion #y se vuelve a unir
            frase_nueva += palabra_trad + " " # aqui se unen las palabra traducidas
        frase_nueva = frase_nueva.strip() #y aqui quitamos los espacion en blanco indeseables
        

        return frase_nueva

    def translate_file(self, filename:Text):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: None 
        """
        
        if not isfile(filename):
            print(f'{filename} no existe o no es un nombre de fichero', file=sys.stderr)

        output_filename = f'{filename.split(".")[0]}_piglatin.txt'

        with open(filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        # lee cada linea del archivo original
            for line in input_file:
                # traduce la linea a Pig Latin y la escribe en el archivo de salida
                translated_line = t.translate_sentence(line.strip())
                output_file.write(translated_line + '\n')

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
