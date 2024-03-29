import seqLister

badArgs = []
print("seqLister version: ", seqLister.__version__)
print("")
print("Testing expandSeq()")
print("")
print(seqLister.expandSeq(1))
print(seqLister.expandSeq(1, badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq("1, 2, 3 4 5", badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq([1, "004", 10, 15], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq([1, "004", 10, 15, "20", "30 35"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq([1, "004", 10, 15, "20,,  ,  30 35"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-4", "010-015"], badArgs))
print("badArgs: ", badArgs)
# Note: Next test, should split the 10 and -15 to
# two separate numbers, NOT treat as range 10-15.
print(seqLister.expandSeq(["1-4", "0010 -0015"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-10x2", "20-60x10"]))
print(seqLister.expandSeq(["1-10x2", "20-60x10"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["5-1"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq("5-1"))
print(seqLister.expandSeq(["5--2"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq("5--2"))
print(seqLister.expandSeq(["10--10x2"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["10--10x-2"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-16x8", "0-16x2"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-16x8", "0-16x2"]))
print(seqLister.expandSeq(["0-99x9"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq("0-99x9"))
print(seqLister.expandSeq(["1-0100x9"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-99x10"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-9", "20-40x2"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-6", "6-14x2", "14-70x10"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["0-64x64", "0-64x32", "0-64x16", "0-64x8", "0-64x4", "0-64x2", "0-64"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["-20--5"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["-10--3"], badArgs))
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-6-12"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1---6"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-6xa"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-6x2-"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["a-b"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["10--10x--2"], badArgs)) # invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(["1-5", "8-a"], badArgs)) # partially invalid
print("badArgs: ", badArgs)
print(seqLister.expandSeq(['20-10x3']))

print("")
print("Testing condenseSeq()")
print("")
print(seqLister.condenseSeq([]))
print(seqLister.condenseSeq([1]))
print(seqLister.condenseSeq(["2"], pad=4))
print(seqLister.condenseSeq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], nonSeqList=badArgs))
print("badArgs: ", badArgs)
print(seqLister.condenseSeq([1, "2", 3, "4", 5, 6, 7, "8", 9, 10], nonSeqList=badArgs))
print("badArgs: ", badArgs)
print(seqLister.condenseSeq([1, "2", 3, "4", 5, 6, 7, "8 9", 10], nonSeqList=badArgs))
print("badArgs: ", badArgs)
print(seqLister.condenseSeq([1, "2", 3, "4", 5, 6, 7, "8, 9", 10], nonSeqList=badArgs))
print("badArgs: ", badArgs)
print(seqLister.condenseSeq([2, 1, 3, 7, 8, 4, 5, 6, 9, 10]))
print(seqLister.condenseSeq([0, 8, 16, 2, 4, 6, 10, 12, 14]))
print(seqLister.condenseSeq([0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99]))
print(seqLister.condenseSeq([1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 91, 100]))
print(seqLister.condenseSeq([0, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
print(seqLister.condenseSeq([1, 1, 1]))
print(seqLister.condenseSeq([1, 1, 1, 2, 3]))
print(seqLister.condenseSeq([1, 1, 1, 3, 3, 5, 5, 5]))
print(seqLister.condenseSeq([1, 2]))
print(seqLister.condenseSeq([1, 5]))
print(seqLister.condenseSeq([1, 2, 5, 6, 9, 10]))
print(seqLister.condenseSeq([1, 5, 13]))

tmpList = seqLister.expandSeq(["0-100x2", 51], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["0-100x2", 51, 101, 102], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["1-5", "7-15x2"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["1-5", "7-15x2", "20-100x5"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["2-10x2", "14-30x4", "35-100x5"], badArgs)
print(seqLister.condenseSeq(tmpList))

print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10]))
print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8]))
print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10, 12, 13, 14, 15, 16]))
print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10, 12, 13, 14, 15]))
print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10, 11, 12]))
print(seqLister.condenseSeq([1, 2, 3, 4, 6, 8, 10, 11]))

print(seqLister.condenseSeq([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]))
print(seqLister.condenseSeq([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]))
print(seqLister.condenseSeq([0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 24, 34, 44, 54, 64]))
print(seqLister.condenseSeq([4, 5, 6, 8, 10, 12, 14, 24, 34, 44, 54, 64]))
print(seqLister.condenseSeq([0, 64, 32, 16, 48, 8, 24, 40, 56, 4, 12, 20, 28, 36, 44, 52, 60, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51], pad=2))
print(seqLister.condenseSeq([0, 64, 32, 16, 48, 8, 24, 40, 56, 4, 12, 20, 28, 36, 44, 52, 60, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21], pad=4))
print(seqLister.condenseSeq([0, 64, 32, 16, 48, 8, 24, 40, 56, 4, 12, 20, 28, 36, 44, 52, 60, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42], pad=4))

tmpList = seqLister.expandSeq(["5-400x5", "7-400x7", "11-400x11", "13-400x13"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["5-400x5", "7-400x7", "11-400x11", "13-400x13", "17-400x17", "19-400x19"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["5-400x5", "7-400x7", "11-400x11", "13-400x13", "17-400x17", "19-400x19", "23-400x23", "29-400x29", "31-400x31"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["3-400x3", "5-400x5", "7-400x7", "11-400x11", "13-400x13", "17-400x17", "19-400x19", "23-400x23", "29-400x29", "31-400x31"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["2-400x2", "3-400x3", "5-400x5", "7-400x7", "11-400x11", "13-400x13", "17-400x17", "19-400x19", "23-400x23", "29-400x29", "31-400x31"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["2-400x2", "3-400x3", "5-400x5", "7-400x7", "11-400x11", "13-400x13", "17-400x17", "19-400x19", "23-400x23", "29-400x29", "31-400x31", "120-301"], badArgs)
print(seqLister.condenseSeq(tmpList))

tmpList = seqLister.expandSeq(["2-50x2", "3-50x3", "5-50x5", "7-50x7", "11-50x11", "13-50x13", "17-50x17", "19-50x19", "23-50x23"], badArgs)
print(seqLister.condenseSeq(tmpList))

print(seqLister.condenseSeq(["1-100"], nonSeqList=badArgs))
print("badArgs: ", badArgs) # This should return "1-100" as bad.

# This should just treat as two numbers, 1 and -100
print(seqLister.condenseSeq(["1 -100"], nonSeqList=badArgs))
print("badArgs: ", badArgs)

print(seqLister.condenseSeq(["2-50x2", "3-50x3", "5-50x5", "7-50x7", "11-50x11", "13-50x13", "17-50x17", "19-50x19", "23-50x23"], nonSeqList=badArgs))
print("badArgs: ", badArgs)

print(seqLister.condenseSeq([-10, -9, -8, -7, -5, -4, -3, -2, -1], 1))
print(seqLister.condenseSeq(['-10', '-9', '-8', '-7', '-5', '-4', '-3', '-2', '-1']))
print(seqLister.condenseSeq(['-10, -9', '-8,,  , -7', '-5', '-4 -3', '-2', '-1']))

tmpList = seqLister.expandSeq(["1-10"])
print(seqLister.condenseSeqOnes(tmpList))
print(seqLister.condenseSeqOnes([-10, -9, -8, -7, -5, -4, -3, -2, -1, 2, 4, 6, 8, 9], 1))
print(seqLister.condenseSeqOnes([-10, -9, -8, -7, -5, -4, -3, -2, -1, 2, 4, 6, 8, 9, 10], 1))
print(seqLister.condenseSeqOnes(['-10', '-9', '-8', '-7', '-5', '-4', '-3', '-2', '-1', '2', '4', '6', '8']))
print(seqLister.condenseSeqOnes(['-10, -9', '-8,,  , -7', '-5', '-4 -3', -2, '-1', '2', 4, 6, 8]))
print(seqLister.condenseSeqOnes([2, 1, 3, 7, 8, 4, 5, 6, 9, 10]))
print(seqLister.condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 14]))
print(seqLister.condenseSeqOnes([0, 8, 16, 2, 4, 6, 10, 12, 13, 14]))
