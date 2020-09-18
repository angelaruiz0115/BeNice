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

from praw.models import MoreComments



def create_reddit_instance(id_string, secret_string, username_string, password_string):

    reddit = praw.Reddit(user_agent="Comment Extraction",
                     client_id=id_string, client_secret=secret_string,
                     username=username_string, password=password_string)

    return reddit

def main(username, id_string, secret_string, username_string, password_string):
    
    nlp = spacy.load('en_core_web_md')
    
    # We're looking for sentences like "You fucking loser"
    # PRONOUN - ADJECTIVE - NOUN
    # A PRONOUN that comes before an ADJECTIVE (family of expletives) 
    #  that comes before a NOUN
    
    reddit = create_reddit_instance(id_string, secret_string, username_string, password_string)


    rude_posts = []

    post_count = populateComments(rude_posts, username, reddit, nlp)
    rude_post_count = len(rude_posts)
    rude_percent = truncate(rude_post_count/post_count * 100, 3)
            
    print ("Number of rude posts: " + str(rude_post_count))
    print ("Total number of posts: " + str(post_count))
    print("\nRude percentage: " + str(rude_percent))

    if rude_percent < 50:
        print("\nCongrats! This user is not that rude.")
    else:
        print("\nThis user is pretty rude!")

    print ("\n\nExiting.")


def isRudeComment(comment, nlp):

    #The key is here is to look for insulting sentences
    # if one is found, return true.

    for sentence in comment.split("."):

        sentence_doc = nlp('u' + sentence)
        
        return isInsultSentence(nlp, sentence_doc)





def isYou(nlp, input_token):
    
    
    you_tokens = nlp(u'You')
    total = 0
    
    for token in you_tokens:
        
        if input_token.similarity(token) > 0.5:
            return True
        else:
            return False

            

def isInsultSentence(nlp, doc):
    
    pronoun_index = 0
    adj_index = 0
    
    for i in range(len(doc)):
        
        token = doc[i]
        
        if token.pos_ is "PRON" and isYou(nlp, token):
            pronoun_index = i
            
        if token.pos_ is "ADJ" and isInsult(nlp, token):
            adj_index = i
            
            
    if pronoun_index < adj_index:
        return True
    else:
        return False
    
       
                
def isInsult(nlp, input_token):
    #determines if the word belongs to a family of insults
    
    
    swear_tokens = nlp(u'fucking loser retard retarded moron')
    total = 0
    
    for swear_token in swear_tokens:
        
        total += input_token.similarity(swear_token)
        
    #Find the average similarity score
    average = total/len(swear_tokens)
    
    if average > 0.6:
        return True
    else:
        return False
    
        
        
def populateComments(rude_comments, user, reddit, nlp):

    user_object = reddit.redditor(user)


    f = open("rude_ouput.txt", "w")

    print("\nWriting to output file...")

    i = 0 

    for comment in user_object.comments.controversial(limit=None):
        i+=1

        if isRudeComment(comment.body, nlp):

            rude_comments.append(comment.body)



            f.write("========================================")
            f.write("    " + comment.body)
            f.write("========================================")

    f.close()

    return i

            

    """
    for comment in user_object.comments.new(limit=None):

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue

    for comment in user_object.comments.hot(limit=None):

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue


    for comment in user_object.comments.top(limit=None):

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue      

    for comment in user_object.comments.controversial(limit=None):

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue  
"""

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier
              


if __name__ == '__main__':

    # Read id and secret from CONFIG.txt
    config_file = open('CONFIG.txt', 'r')

    lines = config_file.readlines()
    id_string = "" 
    secret_string = ""
    username_string = ""
    password_string = ""

    for line in lines:

        parts = line.split(":")

        if parts[0] == "id_string":
            id_string = parts[1].strip()
        elif parts[0] == "secret_string":
            secret_string = parts[1].strip()
        elif parts[0] == "username":
            username_string = parts[1].strip()
        else:
            password_string = parts[1].strip()

    print("\n=== Please BeNice! ===\n")

    print("id_string is: " + id_string)
    print ("secret_string is: " + secret_string)

    argv = sys.argv[1:]
    program_name = sys.argv[0]
    
    
    if len(argv) != 2:
        print ('\nusage: ' + program_name + ' -u <username>\n')
        sys.exit(2)        


    try:
        opts, args = getopt.getopt(argv,"hu:")
        
    except getopt.GetoptError:
        
        print ('\nusage: ' + program_name + ' -u <username>\n')
        sys.exit(2)
    
    
    username = ""
    
    for opt, arg in opts:
        
        if opt == '-h':
            print ('\nusage: ' + program_name + ' -u <username>\n')
            sys.exit()
        elif opt == '-u':
            username = arg
    
    print ("\nSearching posts for user /u/" + username + "...")
    print("\nThis may take a while...")

    main(username, id_string, secret_string, username_string, password_string)