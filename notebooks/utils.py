import math 
import random
import re
def text_to_num(text):
    text=text.lower()
    textAsNum=[]
    for i in range (len(text)):
        if ord(text[i])==32:
            #print (" ", end =" "),
            textAsNum.append(26)
        else:
            #print (ord(text[i])-97,end =" "),
            textAsNum.append(ord(text[i])-97)
    return textAsNum

def num_to_text(numbers):
    letterList=[]
    for i in range (len(numbers)):
        if numbers[i]==26:
            letterList.append(" ");
        else:
            letterList.append(chr(numbers[i]+97))
    return "".join(letterList)

def encode_shift (text, key):
    text=extract_characters(text)
    listNum = text_to_num(text)
    for i in range (len(listNum)):
        if listNum[i] != 26:
            newNum=listNum[i]+key
            listNum[i]=newNum%26
    return num_to_text(listNum)

#shifts text downward by key
def decode_shift(text, key):
    listNum = text_to_num(text)
    for i in range (len(listNum)):
        if listNum[i] != 26:
            newNum=listNum[i]-key
            listNum[i]=newNum%26
    return num_to_text(listNum)

#creates a random key
def get_random_key():
    key=list(range(0, 26))
    random.shuffle(key)
    return key

#encodes a given plaintext using a given key
def encode_arist(text,key):
    text=extract_characters(text)
    listNum = text_to_num(text)
    for i in range (len(listNum)):
        if listNum[i] != 26:
            listNum[i]=key[listNum[i]]
    return num_to_text(listNum)

#decodes a given aristocrat ciphertext using a given key
def decode_arist(text,key):
    listNum = text_to_num(text)
    for i in range (len(listNum)):
        if listNum[i] != 26:
            listNum[i]=key.index(listNum[i])
    return num_to_text(listNum)


def extract_characters(string: str):
    string=string.lower()
    string=re.sub('\n',' ',string)
    string=re.sub(' ',' ',string)
    lettersList = re.findall('[a-z]|\ ', string)
    string = ''.join(lettersList)
    return string


#define method which finds frequency of each letter
def freq_array(string):
    string=string.lower()
    numberOfEach=[]
    for i in range (26):
        currentLetter=chr(97+i)
        numLetter = len(re.findall(currentLetter, string))
        numberOfEach.append(numLetter)
    numSpace = len(re.findall(' ', string))
    numberOfEach.append(numSpace)
    return numberOfEach

#how many number pairs
def get_pairs_array(ciphertext,pseudo=0):
    pairsList=[]
    #checks a-z pairs
    for i in range (26):
        firstLetter=chr(97+i)
        fList=[]
        pairsList.append(fList)
        for j in range (26):
            secondLetter=chr(97+j)
            pair=firstLetter+secondLetter
            lookahead='(?=('+pair+'))'
            numPair = len(re.findall(lookahead, ciphertext))+pseudo
            pairsList[i].append(numPair)
        secondLetter=' '
        pair=firstLetter+secondLetter
        numPair = len(re.findall(pair, ciphertext))+pseudo
        pairsList[i].append(numPair)
    firstLetter=' '
    fList=[]
    pairsList.append(fList)
    for j in range (26):
        secondLetter=chr(97+j)
        pair=firstLetter+secondLetter
        lookahead='(?=('+pair+'))'
        numPair = len(re.findall(lookahead, ciphertext))+pseudo
        pairsList[26].append(numPair)
    secondLetter=' '
    pair=firstLetter+secondLetter
    numPair = len(re.findall(pair, ciphertext))+pseudo
    pairsList[i].append(numPair)
    return pairsList

#calculate the likelihood of a certain shift given a ciphertext

def calc_likelihood(ciphertext, key,probabilities):
    plaintext=decode_shift(ciphertext, key)
    freqArray=freq_array(plaintext)
    product=1
    for i in range (27):
        #for every letter multiply the frequency of that decoded letter into a product
        product=product*probabilities[i]**freqArray[i]
    return product

def calc_log_likelihood(ciphertext, key,probabilities):
    plaintext=decode_shift(ciphertext, key)
    freqArray=freq_array(plaintext)
    logsum=0
    for i in range (27):
        #for every letter multiply the frequency of that decoded letter into a product
        logsum=logsum+freqArray[i]*log(probabilities[i])
    return logsum

#test each shift and use relative liklihoods to find the most likely shift for a given ciphertext
def most_likely_key(ciphertext):
    liklihoodList=[]
    for i in range (27):
        l=calc_log_likelihood(ciphertext,i)
        liklihoodList.append(l)
    maxval=max(liklihoodList)
    return liklihoodList.index(maxval) 

#use the most likely key to decode the ciphertext 
def most_likely_plaintext(ciphertext):
    key=most_likely_key(ciphertext)
    return decode_shift(ciphertext,key)

def calc_liklihood_arist_key(ciphertext, key,probabilities):
    plaintext=decode_arist(ciphertext, key)
    freqArray=freq_array(plaintext)
    product=1
    for i in range (27):
        product=product*probabilities[i]**freqArray[i]
    return product

def rank_occurrence(ciphertext):
    freqArray=freq_array(ciphertext)
    rankCipher=[]
    for i in range (len(freqArray)):
        maxi=freqArray.index(max(freqArray))
        rankCipher.append(maxi)
        freqArray[maxi]=-1
    return rankCipher

#substitutes letters based on relative frequency from crime and punishment

def substitute_singles_key(ciphertext, avfreq):
    ciphertext=extract_characters(ciphertext)
    cipher=rank_occurrence(ciphertext)
    temp=list(avfreq)
    if len(temp)==27:
        temp.pop(26)
    ranks=[]
    for i in range (len(temp)):
        maxi=temp.index(max(temp))
        ranks.append(maxi)
        temp[maxi]=-1
    #now i need to find the key. the index in the key will be the ranks value and the value will be the cipher value
    key=[None] * 26
    for i in range (26):
        index=ranks[i]
        key[index]=cipher[i]
    return key

def substitute_singles(ciphertext,avfreq):
    key=substitute_singles_key(ciphertext,avfreq)
    plaintext=decode_arist(ciphertext,key)
    return plaintext

#returns markov matrix for letter pairs
def get_pair_freq(text, pseudo=0.5):
    pairs=get_pairs_array(text, pseudo)
    for i in range (len(pairs)):
        row=sum(pairs[i])
        for j in range(len(pairs[i])):
            pairs[i][j]=(pairs[i][j])/row
    return pairs

#uses pair and single letter frequencies to find the liklihood under a model    
def liklihood_pairs(plaintext,probabilities,pairProbs):
    dictpairs=list(pairProbs)
    numList=text_to_num(plaintext)
    f=probabilities[numList[0]]
    for i in range (len(numList)-1):
        probs=dictpairs[numList[i]][numList[i+1]]
        f=f*probs
    return(f) 

#uses pair and single letter frequencies to find the log liklihood under a model    
def log_liklihood_pairs(plaintext,probabilities,pairProbs):
    dictpairs=list(pairProbs)
    numList=text_to_num(plaintext)
    logsum=probabilities[numList[0]]
    for i in range (len(numList)-1):
        probs=dictpairs[numList[i]][numList[i+1]]
        logsum=logsum+math.log(probs)
    return(logsum) 