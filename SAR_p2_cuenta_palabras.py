#! -*- encoding: utf8 -*-

## Nombres: JOAN VIDAL CARBO

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import os
import re
import operator
from typing import Optional

def sort_dic_by_values(d:dict) -> list:
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename:str, stats:dict, use_stopwords:bool, full:bool):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """

        with open(filename, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('Lines: ' + str(stats['nlines']) + '\n')
            fh.write('Number words (including stopwords): ' + str(stats['nwords']) + '\n')
            fh.write('Vocabulary size: ' + str(len(stats.get('word', {}))) + '\n')
            
            if use_stopwords:
                fh.write('Numero de palabras (sin stopwords): ' + str(stats['wordS']) + '\n')
            fh.write('Number of symbols: ' + str(stats['symbol']) + '\n')
            fh.write('Number of different symbols: ' + str(len(stats.get('symbolD', {}))) + '\n')
            #fh.write('Número de prefijos: ' + str(stats['prefix']) + '\n')
            #fh.write('Número de sufijos: ' + str(stats['suffix']) + '\n')

            fh.write('Words (alphabetical order):\n')
            dicpalabras = sorted(stats["word"].items())
            i = 0
            for palabra in dicpalabras:
                fh.write("\t" + palabra[0] + ": " + str(palabra[1]) + "\n")
                i += 1
                if not full and i >=20:
                    break
            pass
 
            fh.write('Words (by frequency):\n')
            dicpalabras = sorted(stats['word'].items(), key = lambda v: (-v[1],v[0]))
            #dicpalabras = sorted(stats['word'].items(), key=operator.itemgetter(1), reverse=True)

            i = 0
            for palabra in dicpalabras:
                fh.write('\t' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                i = i + 1
                if full == False and i >= 20:
                    break
            pass
            fh.write('Symbols (alphabetical order):\n')
            dicpalabras = sorted(stats["symbolD"].items())
            i = 0
            for palabra in dicpalabras:
                fh.write('\t' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                i = i + 1
                if full == False and i>= 20:
                    break

            pass
            fh.write('Symbols (by frequency):\n')
            dicpalabras = sorted(stats["symbolD"].items(),  key = lambda v: (-v[1],v[0]))
            i = 0
            for palabra in dicpalabras:
                fh.write('\t' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                i = i + 1
                if full == False and i>= 20:
                    break
            pass

            


            #BIGRAMAS
            if 'biword' and 'bisymbol' in stats:
                fh.write('Word pairs (alphabetical order):\n')
                dicpalabras = sorted(stats["biword"].items())
                i = 0
                for palabra in dicpalabras:
                    fh.write('\t' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                    i = i + 1
                    if full == False and i>= 20:
                        break
                
                pass
                
                fh.write('Word pairs (by frequency):\n')

                
                dicpalabras = sorted(stats["biword"].items(), key = lambda v: (-v[1],v[0]))
                i = 0
                for palabra in dicpalabras:
                    fh.write('\t' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                    i = i + 1
                    if full == False and i>= 20:
                        break
                pass

                fh.write('Symbol pairs (alphabetical order):\n')
                dicpalabras = sorted(stats["bisymbol"].items())
                i = 0
                for palabra in dicpalabras:
                    fh.write('\t' + palabra[0].replace(' ', '') + ': ' + str(palabra[1]) + '\n')
                    i = i + 1
                    if full == False and i>= 20:
                        break
                
                pass

                fh.write('Symbol pairs (by frequency):\n')
                dicpalabras = sorted(stats["bisymbol"].items(), key = lambda v: (-v[1],v[0]))
                i = 0
                for palabra in dicpalabras:
                    fh.write('\t' + palabra[0].replace(' ', '') + ': ' + str(palabra[1]) + '\n')
                    i = i + 1
                    if full == False and i>= 20:
                        break
                
                pass
            fh.write('Prefixes (by frequency):\n')
            dicpalabras = sorted(stats["prefix"].items(), key = lambda v: (-v[1],v[0]))
            i = 0
            for palabra in dicpalabras:
                fh.write('\t' + palabra[0] + '-: ' + str(palabra[1]) + '\n')
                i = i + 1
                if full == False and i>= 20:
                    break
            pass
            
            fh.write('Suffixes (by frequency):\n')
            dicpalabras = sorted(stats["suffix"].items(), key = lambda v: (-v[1],v[0]))
            i = 0
            for palabra in dicpalabras:
                fh.write('\t' + '-' + palabra[0] + ': ' + str(palabra[1]) + '\n')
                i = i + 1
                if full == False and i>= 20:
                    break
            pass
            
    def file_stats(self, fullfilename:str, lower:bool, stopwordsfile:Optional[str], bigrams:bool, full:bool):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            fullfilename: el nombre del fichero, puede incluir ruta.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile, encoding='utf-8').read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'wordS': {},
                'symbol': 0, 
                'symbolD': {},
                'prefix': {},
                'suffix': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        # COMPLETAR
        # AYUDA: line = self.clean_re.sub(' ', line)
        with open(fullfilename, 'r') as f:
            
            for line in f:
                sts['nlines'] = sts.get("nlines", 0) + 1
                if lower:
                    line = line.lower()
                line = self.clean_re.sub(' ', line)
                palabras = line.split()
                for p in range(len(palabras)):
                    sts['nwords'] = sts.get("nwords", 0) + 1
                    if palabras[p] not in stopwords:

                        sts['wordS'][palabras[p]] = sts["wordS"].get("wordS", 0) + 1
                        
                        sts['word'][palabras[p]] = sts["word"].get(palabras[p], 0) + 1
                        for symbol in palabras[p]:
                            sts['symbol'] = sts.get("symbol", 0) + 1 #simbolos
                            sts['symbolD'][symbol] = sts["symbolD"].get(symbol, 0) + 1    
                        
                        if len(palabras[p]) > 4: # para las palabras de mas de 4 letras se añaden todos sus sufijos
                            p =palabras[p]
                            prefix = p[0:4]
                            prefix3 = p[0:3]
                            prefix2 = p[0:2]
                            sts['prefix'][prefix] = sts['prefix'].get(prefix, 0) + 1 
                            sts['prefix'][prefix3] = sts['prefix'].get(prefix3, 0) + 1 
                            sts['prefix'][prefix2] = sts['prefix'].get(prefix2, 0) + 1 

                            suffix = p[-4:]
                            suffix3 = p[-3:]
                            suffix2 = p[-2:]
                            sts['suffix'][suffix] = sts['suffix'].get(suffix, 0) + 1 
                            sts['suffix'][suffix3] = sts['suffix'].get(suffix3, 0) + 1 
                            sts['suffix'][suffix2] = sts['suffix'].get(suffix2, 0) + 1 
                        elif len(palabras[p]) > 3:
                                p =palabras[p]
                                prefix = p[0:3]
                                prefix2 = p[0:2]
                                sts['prefix'][prefix2] = sts['prefix'].get(prefix2, 0) + 1
                                sts['prefix'][prefix] = sts['prefix'].get(prefix, 0) + 1 
                                suffix = p[-3:]
                                suffix2 = p[-2:]
                                sts['suffix'][suffix] = sts['suffix'].get(suffix, 0) + 1
                                sts['suffix'][suffix2] = sts['suffix'].get(suffix2, 0) + 1 

                        elif len(palabras[p]) > 2:
                                    p =palabras[p]
                                    prefix = p[0:2]
                                    suffix = p[-2:]
                                    sts['suffix'][suffix] = sts['suffix'].get(suffix, 0) + 1 
                                    sts['prefix'][prefix] = sts['prefix'].get(prefix, 0) + 1 
    
        pass
        

        #BIGRAMAS
        
        with open(fullfilename, 'r') as f:
            if bigrams:

                for line in f:
                    line = self.clean_re.sub(' ', line)
                    if len(line) > 1:
                        line = '$ ' + line + '$'
                    if lower:
                        line = line.lower()
                    for palabra in range(len(stopwords)):
                        line = re.sub(" " + stopwords[s] + " ")
                    words = line.split()

                    for p in range(len(words) - 1):
                        if words[p] not in stopwords and words[p+1] not in stopwords:
                            par1, par2 = words[p:p+2]
                            sts['biword'][par1 + ' ' + par2] = sts['biword'].get(par1 + ' ' + par2, 0) + 1
                            for symbolD in range(len(words[p]) - 1):

                                x = words[p][symbolD]
                                num = words[p][symbolD + 1]
                                sts['bisymbol'][x + ' ' + num] = sts['bisymbol'].get(x + ' ' + num, 0) + 1
        pass

        filename, ext0 = os.path.splitext(fullfilename)#separa entre el nombre y la extension del texto
        new_filename = filename + '_'
        barra= True
        if lower:
            new_filename = new_filename + 'l'
            barra = False
        if stopwords:
            new_filename = new_filename + 's'
            barra = False
        if bigrams:
            new_filename = new_filename + 'b'
            barra = False
        if full:
            new_filename = new_filename + 'f'
            barra = False
        if not barra:
            new_filename = new_filename + '_'
        new_filename = new_filename + 'stats.' + ext0
        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames:str, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)
