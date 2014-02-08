#!/usr/bin/env python3
from prettyprint import *

from sys import argv
from urllib.error import HTTPError
import urllib.request
import urllib.error
import json
import os
import re

__author__ = 'Adrian Chmielewski-Anders'


def remove_tags(html):
    no_tags = ''
    intag = False
    for i in html:
        if i == '<':
            intag = True
        elif intag and i == '>':
            intag = False
        elif not intag:
            no_tags += i
    return no_tags


def wiki(what):
    cache = os.getenv('HOME') + '/.whatis/wiki/' + what
    if os.path.exists(cache):
        f = open(cache, 'r', encoding='utf-8')
        definition = f.read()
        f.close()
        #return definition
    try:
        resp = urllib.request.urlopen('http://en.wikipedia.org/w/api.php?action=query&titles=' +
                                      what +'&prop=extracts&exintro&exchars=1000&format=json')
    except HTTPError as e:
        print(e)
        return 'The page: ' + 'http://en.wikipedia.org/wiki/' + what + \
               ' does not exist.'
    jsonresp = resp.read().decode('utf-8')
    data = json.loads(jsonresp)['query']
    
    key, page = data['pages'].popitem()
    
    #print(page['extract'])
    
    definition = remove_tags(page['extract'])
    parser = HTMLPrettyPrinter();
    parser.feed(page['extract'])
    print('\033[0m')
    print('Read more at: ' + '\033[31m' + 'http://en.wikipedia.org/wiki/'+what +'\033[0m')
    
    
    f = open(cache, 'w', encoding='utf-8')
    f.write(definition)
    f.close()
    return definition
    return urban(what)


def urban(word, user=0):
    cache = os.getenv('HOME') + '/.whatis/urban/' + word + '_' + str(user)
    if os.path.exists(cache):
        f = open(cache, 'r', encoding='utf-8')
        definition = f.read()
        f.close()
        return definition
    resp = urllib.request.urlopen(
        'http://api.urbandictionary.com/v0/define?term='
        + word)
    j = resp.read().decode('utf-8')
    definitions = json.loads(j)
    if definitions['result_type'] == 'no_results':
        return "There were no results found for " + word
    if user > len(definitions['list']):
        user = len(definitions['list']) - 1
    return_string = 'Definition:\n'
    return_string += definitions['list'][user]['definition']
    return_string += '\nExample:\n' + definitions['list'][user]['example']
    f = open(cache, 'w', encoding='utf-8')
    f.write(return_string)
    f.close()
    return return_string


def main():
    print('\033[34m') #let's get some green
    if not os.path.exists(os.getenv('HOME') + '/.whatis/wiki'):
        os.makedirs(os.getenv('HOME') + '/.whatis/wiki')
    if not os.path.exists(os.getenv('HOME') + '/.whatis/urban'):
        os.makedirs(os.getenv('HOME') + '/.whatis/urban')
    if argv[1] == '-u':
        matches = re.findall(r'-[0-9]+', argv[2])
        if len(matches) == 0:
            print(urban(argv[2]))
        elif len(matches) > 0:
            print(urban(argv[3], int(matches[0][1:])))
    else:
        args = ''
        for arg in argv[1:]:
            if arg == argv[1]:
                args += arg
            else:
                args += '_' + arg
        wiki(args)
    print('\033[0m')
    
    
    


if __name__ == '__main__':
    main()
