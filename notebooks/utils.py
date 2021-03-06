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
    string=re.sub('   ',' ',string)
    string=re.sub('  ',' ',string)
    lettersList = re.findall('[a-z]|\ ', string)
    string = ''.join(lettersList)
    return string


#define method which finds frequency of each letter
def freq_array(string):
    stringLow=str(string)
    stringLow.lower()
    numberOfEach=[]
    for i in range (26):
        currentLetter=chr(97+i)
        numLetter = len(re.findall(currentLetter, stringLow))
        numberOfEach.append(numLetter)
    numSpace = len(re.findall(' ', stringLow))
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
    pairsList[26].append(numPair)
    return pairsList

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

'''#test each shift and use relative liklihoods to find the most likely shift for a given ciphertext
def most_likely_key(ciphertext,probabilities):
    liklihoodList=[]
    for i in range (27):
        l=calc_log_likelihood(ciphertext,i)
        liklihoodList.append(l)
    maxval=max(liklihoodList)
    return liklihoodList.index(maxval) '''

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
    return rank_occurrence_of_list(freqArray)

def rank_occurrence_of_list(freqArray):
    tempfA=list(freqArray)
    tempfA.pop(26)
    rankCipher=[]
    for i in range (len(tempfA)):
        maxindex=tempfA.index(max(tempfA))
        rankCipher.append(maxindex)
        tempfA[maxindex]=-1
    return rankCipher
#substitutes letters based on relative frequency from crime and punishment

def substitute_singles_key(ciphertext, probabilities):
    ciphertext=extract_characters(ciphertext)
    cipherRanks=rank_occurrence(ciphertext)
    temp=list(probabilities)
    averageRanks=rank_occurrence_of_list(probabilities)
    #now i need to find the key. the index in the key will be the ranks value and the value will be the cipher value
    key=[None] * 26
    for i in range (len(cipherRanks)):
        index=averageRanks[i]
        key[index]=cipherRanks[i]
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
    logsum=math.log(probabilities[numList[0]])
    for i in range (len(numList)-1):
        probs=dictpairs[numList[i]][numList[i+1]]
        logsum=logsum+math.log(probs)
    return(logsum) 

def calc_liklihood_difference(l1,l2,plainPairCounts,probabilities,pairProbs,firstl):
    rowSum=0
    for i in range (len(pairProbs)):
        if i!=l1 and i!=l2:
            logs=math.log(pairProbs[i][l1])-math.log(pairProbs[i][l2])
            rowSum=rowSum+(plainPairCounts[i][l1]-plainPairCounts[i][l2])*logs
    collumnSum=0
    for j in range(len(pairProbs[0])):
        if j!=l1 and j!=l2:
            logs=math.log(pairProbs[l1][j])-math.log(pairProbs[l2][j])
            collumnSum=collumnSum+(plainPairCounts[l1][j]-plainPairCounts[l2][j])*logs
    logs=math.log(pairProbs[l1][l1])-math.log(pairProbs[l2][l2])
    overlap=(plainPairCounts[l1][l1]-plainPairCounts[l2][l2])*logs
    logs=math.log(pairProbs[l1][l2])-math.log(pairProbs[l2][l1])
    overlap=overlap+(plainPairCounts[l1][l2]-plainPairCounts[l2][l1])*logs
    #add difference in probability of first letter
    firstProb=0
    if firstl==l2:
        firstProb=math.log(probabilities[l2])-math.log(probabilities[l1])
    if firstl==l1:
        firstProb=math.log(probabilities[l1])-math.log(probabilities[l2])
    finalSum=rowSum+collumnSum+overlap+firstProb
    return -1*finalSum
    
def switch_two_indices(i1,i2,matrix):
    #switch rows
    rowl1=list(matrix[i1])
    rowl2=list(matrix[i2])
    matrix[i1]=rowl2
    matrix[i2]=rowl1
    #switch collumns
    coll1=[]
    coll2=[]
    for j in range (len(matrix)):
        newl1=int(matrix[j][i2])
        newl2=int(matrix[j][i1])
        matrix[j][i1]=newl1
        matrix[j][i2]=newl2
        
def switch_two_items(i1,i2,listy):
    templetter=int(listy[i1])
    listy[i1]=int(listy[i2])
    listy[i2]=int(templetter)
    
def climb_that_hill_fast(ciphertext,probabilities,pairProbs):
    startKey=substitute_singles_key(ciphertext,probabilities)
    i=0
    plaintext=decode_arist(ciphertext,startKey)
    plainPairCounts=get_pairs_array(plaintext)
    while i<100000:
        #get two random indices
        l1=random.randint(0,25)
        l2=random.randint(0,25)
        while l2==l1:
            l2=random.randint(0,25)
        #calculate the difference in likelihood for a model after switching two letters from the original model 
        diff=calc_liklihood_difference(l1,l2,plainPairCounts,probabilities,pairProbs)
        #if difference is positive switch the two letters
        if diff>0:
            switch_two_items(l1,l2,startKey)
            switch_two_indices(l1,l2,plainPairCounts)
        else:
            i+=1
    return startKey

def shift_key(number):
    key=list(range(0, 26))
    for i in range (number):
        shifting=int(key[0])
        key.pop(0)
        key.append(shifting)
    return key

#encodes a given plaintext using a given vigenere key
def encode_vigenere(text,key):
    text=extract_characters(text)
    listNum = text_to_num(text)
    #make keynum list, find length and set index to 0
    keyNum= text_to_num(key)
    keyLen=len(keyNum)
    ki=0
    #find the shift for each letter
    for i in range (len(listNum)):
        shift=keyNum[ki]
        currentKey=shift_key(shift)
        if listNum[i] != 26:
            listNum[i]= currentKey[listNum[i]]
        ki+=1
        if ki>keyLen-1:
            ki=0
    return num_to_text(listNum)

def decode_vigenere(ciphertext,key):
    listNum = text_to_num(ciphertext)
    #make keynum list, find length and set index to 0
    keyNum= text_to_num(key)
    keyLen=len(keyNum)
    ki=0
    #find the shift for each letter
    for i in range (len(listNum)):
        shift=keyNum[ki]
        currentKey=shift_key(shift)
        if listNum[i] != 26:
            listNum[i]= currentKey.index(listNum[i])
        ki+=1
        if ki>keyLen-1:
            ki=0
    return num_to_text(listNum)