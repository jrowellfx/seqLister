# BSD 3-Clause License
#
# Copyright (c) 2008-2023, James Philip Rowell,
# Alpha Eleven Incorporated
# www.alpha-eleven.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   - Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#   - Neither the name of "Alpha Eleven, Inc."  nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# seqLister is a python library for expanding and condensing
# integer-sequences using a simple syntax widely used within
# the VFX-industry for specifying frame-ranges.
#
# Definition: 'Frame-Range'.
#
# Given that 'A', 'B' and 'N' are integers, the syntax
# for specifying an integer sequence used to describe
# frame-ranges is one of the following three cases:
#
#    'A'     just the integer A.
#
#    'A-B'   all the integers from A to B inclusive.
# 
#    'A-BxN' every Nth integer starting at A and increasing
#            to be no larger than B when A < B, or descending
#            to be no less than B when A > B.
#
# The above three cases may often be combined to describe 
# less regular lists of Frame-Ranges by concatenating one
# Frame-Range after another separated by spaces or commas.
#
# Examples:
# 
# Individual numbers: 1, 4, 10, 15
# 
# Ranges of numbers: 1-4, 10-15,
#     representing the numbers 1, 2, 3, 4, 10, 11, 12, 13, 14, 15
# 
# Ranges of skipped numbers: 1-10x2, 20-60x10
#     representing the numbers 1, 3, 5, 7, 9, 20, 30, 40, 50, 60
# 
# Range of Negative numbers: -10--8
#     representing the numbers -10, -9, -8
# 
# Range in reverse order: 5-1
#     representing the numbers 5, 4, 3, 2, 1
# 
# Reverse order on threes: 20-10x3
#     representing the numbers 20, 17, 14, 11
# 
# MAJOR version for incompatible API changes
# MINOR version for added functionality in a backwards compatible manner
# PATCH version for backwards compatible bug fixes
#
__version__ = "1.2.0"

# expandSeq() - Expands the argument 'seqList' into a list of integers.
#
# 'seqList' may be a single string or int, or a list of ints
# and/or strings. The strings must contain Frame-Ranges
# (syntax described above). If a string contains more than
# one Frame-Range they must be separated by whitespace or a comma.
#
# Examples,
#
# individual frame numbers:
#     expandSeq([1, "4", 10, 15])
#         returns -> [1, 4, 10, 15]
#
# sequences of successive frame numbers:
#     expandSeq(["1-4", "10-15"])
#         returns -> [1, 2, 3, 4, 10, 11, 12, 13, 14, 15]
#
# sequences of skipped frame numbers:
#     expandSeq(["1-10x2", "20-60x10"])
#         returns -> [1, 3, 5, 7, 9, 20, 30, 40, 50, 60]
#
# reverse sequences work too:
#     expandSeq(["5-1"])
#         returns -> [5, 4, 3, 2, 1]
#
# as do negative numbers:
#     expandSeq(["-10--3"])
#         returns -> [-10, -9, -8, -7, -6, -5, -4, -3]
#
# These formats may be listed in any order, but if a number has
# been listed once, it will not be listed again. For example:
#     expandSeq(["0-16x8", "0-16x2"])
#         returns -> [0, 8, 16, 2, 4, 6, 10, 12, 14]
#
# Anything that is not of the above format is ignored for
# the purposes of building the list of integers and the ignored
# item is appended to the optional argument "nonSeqList".
#
# The returned list of integers is NOT sorted.
#
# New as of v1.2.0: Strings containing whitespace (and/or commas)
# will be split into multiple list entries, and processed as
# described above.
#
def expandSeq(seqList, nonSeqList=[]) :

    nonSeqList.clear()

    if not isinstance(seqList, list) :
        tmp=seqList
        seqList = [tmp]

    resultList = []
    for seqItem in seqList :
        origItem = seqItem
        if not (isinstance(seqItem, int) or isinstance(seqItem, str)) :
            # Discard item and continue to next one
            nonSeqList.append(origItem)
            continue

        if isinstance(seqItem, int) :
            if seqItem not in resultList :
                resultList.append(seqItem)
            continue

        stepValue = 1

        # Turn any embedded commas and tabs into spaces.
        # Then split the seqItem into separate items if containing
        # spaces which allows, for a looser interpretation of
        # what can be in passed to us here via seqList.
        #
        # For example these lists are treated the same in this function:
        #    ['1', '2', '3', '4'] == ['1 2,3', '4']
        #
        seqItem = seqItem.replace(",", " ")
        splitSeqItem = seqItem.split() # Treats consecutive whitespace as one separator.

        for seqItem in splitSeqItem :

            # No stepping by negative numbers - step back by reversing start/end
            # This next step is equivalent to taking the absolute value of "x"
            #
            seqItem = seqItem.replace("x-", "x")

            seqItemList = seqItem.split("-") # might be range or neg number.

            if "x" in seqItemList[-1] :
                lastItem = seqItemList[-1].split("x")
                if len(lastItem) != 2 :
                    nonSeqList.append(origItem)
                    continue
                if not lastItem[1].isdigit() :
                    nonSeqList.append(origItem)
                    continue
                stepValue = int(lastItem[1])
                seqItemList[-1] = lastItem[0] # Stick last element back in the list w/o "xN" part

            if seqItemList[0] == "" : # Means there was leading minus sign.
                seqItemList.pop(0)
                if len(seqItemList) == 0:
                    nonSeqList.append(origItem)
                    continue
                if not seqItemList[0].isdigit() :
                    nonSeqList.append(origItem)
                    continue
                seqItemList[0] = -1 * int(seqItemList[0]) # Repace first entry...
            elif seqItemList[0].isdigit() :
                seqItemList[0] = int(seqItemList[0]) #...with an integer.
            else :
                nonSeqList.append(origItem)
                continue

            if len(seqItemList) == 1 : # Was just string with one number in it.
                if seqItemList[0] not in resultList :
                    resultList.append(seqItemList[0])
                continue

            if seqItemList[1] == "" : # Same as above for next entry.
                seqItemList.pop(1)
                if len(seqItemList) == 1:
                    nonSeqList.append(origItem)
                    continue
                if not seqItemList[1].isdigit() :
                    nonSeqList.append(origItem)
                    continue
                seqItemList[1] = -1 * int(seqItemList[1])
            elif seqItemList[1].isdigit() :
                seqItemList[1] = int(seqItemList[1])
            else :
                nonSeqList.append(origItem)
                continue

            # Should only be exactly two entries at this point.
            if len(seqItemList) != 2 :
                nonSeqList.append(origItem)
                continue

            # Ummm - dumb but why not? list from n to n, i.e., one number.
            if seqItemList[0] == seqItemList[1] :
                if seqItemList[0] not in resultList :
                    resultList.append(seqItemList[0])
            elif seqItemList[0] < seqItemList[1] : # Counting up.
                frameNum = seqItemList[0]
                while frameNum <= seqItemList[1] :
                    if frameNum not in resultList :
                        resultList.append(frameNum)
                    frameNum =  frameNum + stepValue
            else : # Counting down.
                frameNum = seqItemList[0]
                while frameNum >= seqItemList[1] :
                    if frameNum not in resultList :
                        resultList.append(frameNum)
                    frameNum =  frameNum - stepValue

    return resultList

class _gapRun :
    def __init__(self, seqLen, startInd, gapSize, isCorrected=False) :
        self.seqLen = seqLen
        self.startInd = startInd
        self.gapSize = gapSize
        self.isCorrected = isCorrected

    def __str__(self) :
        return "[seqLen = " + str(self.seqLen) + \
            " startInd = " + str(self.startInd) + \
            " gapSize = " + str(self.gapSize) + \
            " isCorrected = " + str(self.isCorrected) + "]"

# "__" at the start of function nane indicated private in module.
#
def __debugPrintList(li) :
    for l in li :
        # print "%02d" % l,
        print("%02d" % l, end='')
    # print ""
    print()


# condenseSeq() - Takes a list of frames which can be a mix of ints
# and strings. The strings must contain ONLY integers (that is,
# NO Frame-Ranges). The list of frames is then condensed into the most
# succinct list of 'Frame-Ranges' possible to fully describe the 
# original list of frames.
#
# It is possible to zero-pad the returned list of Frame-Ranges
# with the optional 'pad' argument.
#
# Examples:
#     condenseSeq([2, 1, 3, 7, 8, 4, 5, 6, 9, 10])
#         returns -> ['1-10']
#
#     condenseSeq([0, 8, 16, 2, 4, 6, 10, 12, 14])
#         returns -> ['0-16x2']
#
# condenseSeq() tries to create Frame-Ranges that cover as long
# a run of frames as possible while also trying to keep random
# smatterings of frames numbers simply as single-frames and not
# strange sequences, for example:
#
#     condenseSeq(expandSeq(["0-100x2", 51]))
#         returns -> ['0-50x2', '51', '52-100x2']
#
#     condenseSeq([1, 5, 13])
#         returns -> ['1', '5', '13']
#
# Other examples:
#     condenseSeq([1, 1, 1, 3, 3, 5, 5, 5])
#         returns -> ['1-5x2']
#
#     condenseSeq([1, 2, 3, 4, 6, 8, 10])
#         returns -> ['1-4', '6-10x2']
#
#     condenseSeq([1, 2, 3, 4, 6, 8])
#         returns -> ['1-4', '6', '8']
#
#     condenseSeq(expandSeq(["2-50x2", "3-50x3", "5-50x5", "7-50x7",
#             "11-50x11", "13-50x13", "17-50x17", "19-50x19", "23-50x23"]))
#         returns -> ['2-28', '30', '32-36', '38-40', '42', '44-46', '48-50']
#
#     condenseSeq([97, 98, 99, 100, 101, 102, 103], pad=4)
#         returns -> ['0097-0103']
#
# Any strings passed in that do not contain only frames
# are ignored and that string is appended to the optional
# argument "nonSeqList".
#
# New as of v1.2.0: Strings containing whitespace (and/or commas)
# will be split into multiple list entries, and processed as
# described above.
#
def condenseSeq(seqList, pad=1, nonSeqList=[]) :

    condensedList = []

    nonSeqList.clear()

    # Turn seqList into all integers and stash invalid entries
    #
    tmpSeqList = seqList
    seqList = []
    for n in tmpSeqList :
        if isinstance(n, int) :
            seqList.append(int(n))
        elif isinstance(n, str) :
            ## print("DEBUG: ", n)
            n = n.replace(",", " ")
            nSplit = n.split()
            for n in nSplit :
                if n.isdigit() :
                    seqList.append(int(n))
                elif n[0] == "-" and n[1:].isdigit() :
                    seqList.append(-1 * int(n[1:]))
                else :
                    nonSeqList.append(n)
        else :
            nonSeqList.append(n)

    if len(seqList) == 0 : # Take care of 1st trivial case
        return condensedList

    # Remove duplicates
    #
    seqList.sort()
    tmpSeqList = seqList
    seqList = []
    seqList.append(tmpSeqList[0])
    tmpSeqList.pop(0)
    for n in tmpSeqList :
        if n != seqList[-1] :
            seqList.append(n)

    formatStr = "%0" + str(pad) + "d"

    if len(seqList) == 1 : # Take care of second trivial case.
        condensedList.append(formatStr % seqList[0])
        return condensedList

    # At this point - guaranteed that len(seqList) > 1

    gapList = []
    i = 1
    while i < len(seqList) : # Record gaps between frame #'s
        gapList.append(seqList[i] - seqList[i-1])
        i += 1

    # Count lengths of similar "gaps".
    i = 0
    currentGap = 0 # Impossible - good starting point.
    gapRunList = []
    while i < len(gapList) :
        if gapList[i] != currentGap :
            currentGap = gapList[i]
            gapRunList.append(_gapRun(2, i, currentGap))
        else :
            gapRunList[-1].seqLen += 1
        i += 1
    gapRunList.append(_gapRun(0, i, 0)) # Add entry for last number in seqList (note zero gapSize)

    # The largest runs steals from the prior and next runs last and first frame (respectively)
    # if possible, working our way to smaller and smaller runs.
    #
    while True :

        # Find largest run with smallest gapSize.
        #
        runInd = len(gapRunList) - 1 # This will contain index to desired run
        maxSeqLen = 0
        maxSeqLenGapSize = 0
        i = 0
        for run in gapRunList :
            if not run.isCorrected :
                if run.seqLen > maxSeqLen :
                    runInd = i
                    maxSeqLen = run.seqLen
                    maxSeqLenGapSize = run.gapSize
                elif run.seqLen == maxSeqLen and run.gapSize < maxSeqLenGapSize :
                    runInd = i
                    maxSeqLenGapSize = run.gapSize
            i += 1

        if runInd == len(gapRunList) - 1 :
            break

        gapRunList[runInd].isCorrected = True

        if gapRunList[runInd].seqLen == 0 :
            continue

        # Correct prior sequence if possible.
        if runInd > 0 :
            if not gapRunList[runInd-1].isCorrected :
                gapRunList[runInd-1].seqLen -= 1

        # Also correct next sequence if possible.
        if runInd < len(gapRunList) - 1 :
            if not gapRunList[runInd+1].isCorrected : # Means it was bigger than this one and we can't steal from it.
                gapRunList[runInd+1].seqLen -= 1
                gapRunList[runInd+1].startInd += 1

    condensedList = []

    for run in gapRunList :
        if run.seqLen <= 0 :
            continue

        if run.seqLen == 1 :
            condensedList.append(formatStr % seqList[run.startInd])
            continue

        # Don't print out this case as a range, but as two separate entries.
        #
        if run.seqLen == 2 and run.gapSize > 1:
            condensedList.append(formatStr % seqList[run.startInd])
            condensedList.append(formatStr % seqList[run.startInd+1])
            continue

        firstFrame = seqList[run.startInd]
        lastFrame = seqList[run.startInd + run.seqLen - 1]
        gap = run.gapSize
        condensedList.append(formatStr % firstFrame +"-"+ formatStr % lastFrame)
        if gap > 1 :
            condensedList[-1] = condensedList[-1] + "x" + str(gap)

    return condensedList

# The same as condenseseq() above, in that it takes a list of frames
# and condenses it into the most succinct set of Frame-Ranges with
# the difference that sequences are compressed to a range (A-B) if
# and only if the numbers are successive. For example,
#
#     condenseSeqOnes([2, 1, 3, 7, 8, 4, 5, 6, 9, 10])
#         returns -> ['1-10']
#
#     condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 14])
#         returns -> ['0', '2', '4', '6', '8', '10', '12', '14', '16']
#
#     condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 13, 14])
#         returns -> ['0', '2', '4', '6', '8', '10', '12-14', '16']
#
def condenseSeqOnes(seqList, pad=1, nonSeqList=[]) :

    condensedList = []

    nonSeqList.clear()

    # Turn seqList into all integers and stash invalid entries
    #
    tmpSeqList = seqList
    seqList = []
    for n in tmpSeqList :
        if isinstance(n, int) :
            seqList.append(int(n))
        elif isinstance(n, str) :
            n = n.replace(",", " ")
            nSplit = n.split()
            for n in nSplit :
                if n.isdigit() :
                    seqList.append(int(n))
                elif n[0] == "-" and n[1:].isdigit() :
                    seqList.append(-1 * int(n[1:]))
                else:
                    nonSeqList.append(n)
        else:
            nonSeqList.append(n)

    if len(seqList) == 0 : # Take care of 1st trivial case
        return condensedList

    # Remove duplicates
    #
    seqList.sort()
    tmpSeqList = seqList
    seqList = []
    seqList.append(tmpSeqList[0])
    tmpSeqList.pop(0)
    for n in tmpSeqList :
        if n != seqList[-1] :
            seqList.append(n)

    formatStr = "%0" + str(pad) + "d"

    if len(seqList) == 1 : # Take care of second trivial case.
        condensedList.append(formatStr % seqList[0])
        return condensedList

    # At this point - guaranteed that len(seqList) > 1

    condensedList = []

    firstFrame = seqList[0]
    lastFrame = seqList[0]
    seqList.pop(0)
    for f in seqList :
        if f == lastFrame + 1 : # Sequence is on ones.
            lastFrame = f
        else :
            if firstFrame == lastFrame : # Last one was a single entry.
                condensedList.append(formatStr % firstFrame)
            else : # Had a range.
                condensedList.append(formatStr % firstFrame +"-"+ formatStr % lastFrame)
            firstFrame = f
            lastFrame = f

    if firstFrame == lastFrame :
        condensedList.append(formatStr % firstFrame)
    else :
        condensedList.append(formatStr % firstFrame +"-"+ formatStr % lastFrame)

    return condensedList
