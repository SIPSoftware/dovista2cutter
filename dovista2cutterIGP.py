from default_config import default_config
import shape
from dovista import *
import json
from xml.dom import minidom
from datetime import date
import re
import argparse
import sys
import os
import xml.etree.ElementTree as ET
COIFVERSION = "1.0"
BUILDVERSION = "1.0.2"


ns = {'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
      'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
      'ccts': "urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2",
      'sdt': "urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2",
      'udt': "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2",
      'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

# przygotowanie parsowania parametrów wejściowych
parser = argparse.ArgumentParser(
    description='Skrypt konwersji pliku Dovista XML (wersja IGP) do formatu Cutter Customer Order Import File')
parser.add_argument('-i', dest='inputfile',
                    help='plik wejściowy')
parser.add_argument('-o', dest='outputfile',
                    help='plik wyjściowy')
parser.add_argument('--sepfn', action="extend", nargs="+", type=str, dest='separate_order_factory_number',
                    help='lista factoryNumber dla których będzie podział zlecenia ze wzgledu na Elevation Shape')
parser.add_argument('--config-file', dest='config_file_path',
                    help='ścieżka do pliku konfiguracyjnego')

# parsowanie parametrów wejściowych
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

# sprawdzenie parametrów wejściowych
if os.path.exists(args.inputfile):
    input_filename = args.inputfile
    if args.outputfile is None:
        output_filename = os.path.splitext(
            os.path.basename(input_filename))[0]+'.csv'
        output_filename = os.path.join(
            os.path.dirname(input_filename), output_filename)
    else:
        output_filename = args.outputfile
else:
    print("No such file: "+args.inputfile)
    sys.exit()

# wczytanie konfiguracji skryptu
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

if args.config_file_path is None:
    config_file_path = os.path.join(dname, 'dovista.config.json')
else:
    config_file_path = args.config_file_path

config = None
print("config file path: "+config_file_path)
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as f:
        config = json.load(f)

config_cutter_customer_info = None


print('input file: '+input_filename)
print('output file: '+output_filename)
print('separate_order_factory_number: ' +
      str(args.separate_order_factory_number))
print('-'*50)

# parsowanie pliku XML
tree = ET.parse(input_filename)
root = tree.getroot()

orders = {}

# adres dostawy
deliveryAddress = getNodeValue(
    root, ns, './cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name')
deliveryCity = getNodeValue(
    root, ns, './cac:Delivery/cac:DeliveryParty/cac:PostalAddress/cbc:StreetName')
factoryNumber = getFactoryNumber(deliveryAddress)

# iteracja po OrderLine
for order_line_node in root.findall('cac:OrderLine', ns):
    # iteracja po LineItem
    document_reference = getNodeValue(
        order_line_node, ns, './cac:DocumentReference/cbc:ID')
    for line_item_node in order_line_node.findall('cac:LineItem', ns):
        # pobranie informacji o pozycji

        # pobranie dodatkowych informacji z <AdditionalItemProperty> do dictionary position['additional_properties']
        additional_properties = {}
        for additional_item_property_node in line_item_node.findall("./cac:Item/cac:AdditionalItemProperty", ns):
            name = getNodeValue(additional_item_property_node, ns, 'cbc:Name')
            value = getNodeValue(
                additional_item_property_node, ns, 'cbc:Value')
            id = getNodeValue(additional_item_property_node, ns, 'cbc:Name')

            node = additional_item_property_node.find(
                "./cac:ItemPropertyGroup/cbc:Name", ns)
            if node is not None:
                additional_properties[node.text] = {
                    'name': name, 'value': value, 'id': id}

        additional_properties2 = {}
        for additional_item_property_node in line_item_node.findall("./cac:Item/cac:AdditionalItemProperty", ns):
            name = getNodeValue(additional_item_property_node, ns, 'cbc:Name')
            value = getNodeValue(
                additional_item_property_node, ns, 'cbc:Value')

            additional_properties2[name] = {
                'name': name, 'value': value
            }
        # podział pozycje na różne zlecenia w zależności od daty dostawy i innych informacji
        order_note = ''
        delivery_date = getNodeValue(
            line_item_node, ns, './cac:Delivery/cbc:LatestDeliveryDate')
        separate_order_string = delivery_date

        # podział pozycje ze względu na numer production_order2
        production_order2 = ''
        vendor_info = getNodeValue(
            line_item_node, ns, './cac:Item/cac:SellersItemIdentification/cbc:ID')
        glass_long_text = getNodeValue(
            line_item_node, ns, "./cac:Item/cac:AdditionalItemProperty/cbc:Name[.='Glass Long Text']/../cbc:Value")

        matchObj = re.match(r'[^\-]*', vendor_info)
        if matchObj is not None:
            production_order2 = matchObj.group(0)
            separate_order_string = separate_order_string + production_order2

        elevation_shape = ''
        platform = ''
        internal_order = ''
        delivery_info = ''
        finished_product_shape = ''
        platform = getAdditionalPropertiesValue(
            {'additional_properties': additional_properties}, 'C_PLATFORM', 'value')
        elevation_shape = getAdditionalPropertiesValue(
            {'additional_properties': additional_properties}, 'C_ELEVATION_SHAPE', 'value')
        finished_product_shape = getAdditionalPropertiesValue(
            {'additional_properties': additional_properties2}, 'Finished Product Shape', 'value')
        print(finished_product_shape)
        vendor = getAdditionalPropertiesValue(
            {'additional_properties': additional_properties}, 'C_VENDOR', 'value')
        dva_order_string = '_'.join(
            [factoryNumber[0:2], finished_product_shape[0:2], platform[0:2]]).upper()
        # dva_order_string = '_'.join([factoryNumber[0:2],platform[0:2]]).upper()
        if args.separate_order_factory_number and factoryNumber in args.separate_order_factory_number:
            delivery_info = dva_order_string
            separate_order_string = separate_order_string + finished_product_shape
        internal_order = f'({dva_order_string}) {production_order2}'

        if separate_order_string in orders.keys():
            order_positions = orders[separate_order_string]['positions']
        else:
            orders[separate_order_string] = []
            orders[separate_order_string] = {
                'positions': [],
                'delivery_date': delivery_date,
                'note': order_note,
                'internal_order': internal_order,
                'delivery_info': delivery_info,
                'vendor': vendor
            }
            order_positions = orders[separate_order_string]['positions']

        order_positions.append({'additional_properties': additional_properties,
                                'additional_properties2': additional_properties2,
                                'order_position': getNodeValue(line_item_node, ns, './cbc:ID'),
                                'vendor_info': getNodeValue(line_item_node, ns, './cac:Item/cac:SellersItemIdentification/cbc:ID'),
                                'delivery_date': getNodeValue(line_item_node, ns, './cac:Delivery/cbc:LatestDeliveryDate'),
                                'buyers_item_identification': getNodeValue(line_item_node, ns, './cac:Item/cac:BuyersItemIdentification/cbc:ID'),
                                'quantity': dovista_float2int(getNodeValue(line_item_node, ns, './cbc:Quantity')),
                                'production_order2': production_order2,
                                'document_reference': document_reference,
                                })

# przygotowanie pliku wyjsciowego
xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
# xsi = "D:\sip\src\python\cutter-xsd-schemas\cutter_order_import_file.xsd"
xsi = "https://sipsoftware.github.io/cutter-xsd-schemas/cutter_order_import_file.xsd"
xml_import = ET.Element('cutter_import_order_file', attrib={
                        "xmlns:xsi": xmlns_xsi, "xsi:noNamespaceSchemaLocation": xsi, "format_version": COIFVERSION, "script": "dovista2cutter", "script_version": BUILDVERSION})
ET.SubElement(xml_import, 'original_filename').text = os.path.basename(
    input_filename)

# generowanie gałęzi <customer> - na razie nie wiem po co
# xml_customer = ET.SubElement(xml_import,'customer')
# ET.SubElement(xml_customer,'name').text = 'Olek'


# generowanie pozycji w pliku wyjściowym
for k in orders.keys():
    # generowanie gałezi <order>
    positions = orders[k]['positions']
    xml_order = ET.SubElement(xml_import, 'order', attrib={"comment": k})

    # generowanie zlec_typ dla zlecenia
    ET.SubElement(xml_order, 'additional_info', attrib={
                  "type": "61", "comment": "C_VENDOR"}).text = orders[k]['vendor']

    # pobieranie danych z nagłówka

    # pobranie informacji o kliencie z C_BRAND z 1. pozycji
    customer_brand = getAdditionalPropertiesValue(
        positions[0], 'C_BRAND', 'value')

    xml_address = ET.SubElement(xml_order, 'delivery')
    ET.SubElement(xml_address, 'address', {
                  "info": orders[k]['delivery_info']}).text = deliveryAddress[:-1]
    ET.SubElement(xml_address, 'city').text = deliveryCity
    ET.SubElement(xml_order, 'customer_name', {
                  'comment': 'factory='+factoryNumber}).text = customer_brand
    orderNumberByCustomer = getNodeValue(root, ns, './cbc:ID')
    ET.SubElement(xml_order, 'number_by_customer').text = orderNumberByCustomer
    ET.SubElement(xml_order, 'order_date').text = date2Cutter(date.today())
    ET.SubElement(xml_order, 'notes').text = orders[k]['note']
    ET.SubElement(
        xml_order, 'internal_number').text = orders[k]['internal_order']
    ET.SubElement(xml_order, 'end_user_name2').text = orders[k]['vendor']

    # delivery date z pozycji zlecenia
    delivery_date = dovista_string2date(orders[k]['delivery_date'])
    ET.SubElement(xml_order, 'delivery_date').text = date2Cutter(delivery_date)
    ET.SubElement(xml_order, 'customer_date').text = date2Cutter(delivery_date)

    for position in positions:
        xml_position = ET.SubElement(xml_order, 'position')
        ET.SubElement(xml_position, 'width').text = str(dovista_int2int(
            getAdditionalPropertiesValue(position, 'C_GLASS_WIDTH', 'value')))
        ET.SubElement(xml_position, 'height').text = str(dovista_int2int(
            getAdditionalPropertiesValue(position, 'C_GLASS_HEIGHT', 'value')))
        ET.SubElement(xml_position, 'quantity').text = str(
            position['quantity'])

        glass_unit = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_UNIT', 'name'))
        if glass_unit == 'DGU':
            elements = [
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET2', 'value'),
            ]
        elif glass_unit == 'TGU':
            elements = [
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET3', 'value'),
            ]
        elif glass_unit == 'QGU':
            elements = [
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET3', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER3', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET4', 'value'),
            ]
        else:
            elements = [
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER1', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER2', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET3', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER3', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET4', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SPACER4', 'value'),
                getAdditionalPropertiesValue(
                    position, 'C_GLASS_SHEET5', 'value')
            ]

        ET.SubElement(xml_position, 'structure_name').text = joinStringsWithoutEmpty(
            elements, '/')
        ET.SubElement(xml_position, 'structure_code').text = getAdditionalPropertiesValue(
            position, 'C_GLASS_CODE', 'name')
        ET.SubElement(xml_position, 'structure_code2').text = getAdditionalPropertiesValue(
            position, 'C_GLASS_CODE', 'value')

        xml_product = ET.SubElement(xml_position, 'product')

        glass1 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SHEET1', 'name'))
        spacer1 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER1', 'name'))
        gas1 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_AIR_SPACER1', 'name'))
        glass2 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SHEET2', 'name'))
        spacer2 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER2', 'name'))
        gas2 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_AIR_SPACER2', 'name'))
        glass3 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SHEET3', 'name'))
        spacer3 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER3', 'name'))
        gas3 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_AIR_SPACER3', 'name'))
        glass4 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SHEET4', 'name'))
        spacer4 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER4', 'name'))
        gas4 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_AIR_SPACER4', 'name'))
        glass5 = str(getAdditionalPropertiesValue(
            position, 'C_GLASS_SHEET5', 'name'))

        frame1_thickness = getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER1_THICKNESS', 'name')
        if not frame1_thickness:
            frame1_thickness = "0"
        frame2_thickness = getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER2_THICKNESS', 'name')
        if not frame2_thickness:
            frame2_thickness = "0"
        frame3_thickness = getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER3_THICKNESS', 'name')
        if not frame3_thickness:
            frame3_thickness = "0"
        frame4_thickness = getAdditionalPropertiesValue(
            position, 'C_GLASS_SPACER4_THICKNESS', 'name')
        if not frame4_thickness:
            frame4_thickness = "0"

        if glass1 != '' and glass1 != '0':
            ET.SubElement(xml_product, 'glass1',).text = glass1
        if spacer1 != '' and spacer1 != '0':
            ET.SubElement(xml_product, 'spacer1', {
                          "thickness": frame1_thickness}).text = spacer1

        if gas1 != '' and gas1 != '0':
            ET.SubElement(xml_product, 'gas1',).text = gas1

        if glass2 != '' and glass2 != '0':
            ET.SubElement(xml_product, 'glass2',).text = glass2

        if spacer2 != '' and spacer2 != '0':
            ET.SubElement(xml_product, 'spacer2', {
                          "thickness": frame2_thickness}).text = spacer2

        if gas2 != '' and gas2 != '0':
            ET.SubElement(xml_product, 'gas2').text = gas2

        if glass3 != '' and glass3 != '0':
            ET.SubElement(xml_product, 'glass3').text = glass3

        if spacer3 != '' and spacer3 != '0':
            ET.SubElement(xml_product, 'spacer3', {
                          "thickness": frame3_thickness}).text = spacer3

        if gas3 != '' and gas3 != '0':
            ET.SubElement(xml_product, 'gas3').text = gas3

        if glass4 != '' and glass4 != '0':
            ET.SubElement(xml_product, 'glass4').text = glass4

        if spacer4 != '' and spacer4 != '0':
            ET.SubElement(xml_product, 'spacer4', {
                          "thickness": frame4_thickness}).text = spacer4

        if gas4 != '' and gas4 != '0':
            ET.SubElement(xml_product, 'gas4').text = gas4

        if glass5 != '' and glass5 != '0':
            ET.SubElement(xml_product, 'glass5').text = glass5

        # ET.SubElement(xml_position,'description').text = str(position['vendor_info']).replace('GLASS_','').replace('-','').replace(' ','').replace('(','').replace(')','')
        ET.SubElement(xml_position, 'description').text = str(
            position['vendor_info'])
        ET.SubElement(
            xml_position, 'delivery_date').text = position['delivery_date']
        # ET.SubElement(xml_position,'key').text = str(position['production_order2'])+str(position['delivery_date'])+str(position['elevation_shape'])
        ET.SubElement(xml_position, 'key').text = str(position['vendor_info'])
        ET.SubElement(xml_position, 'additional_description').text = orderNumberByCustomer + \
            str(position['order_position'])

        # --- BEGIN --- obsługa kształtów DOVISTA
        shape_drawing = getAdditionalPropertiesValue(
            position, 'C_DRAWING', 'value')
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
            xml_shape = ET.SubElement(xml_position, 'shape', {
                                      'desc': shape_drawing})
            shape_number = dovista_drawing2shape(shape_drawing)
            if shape_number > 0:
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
                    value = dovista_float2int(getAdditionalPropertiesValue(
                        position, shape_params_def[k], 'value'))
                    if k == 'l' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(
                            position, 'C_GLASS_WIDTH', 'value'))
                    if k == 'h' and value == 0:
                        value = dovista_int2int(getAdditionalPropertiesValue(
                            position, 'C_GLASS_HEIGHT', 'value'))
                    if value > 0:
                        shape_params[k] = value
                # Odwrócenie kształtu. Kształty DVA są z widokiem od zewnątrz. W EFF trzeba odwrócić
                shape_params = shape.mirror(shape_params)
                # Zapisanie nie zerowych parametrów kształtu do XMLa.
                for k in shape_params.keys():
                    if shape_params[k] > 0:
                        ET.SubElement(xml_shape, k).text = str(shape_params[k])
            else:
                ET.SubElement(xml_shape, 'catalogue').text = '3'
        # --- END --- obsługa kształtów DOVISTA

        # --- BEGIN --- obsługa szprosów dowolnych
        if(spacer1 != '' and spacer1 != '0'):
            chamber_count = 1
        if(spacer2 != '' and spacer2 != '0'):
            chamber_count = 2
        if(spacer3 != '' and spacer3 != '0'):
            chamber_count = 3
        if(spacer4 != '' and spacer4 != '0'):
            chamber_count = 4

        if len(getAdditionalPropertiesValue(position, 'C_GLASS_SEQ_W1', 'value')) > 0:
            xml_gb = ET.SubElement(xml_position, 'custom_glazing_bar')
            for frameno in range(1, chamber_count+1):
                xml_gb_frame = ET.SubElement(
                    xml_gb, 'frame', {'no': str(frameno)})

                # ET.SubElement(xml_gb_frame,'elevation').text = gb_elevation

                xml_gb_frame_dim = ET.SubElement(xml_gb_frame, 'dimmensions')
                d = {
                    'w1': 'C_GLASS_GW9',
                    'w2': 'C_GLASS_GW8',
                    'w3': 'C_GLASS_GW7',
                    'w4': 'C_GLASS_GW6',
                    'w5': 'C_GLASS_GW5',
                    'w6': 'C_GLASS_GW4',
                    'w7': 'C_GLASS_GW3',
                    'w8': 'C_GLASS_GW2',
                    'w9': 'C_GLASS_GW1',
                    'h9': 'C_GLASS_GH9',
                    'h8': 'C_GLASS_GH8',
                    'h7': 'C_GLASS_GH7',
                    'h6': 'C_GLASS_GH6',
                    'h5': 'C_GLASS_GH5',
                    'h4': 'C_GLASS_GH4',
                    'h3': 'C_GLASS_GH3',
                    'h2': 'C_GLASS_GH2',
                    'h1': 'C_GLASS_GH1'
                }

                bar_no_w = 0
                # analiza listew pionowych
                width = dovista_int2int(getAdditionalPropertiesValue(
                    position, 'C_GLASS_WIDTH', 'value'))
                for k in d.keys():
                    value = dovista_float2int(
                        getAdditionalPropertiesValue(position, d[k], 'value'))
                    if value > 0 and k[0] == 'w':
                        value = int(width)-int(value)
                        bar_no_w = bar_no_w + 1
                        ET.SubElement(xml_gb_frame_dim,
                                      k[0]+str(bar_no_w)).text = str(value)
                # analiza listew poziomych (od góry)
                bar_no_h = 0
                height = dovista_int2int(getAdditionalPropertiesValue(
                    position, 'C_GLASS_HEIGHT', 'value'))
                for k in d.keys():
                    value = dovista_float2int(
                        getAdditionalPropertiesValue(position, d[k], 'value'))
                    if value > 0 and k[0] == 'h':
                        value = int(height)-int(value)
                        bar_no_h = bar_no_h + 1
                        ET.SubElement(xml_gb_frame_dim,
                                      k[0]+str(bar_no_h)).text = str(value)

                xml_gb_frame_seq = ET.SubElement(xml_gb_frame, 'sequence')
                d = {
                    'w1': 'C_GLASS_SEQ_W1',
                    'w2': 'C_GLASS_SEQ_W2',
                    'w3': 'C_GLASS_SEQ_W3',
                    'w4': 'C_GLASS_SEQ_W4',
                    'w5': 'C_GLASS_SEQ_W5',
                    'w6': 'C_GLASS_SEQ_W6',
                    'w7': 'C_GLASS_SEQ_W7',
                    'w8': 'C_GLASS_SEQ_W8',
                    'w9': 'C_GLASS_SEQ_W9',
                    'h1': 'C_GLASS_SEQ_H1',
                    'h2': 'C_GLASS_SEQ_H2',
                    'h3': 'C_GLASS_SEQ_H3',
                    'h4': 'C_GLASS_SEQ_H4',
                    'h5': 'C_GLASS_SEQ_H5',
                    'h6': 'C_GLASS_SEQ_H6',
                    'h7': 'C_GLASS_SEQ_H7',
                    'h8': 'C_GLASS_SEQ_H8',
                    'h9': 'C_GLASS_SEQ_H9'
                }
                for k in d.keys():
                    value = getAdditionalPropertiesValue(
                        position, d[k], 'value')
                    if k[0] == 'w':
                        # wycięcie nie potrzebnych zer
                        value = value[0:bar_no_h+1]
                        # odwrócenie stringu - sekwencja belek jest podana od góry
                        value = value[::-1]
                    if k[0] == 'h':
                        value = value[0:bar_no_w+1]
                    if value != '' and value != '0':
                        ET.SubElement(xml_gb_frame_seq, k).text = value

                xml_gb_frame_mat = ET.SubElement(xml_gb_frame, 'material')
                d = {
                    'w1': 'C_GLASS_VAR_GW1',
                    'w2': 'C_GLASS_VAR_GW2',
                    'w3': 'C_GLASS_VAR_GW3',
                    'w4': 'C_GLASS_VAR_GW4',
                    'w5': 'C_GLASS_VAR_GW5',
                    'w6': 'C_GLASS_VAR_GW6',
                    'w7': 'C_GLASS_VAR_GW7',
                    'w8': 'C_GLASS_VAR_GW8',
                    'w9': 'C_GLASS_VAR_GW9',
                    'h1': 'C_GLASS_VAR_GH1',
                    'h2': 'C_GLASS_VAR_GH2',
                    'h3': 'C_GLASS_VAR_GH3',
                    'h4': 'C_GLASS_VAR_GH4',
                    'h5': 'C_GLASS_VAR_GH5',
                    'h6': 'C_GLASS_VAR_GH6',
                    'h7': 'C_GLASS_VAR_GH7',
                    'h8': 'C_GLASS_VAR_GH8',
                    'h9': 'C_GLASS_VAR_GH9'
                }
                for k in d.keys():
                    value = getAdditionalPropertiesValue(
                        position, d[k], 'name')
                    if value != '' and value != '00':
                        ET.SubElement(xml_gb_frame_mat, k).text = value

        # --- END --- obsługa szprosów dowolnych

        # generowanie zlec_typ dla pozycji
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "1", "comment": "Purchase order position "}).text = str(position['order_position'])
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "5", "comment": "OrderLine.Document Reference "}).text = str(position['document_reference']).split('/')[0]
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "6", "comment": "OrderLine.Document Reference "}).text = str(position['document_reference']).split('/')[1]
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "27", "comment": "SellersItemIdentification"}).text = str(position['vendor_info'])
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "57", "comment": "C_GLASS_CODE.value"}).text = getAdditionalPropertiesValue(position, 'C_GLASS_CODE', 'value')
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "176", "comment": "Customer"}).text = customer_brand
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "207", "comment": "Glass Long Text"}).text = glass_long_text
        ET.SubElement(xml_position, 'additional_info', attrib={
                      "type": "211", "comment": "Delivery address"}).text = deliveryAddress
        ET.SubElement(xml_position, 'additional_info', attrib={"type": "226", "comment": "C_DRAWING"}).text = str(
            getAdditionalPropertiesValue(position, 'C_DRAWING', 'value'))
        ET.SubElement(xml_position, 'additional_info', attrib={"type": "227", "comment": "C_FIELD_ELEVATION"}).text = str(
            getAdditionalPropertiesValue(position, 'C_GLZBAR_G_ELEV', 'name'))
        ET.SubElement(xml_position, 'additional_info', attrib={"type": "228", "comment": "C_GLZBAR_G_VAR"}).text = str(
            getAdditionalPropertiesValue(position, 'C_GLZBAR_G_VAR', 'value'))
        ET.SubElement(xml_position, 'additional_info', attrib={"type": "261", "comment": "C_PLATFORM.value"}).text = str(
            getAdditionalPropertiesValue(position, 'C_PLATFORM', 'value'))
        ET.SubElement(xml_position, 'additional_info', attrib={"type": "906", "comment": "Finished Product Shape.value"}).text = str(
            getAdditionalPropertiesValue({'additional_properties': position['additional_properties2']}, 'Finished Product Shape', 'value')).upper()

# koniec iteracji po pozycjach

# zapis pliku wyjściowego w formacie xml
xmlstr = minidom.parseString(ET.tostring(
    xml_import, encoding="utf-8")).toprettyxml(indent="   ")
# print(xmlstr)
with open(output_filename, "w", encoding="utf-8") as xmlfile:
    xmlfile.write(xmlstr)
