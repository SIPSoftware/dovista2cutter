<?xml version="1.0" encoding="UTF-8"?> 
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"  xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 	xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
	<cbc:UBLVersionID>2.0</cbc:UBLVersionID>
	<cbc:CustomizationID>OIOUBL-2.01</cbc:CustomizationID>
	<cbc:ProfileID schemeAgencyID="320" schemeID="urn:oioubl:id:profileid-1.2">Procurement-BilSim-1.0</cbc:ProfileID>
<!$MGREPEAT><!$MGIF_DataExists_F1>
	<cbc:ID><!$MG_Invoice_ID></cbc:ID> 
	<cbc:CopyIndicator>false</cbc:CopyIndicator>
	<cbc:UUID><!$MG_GUID></cbc:UUID> 
	<cbc:IssueDate><!$MG_Inv_Date></cbc:IssueDate> 
	<cbc:InvoiceTypeCode listAgencyID="320" listID="urn:oioubl:codelist:invoicetypecode-1.1"><!$MG_Inv_Code></cbc:InvoiceTypeCode> 
	<cbc:Note> <!$MG_Inv_Notes></cbc:Note> 
	<cbc:DocumentCurrencyCode><!$MG_Inv_Curr></cbc:DocumentCurrencyCode> 

	<cac:OrderReference>
		<cbc:ID><!$MG_Inv_Cust_Order_No></cbc:ID>
		<cbc:SalesOrderID><!$MG_Cutter_Order_No></cbc:SalesOrderID> 
		<cbc:IssueDate><!$MG_Order_Date></cbc:IssueDate> 
	</cac:OrderReference>

	<cac:AccountingSupplierParty>
		<cac:Party>
			<cbc:EndpointID schemeAgencyID="9" schemeID="GLN">5909000833616</cbc:EndpointID>
			<cac:PartyIdentification>
				<cbc:ID schemeID="GLN">5909000833616</cbc:ID> 
			</cac:PartyIdentification>
			<cac:PartyName>
				<cbc:Name><!$MG_Inv_Nazwa_Firmy2></cbc:Name> 
			</cac:PartyName>
			<cac:PostalAddress>
				<cbc:AddressFormatCode listID="urn:oioubl:codelist:addressformatcode-1.1" listAgencyID="320">StructuredDK</cbc:AddressFormatCode>
				<cbc:StreetName>Hauke-Bosaka</cbc:StreetName>
				<cbc:BuildingNumber>2</cbc:BuildingNumber>
				<cbc:CityName>Kielce</cbc:CityName>
				<cbc:PostalZone>25-214</cbc:PostalZone>
				<cac:Country>
					<cbc:IdentificationCode>PL</cbc:IdentificationCode>
				</cac:Country>
			</cac:PostalAddress>
			<cac:PartyLegalEntity>
				<cbc:CompanyID schemeID="ZZZ">PL6341023465</cbc:CompanyID> 
			</cac:PartyLegalEntity>
		</cac:Party>
	</cac:AccountingSupplierParty>

	<cac:AccountingCustomerParty>
		<cac:Party>
			<cbc:EndpointID schemeAgencyID="9" schemeID="GLN"><!$MG_zt_z301></cbc:EndpointID>
			<cac:PartyIdentification>
				<cbc:ID schemeID="GLN"><!$MG_zt_z301></cbc:ID> 
			</cac:PartyIdentification> 
			<cac:PartyName>
				<cbc:Name>DOVISTA POLSKA SP. Z O.O.</cbc:Name>
			</cac:PartyName>
			<cac:PostalAddress> 
				<cbc:AddressFormatCode listAgencyID="320" listID="urn:oioubl:codelist:addressformatcode-1.1">StructuredDK</cbc:AddressFormatCode>
				<cbc:StreetName><!$MG_Inv_Adr_Dost_Street></cbc:StreetName> 
				<cbc:BuildingNumber><!$MG_Inv_Adr_Dost_Nr></cbc:BuildingNumber> 
				<cbc:CityName><!$MG_Inv_Adr_Dost_City></cbc:CityName> 
				<cbc:PostalZone><!$MG_Inv_Adr_Dost_Post_Code></cbc:PostalZone>
				<cac:Country>
					<cbc:IdentificationCode><!$MG_Inv_Adr_Dost_Country_Abbr></cbc:IdentificationCode>
				</cac:Country>
			</cac:PostalAddress>
			<cac:PartyTaxScheme>
				<cbc:CompanyID schemeID="ZZZ"><!$MG_Inv_Adr_Dost_NIP></cbc:CompanyID>
				<cac:TaxScheme>
					<cbc:ID schemeAgencyID="320" schemeID="urn:oioubl:id:taxschemeid-1.4" >63</cbc:ID>
					<cbc:Name>Moms</cbc:Name>
					<cac:JurisdictionRegionAddress>
						<cac:Country>
							<cbc:IdentificationCode><!$MG_Inv_CountryCode></cbc:IdentificationCode> 
						</cac:Country>
					</cac:JurisdictionRegionAddress>
				</cac:TaxScheme>
			</cac:PartyTaxScheme>
			<cac:PartyLegalEntity>
				<cbc:CompanyID schemeID="ZZZ"><!$MG_Inv_Adr_Dost_NIP></cbc:CompanyID>
			</cac:PartyLegalEntity>
			<cac:Contact>
				<cbc:ID>n/a</cbc:ID>
			</cac:Contact>
		</cac:Party>
	</cac:AccountingCustomerParty>

	<cac:PaymentMeans>
		<cbc:ID>1</cbc:ID>
		<cbc:PaymentMeansCode><!$MG_Inv_Payment_Code></cbc:PaymentMeansCode> 
		<cbc:PaymentDueDate><!$MG_Inv_Payment_Due_Date></cbc:PaymentDueDate> 
		<cbc:PaymentChannelCode listAgencyID="320" listID="urn:oioubl:codelist:paymentchannelcode-1.1">IBAN</cbc:PaymentChannelCode>
		<cac:PayeeFinancialAccount>
			<cbc:ID><!$MG_Inv_Payment_Account2></cbc:ID>
			<cbc:PaymentNote><!$MG_Inv_Payment_Note></cbc:PaymentNote>
			<cac:FinancialInstitutionBranch>
				<cac:FinancialInstitution >
					<cbc:ID><!$MG_Inv_Payment_SWIFT2></cbc:ID>
					<cbc:Name><!$MG_Inv_Payment_Bank2></cbc:Name>
				</cac:FinancialInstitution>
			</cac:FinancialInstitutionBranch>
		</cac:PayeeFinancialAccount>
	</cac:PaymentMeans>

	<cac:TaxTotal>
		<cbc:TaxAmount currencyID="PLN"><!$MG_Inv_Payment_VAT_PLN></cbc:TaxAmount> 
		<cac:TaxSubtotal>
			<cbc:TaxableAmount currencyID="PLN"><!$MG_Inv_Payment_Net_Value_PLN></cbc:TaxableAmount> 
			<cbc:TaxAmount currencyID="PLN"><!$MG_Inv_Payment_VAT_Value_PLN></cbc:TaxAmount> 
			<cac:TaxCategory>
				<cbc:ID schemeAgencyID="320" schemeID="urn:oioubl:id:taxcategoryid-1.1">StandardRated</cbc:ID>
				<cbc:Percent><!$MG_Inv_Payment_VAT_RATE></cbc:Percent> 
				<cac:TaxScheme>
					<cbc:ID schemeAgencyID="320" schemeID="urn:oioubl:id:taxschemeid-1.1">63</cbc:ID>
					<cbc:Name>Moms</cbc:Name>
				</cac:TaxScheme>
			</cac:TaxCategory>
		</cac:TaxSubtotal>
	</cac:TaxTotal>

	<cac:LegalMonetaryTotal>
		<cbc:LineExtensionAmount currencyID="<!$MG_Inv_Payment_CurrencyID>"><!$MG_Inv_Payment_Net_Value></cbc:LineExtensionAmount> 
		<cbc:PayableAmount currencyID="PLN"><!$MG_Inv_Payment_Tot_Value></cbc:PayableAmount> 
	</cac:LegalMonetaryTotal>
<!$MGREPEAT><!$MGIF_DataExists_F2>
	<cac:InvoiceLine>
		<cbc:ID><!$MG_Inv_Line_Nr></cbc:ID> 
		<cbc:Note><!$MG_zt_p306></cbc:Note> 
		<cbc:InvoicedQuantity unitCode="EA"><!$MG_Inv_Line_Qty_Pcs></cbc:InvoicedQuantity> 
		<cbc:LineExtensionAmount currencyID="<!$MG_Inv_Currency_code2>"><!$MG_Inv_Line_Value></cbc:LineExtensionAmount> 
		<cac:OrderLineReference> 
			<cbc:LineID><!$MG_zt_p304></cbc:LineID>
			<cac:OrderReference>
				<cbc:ID><!$MG_zt_p303></cbc:ID>
			</cac:OrderReference>
		</cac:OrderLineReference>
		<cac:TaxTotal>
			<cbc:TaxAmount currencyID="<!$MG_Inv_Currency_code3>"><!$MG_Inv_Line_VAT_Value></cbc:TaxAmount> 
			<cac:TaxSubtotal>
				<cbc:TaxableAmount currencyID="<!$MG_Inv_Currency_code4>"><!$MG_Inv_Line_Unit_Price></cbc:TaxableAmount>
				<cbc:TaxAmount currencyID="<!$MG_Inv_Currency_code5>"><!$MG_Inv_Line_VAT_Unit_Value></cbc:TaxAmount> 
				<cac:TaxCategory>
					<cbc:ID schemeAgencyID="320" schemeID="urn:oioubl:id:taxcategoryid-1.1">StandardRated</cbc:ID>
					<cbc:Percent><!$MG_Inv_Line_VAT_Rate></cbc:Percent> 
					<cac:TaxScheme>
						<cbc:ID schemeAgencyID="320" schemeID="urn:oioubl:id:taxschemeid-1.1">63</cbc:ID>
						<cbc:Name>Moms</cbc:Name>
					</cac:TaxScheme>
				</cac:TaxCategory>
			</cac:TaxSubtotal>
		</cac:TaxTotal>
		<cac:Item>
			<cbc:Description><!$MG_Inv_Line_Weight> kg</cbc:Description> 
			<cbc:Name><!$MG_zt_p309></cbc:Name> 
			<cac:SellersItemIdentification>
				<cbc:ID><!$MG_zt_p304></cbc:ID> 
			</cac:SellersItemIdentification>
		</cac:Item>
		<cac:Price>
			<cbc:PriceAmount currencyID="<!$MG_Inv_Currency_code6>"><!$MG_Inv_Line_Value></cbc:PriceAmount> 
		</cac:Price>
	</cac:InvoiceLine>
<!$MGENDIF> <!$MGENDREPEAT>
<!$MGENDIF> <!$MGENDREPEAT>   
</Invoice>