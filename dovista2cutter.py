COIFVERSION = "1.0"
BUILDVERSION = "1.0.1"

import xml.etree.ElementTree as ET
import csv
import os
import sys
import argparse
import re
from datetime import date
from xml.dom import minidom

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
    else:
        return 0

def mirrorShape(shape_params): 
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


ns = {  'cac':"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        'cbc':"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        'ccts':"urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2",
        'sdt':"urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2",
        'udt':"urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2",
        'xsi':"http://www.w3.org/2001/XMLSchema-instance"}

# przygotowanie parsowania parametrów wejściowych
parser = argparse.ArgumentParser(description='Skrypt konwersji pliku Dovista XML do formatu Cutter Customer Order Import File')
parser.add_argument('-i',dest='inputfile',
                    help='plik wejściowy')
parser.add_argument('-o',dest='outputfile',
                    help='plik wyjściowy')
parser.add_argument('--sepfn',action='store_true',dest='separate_order_factory_number',
                    help='podział zlecenia według factoryNumber')

#parsowanie parametrów wejściowych
args = parser.parse_args()

#sprawdzenie parametrów wejściowych
if os.path.exists(args.inputfile):
    input_filename = args.inputfile
    if args.outputfile is None:
        output_filename = os.path.splitext(os.path.basename(input_filename))[0]+'.csv'
        output_filename = os.path.join(os.path.dirname(input_filename),output_filename)
    else:
        output_filename = args.outputfile
else:
    print("No such file: "+args.inputfile)
    sys.exit()

print('input file: '+input_filename)
print('output file: '+output_filename)
print('separate_order_factory_number: '+str(args.separate_order_factory_number))
print('-'*50)

#usun plik wyjściowy jeżeli istnieje
# if os.path.exists(output_filename):
    # os.remove(output_filename)

#parsowanie pliku XML
tree = ET.parse(input_filename)
root = tree.getroot()

orders = {}

#adres dostawy
deliveryAddress = getNodeValue(root,ns,'./cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name')
factoryNumber = getFactoryNumber(deliveryAddress)

#iteracja po OrderLine
for order_line_node in root.findall('cac:OrderLine',ns):
    #iteracja po LineItem
    for line_item_node in order_line_node.findall('cac:LineItem',ns):
        #pobranie informacji o pozycji
    
        # pobranie dodatkowych informacji z <AdditionalItemProperty> do dictionary position['additional_properties']
        additional_properties = {}
        for additional_item_property_node in line_item_node.findall("./cac:Item/cac:AdditionalItemProperty",ns):
            name = getNodeValue(additional_item_property_node,ns,'cbc:Name')
            value = getNodeValue(additional_item_property_node,ns,'cbc:Value')
            id = getNodeValue(additional_item_property_node,ns,'cbc:Name')

            node = additional_item_property_node.find("./cac:ItemPropertyGroup/cbc:Name",ns)
            if node is not None:
                additional_properties[node.text] = {'name':name,'value':value,'id':id}

        #podział pozycje na różne zlecenia w zależności od daty dostawy i innych informacji
        order_note = ''
        delivery_date = getNodeValue(line_item_node,ns,'./cac:Delivery/cbc:LatestDeliveryDate')
        separate_order_string = delivery_date
        if args.separate_order_factory_number:
            if factoryNumber == 'T3':
                elevation_shape = getAdditionalPropertiesValue({'additional_properties': additional_properties},'C_ELEVATION_SHAPE','value')
                separate_order_string = separate_order_string + elevation_shape
                order_note = 'Strefa montażu {0} {1}! NIE ŁĄCZYĆ Z SZBAMI INNYCH STREF DVA !'.format(factoryNumber,elevation_shape)
            if factoryNumber == 'T7':
                platform = getAdditionalPropertiesValue({'additional_properties': additional_properties},'C_PLATFORM','value')
                separate_order_string = separate_order_string + platform
                order_note = 'Strefa montażu {0} {1}! NIE ŁĄCZYĆ Z SZBAMI INNYCH STREF DVA !'.format(factoryNumber,platform)

        if separate_order_string in orders.keys():
            order_positions = orders[separate_order_string]['positions']
        else:
            orders[separate_order_string] = []
            orders[separate_order_string] = {
                'positions': [],
                'delivery_date': delivery_date,
                'note': order_note
            }
            order_positions = orders[separate_order_string]['positions']

        order_positions.append({    'additional_properties': additional_properties,
                                    'order_position': getNodeValue(line_item_node,ns,'./cbc:ID'),
                                    'sales_order': getNodeValue(order_line_node,ns,'./cac:DocumentReference/cbc:ID'),
                                    'vendor_info': getNodeValue(line_item_node,ns,'./cac:Item/cac:SellersItemIdentification/cbc:ID'),
                                    'delivery_date': getNodeValue(line_item_node,ns,'./cac:Delivery/cbc:LatestDeliveryDate'),
                                    'buyers_item_identification': getNodeValue(line_item_node,ns,'./cac:Item/cac:BuyersItemIdentification/cbc:ID'),
                                    'quantity': dovista_float2int(getNodeValue(line_item_node,ns,'./cbc:Quantity'))
                                })

#przygotowanie pliku wyjsciowego
xml_import = ET.Element('cutterImportOrderFile',attrib={"format_version":COIFVERSION,"script":"dovista2cutter","script_version":BUILDVERSION})
ET.SubElement(xml_import,'original_filename').text = os.path.basename(input_filename)

#generowanie gałęzi <customer> - na razie nie wiem po co
# xml_customer = ET.SubElement(xml_import,'customer')
# ET.SubElement(xml_customer,'name').text = 'Olek'


#generowanie pozycji w pliku wyjściowym
# print(orders.keys())
for k in orders.keys():
#generowanie gałezi <order>
    positions = orders[k]['positions']
    xml_order = ET.SubElement(xml_import,'order',attrib={"comment":k})

    #generowanie zlec_typ dla zlecenia 
    ET.SubElement(xml_order,'additionalInfo',attrib={"type": "301", "comment":"OrderConfirmation: BuyerCustomerParty/ID"}).text = getNodeValue(root,ns,'./cac:BuyerCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID')
    ET.SubElement(xml_order,'additionalInfo',attrib={"type": "302", "comment":"OrderConfirmation: BuyerCustomerParty/CompanyID"}).text = getNodeValue(root,ns,'./cac:BuyerCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID')

    #pobieranie danych z nagłówka 

    #pobranie informacji o kliencie z C_BRAND z 1. pozycji 
    customer_brand = getAdditionalPropertiesValue(positions[0],'C_BRAND','name')

    cutter_customer_info = {
        'RATIONEL': {
            'cutter_number': 60261,
            'delivery_adresses':{
                'T1': '522',
                'T2': '523',
                'T3': '524',
                'T4': '525',
                'T5': '526',
                'T7': '527',
                'M1': '528'
            }
        },
        'VELFAC': {
            'cutter_number': 60262,
            'delivery_adresses':{
                'T1': '529',
                'T2': '530',
                'T3': '531',
                'T4': '532',
                'T5': '533',
                'T7': '534',
                'M1': '535'
            }
        }
    }

    ET.SubElement(xml_order,'deliveryAddress').text = deliveryAddress
    ET.SubElement(xml_order,'customer_name',{'comment':'factory='+factoryNumber}).text = customer_brand
    if customer_brand in cutter_customer_info:
        if 'cutter_number' in cutter_customer_info[customer_brand]:
            ET.SubElement(xml_order,'customer_cutter_number').text = str(cutter_customer_info[customer_brand]['cutter_number'])
        if 'delivery_adresses' in cutter_customer_info[customer_brand]:
            if factoryNumber in cutter_customer_info[customer_brand]['delivery_adresses']:
                ET.SubElement(xml_order,'delivery_cutter_number').text = str(cutter_customer_info[customer_brand]['delivery_adresses'][factoryNumber])
    orderNumberByCustomer = getNodeValue(root,ns,'./cbc:ID')
    ET.SubElement(xml_order,'numberByCustomer').text = orderNumberByCustomer
    ET.SubElement(xml_order,'order_date').text = date2Cutter(date.today())
    ET.SubElement(xml_order,'notes').text = orders[k]['note']
    ET.SubElement(xml_order,'internal_number').text = ''

    #delivery date z pozycji zlecenia
    delivery_date = dovista_string2date(orders[k]['delivery_date'])
    ET.SubElement(xml_order,'delivery_date').text = date2Cutter(delivery_date)
    ET.SubElement(xml_order,'customer_date').text = date2Cutter(delivery_date)

    for position in positions:
        xml_position = ET.SubElement(xml_order,'position')
        ET.SubElement(xml_position,'width').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))
        ET.SubElement(xml_position,'height').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))  
        ET.SubElement(xml_position,'quantity').text = str(position['quantity'])

        code = ''
        glass_unit = str(getAdditionalPropertiesValue(position,'C_GLASS_UNIT','name'))
        if glass_unit == 'DGU':
            elements = [
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value'),
            ]
        elif glass_unit == 'TGU':
            elements = [
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value'),
            ]

        elif glass_unit == 'QGU':
            elements = [
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER3','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET4','value'),
            ]
        else:
            elements = [
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER3','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET4','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SPACER4','value'),
                getAdditionalPropertiesValue(position,'C_GLASS_SHEET5','value')
            ]

        code = joinStringsWithoutEmpty(elements,'/')

        ET.SubElement(xml_position,'structureCode').text = code
        ET.SubElement(xml_position,'structureName').text = getAdditionalPropertiesValue(position,'C_GLASS_CODE','value')
        ET.SubElement(xml_position,'description').text = str(position['vendor_info']).replace('GLASS_','').replace('-','').replace(' ','').replace('(','').replace(')','')
        ET.SubElement(xml_position,'delivery_date').text = position['delivery_date']

        # --- BEGIN --- obsługa kształtów DOVISTA
        shape_drawing = getAdditionalPropertiesValue(position,'C_DRAWING','value')
        shape_params_def = {
            'l':    'C_W',
            'l1':   'C_W1',
            'l2':   'C_W2',
            'h':    'C_H',
            'h1':   'C_H1',
            'h2':   'C_H2',
            'r':    'C_RADIUS',
            'r1':   'C_RADIUS1',
            'r2':   'C_RADIUS2',
            'r3':   'C_RADIUS3'
        }
            
        if shape_drawing != '':
            xml_shape = ET.SubElement(xml_position,'shape',{'desc':shape_drawing})
            shape_number = dovista_drawing2shape(shape_drawing)
            if shape_number>0:
                #ET.SubElement(xml_shape,'catalogue',).text = '3'
                #ET.SubElement(xml_shape,'number').text = str(shape_number)
                shape_params = {
                    'catalogue': 3,
                    'number': shape_number,
                    'l':    0,
                    'l1':   0,
                    'l2':   0,
                    'h':    0,
                    'h1':   0,
                    'h2':   0,
                    'r':    0,
                    'r1':   0,
                    'r2':   0,
                    'r3':   0
                }
                
                # Pobranie parametrów do dict shape_params
                for k in shape_params_def.keys():
                    value = dovista_float2int(getAdditionalPropertiesValue(position,shape_params_def[k],'value'))
                    if k =='l' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value'))
                    if k == 'h' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value'))
                    if value > 0:
                        shape_params[k] = value
                # Odwrócenie kształtu. Kształty DVA są z widokiem od zewnątrz. W EFF trzeba odwrócić
                shape_params = mirrorShape(shape_params)
                # Zapisanie nie zerowych parametrów kształtu do XMLa.
                for k in shape_params.keys():
                    if shape_params[k]>0:
                        ET.SubElement(xml_shape,k).text = str(shape_params[k])
            else:
                ET.SubElement(xml_shape,'catalogue').text = '3'
        # --- END --- obsługa kształtów DOVISTA

        if (getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value')!=''):
            chamber_count = 1
        if (getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value')!=''):
            chamber_count = 2
        if (getAdditionalPropertiesValue(position,'C_GLASS_SPACER3','value')!=''):
            chamber_count = 3
        if (getAdditionalPropertiesValue(position,'C_GLASS_SPACER4','value')!=''):
            chamber_count = 4
        # --- BEGIN --- obsługa szprosów dowolnych
        gb_elevation = 0
        if 'C_GLZBAR_G_ELEV' in position['additional_properties']:
            gb_elevation = position['additional_properties']['C_GLZBAR_G_ELEV']['name']
        if len(getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W1','value'))>0:
            xml_gb = ET.SubElement(xml_position,'custom_glazing_bar')
            for frameno in range(1,chamber_count+1):
                xml_gb_frame = ET.SubElement(xml_gb,'frame',{'no':str(frameno)})

                ET.SubElement(xml_gb_frame,'elevation').text = gb_elevation

                xml_gb_frame_seq = ET.SubElement(xml_gb_frame,'sequence')
                d = {
                    'w1' : 'C_GLASS_SEQ_W1',
                    'w2' : 'C_GLASS_SEQ_W2',
                    'w3' : 'C_GLASS_SEQ_W3',
                    'w4' : 'C_GLASS_SEQ_W4',
                    'w5' : 'C_GLASS_SEQ_W5',
                    'w6' : 'C_GLASS_SEQ_W6',
                    'w7' : 'C_GLASS_SEQ_W7',
                    'w8' : 'C_GLASS_SEQ_W8',
                    'w9' : 'C_GLASS_SEQ_W9',
                    'h1' : 'C_GLASS_SEQ_H1',
                    'h2' : 'C_GLASS_SEQ_H2',
                    'h3' : 'C_GLASS_SEQ_H3',
                    'h4' : 'C_GLASS_SEQ_H4',
                    'h5' : 'C_GLASS_SEQ_H5',
                    'h6' : 'C_GLASS_SEQ_H6',
                    'h7' : 'C_GLASS_SEQ_H7',
                    'h8' : 'C_GLASS_SEQ_H8',
                    'h9' : 'C_GLASS_SEQ_H9'
                }
                for k in d.keys():
                    value = getAdditionalPropertiesValue(position,d[k],'value')
                    if value != '' and value != '0':
                        ET.SubElement(xml_gb_frame_seq,k).text = value

                xml_gb_frame_dim = ET.SubElement(xml_gb_frame,'dimmensions')
                d = {
                    'w1' : 'C_GLASS_GW9',
                    'w2' : 'C_GLASS_GW8',
                    'w3' : 'C_GLASS_GW7',
                    'w4' : 'C_GLASS_GW6',
                    'w5' : 'C_GLASS_GW5',
                    'w6' : 'C_GLASS_GW4',
                    'w7' : 'C_GLASS_GW3',
                    'w8' : 'C_GLASS_GW2',
                    'w9' : 'C_GLASS_GW1',
                    'h9' : 'C_GLASS_GH9',
                    'h8' : 'C_GLASS_GH8',
                    'h7' : 'C_GLASS_GH7',
                    'h6' : 'C_GLASS_GH6',
                    'h5' : 'C_GLASS_GH5',
                    'h4' : 'C_GLASS_GH4',
                    'h3' : 'C_GLASS_GH3',
                    'h2' : 'C_GLASS_GH2',
                    'h1' : 'C_GLASS_GH1'
                }

                bar_no = 0
                # analiza listew pionowych
                width = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value'))
                for k in d.keys():
                    value = dovista_float2int(getAdditionalPropertiesValue(position,d[k],'value'))
                    if value>0 and k[0]=='w':
                        value = int(width)-int(value)
                        bar_no = bar_no + 1
                        ET.SubElement(xml_gb_frame_dim,k[0]+str(bar_no)).text = str(value)
                #analiza listew poziomych (od góry)
                bar_no = 0
                height = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value'))
                for k in d.keys():
                    value = dovista_float2int(getAdditionalPropertiesValue(position,d[k],'value'))
                    if value>0 and k[0]=='h':
                        value = int(height)-int(value)
                        bar_no = bar_no + 1
                        ET.SubElement(xml_gb_frame_dim,k[0]+str(bar_no)).text = str(value)

                xml_gb_frame_mat = ET.SubElement(xml_gb_frame,'material')
                d = {
                    'w1' : 'C_GLASS_VAR_GW1',
                    'w2' : 'C_GLASS_VAR_GW2', 
                    'w3' : 'C_GLASS_VAR_GW3', 
                    'w4' : 'C_GLASS_VAR_GW4',
                    'w5' : 'C_GLASS_VAR_GW5', 
                    'w6' : 'C_GLASS_VAR_GW6', 
                    'w7' : 'C_GLASS_VAR_GW7', 
                    'w8' : 'C_GLASS_VAR_GW8', 
                    'w9' : 'C_GLASS_VAR_GW9',
                    'h1' : 'C_GLASS_VAR_GH1', 
                    'h2' : 'C_GLASS_VAR_GH2', 
                    'h3' : 'C_GLASS_VAR_GH3', 
                    'h4' : 'C_GLASS_VAR_GH4', 
                    'h5' : 'C_GLASS_VAR_GH5', 
                    'h6' : 'C_GLASS_VAR_GH6', 
                    'h7' : 'C_GLASS_VAR_GH7', 
                    'h8' : 'C_GLASS_VAR_GH8', 
                    'h9' : 'C_GLASS_VAR_GH9'
                }
                gb_colour = getAdditionalPropertiesValue(position,'C_GLASS_SPACER'+str(frameno)+'_COLOUR','value')
                for k in d.keys():
                    value = getAdditionalPropertiesValue(position,d[k],'name')
                    if value != '' and  value != '00':
                        ET.SubElement(xml_gb_frame_mat,k).text = value +' '+gb_colour

        # --- END --- obsługa szprosów dowolnych


        # generowanie zlec_typ dla pozycji
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "301", "comment":"Label/Frame: DVA Vendor number"}).text = str(getAdditionalPropertiesValue(position,'C_VENDOR','value'))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "303", "comment":"Label: DVA Purchase order number"}).text = orderNumberByCustomer
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "304", "comment":"Label: DVA Purchase order position "}).text = str(position['order_position'])
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "305", "comment":"Label/Frame: DVA Sales order"}).text = str(position['sales_order'])
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "306", "comment":"Label: DVA Vendor info"}).text = str(position['vendor_info'])
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "307", "comment":"Label: DVA Platform"}).text = str(getAdditionalPropertiesValue(position,'C_PLATFORM','value'))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "308", "comment":"Label: DVA Factory number"}).text = factoryNumber

        if 'C_GLASS_SHEET1' in position['additional_properties']:
            code = getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value')

        product_code_long_name = ''
        sep = '/'
        if glass_unit == 'DGU':
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value') + ' '
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value') + ' '
        elif glass_unit == 'TGU':
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value') + ' '
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value') + ' '
        elif glass_unit == 'QGU':
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value') + ' '
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER3','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER3','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET4','value') + ' '
        else:       
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value') + ' '
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER1','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER2','value') + sep
            product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value') + ' '

        product_code_long_name = product_code_long_name + 'U='+getAdditionalPropertiesValue(position,'C_GLASS_U_VALUE','value') + ' '
        product_code_long_name = product_code_long_name + 'Lt='+getAdditionalPropertiesValue(position,'C_GLASS_LT_VALUE','name') + ' '
        product_code_long_name = product_code_long_name + 'G='+getAdditionalPropertiesValue(position,'C_GLASS_G_VALUE','value')

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "309", "comment":"Label: DVA Glass code long text descrition"}).text = product_code_long_name
        
        dimensions = ''
        dimensions = dimensions + str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))+'x'
        dimensions = dimensions + str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))+'x'
        #glass_thick_list = str(getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value')).split('-')
        glass_thick_list = [
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SHEET1_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SHEET2_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SHEET3_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SHEET4_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SHEET5_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SPACER1_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SPACER2_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SPACER3_THICKNESS','name')),
            dovista_float(getAdditionalPropertiesValue(position,'C_GLASS_SPACER4_THICKNESS','name'))
        ]
        total_thickness = 0
        for t in range(0, len(glass_thick_list)): 
            #if len(glass_thick_list[t].strip())>0:
            total_thickness = total_thickness + glass_thick_list[t]
        dimensions = dimensions + str(total_thickness) + 'MM'
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "310", "comment":"Label: DVA Dimmensions(width,height,thickness)"}).text = dimensions

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "311", "comment":"Label: DVA Drawing 1"}).text = getAdditionalPropertiesValue(position,'C_DRAWING','value')
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "312", "comment":"Label: DVA Glazing bar elev. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_ELEV','name')
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "313", "comment":"Label: DVA Glazing bar var. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_VAR','name')
        #14 Emalit colour
        # ET.SubElement(xml_position,'additionalInfo',attrib={"type": "314"}).text = ''
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "316", "comment":"Label: DVA Barcode on label"}).text = orderNumberByCustomer+str(position['order_position'])
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "317", "comment":"Label/Frame: C_GLASS_CODE"}).text = getAdditionalPropertiesValue(position,'C_GLASS_CODE','value')
        production_order = ''
        matchObj = re.match(r'[^\/]*',str(position['vendor_info']))
        if matchObj is not None:
            production_order = matchObj.group(0)
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "318", "comment":"Frame: production order"}).text = production_order
        production_order2 = ''
        matchObj = re.match(r'[^\-]*',str(position['vendor_info']))
        if matchObj is not None:
            production_order2 = matchObj.group(0)
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "319", "comment":"Delivery doc: production order2"}).text = production_order2

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "109", "comment":"Prints: Opis struktury według klienta"}).text = product_code_long_name

        #klucze dla OrderConfirmation
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "320", "comment":"OrderConfirmation: DVA Purchase order position "}).text = str(position['order_position'])
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "321", "comment":"OrderConfirmation: DVA Glass code long text descrition"}).text = product_code_long_name
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "322", "comment":"OrderConfirmation: BuyersItemIdentification"}).text = str(position['buyers_item_identification'])

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "330", "comment":"Label/Frame: DVA width"}).text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "331", "comment":"Label/Frame: DVA height"}).text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "332", "comment":"Label: DVA thickness"}).text = str(total_thickness)
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "333", "comment":"Frame: U-Value"}).text = str(getAdditionalPropertiesValue(position,'C_GLASS_U_VALUE','value'))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "334", "comment":"Frame: G-Value"}).text = str(getAdditionalPropertiesValue(position,'C_GLASS_G_VALUE','value'))
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "335", "comment":"Frame: Lt-Value"}).text = str(getAdditionalPropertiesValue(position,'C_GLASS_LT_VALUE','value'))
        sideinout_text = 'THIS SIDE IN'
        if factoryNumber in ['T1','T2','T3','T4']:
            sideinout_text = 'THIS SIDE OUT'
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "336", "comment":"Label: Side In/Out"}).text = sideinout_text


# koniec iteracji po pozycjach


# xml = ET.ElementTree(xml_import)

#zapis pliku wyjściowego w formacie xml
xmlstr = minidom.parseString(ET.tostring(xml_import,encoding="utf-8")).toprettyxml(indent="   ")
# print(xmlstr)
with open (output_filename, "w", encoding="utf-8") as xmlfile: 
    xmlfile.write(xmlstr)
