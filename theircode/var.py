from time import process_time as timer
import argparse
import re
from collections import deque, Counter, defaultdict
from enum import Enum

def_prob=10e-32
tag_tuple=('O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'START', 'STOP', '#UNK#')
tag_array=[(tag, ('', 0.0)) for tag in tag_tuple if not (tag=='START' or tag=='STOP')]

class Filter(Enum):
    train=r'(\S+) ((?:O|B-|I-|START|STOP|#UNK#)(?:positive|neutral|negative)?)'
    dev=r'(\S+)()'
