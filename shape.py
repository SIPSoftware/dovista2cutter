def mirror(shape_params): 
    catalogue = shape_params['catalogue']
    number = shape_params['number']
    l = shape_params['l']
    l1 = shape_params['l1']
    l2 = shape_params['l2']
    h = shape_params['h']
    h1 = shape_params['h1']
    h2 = shape_params['h2']
    r = shape_params['r']
    r1 = shape_params['r1']
    r2 = shape_params['r2']
    r3= shape_params['r3']

    nCatalogue = 0
    nNumber = 0
    nL = l
    nL1 = l1
    nL2 = l2
    nH = h
    nH1 = h1
    nH2 = h2
    nR = r
    nR1 = r1
    nR2 = r2
    nR3 = r3

    if catalogue == 3:
        nCatalogue = catalogue

        if number == 1:
            nNumber = 2

        elif number == 2:
            nNumber = 1

        elif number == 3:
            nNumber = 4

        elif number == 4:
            nNumber = 3

        elif number == 5:
            nNumber = 6
            nL1 = l - l1

        elif number == 6:
            nNumber = 5
            nL1 = l - l1

        elif number == 7:
            nNumber = 7
            nL1 = l - l1

        elif number == 8:
            nNumber = 9

        elif number == 9:
            nNumber = 8

        elif number == 10:
            nNumber = 11

        elif number == 11:
            nNumber = 10

        elif number == 12:
            nNumber = 12
            nL1 = l - l1

        elif number == 13:
            nNumber = 13
            nL1 = l - l1
            nH1 = h2
            nH2 = h1

        elif number == 14:
            nNumber = 15

        elif number == 15:
            nNumber = 14

        elif number == 16:
            nNumber = 17
            nL1 = l - l1

        elif number == 17:
            nNumber = 16
            nL1 = l - l1

        elif number == 18:
            nNumber = 19
            nL1 = l - l1

        elif number == 19:
            nNumber = 18
            nL1 = l - l1

        elif number == 20:
            nNumber = 21

        elif number == 21:
            nNumber = 20

        elif number == 22:
            nNumber = 23
            nL1 = l - l1

        elif number == 23:
            nNumber = 22
            nL1 = l - l1

        elif number == 24:
            nNumber = 27
            nL1 = l - l1

        elif number == 25:
            nNumber = 30
            nL1 = l - l1

        elif number == 26:
            nNumber = 101
            nL1 = l - l1

        elif number == 27:
            nNumber = 24
            nL1 = l - l1

        elif number == 28:
            nNumber = 29
            nL1 = l - l1

        elif number == 29:
            nNumber = 28
            nL1 = l - l1

        elif number == 30:
            nNumber = 25
            nL1 = l - l1

        elif number == 31:
            nNumber = 32

        elif number == 32:
            nNumber = 31

        elif number == 33: # zmiana L1/L2
            nNumber = 33
            nL1 = l - l2
            nL2 = l - l1

        elif number == 34: # zmiana L1/L2
            nNumber = 34
            nL1 = l - l2
            nL2 = l - l1
            nH1 = h2
            nH2 = h1

        elif number == 35: # brak w sekcji def dovista_drawing2shape(drawing):
            nNumber = 26

        elif number == 36: # brak w sekcji def dovista_drawing2shape(drawing):
            nNumber = 67

        elif number == 37: # brak w sekcji def dovista_drawing2shape(drawing):
            nNumber = 69

        elif number == 50:
            nNumber = 50

        elif number == 51:
            nNumber = 52

        elif number == 52:
            nNumber = 51

        elif number == 53:
            nNumber = 53

        elif number == 54:
            nNumber = 55

        elif number == 55:
            nNumber = 54

        elif number == 56:
            nNumber = 56

        elif number == 57:
            nNumber = 57

        elif number == 58:
            nNumber = 58

        elif number == 59:
            nNumber = 60

        elif number == 60:
            nNumber = 59

        elif number == 61:
            nNumber = 62

        elif number == 62:
            nNumber = 61

        elif number == 63:
            nNumber = 64
            nL1 = l - l1

        elif number == 64:
            nNumber = 63
            nL1 = l - l1

        elif number == 65: # brak rysunku w katalogu ksztaltow Dovisty
            nNumber = 66

        elif number == 66: # brak rysunku w katalogu ksztaltow Dovisty
            nNumber = 65

        elif number == 67:
            nNumber = 36

        elif number == 68:
            nNumber = 68

        elif number == 69:
            nNumber = 37

        elif number == 70:
            nNumber = 71
            nL1 = l - l1

        elif number == 71:
            nNumber = 70
            nL1 = l - l1

        elif number == 73:
            nNumber = 73
            nL1 = l - l1
        
        elif number == 74:
            nNumber = 75
            nL1 = l - l1

        elif number == 75:
            nNumber = 74
            nL1 = l - l1

        elif number == 76:
            nNumber = 78
            nL1 = l - l1

        # elif number == 77: # ksztalt ma wymiar L3 - nie jest oprogramowany, przy transferze z DVA byl traktowany jako ksztalt symetryczny (podstawa)
        #     nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 78:
            nNumber = 76
            nL1 = l - l1

        elif number == 79: # zmiana L1/L2
            nNumber = 79
            nL1 = l - l2
            nL2 = l - l1

        elif number == 80:
            nNumber = 81
            nL1 = l - l1

        elif number == 81:
            nNumber = 80
            nL1 = l - l1

        elif number == 82:
            nNumber = 83
            nL1 = l - l1

        elif number == 83:
            nNumber = 82
            nL1 = l - l1

        elif number == 84:
            nNumber = 85
            nL1 = l - l1

        elif number == 85:
            nNumber = 84
            nL1 = l - l1

        elif number == 86: # poprawic wymiarowanie w katalogu ksztaltow Dovisty - '19,06' zmienic na 'W'
            nNumber = 87
            nL1 = l - l1

        elif number == 87:
            nNumber = 86
            nL1 = l - l1

        elif number == 101:
            nNumber = 26
            nL1 = l - l1

        elif number == 102:
            nNumber = 102
            nL1 = l - l1

        elif number == 103:
            nNumber = 104

        elif number == 104:
            nNumber = 103

        elif number == 105:
            nNumber = 106

        elif number == 106:
            nNumber = 105

        elif number == 107:
            nNumber = 107
            nL1 = l - l1
            nL2 = l - l2
            nH1 = h2
            nH2 = h1

        # elif number == 108: # brak rysunku w katalogu ksztaltow Dovisty
            # nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 109:
            nNumber = 135
            nL1 = l - l1

        # elif number == 110: # brak odpowiednika w katalogu ksztaltow Dovisty
        #     nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        # elif number == 111: # brak rysunku w katalogu ksztaltow Dovisty
            # nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 112:
            nNumber = 113

        elif number == 113:
            nNumber = 112

        elif number == 114: # zmiana L1/L2
            nNumber = 115
            nL1 = l - l2
            nL2 = l - l1

        elif number == 115: # zmiana L1/L2
            nNumber = 114
            nL1 = l - l2
            nL2 = l - l1

        elif number == 116: # zmiana L1/L2
            nNumber = 117
            nL1 = l - l2
            nL2 = l - l1

        elif number == 117: # zmiana L1/L2
            nNumber = 116
            nL1 = l - l2
            nL2 = l - l1

        # elif number == 118: # brak rysunku w katalogu ksztaltow Dovisty
            # nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        # elif number == 119: # brak rysunku w katalogu ksztaltow Dovisty
            # nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        # elif number == 120: # brak odpowiednika w katalogu ksztaltow Dovisty
        #     nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 121: # zmiana L1/L2
            nNumber = 121
            nL1 = l - l2
            nL2 = l - l1

        elif number == 122:
            nNumber = 123

        elif number == 123:
            nNumber = 122

        elif number == 124:
            nNumber = 125
            nL1 = l - l1

        elif number == 125:
            nNumber = 124
            nL1 = l - l1

        # elif number == 126: # brak odpowiednika w katalogu ksztaltow Dovisty
        #     nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 127:
            nNumber = 128
            nL1 = l - l1

        elif number == 128:
            nNumber = 127
            nL1 = l - l1

        elif number == 129:
            nNumber = 129
            nH1 = h2
            nH2 = h1

        elif number == 130:
            nNumber = 130

        # elif number == 131: # brak odpowiednika w katalogu ksztaltow Dovisty
        #     nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        # elif drawing == 132: # brak rysunku w katalogu ksztaltow Dovisty
            # nNumber = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif number == 133:
            nNumber = 133
            nL1 = l - l1

        elif number == 134:
            nNumber = 134
            nL1 = l - l1
            nL2 = l - l2
            nH1 = h2
            nH2 = h1

        elif number == 135:
            nNumber = 109
            nL1 = l - l1

        elif number == 136: # zmiana L1/L2
            nNumber = 136
            nL1 = l - l2
            nL2 = l - l1
            
        elif number == 137:
            nNumber = 137
            nL1 = l - l1

        elif number == 138:
            nNumber = 139
            nL1 = l - l1

        elif number == 139:
            nNumber = 138
            nL1 = l - l1

        elif number == 140:
            nNumber = 141
            nL1 = l - l1

        elif number == 141:
            nNumber = 140
            nL1 = l - l1

        elif number == 142:
            nNumber = 143
            nL1 = l - l2
            nL2 = l - l1

        elif number == 143:
            nNumber = 142
            nL1 = l - l2
            nL2 = l - l1

        else:
            nNumber = 0
            nL = 0
            nL1 = 0
            nL2 = 0
            nH = 0
            nH1 = 0
            nH2 = 0
            nR = 0
            nR1 = 0
            nR2 = 0
            nR3 = 0

    return {
        'catalogue': nCatalogue,
        'number': nNumber,
        'l': nL,
        'l1': nL1,
        'l2': nL2,
        'h': nH,
        'h1': nH1,
        'h2': nH2,
        'r': nR,
        'r1': nR1,
        'r2': nR2,
        'r3': nR3,
    }
