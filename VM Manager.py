import sys

PM = [None] * 524288
Disk = [[None]*1024 for j in range(512)]
FreeFrame = [0, 1]


def parseLine1(s, z, f):
    if f not in FreeFrame:
        if f >= 2:
            FreeFrame.append(f)

    PM[2 * s] = z
    PM[2 * s + 1] = f


def parseLine2(s, p, f):
    if f not in FreeFrame:
        if f >= 2:
            FreeFrame.append(f)

    if PM[2 * s + 1] < 0:
        Disk[abs(PM[2 * s + 1])][p] = f
    else:
        PM[PM[2 * s + 1] * 512 + p] = f


def read_block(b, m):
    for c in range(512):
        if Disk[b][c] is not None:
            PM[m+c] = Disk[b][c]
            Disk[b][c] = None


vaList = []
inputList = []
switch = 0
if len(sys.argv) == 3:
    out_file = open('output-dp.txt', 'w')
    with open(sys.argv[1], 'r') as vaFile:
        lines = vaFile.readlines()
        for line in lines:
            Vas = line.split()
            for va in Vas:
                vaList.append(int(va))
    with open(sys.argv[2], 'r') as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            inpList = line.split()
            for init in inpList:
                inputList.append(int(init))
            inputList.append('\n')

    i = 0
    while i in range(len(inputList)):
        if inputList[i] == '\n':
            i += 1
            switch += 1
        if switch == 0:
            parseLine1(inputList[i], inputList[i+1], inputList[i+2])
        elif switch == 1:
            parseLine2(inputList[i], inputList[i + 1], inputList[i + 2])
        i += 3

    for va in vaList:
        s = va >> 18
        w = va & 511  # 1FF
        p = (va >> 9) & 511  # 1FF
        pw = va & 262143  # 3FFFF

        if pw >= PM[2*s]:
            out_file.write('-1')
            out_file.write(' ')
        else:
            if PM[2*s + 1] < 0:
                free = 0
                for a in range(2, 1024):
                    if a not in FreeFrame:
                        FreeFrame.append(a)
                        free = a
                        break
                b = abs(PM[2*s + 1])  # disk block
                read_block(b, free * 512)
                PM[2 * s + 1] = free
            if PM[PM[2*s +1]*512 +p] < 0:
                free = 0
                for a in range(2, 1024):
                    if a not in FreeFrame:
                        FreeFrame.append(a)
                        free = a
                        break
                b = abs(PM[PM[2*s+1]*512 + p])
                read_block(b, free*512)
                PM[PM[2 * s + 1] * 512 + p] = free
            PA = PM[PM[2*s+1]*512+p]*512 + w

            out_file.write(str(PA))
            out_file.write(' ')
