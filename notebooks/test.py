from utils import *
import math

crime = open("../data/Crime.txt", "r")
crimeString= crime.read()
crimeString=extract_characters(crimeString)
freqCrime=freq_array(crimeString)
pairProbsCrime=get_pair_freq(crimeString)

probabilitiesCrime=list(freqCrime)
for i in range (len(probabilitiesCrime)):
    probabilitiesCrime[i]=probabilitiesCrime[i]/sum(freqCrime)

def test_liklihood_difference():
    text="hi my name is bethany and every single letter in this sentence is perfectly correct"
    text2="hd my name ds bethany ani every sdngle letter dn thds sentence ds perfectly correct"
    diffFun=calc_liklihood_difference(3,8,get_pairs_array(text2),probabilitiesCrime, pairProbsCrime,7)
    diff=log_liklihood_pairs(text, probabilitiesCrime, pairProbsCrime)-log_liklihood_pairs(text2, probabilitiesCrime, pairProbsCrime)
    assert math.isclose(diff,diffFun), "should be equal1"
    text="h"
    text2="e"
    diffFun=calc_liklihood_difference(4,7,get_pairs_array(text2),probabilitiesCrime, pairProbsCrime,4)
    diff=log_liklihood_pairs(text, probabilitiesCrime, pairProbsCrime)-log_liklihood_pairs(text2, probabilitiesCrime, pairProbsCrime)
    assert math.isclose(diff,diffFun), "should be equal"
    
def test_switch_indices():
    matrix=[[1,2,3],[4,5,6],[7,8,9]]
    switch_two_indices(0,1,matrix)
    assert matrix==[[5,4,6],[2,1,3],[8,7,9]], "should be equal"
    
def test_switch_items(): 
    listy=[1,2,3,4,5]
    switch_two_items(0,1,listy)
    assert listy==[2,1,3,4,5], "should be equal"
    
def test_vigenere_encode():
    text="this is my fight song"
    vigenere=encode_vigenere(text, 'ab')
    assert vigenere=='tiit js mz gihhu toog', "should be equal"
    
test_liklihood_difference()
test_switch_indices()
test_switch_items()
test_vigenere_encode()

print('test complete')