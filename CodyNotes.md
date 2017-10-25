## Helpful Notes that got me through the struggle:

### Problems and Resolutions

__Problem Zero__:
So, when you run python in the terminal for cloud9 it defaults to python2.7. 
However if you do this you will get this error: 
    TypeError: 'encoding' is an invalid keyword argument for this function

__FIX 0__:
`python3 vaderSentiment.py` (terminal)

__Problem One__:
So, if you would like to use nltk you will have to install it first. Remember to install
it through python3.

__FIX 1__:
`pip3 install nltk` (terminal)

__Problem Two__:
punkt is a resourced needed by nltk in order to parse out large files.

__FIX 2__:
`import nltk`
`nltk.download('punkt')`

(vaderSentiment.py)