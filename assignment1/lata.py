def lata(*arg):
    if len(arg) == 1:
        M = arg[0]

    elif len(arg) > 1:
        M = arg[0]
        inDec = arg[1]
    else:
        print("Give lata() one or two arguments: (M, inDec)")

    if len(arg) > 0:
        size = M.shape


        #get the greates number of integers and decimals
        d_old = ''
        colMax = ['' for x in range(size[1])]
        for i in range(0,size[0]):
            for j in range(0,size[1]):
                nummer = M[i,j]

                #Separate integers from its decimals
                geheel = int(nummer)
                decimalen = abs(float(nummer) - geheel)

                #Stringafy the numbers
                geheel = str(geheel)
                decimalen = str(decimalen)

                if len(decimalen) > len(d_old):
                    d_old = decimalen
                if len(geheel) > len(colMax[j]):
                    colMax[j] = geheel

        if len(arg) == 1:
            if float(d_old) != 0:
                inDec = len(d_old) - 2
            else:
                inDec = 0

        #Round M with inDec
        for i in range(0,size[0]):
            for j in range(0,size[1]):
                M[i,j] = round(M[i,j],inDec)

        #Create a string for centering the numbers
        beginTabString = '\\begin{tabular}{|'
        for i in range(0,size[1]):
            beginTabString = beginTabString + 'c|'
        beginTabString = beginTabString + '}'


        print("\n \n \n")
        print("\\begin{table}[H]")
        print("\\centering")
        print(beginTabString)
        print('\\hline')

        for i in range(0,size[0]):
            for j in range(0,size[1]):
                lenMax = len(colMax[j])
                lenCurr = len(str(int(M[i,j])))
                lenDiff = lenMax - lenCurr
                k = 0
                string = ''
                while k < lenDiff:
                    string = string + ' '
                    k += 1

                if j == (size[1]-1):
                    string = string + '%.' + str(inDec) + 'f' + ' \\\\ \\hline'
                    print(string % M[i,j])
                else:
                    string = string + '%.' + str(inDec) + 'f' + ' &'
                    print(string % M[i,j], end=" ")

        print('\\end{tabular}')
        print('\\caption{}')
        print('\\label{tab:}')
        print('\\end{table}')
        print('\n \n \n')
