# About seqLister

`seqLister` is a python library for expanding and condensing
integer-sequences using a simple syntax widely used within
the VFX-industry for specifying frame-ranges.

## Definition: 'Frame-Range'.

Given that 'A', 'B' and 'N' are integers, the syntax
for specifying an integer sequence used to describe
frame-ranges is one of the following three cases:

1. 'A' : just the integer A.

2. 'A-B' : all the integers from A to B inclusive.

3. 'A-BxN' : every Nth integer starting at A and increasing
to be no larger than B when A < B, or descending
to be no less than B when A > B.

The above three cases may often be combined to describe
less regular lists of Frame-Ranges by concatenating one
Frame-Range after another separated by spaces or commas.

#### Examples:

- Individual numbers: 1, 4, 10, 15

- Ranges of numbers: 1-4, 10-15,
    representing the numbers 1, 2, 3, 4, 10, 11, 12, 13, 14, 15

- Ranges of skipped numbers: 1-10x2, 20-60x10
    representing the numbers 1, 3, 5, 7, 9, 20, 30, 40, 50, 60

- Range of Negative numbers: -10--8
    representing the numbers -10, -9, -8

- Range in reverse order: 5-1
    representing the numbers 5, 4, 3, 2, 1

- Reverse order on threes: 20-10x3
    representing the numbers 20, 17, 14, 11

## How to install the seqLister module on your system.

```
python3 -m pip install seqLister --upgrade
```

## Libary functions

### expandSeq(seqList, nonSeqList=[])

 Expands the argument `seqList` into a list of integers.

`seqList` may be a single string or int, or a list of ints
and/or strings. The strings must contain Frame-Ranges
(syntax described above). If a string contains more than one
Frame-Range they must be separated by whitespace and/or commas.

#### Examples,

- individual frame numbers:
expandSeq([1, "4", 10, 15])  
returns -> [1, 4, 10, 15]

- sequences of successive frame numbers:
expandSeq(["1-4", "10-15"])  
returns -> [1, 2, 3, 4, 10, 11, 12, 13, 14, 15]

- sequences of skipped frame numbers:
expandSeq(["1-10x2", "20-60x10"])  
returns -> [1, 3, 5, 7, 9, 20, 30, 40, 50, 60]

- reverse sequences work too:
expandSeq(["5-1"])  
returns -> [5, 4, 3, 2, 1]

- as do negative numbers:
expandSeq(["-10--3"])  
returns -> [-10, -9, -8, -7, -6, -5, -4, -3]

These formats may be listed in any order, but if a number has
been listed once, it will not be listed again. For example:

- expandSeq(["0-16x8", "0-16x2"])  
returns -> [0, 8, 16, 2, 4, 6, 10, 12, 14]

Anything that is not a `Frame-Range` is ignored for
the purposes of building the list of integers and the ignored
item is appended to the optional argument `nonSeqList`.

The returned list of integers is *NOT* sorted.

New as of `v1.2.0`: Strings containing whitespace (and/or commas)
will be split into multiple list entries, and processed as
described above.

### condenseSeq(seqList, pad=1, nonSeqList=[])

Takes a list of frames which can be a mix of ints
and strings. The strings must contain ONLY integers (that is,
NO Frame-Ranges). The list of frames is then condensed into the most
succinct list of 'Frame-Ranges' possible to fully describe the
original list of frames.

It is possible to zero-pad the returned list of Frame-Ranges
with the optional 'pad' argument.

#### Examples:
- condenseSeq([2, 1, 3, 7, 8, 4, 5, 6, 9, 10])  
returns -> ['1-10']

- condenseSeq([0, 8, 16, 2, 4, 6, 10, 12, 14])  
returns -> ['0-16x2']

condenseSeq() tries to create Frame-Ranges that cover as long
a run of frames as possible while also trying to keep random
smatterings of frames numbers simply as single-frames and not
strange sequences, for example:

- condenseSeq(expandSeq(["0-100x2", 51]))  
returns -> ['0-50x2', '51', '52-100x2']

- condenseSeq([1, 5, 13])  
returns -> ['1', '5', '13']

#### Other examples:
- condenseSeq([1, 1, 1, 3, 3, 5, 5, 5])  
returns -> ['1-5x2']

- condenseSeq([1, 2, 3, 4, 6, 8, 10])  
returns -> ['1-4', '6-10x2']

- condenseSeq([1, 2, 3, 4, 6, 8])  
returns -> ['1-4', '6', '8']

- condenseSeq(expandSeq(["2-50x2", "3-50x3", "5-50x5", "7-50x7",  
"11-50x11", "13-50x13", "17-50x17", "19-50x19", "23-50x23"]))  
returns -> ['2-28', '30', '32-36', '38-40', '42', '44-46', '48-50']

- condenseSeq([97, 98, 99, 100, 101, 102, 103], pad=4)  
returns -> ['0097-0103']

Any strings passed in that do not contain only frames
are ignored and that string is appended to the optional
argument `nonSeqList`.

New as of `v1.2.0`: Strings containing whitespace (and/or commas)
will be split into multiple list entries, and processed as
described above.

### condenseSeqOnes(seqList, pad=1, nonSeqList=[])

The same as `condenseSeq()` above, in that it takes a list of frames
and condenses it into the most succinct set of Frame-Ranges with
the difference that sequences are compressed to a range (A-B) if
and only if the numbers are successive. For example,

- condenseSeqOnes([2, 1, 3, 7, 8, 4, 5, 6, 9, 10])  
returns -> ['1-10']

- condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 14])  
returns -> ['0', '2', '4', '6', '8', '10', '12', '14', '16']

- condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 13, 14])  
returns -> ['0', '2', '4', '6', '8', '10', '12-14', '16']
