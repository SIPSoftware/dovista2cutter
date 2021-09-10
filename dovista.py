from datetime import date
import re

def dovista_int2int(string_number):
    if len(string_number)>0:
        string_number = string_number.replace(',','')
        string_number = string_number.replace('.','')
        return int(string_number)
    else:
        return 0

def dovista_float2int(string_number):
    string_number = string_number.replace(',','')
    if len(string_number)>0:
        return round(float(string_number))
    else:
        return 0

def dovista_float(string_number):
    string_number = string_number.replace(',','')
    if len(string_number)>0:
        return float(string_number)
    else:
        return 0

def dovista_string2date(string_date):
    d = string_date.split('-')
    return date(int(d[0]),int(d[1]),int(d[2]))

def dovista_drawing2shape(drawing):
    if drawing == '3011.0085-1':
        return 1
    elif drawing == '3011.0085-2':
        return 2
    elif drawing == '3011.0085-3':
        return 3
    elif drawing == '3011.0085-4':
        return 4
    elif drawing == '3011.0085-5':
        return 5
    elif drawing == '3011.0085-6':
        return 6
    elif drawing == '3011.0085-7':
        return 7
    elif drawing == '3011.0085-8':
        return 8
    elif drawing == '3011.0085-9':
        return 9
    elif drawing == '3011.0085-10':
        return 10
    elif drawing == '3011.0085-11':
        return 11
    elif drawing == '3011.0085-12':
        return 12
    elif drawing == '3011.0085-13':
        return 13
    elif drawing == '3011.0085-14':
        return 14
    elif drawing == '3011.0085-15':
        return 15
    elif drawing == '3011.0085-16':
        return 16
    elif drawing == '3011.0085-17':
        return 17
    elif drawing == '3011.0087-18':
        return 18
    elif drawing == '3011.0087-19':
        return 19
    elif drawing == '3011.0087-20':
        return 20
    elif drawing == '3011.0087-21':
        return 21
    elif drawing == '3011.0087-22':
        return 22
    elif drawing == '3011.0087-23':
        return 23
    elif drawing == '3011.0087-24':
        return 24
    elif drawing == '3011.0087-25':
        return 25
    elif drawing == '3011.0087-26':
        return 26
    elif drawing == '3011.0087-27':
        return 27
    elif drawing == '3011.0087-28':
        return 28
    elif drawing == '3011.0087-29':
        return 29
    elif drawing == '3011.0087-30':
        return 30
    elif drawing == '3011.0087-14':
        return 31
    elif drawing == '3011.0087-15':
        return 32
    elif drawing == '3011.0087-16':
        return 33
    elif drawing == '3011.0087-17':
        return 34
    elif drawing == '3011.0088-50':
        return 50
    elif drawing == '3011.0088-51':
        return 51
    elif drawing == '3011.0088-52':
        return 52
    elif drawing == '3011.0088-53':
        return 53
    elif drawing == '3011.0088-54':
        return 54
    elif drawing == '3011.0088-55':
        return 55
    elif drawing == '3011.0088-56':
        return 56
    elif drawing == '3011.0088-57':
        return 57
    elif drawing == '3011.0088-58':
        return 58
    elif drawing == '3011.0088-59':
        return 59
    elif drawing == '3011.0088-60':
        return 60
    elif drawing == '3011.0088-61':
        return 61
    elif drawing == '3011.0088-62':
        return 62
    elif drawing == '3011.0088-63':
        return 63
    elif drawing == '3011.0088-64':
        return 64
    elif drawing == '3011.0088-65':
        return 65
    elif drawing == '3011.0088-66':
        return 66
    elif drawing == '3011.0088-67':
        return 67
    elif drawing == '3011.0088-68':
        return 68
    elif drawing == '3011.0088-69':
        return 69
    elif drawing == '3011.0089-70':
        return 70
    elif drawing == '3011.0089-71':
        return 71
    elif drawing == '3011.0089-73':
        return 73
    elif drawing == '3011.0089-74':
        return 74
    elif drawing == '3011.0089-75':
        return 75
    elif drawing == '3011.0089-76':
        return 76
    # elif drawing == '3011.0089-77':
    #     return 77
    elif drawing == '3011.0089-78':
        return 78
    elif drawing == '3011.0089-79':
        return 79
    elif drawing == '3011.0089-80':
        return 80
    elif drawing == '3011.0089-81':
        return 81
    elif drawing == '3011.0089-82':
        return 82
    elif drawing == '3011.0089-83':
        return 83
    elif drawing == '3011.0089-84':
        return 84
    elif drawing == '3011.0089-85':
        return 85
    elif drawing == '3011.0089-68':
        return 86
    elif drawing == '3011.0089-69':
        return 87
    elif drawing == '3011.0094-1':
        return 101
    elif drawing == '3011.0094-2':
        return 102
    elif drawing == '3011.0094-3':
        return 103
    elif drawing == '3011.0094-4':
        return 104
    elif drawing == '3011.0094-5':
        return 105
    elif drawing == '3011.0094-6':
        return 106
    elif drawing == '3011.0094-7':
        return 107
    # elif drawing == '3011.0094-8': konwersja do AW
        # return 108
    elif drawing == '3011.0094-9':
        return 109
    elif drawing == '3011.0094-10':
        return 110
    # elif drawing == '3011.0094-11': konwersja do aw
        # return 111
    elif drawing == '3011.0094-12':
        return 112
    elif drawing == '3011.0094-13':
        return 113
    elif drawing == '3011.0094-14':
        return 114
    elif drawing == '3011.0094-15':
        return 115
    elif drawing == '3011.0094-16':
        return 116
    elif drawing == '3011.0094-17':
        return 117
    # elif drawing == '3011.0096-01':
        # return 118
    # elif drawing == '3011.0096-02':
        # return 119
    elif drawing == '3011.0096-03':
        return 120
    elif drawing == '3011.0096-04':
        return 121
    elif drawing == '3011.0096-05':
        return 122
    elif drawing == '3011.0096-06':
        return 123
    elif drawing == '3011.0096-07':
        return 124
    elif drawing == '3011.0096-08':
        return 125
    elif drawing == '3011.0096-09':
        return 126
    elif drawing == '3011.0096-10':
        return 127
    elif drawing == '3011.0096-11':
        return 128
    elif drawing == '3011.0096-12':
        return 129
    elif drawing == '3011.0096-13':
        return 130
    elif drawing == '3011.0096-14':
        return 131
    # elif drawing == '3011.0096-15':
    #     return 132
    elif drawing == '3011.0096-16':
        return 133
    elif drawing == '3011.0096-17':
        return 134
    elif drawing == '3011.0096-18':
        return 135
    elif drawing == '3011.0096-19':
        return 136
    elif drawing == '3011.0096-20':
        return 137
    elif drawing == '3011.0096-21':
        return 138
    elif drawing == '3011.0096-22':
        return 139
    elif drawing == '3011.0096-23':
        return 140
    elif drawing == '3011.0096-24':
        return 141
    elif drawing == '3011.0094-18':
        return 142
    elif drawing == '3011.0094-19':
        return 143
    else:
        return 0
        
def getNodeValue(rootNode,nameSpace,nodeName):
    node = rootNode.find(nodeName,nameSpace)
    if node is not None:
        return node.text
    else:
        return ''

def getAdditionalPropertiesValue(properties,propertyName,propertyType):
    if propertyName in properties['additional_properties']:
        return properties['additional_properties'][propertyName][propertyType]
    else:
        return ''

def joinStringsWithoutEmpty(elements,sep):
    for i in range(len(elements)-1,-1,-1):
        if len(elements[i].strip())==0:
            elements.remove(elements[i])
    return sep.join(elements)

def date2Cutter(d):
    return d.strftime("%Y-%m-%d")

def getFactoryNumber(deliveryAddress):
    # ----wersja 1. tylko litera T i póżniej ciąg cyfr
    # matchObj = re.match(r'.*(T[0-9]*)',deliveryAddress)
    # ----wersja 2. Factory potem dowolny znak potem ciąg cyfr
    factoryNumber = ''
    matchObj = re.match(r'.*Factory (.[0-9]*)',deliveryAddress)
    if matchObj is not None:
        factoryNumber = matchObj.group(1)
    return factoryNumber

