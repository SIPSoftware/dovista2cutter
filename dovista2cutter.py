COIFVERSION = "1.0"
BUILDVERSION = "1.0.2"

import xml.etree.ElementTree as ET
import os
import sys
import argparse
import re
from datetime import date
from xml.dom import minidom

from dovista import *
import shape

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
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
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
                shape_params = shape.mirror(shape_params)
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
