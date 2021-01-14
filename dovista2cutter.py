import xml.etree.ElementTree as ET
import csv
import os
import sys
import argparse
import re
from xml.dom import minidom

def dovista_int2int(string_number):
    if len(string_number)>0:
        string_number = string_number.replace(',','')
        string_number = string_number.replace('.','')
        return int(string_number)
    else:
        return 0

def dovista_float2int(string_number):
    # print(string_number)
    # print(round(float(string_number)))
    if len(string_number)>0:
        return round(float(string_number))
    else:
        return 0

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
    elif drawing == '3011.0089-77':
        return 77
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

print(input_filename)
print(output_filename)
print('-'*50)

#parsowanie pliku XML
tree = ET.parse(input_filename)
root = tree.getroot()

#przygotowanie pliku wyjsciowego
xml_import_order = ET.Element('cutterImportOrderFile')

#generowanie gałezi <order>
xml_order = ET.SubElement(xml_import_order,'order')

#pobieranie danych z nagłówka 
ET.SubElement(xml_order,'deliveryAddress').text = getNodeValue(root,ns,'./cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name')

orderNumberByCustomer = getNodeValue(root,ns,'./cbc:ID')
ET.SubElement(xml_order,'numberByCustomer').text = orderNumberByCustomer

#generowanie gałęzi <customer>
xml_customer = ET.SubElement(xml_import_order,'customer')
ET.SubElement(xml_customer,'name').text = 'VELFAC'


order_positions = []
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

        order_positions.append({    'additional_properties': additional_properties,
                                    'sellers_item_identification':getNodeValue(line_item_node,ns,'./cac:Item/cac:SellersItemIdentification/cbc:ID'),
                                    'order_position': getNodeValue(line_item_node,ns,'./cbc:ID'),
                                    'sales_order': getNodeValue(order_line_node,ns,'./cac:DocumentReference/cbc:ID'),
                                    'vendor_info': getNodeValue(line_item_node,ns,'./cac:Item/cac:SellersItemIdentification/cbc:ID')})

#generowanie zlec_typ dla zlecenia 
# ET.SubElement(xml_order,'additionalInfo',attrib={"type": "10"}).text = "Zlec_typ 10 dla zlecenia"

#generowanie pozycji w pliku wyjściowym
for position in order_positions:
    xml_position = ET.SubElement(xml_order,'position')
    ET.SubElement(xml_position,'width').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))
    ET.SubElement(xml_position,'height').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))  

    code = ''
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
    ET.SubElement(xml_position,'description').text = position['sellers_item_identification']

# obsługa kształtów DOVISTA
    shape_params = {    'drawing': None,
                        'l': None,
                        'l1': None,
                        'l2': None,
                        'h': None,
                        'h1': None,
                        'h2': None,
                        'r': None,
                        'r1': None,
                        'r2': None,
                        'r3': None,
    }
    shape_params['drawing'] = getAdditionalPropertiesValue(position,'C_DRAWING','value')
    shape_params['l'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_W','value'))
    shape_params['l1'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_W1','value'))
    shape_params['l2'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_W2','value'))
    shape_params['h'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_H','value'))
    shape_params['h1'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_H1','value'))
    shape_params['h2'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_H2','value'))
    shape_params['r'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_R','value'))
    shape_params['r1'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_R1','value'))
    shape_params['r2'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_R2','value'))
    shape_params['r3'] = dovista_float2int(getAdditionalPropertiesValue(position,'C_R3','value'))

    if shape_params['drawing'] is not None:
        xml_shape = ET.SubElement(xml_position,'shape')
        shape_number = dovista_drawing2shape(shape_params['drawing'])
        if shape_number>0:
            ET.SubElement(xml_shape,'catalogue').text = '3'
            ET.SubElement(xml_shape,'number').text = str(shape_number)
            if shape_params['l'] is not None:
                ET.SubElement(xml_shape,'L').text = str(shape_params['l'])
            else:
                ET.SubElement(xml_shape,'L').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))
            if shape_params['l1'] is not None:
                ET.SubElement(xml_shape,'L1').text = str(shape_params['l1'])
            if shape_params['l2'] is not None:
                ET.SubElement(xml_shape,'L2').text = str(shape_params['l2'])
            if shape_params['h'] is not None:
                ET.SubElement(xml_shape,'H').text = str(shape_params['h'])
            else:
                ET.SubElement(xml_shape,'H').text = str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))
            if shape_params['h1'] is not None:
                ET.SubElement(xml_shape,'H1').text = str(shape_params['h1'])
            if shape_params['h2'] is not None:
                ET.SubElement(xml_shape,'H2').text = str(shape_params['h2'])
            if shape_params['r'] is not None:
                ET.SubElement(xml_shape,'R').text = str(shape_params['r'])
            if shape_params['r1'] is not None:
                ET.SubElement(xml_shape,'R1').text = str(shape_params['r1'])
            if shape_params['r2'] is not None:
                ET.SubElement(xml_shape,'R2').text = str(shape_params['r2'])
            if shape_params['r3'] is not None:
                ET.SubElement(xml_shape,'R3').text = str(shape_params['r3'])
    
    #obsługa szprosów dowolnych
    gb_elevation = 0
    if 'C_GLZBAR_G_ELEV' in position['additional_properties']:
        gb_elevation = position['additional_properties']['C_GLZBAR_G_ELEV']['name']
    if gb_elevation is None or gb_elevation!='G1':
        xml_gb = ET.SubElement(xml_position,'georgian_bar_custom')
        ET.SubElement(xml_gb,'elevation').text = gb_elevation

        xml_gb_seq = ET.SubElement(xml_gb,'sequence')
        ET.SubElement(xml_gb_seq,'w1').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W1','value')
        ET.SubElement(xml_gb_seq,'w2').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W2','value')
        ET.SubElement(xml_gb_seq,'w3').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W3','value')
        ET.SubElement(xml_gb_seq,'w4').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W4','value')
        ET.SubElement(xml_gb_seq,'w5').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W5','value')
        ET.SubElement(xml_gb_seq,'w6').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W6','value')
        ET.SubElement(xml_gb_seq,'w7').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W7','value')
        ET.SubElement(xml_gb_seq,'w8').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W8','value')
        ET.SubElement(xml_gb_seq,'w9').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_W9','value')
        ET.SubElement(xml_gb_seq,'h1').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H1','value')
        ET.SubElement(xml_gb_seq,'h2').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H2','value')
        ET.SubElement(xml_gb_seq,'h3').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H3','value')
        ET.SubElement(xml_gb_seq,'h4').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H4','value')
        ET.SubElement(xml_gb_seq,'h5').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H5','value')
        ET.SubElement(xml_gb_seq,'h6').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H6','value')
        ET.SubElement(xml_gb_seq,'h7').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H7','value')
        ET.SubElement(xml_gb_seq,'h8').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H8','value')
        ET.SubElement(xml_gb_seq,'h9').text = getAdditionalPropertiesValue(position,'C_GLASS_SEQ_H9','value')

        xml_gb_dim = ET.SubElement(xml_gb,'dimmensions')
        ET.SubElement(xml_gb_dim,'w1').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW1','value')))
        ET.SubElement(xml_gb_dim,'w2').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW2','value')))
        ET.SubElement(xml_gb_dim,'w3').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW3','value')))
        ET.SubElement(xml_gb_dim,'w4').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW4','value')))
        ET.SubElement(xml_gb_dim,'w5').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW5','value')))
        ET.SubElement(xml_gb_dim,'w6').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW6','value')))
        ET.SubElement(xml_gb_dim,'w7').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW7','value')))
        ET.SubElement(xml_gb_dim,'w8').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW8','value')))
        ET.SubElement(xml_gb_dim,'w9').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GW9','value')))
        ET.SubElement(xml_gb_dim,'h1').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH1','value')))
        ET.SubElement(xml_gb_dim,'h2').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH2','value')))
        ET.SubElement(xml_gb_dim,'h3').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH3','value')))
        ET.SubElement(xml_gb_dim,'h4').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH4','value')))
        ET.SubElement(xml_gb_dim,'h5').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH5','value')))
        ET.SubElement(xml_gb_dim,'h6').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH6','value')))
        ET.SubElement(xml_gb_dim,'h7').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH7','value')))
        ET.SubElement(xml_gb_dim,'h8').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH8','value')))
        ET.SubElement(xml_gb_dim,'h9').text = str(dovista_float2int(getAdditionalPropertiesValue(position,'C_GLASS_GH9','value')))


    # generowanie zlec_typ dla pozycji
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "301", "comment":"DVA Vendor number"}).text = str(getAdditionalPropertiesValue(position,'C_VENDOR','value'))
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "303", "comment":"DVA Purchase order number"}).text = orderNumberByCustomer
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "304", "comment":"DVA Purchase order position "}).text = str(position['order_position'])
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "305", "comment":"DVA Sales order"}).text = str(position['sales_order'])
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "306", "comment":"DVA Vendor info"}).text = str(position['vendor_info'])
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "307", "comment":"DVA Platform"}).text = str(getAdditionalPropertiesValue(position,'C_PLATFORM','value'))
    deliveryAddress = getNodeValue(root,ns,'./cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name')
    factoryNumber=''
    # ----wersja 1. tylko litera T i póżniej ciąg cyfr
    # matchObj = re.match(r'.*(T[0-9]*)',deliveryAddress)
    # ----wersja 2. Factory potem dowolny znak potem ciąg cyfr
    matchObj = re.match(r'.*Factory (.[0-9]*)',deliveryAddress)
    if matchObj is not None:
        factoryNumber = matchObj.group(1)
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "308", "comment":"DVA Factory number"}).text = factoryNumber

    if 'C_GLASS_SHEET1' in position['additional_properties']:
        code = getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value')

    product_code_long_name = ''
    sep = '/'
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value') + ' '
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET1','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER1','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER1','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET2','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SPACER2','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_AIR_SPACER2','value') + sep
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_SHEET3','value') + ' '
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_U_VALUE','value') + ' '
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_LT_VALUE','name') + ' '
    product_code_long_name = product_code_long_name + getAdditionalPropertiesValue(position,'C_GLASS_G_VALUE','value')

    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "309", "comment":"DVA Glass code long text descrition"}).text = product_code_long_name
    
    dimensions = ''
    dimensions = dimensions + str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value')))+'x'
    dimensions = dimensions + str(dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value')))+'x'
    glass_thick_list = str(getAdditionalPropertiesValue(position,'C_GLASS_THICK_BUILDUP','value')).split('-')
    total_thickness = 0
    for t in range(0, len(glass_thick_list)): 
        total_thickness = total_thickness + int(glass_thick_list[t])
    dimensions = dimensions + str(total_thickness) + 'MM'
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "310", "comment":"DVA Dimmensions(width,height,thickness)"}).text = dimensions

    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "311", "comment":"DVA Drawing 1"}).text = getAdditionalPropertiesValue(position,'C_DRAWING','value')
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "312", "comment":"DVA Glazing bar elev. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_ELEV','name')
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "313", "comment":"DVA Glazing bar var. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_VAR','name')
    #14 Emalit colour
    # ET.SubElement(xml_position,'additionalInfo',attrib={"type": "314"}).text = ''
    ET.SubElement(xml_position,'additionalInfo',attrib={"type": "316", "comment":"DVA Barcode on label"}).text = orderNumberByCustomer+str(position['order_position'])
    

# koniec iteracji po pozycjach


# xml = ET.ElementTree(xml_import_order)

#zapis pliku wyjściowego w formacie xml
xmlstr = minidom.parseString(ET.tostring(xml_import_order,encoding="utf-8")).toprettyxml(indent="   ")
# print(xmlstr)
with open (output_filename, "w", encoding="utf-8") as xmlfile: 
    xmlfile.write(xmlstr)
