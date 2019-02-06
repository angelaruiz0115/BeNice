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




def main(username):
    
    model=None
    output_dir=None
    n_iter=20
    n_texts=2000

    
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

 
    
    textcat = nlp.create_pipe('textcat')
    nlp.add_pipe(textcat, last=True)
    textcat.add_label('POSITIVE')
    optimizer = nlp.begin_training()
    
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(train.train_data)
    
    print("Using {} examples ({} training, {} evaluation)"
          .format(n_texts, len(train_texts), len(dev_texts)))
    train_data = list(zip(train_texts,
                          [{'cats': cats} for cats in train_cats]))

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()
        print("Training the model...")
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
        for i in range(n_iter):
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                
                
                
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                           losses=losses)
            with textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
                
            print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                  .format(losses['textcat'], scores['textcat_p'],
                          scores['textcat_r'], scores['textcat_f']))
    
    user = create_reddit_instance().redditor(username)
    comments = []
    populateComments(comments, user)
    
    for comment in comments:

        doc = nlp('u' + comment)
        
        if doc.cats['POSITIVE'] > 0.99:
            
            print ("-------------------------------------\n")
            print (comment)            
            print(doc.cats)
            
        else:
            continue

def create_reddit_instance():
    id_string = "WX4K8AbqnEaYzQ"
    secret_string = "h41anbk-QPHWJQ8EipU9JNlT83s"
    
    
    return praw.Reddit(client_id=id_string,
                         client_secret=secret_string,
                         user_agent='Python Post SearchBot')
        
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
    
    
    argv = sys.argv[1:]
    program_name = sys.argv[0]
    
    print ("Program: " + str(program_name))
    print ("Argv: " + str(argv))
    
    username = ""
    
    if len(argv) != 2:
        print ('usage: ' + program_name + ' -u <username>\n')
        sys.exit(2)        

    parse_directory = ''

    try:
        opts, args = getopt.getopt(argv,"hu:o:")
    except getopt.GetoptError:
        print ('usage: ' + program_name + ' -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: ' + program_name + ' -u <username>')
            sys.exit()
        elif opt == "-u":
            username = arg
     

    
    main(username)
