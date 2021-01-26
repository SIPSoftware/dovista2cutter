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

def date2Cutter(d):
    return d.strftime("%Y-%m-%d")


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

#usun plik wyjściowy jeżeli istnieje
if os.path.exists(output_filename):
    os.remove(output_filename)

#parsowanie pliku XML
tree = ET.parse(input_filename)
root = tree.getroot()

orders = {}
#order_positions = []
#iteracja po OrderLine
for order_line_node in root.findall('cac:OrderLine',ns):
    #iteracja po LineItem
    for line_item_node in order_line_node.findall('cac:LineItem',ns):
        #pobranie informacji o pozycji
    
        #podział pozycje na różne zlecenia w zależności od daty dostawy
        delivery_date = getNodeValue(line_item_node,ns,'./cac:Delivery/cbc:LatestDeliveryDate')
        if delivery_date in orders.keys():
            order_positions = orders[delivery_date]
        else:
            orders[delivery_date] = []
            order_positions = orders[delivery_date]
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
                                    'order_position': getNodeValue(line_item_node,ns,'./cbc:ID'),
                                    'sales_order': getNodeValue(order_line_node,ns,'./cac:DocumentReference/cbc:ID'),
                                    'vendor_info': getNodeValue(line_item_node,ns,'./cac:Item/cac:SellersItemIdentification/cbc:ID'),
                                    'delivery_date': getNodeValue(line_item_node,ns,'./cac:Delivery/cbc:LatestDeliveryDate')
                                })

#przygotowanie pliku wyjsciowego
xml_import = ET.Element('cutterImportOrderFile')
ET.SubElement(xml_import,'original_filename').text = os.path.basename(input_filename)

#generowanie gałęzi <customer> - na razie nie wiem po co
xml_customer = ET.SubElement(xml_import,'customer')
ET.SubElement(xml_customer,'name').text = 'VELFAC'


#generowanie pozycji w pliku wyjściowym
print(orders.keys())
for k in orders.keys():
#generowanie gałezi <order>
    xml_order = ET.SubElement(xml_import,'order')

    #generowanie zlec_typ dla zlecenia 
    # ET.SubElement(xml_order,'additionalInfo',attrib={"type": "10"}).text = "Zlec_typ 10 dla zlecenia"

    #pobieranie danych z nagłówka 
    ET.SubElement(xml_order,'deliveryAddress').text = getNodeValue(root,ns,'./cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name')
    ET.SubElement(xml_order,'delivery_cutter_number').text = str(227)
    orderNumberByCustomer = getNodeValue(root,ns,'./cbc:ID')
    ET.SubElement(xml_order,'numberByCustomer').text = orderNumberByCustomer
    ET.SubElement(xml_order,'order_date').text = date2Cutter(date.today())
    ET.SubElement(xml_order,'notes').text = ''
    ET.SubElement(xml_order,'internal_number').text = ''


    #delivery date z pozycji zlecenia
    delivery_date = dovista_string2date(k)
    ET.SubElement(xml_order,'delivery_date').text = date2Cutter(delivery_date)
    ET.SubElement(xml_order,'customer_date').text = date2Cutter(delivery_date)

    for position in orders[k]:
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
        ET.SubElement(xml_position,'description').text = position['vendor_info']
        ET.SubElement(xml_position,'delivery_date').text = position['delivery_date']

        # --- BEGIN --- obsługa kształtów DOVISTA
        shape_drawing = getAdditionalPropertiesValue(position,'C_DRAWING','value')
        shape_params = {
            'l':    'C_W',
            'l1':   'C_W1',
            'l2':   'C_W2',
            'h':    'C_H',
            'h1':   'C_H1',
            'h2':   'C_H2',
            'r':    'C_R',
            'r1':   'C_R1',
            'r2':   'C_R2',
            'r3':   'C_R3'
        }
            
        if shape_drawing != '':
            xml_shape = ET.SubElement(xml_position,'shape',{'desc':shape_drawing})
            ET.SubElement(xml_shape,'catalogue',).text = '3'
            shape_number = dovista_drawing2shape(shape_drawing)
            if shape_number>0:
                ET.SubElement(xml_shape,'number').text = str(shape_number)
                
                # print(shape_params.keys())
                for k in shape_params.keys():
                    value = dovista_float2int(getAdditionalPropertiesValue(position,shape_params[k],'value'))
                    if k =='l' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_WIDTH','value'))
                    if k == 'h' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(position,'C_GLASS_HEIGHT','value'))
                    if value > 0:
                        ET.SubElement(xml_shape,k).text = str(value)
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
                    'w1' : 'C_GLASS_GW1',
                    'w2' : 'C_GLASS_GW2',
                    'w3' : 'C_GLASS_GW3',
                    'w4' : 'C_GLASS_GW4',
                    'w5' : 'C_GLASS_GW5',
                    'w6' : 'C_GLASS_GW6',
                    'w7' : 'C_GLASS_GW7',
                    'w8' : 'C_GLASS_GW8',
                    'w9' : 'C_GLASS_GW9',
                    'h1' : 'C_GLASS_GH1',
                    'h2' : 'C_GLASS_GH2',
                    'h3' : 'C_GLASS_GH3',
                    'h4' : 'C_GLASS_GH4',
                    'h5' : 'C_GLASS_GH5',
                    'h6' : 'C_GLASS_GH6',
                    'h7' : 'C_GLASS_GH7',
                    'h8' : 'C_GLASS_GH8',
                    'h9' : 'C_GLASS_GH9'
                }

                for k in d.keys():
                    value = dovista_float2int(getAdditionalPropertiesValue(position,d[k],'value'))
                    if value>0:
                        ET.SubElement(xml_gb_frame_dim,k).text = str(value)

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
        product_code_long_name = product_code_long_name + 'U='+getAdditionalPropertiesValue(position,'C_GLASS_U_VALUE','value') + ' '
        product_code_long_name = product_code_long_name + 'Lt='+getAdditionalPropertiesValue(position,'C_GLASS_LT_VALUE','name') + ' '
        product_code_long_name = product_code_long_name + 'G='+getAdditionalPropertiesValue(position,'C_GLASS_G_VALUE','value')

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "309", "comment":"DVA Glass code long text descrition"}).text = product_code_long_name
        
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
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "310", "comment":"DVA Dimmensions(width,height,thickness)"}).text = dimensions

        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "311", "comment":"DVA Drawing 1"}).text = getAdditionalPropertiesValue(position,'C_DRAWING','value')
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "312", "comment":"DVA Glazing bar elev. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_ELEV','name')
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "313", "comment":"DVA Glazing bar var. glass"}).text = getAdditionalPropertiesValue(position,'C_GLZBAR_G_VAR','name')
        #14 Emalit colour
        # ET.SubElement(xml_position,'additionalInfo',attrib={"type": "314"}).text = ''
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "316", "comment":"DVA Barcode on label"}).text = orderNumberByCustomer+str(position['order_position'])
        
        ET.SubElement(xml_position,'additionalInfo',attrib={"type": "109", "comment":"Opis struktury według klienta"}).text = product_code_long_name


# koniec iteracji po pozycjach


# xml = ET.ElementTree(xml_import)

#zapis pliku wyjściowego w formacie xml
xmlstr = minidom.parseString(ET.tostring(xml_import,encoding="utf-8")).toprettyxml(indent="   ")
# print(xmlstr)
with open (output_filename, "w", encoding="utf-8") as xmlfile: 
    xmlfile.write(xmlstr)
