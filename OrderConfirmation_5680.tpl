<?xml version="1.0" encoding="UTF-8"?>
<OrderResponse xmlns="urn:oasis:names:specification:ubl:schema:xsd:OrderResponse-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2" xmlns:sdt="urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:OrderResponse-2 UBL-OrderResponse-2.0.xsd">
	<cbc:UBLVersionID>2.0</cbc:UBLVersionID>
	<cbc:CustomizationID>OIOUBL-2.01</cbc:CustomizationID>
	<cbc:ProfileID schemeAgencyID="320" schemeID="urn:oioubl:id:profileid-1.1">Procurement-OrdSel-BilSim-1.0</cbc:ProfileID>
<!$MGREPEAT> 
<!$MGIF_DataExists_001>
	<cbc:ID><!$MG_customer_order></cbc:ID>
	<cbc:CopyIndicator>false</cbc:CopyIndicator>
	<cbc:UUID>d8fd3155-ec4f-49e6-bd41-ec0c681ac96f</cbc:UUID>
	<cbc:IssueDate><!$MG_order_date></cbc:IssueDate>
	<cbc:DocumentCurrencyCode><!$MG_order_currency></cbc:DocumentCurrencyCode>
	<cbc:AccountingCost>5250124502</cbc:AccountingCost>
	<cac:OrderReference>
		<cbc:ID><!$MG_customer_order></cbc:ID>
		<cbc:IssueDate><!$MG_order_date></cbc:IssueDate>
	</cac:OrderReference>
	<cac:SellerSupplierParty>
		<cac:Party>
			<cbc:EndpointID schemeID="EU:VAT">PL6341023465</cbc:EndpointID>
			<cac:PartyIdentification>
				<cbc:ID schemeID="ZZZ">PL6341023465</cbc:ID>
			</cac:PartyIdentification>
			<cac:PartyLegalEntity>
				<cbc:CompanyID schemeID="ZZZ">PL6341023465</cbc:CompanyID>
			</cac:PartyLegalEntity>
		</cac:Party>
	</cac:SellerSupplierParty>
	<cac:BuyerCustomerParty>	
		<cac:Party>
			<cbc:EndpointID schemeAgencyID="9" schemeID="GLN"><!$MG_zt_z301></cbc:EndpointID>
			<cac:PartyIdentification>
				<cbc:ID schemeAgencyID="9" schemeID="GLN"><!$MG_zt_z301></cbc:ID>
			</cac:PartyIdentification>
			<cac:PartyLegalEntity>
				<cbc:CompanyID schemeID="ZZZ"><!$MG_zt_z302></cbc:CompanyID>
			</cac:PartyLegalEntity>
			<cac:Contact>
				<cbc:ID>n/a</cbc:ID>
			</cac:Contact>
		</cac:Party>
	</cac:BuyerCustomerParty>
<!$MGREPEAT> 
<!$MGIF_DataExists_011>
	<cac:OrderLine>
		<cac:LineItem>
			<cbc:ID><!$MG_zt_p320></cbc:ID>
			<cbc:Quantity unitCode="EA"><!$MG_quantity>.00</cbc:Quantity>
			<cac:Delivery>
				<cbc:LatestDeliveryDate><!$MG_order_delivery_date></cbc:LatestDeliveryDate>
			</cac:Delivery>
			<cac:Item>
				<cbc:Description><!$MG_zt_p321></cbc:Description>
				<cbc:Name><!$MG_zt_p322></cbc:Name>
				<cac:BuyersItemIdentification>
					<cbc:ID schemeAgencyID="9" schemeID="GTIN"><!$MG_zt_p322></cbc:ID>
				</cac:BuyersItemIdentification>
			</cac:Item>
		</cac:LineItem>
	</cac:OrderLine>
<!$MGENDIF> 
<!$MGENDREPEAT>

<!$MGENDIF> 
<!$MGENDREPEAT>
</OrderResponse>
