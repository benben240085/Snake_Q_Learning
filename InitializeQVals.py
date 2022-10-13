# Code to initialize Q-vals taken from https://github.com/jl4r1991/SnakeQlearning
import os
import itertools
import json

sqs = [''.join(s) for s in list(itertools.product(*[['0','1']] * 4))]
widths = ['0','1','NA']
heights = ['2','3','NA']

states = {}
for i in widths:
    for j in heights:
        for k in sqs:
            states[str((i,j,k))] = [0,0,0,0]

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
path = os.path.join(script_dir, "qvalues.json")
with open(path, "w") as f:
    json.dump(states, f)
