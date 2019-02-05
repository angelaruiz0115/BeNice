#!/usr/bin/env python
# coding: utf8
"""Train a convolutional neural network text classifier on the
IMDB dataset, using the TextCategorizer component. The dataset will be loaded
automatically via Thinc's built-in dataset loader. The model is added to
spacy.pipeline, and predictions are available via `doc.cats`. For more details,
see the documentation:
* Training: https://spacy.io/usage/training

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import thinc.extra.datasets

import spacy
from spacy.util import minibatch, compounding


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_texts=("Number of texts to train from", "option", "t", int),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=20, n_texts=2000):
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

    train_data = [
        (u"I love you", {"cats": {"POSITIVE": 0}}),
        (u"You are amazing", {"cats": {"POSITIVE": 0}}),
        (u"That's incredible", {"cats": {"POSITIVE": 0}}),
        (u"Great work", {"cats": {"POSITIVE": 0}}),
        (u"I hate you", {"cats": {"POSITIVE": 1}}),
        (u"You fucking moron", {"cats": {"POSITIVE": 1}}),
        (u"Are you fucking stupid", {"cats": {"POSITIVE": 1}}),
        (u"Everyone hates you", {"cats": {"POSITIVE": 1}}),
    ]    
    
    textcat = nlp.create_pipe('textcat')
    nlp.add_pipe(textcat, last=True)
    textcat.add_label('POSITIVE')
    optimizer = nlp.begin_training()
    for itn in range(100):
        for doc, gold in train_data:
            nlp.update([doc], [gold], sgd=optimizer)
    
    doc = nlp(u'That''s the dumbest thing I ever heard')
    print(doc.cats)    




if __name__ == '__main__':
    plac.call(main)