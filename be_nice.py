#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import thinc.extra.datasets

import multiprocessing as mp
import random
import string

import praw
import itertools
import sys, getopt

random.seed(123)

import spacy
from spacy.util import minibatch, compounding

import nlu_functions
from nlu_functions import load_data, evaluate

import train
from train import train_data


def main():
    test()

def create_reddit_instance():
    id_string = "WX4K8AbqnEaYzQ"
    secret_string = "h41anbk-QPHWJQ8EipU9JNlT83s"
    
    
    return praw.Reddit(client_id=id_string,
                         client_secret=secret_string,
                         user_agent='Python Post SearchBot')

def test():
    
    nlp = spacy.load('en_core_web_md')
    
    # We're looking for sentences like "You fucking loser"
    # PRONOUN - ADJECTIVE - NOUN
    # A PRONOUN that comes before an ADJECTIVE (family of expletives) 
    #  that comes before a NOUN
    
    user = create_reddit_instance().redditor('imfatal')
    comments = []
    populateComments(comments, user)
    
    
    for comment in comments:
        
        for sentence in comment.split("."):

            sentence_doc = nlp('u' + sentence)
            
            pronoun_index = 0
            adj_index = 0
            noun_index = 0
            
            for i in range(len(sentence_doc)):
                
                token = sentence_doc[i]
                
                if token.pos_ is "PRON":
                    pronoun_index = i
                    
                if token.pos_ is "ADJ" and isInsult(nlp, token):
                    adj_index = i
                    
                if token.pos_ is "NOUN":
                    noun_index = i
                
                if pronoun_index < adj_index and adj_index < noun_index:
                    print (comment)
                    break

                
def isInsult(nlp, input_token):
    #determines if the word belongs to a family of insults
    

    swear_tokens = nlp(u'fucking')
    
    for swear_token in swear_tokens:
        
        
        if input_token.similarity(swear_token) > 0.5:
            return True
        else:
            return False 
        
        
def populateComments(comments, user):

    #comments is an empty list

    for comment in user.comments.new():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue

    for comment in user.comments.hot():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue


    for comment in user.comments.top():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue      

    for comment in user.comments.controversial():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue                


if __name__ == '__main__':
    main()
    
    """
    argv = sys.argv[1:]
    program_name = sys.argv[0]
    
    
    if len(argv) != 4:
        print ('usage: ' + program_name + ' -u <username> -n <number_of_comments>\n')
        sys.exit(2)        


    try:
        opts, args = getopt.getopt(argv,"hu:n:")
        
    except getopt.GetoptError:
        print ('usage: ' + program_name + ' -u <username> -n <number_of_comments>\n')
        sys.exit(2)
    
    
    username = ""
    number_of_comments = 1
    
    for opt, arg in opts:
        
        if opt == '-h':
            print ('usage: ' + program_name + ' -u <username> -n <number_of_comments>\n')
            sys.exit()
        elif opt == '-u':
            username = arg
        elif opt == '-n':
            number_of_comments = arg
    

    main(username, number_of_comments)
    """