# Simple extended boolean search engine: indexer based on cranfield format
# Hussein Suleman
# 21 April 2016

import os
import re
import sys

import porter

import parameters

# check parameter for collection name
if len(sys.argv)==1:
   print ("Syntax: index.py <collection>")
   exit(0)
collection = sys.argv[1]

# read and parse input data - extract words, identifiers and titles
f = open (collection, "r") #open the collection for reading; collection here refers to the document e.g apples
identifier = '' #intilaise the identifier
document = '' #initalize the document
title = '' #initialize the title
indocument = False # initialize the indocument to false
intitle = False # intiilaize the intitle to false
data = {} #initialize a set of data
titles = {} #initialize a set if titles
for line in f: #loop across line in the collection
    mo = re.match (r'\.I ([0-9]+)', line)
    if mo:
        if document!='':
            data[identifier] = document # intialize a set of data taking strings from document
        identifier = mo.group (1)
        indoc = False
    else:
        mo = re.match (r'\.T', line)
        if mo:
           title = ''
           intitle = True
        else:
           mo = re.match (r'\.W', line)
           if mo:
               document = ''
               indoc = True
           else:
               if intitle:
                   intitle = False
                   if identifier!='':
                      titles[identifier] = line[:-1][:50] #trying to understand here
               elif indoc:
                   document += " "
                   if parameters.case_folding:
                       document += line.lower()
                   else:
                       document += line    
f.close ()

# document length/title file
g = open (collection + "_index_len", "w")

# create inverted files in memory and save titles/N to file
index = {}
N = len (data.keys())
p = porter.PorterStemmer ()
for key in data:
    content = re.sub (r'[^ a-zA-Z0-9]', ' ', data[key])
    content = re.sub (r'\s+', ' ', content)
    words = content.split (' ')
    doc_length = 0
    for word in words:
        if word != '':
            if parameters.stemming:
                word = p.stem (word, 0, len(word)-1)
            doc_length += 1
            if not word in index:
                index[word] = {key:1}
            else:
                if not key in index[word]:
                    index[word][key] = 1
                else:
                    index[word][key] += 1
    print (key, doc_length, titles[key], sep=':', file=g) 

# document length/title file
g.close ()

# write inverted index to files
try:
   os.mkdir (collection+"_index")
except:
   pass
for key in index:
    f = open (collection+"_index/"+key, "w")
    for entry in index[key]:
        print (entry, index[key][entry], sep=':', file=f)
    f.close ()

# write N
f = open (collection+"_index_N", "w")
print (N, file=f)
f.close ()
