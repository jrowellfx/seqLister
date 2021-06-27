# About seqLister

`seqLister` is a python library for expanding and condensing
integer-sequences using a simple syntax widely used within
the VFX-industry for specifying frame-ranges.

## How to install the seqLister module on your system.

python3 -m pip install seqLister

## Syntax for specifying frame ranges

1.  List of individual numbers, e.g.:  
    1, 4, 10, 15
2.  Ranges of numbers, e.g.:  
    1-4, 10-15, which represents the numbers 1, 2, 3, 4, 10, 11, 12, 13, 14, 15
3.  Ranges of skipped frame numbers, e.g.:  
    1-10x2, 20-60x10 which represents the numbers 1, 3, 5, 7, 9, 20, 30, 40, 50, 60
4.  Any combination of the above.

Negative numbers are also allowed, as well as specifying ranges in reverse order.

## Libary functions

### expandSeq(seqList, nonSeqList=[])

Expands and returns the argument 'seqList' as a list of integers.
'seqList' may be a single string,
or a list of integers and/or
strings of the following format (with examples):

-   individual frame numbers: [1, "4", 10, 15]  
    returns [1, 4, 10, 15]
-   sequences of successive frame numbers: ["1-4", "10-15"]  
    returns [1, 2, 3, 4, 10, 11, 12, 13, 14, 15]
-   sequences of skipped frame numbers: ["1-10x2", "20-60x10"]  
    returns [1, 3, 5, 7, 9, 20, 30, 40, 50, 60]
-   reverse sequences work too: ["5-1"]  
    returns [5, 4, 3, 2, 1]
-   as do negative numbers: ["-10--3"]  
    returns [-10, -9, -8, -7, -6, -5, -4, -3]

The above formats may be listed in any order, but if a number has
been listed once, it will not be listed again.

Eg. seqLister.expandSeq(["0-16x8", "0-16x2"]) returns  
[0, 8, 16, 2, 4, 6, 10, 12, 14]

Anything that is not of the above format is ignored for
the purposes of building the list of integers and the ignored
item is appended to the optional argument "nonSeqList".

The returned list of integers is NOT sorted.

### condenseSeq(seqList, pad=1)

Takes a list of numbers and condenses it into the most minimal
form using the notation described in 'expandSeq()' above.

Examples:  

seqLister.condenseSeq([2, 1, 3, 7, 8, 4, 5, 6, 9, 10]) returns   
['1-10']

seqLister.condenseSeq([0, 8, 16, 2, 4, 6, 10, 12, 14]) returns   
['0-16x2']

condenseSeq tries to keep runs of condensed frame lists as
long as possible while also trying to keep random smatterings
of frame numbers, simply as numbers and not strange sequences.

Eg. seqLister.condenseSeq(seqLister.expandSeq(["0-100x2", 51])) returns   
['0-50x2', '51', '52-100x2']

and seqLister.condenseSeq([1, 5, 13]), returns  
['1', '5', '13']

Other examples:

seqLister.condenseSeq([1, 1, 1, 3, 3, 5, 5, 5]), returns  
['1-5x2']
seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10]), returns  
['1-4', '6-10x2']
seqLister.condenseSeq([1, 2, 3, 4, 6, 8]), returns  
['1-4', '6', '8']

condenseSeq(expandSeq(["2-50x2", "3-50x3", "5-50x5", "7-50x7", "11-50x11", "13-50x13", "17-50x17", "19-50x19", "23-50x23"])), returns  
['2-28', '30', '32-36', '38-40', '42', '44-46', '48-50']

### condenseSeqOnes(seqList, pad=1)

Takes a list of numbers and condenses it into the most minimal
form using with the restriction that sequences are compressed
to a range (A-B) if and only if the numbers are successive.

Examples:

seqLister.condenseSeqOnes([2, 1, 3, 7, 8, 4, 5, 6, 9, 10]), returns   
['1-10']

seqLister.condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 14]), returns   
['0', '2', '4', '6', '8', '10', '12', '14', '16']

