from typing import List, Optional, Dict, Iterable, Any, overload
import io
import collections.abc
from datetime import datetime
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
from uuid import UUID
import groupdocs.signature
import groupdocs.signature.domain
import groupdocs.signature.domain.extensions
import groupdocs.signature.logging
import groupdocs.signature.options
import groupdocs.signature.options.appearances

class Address:
    '''Represents address for contact.'''
    
    @property
    def street(self) -> str:
        '''Gets address street.'''
        raise NotImplementedError()
    
    @street.setter
    def street(self, value : str) -> None:
        '''Sets address street.'''
        raise NotImplementedError()
    
    @property
    def city(self) -> str:
        '''Gets address city.'''
        raise NotImplementedError()
    
    @city.setter
    def city(self, value : str) -> None:
        '''Sets address city.'''
        raise NotImplementedError()
    
    @property
    def state(self) -> str:
        '''Gets address state.'''
        raise NotImplementedError()
    
    @state.setter
    def state(self, value : str) -> None:
        '''Sets address state.'''
        raise NotImplementedError()
    
    @property
    def zip(self) -> str:
        '''Gets address ZIP.'''
        raise NotImplementedError()
    
    @zip.setter
    def zip(self, value : str) -> None:
        '''Sets address ZIP.'''
        raise NotImplementedError()
    
    @property
    def country(self) -> str:
        '''Gets address country.'''
        raise NotImplementedError()
    
    @country.setter
    def country(self, value : str) -> None:
        '''Sets address country.'''
        raise NotImplementedError()
    

class Brush:
    '''Represents base class for various brushes.'''
    

class CryptoCurrencyTransfer:
    '''Represents Cryptocurrency transfer (receive or send) for QR-Code.'''
    
    @property
    def type(self) -> groupdocs.signature.domain.extensions.CryptoCurrencyType:
        '''Gets one of supported cryptocurrency type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : groupdocs.signature.domain.extensions.CryptoCurrencyType) -> None:
        '''Sets one of supported cryptocurrency type.'''
        raise NotImplementedError()
    
    @property
    def amount(self) -> float:
        '''Gets transfer amount.'''
        raise NotImplementedError()
    
    @amount.setter
    def amount(self, value : float) -> None:
        '''Sets transfer amount.'''
        raise NotImplementedError()
    
    @property
    def address(self) -> str:
        '''Gets cryptocurrency public address.'''
        raise NotImplementedError()
    
    @address.setter
    def address(self, value : str) -> None:
        '''Sets cryptocurrency public address.'''
        raise NotImplementedError()
    
    @property
    def message(self) -> str:
        '''Gets optional transfer message.'''
        raise NotImplementedError()
    
    @message.setter
    def message(self, value : str) -> None:
        '''Sets optional transfer message.'''
        raise NotImplementedError()
    
    @property
    def custom_type(self) -> str:
        '''Gets optional transfer message.'''
        raise NotImplementedError()
    
    @custom_type.setter
    def custom_type(self, value : str) -> None:
        '''Sets optional transfer message.'''
        raise NotImplementedError()
    

class DigitalVBA(SignatureExtension):
    '''Represents digital signature for Spreadsheets VBA projects.
    It provides ability to sign VBA project at specific Spreadsheets document formats like Xlsm or Xltm.
    If several DigitalVBA extensions are added to DigitalSignOptions.Extensions only first is involved in document signing.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def comments(self) -> str:
        '''Gets the signature comments.'''
        raise NotImplementedError()
    
    @comments.setter
    def comments(self, value : str) -> None:
        '''Sets the signature comments.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Gets the password of digital certificate.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Sets the password of digital certificate.'''
        raise NotImplementedError()
    
    @property
    def sign_only_vba_project(self) -> bool:
        '''Gets setting of only VBA project signing.
        If set to true, the SpreadSheet document will not be signed, but the VBA project will be signed.'''
        raise NotImplementedError()
    
    @sign_only_vba_project.setter
    def sign_only_vba_project(self, value : bool) -> None:
        '''Sets setting of only VBA project signing.
        If set to true, the SpreadSheet document will not be signed, but the VBA project will be signed.'''
        raise NotImplementedError()
    
    @property
    def certificate_file_path(self) -> str:
        '''Gets digital certificate file path.
        This property is used only if CertificateStream is not specified.'''
        raise NotImplementedError()
    
    @property
    def certificate_stream(self) -> io.RawIOBase:
        '''Gets digital certificate stream.
        If this property is specified it is always used instead CertificateFilePath.'''
        raise NotImplementedError()
    

class EPC:
    '''Represents European Payments Council Quick Response Code.'''
    
    @property
    def name(self) -> str:
        '''Gets Beneficiary\'s Name. Maximum length is 70 characters.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets Beneficiary\'s Name. Maximum length is 70 characters.'''
        raise NotImplementedError()
    
    @property
    def bic(self) -> str:
        '''Gets Beneficiary\'s BIC with up to 11 characters length.'''
        raise NotImplementedError()
    
    @bic.setter
    def bic(self, value : str) -> None:
        '''Sets Beneficiary\'s BIC with up to 11 characters length.'''
        raise NotImplementedError()
    
    @property
    def iban(self) -> str:
        '''Gets Beneficiary\'s Account (IBAN). The IBAN consists of up to 34 alphanumeric characters.'''
        raise NotImplementedError()
    
    @iban.setter
    def iban(self, value : str) -> None:
        '''Sets Beneficiary\'s Account (IBAN). The IBAN consists of up to 34 alphanumeric characters.'''
        raise NotImplementedError()
    
    @property
    def amount(self) -> float:
        '''Gets amount.'''
        raise NotImplementedError()
    
    @amount.setter
    def amount(self, value : float) -> None:
        '''Sets amount.'''
        raise NotImplementedError()
    
    @property
    def code(self) -> str:
        '''Gets Business Code up to 4 characters.'''
        raise NotImplementedError()
    
    @code.setter
    def code(self, value : str) -> None:
        '''Sets Business Code up to 4 characters.'''
        raise NotImplementedError()
    
    @property
    def reference(self) -> str:
        '''Gets Payment Reference (maximum 35 characters). This field and the Remittance Information field are mutually exclusive.'''
        raise NotImplementedError()
    
    @reference.setter
    def reference(self, value : str) -> None:
        '''Sets Payment Reference (maximum 35 characters). This field and the Remittance Information field are mutually exclusive.'''
        raise NotImplementedError()
    
    @property
    def remittance(self) -> str:
        '''Gets Remittance Information (maximum 140 characters). This field and the Payment Reference field are mutually exclusive.'''
        raise NotImplementedError()
    
    @remittance.setter
    def remittance(self, value : str) -> None:
        '''Sets Remittance Information (maximum 140 characters). This field and the Payment Reference field are mutually exclusive.'''
        raise NotImplementedError()
    
    @property
    def information(self) -> str:
        '''Gets hint information. Maximum 70 characters.'''
        raise NotImplementedError()
    
    @information.setter
    def information(self, value : str) -> None:
        '''Sets hint information. Maximum 70 characters.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''EPC / SEPA QR-Code version implementation. By default this value set to 002.'''
        raise NotImplementedError()
    
    @property
    def charset(self) -> str:
        '''EPC / SEPA QR-Code char set implementation. By default this value set to 1'''
        raise NotImplementedError()
    
    @property
    def identification(self) -> str:
        '''EPC / SEPA QR-Code identification. By default this value set to SCT'''
        raise NotImplementedError()
    

class Email:
    '''Represents Email format for QR-Code.'''
    
    @property
    def address(self) -> str:
        '''Gets Email address.'''
        raise NotImplementedError()
    
    @address.setter
    def address(self, value : str) -> None:
        '''Sets Email address.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets email Subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets email Subject.'''
        raise NotImplementedError()
    
    @property
    def body(self) -> str:
        '''Gets Body of email message.'''
        raise NotImplementedError()
    
    @body.setter
    def body(self, value : str) -> None:
        '''Sets Body of email message.'''
        raise NotImplementedError()
    

class Event:
    '''Represents standard QR-Code Event details.'''
    
    @property
    def title(self) -> str:
        '''Gets event title.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets event title.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets description.'''
        raise NotImplementedError()
    
    @description.setter
    def description(self, value : str) -> None:
        '''Sets description.'''
        raise NotImplementedError()
    
    @property
    def location(self) -> str:
        '''Gets event location.'''
        raise NotImplementedError()
    
    @location.setter
    def location(self, value : str) -> None:
        '''Sets event location.'''
        raise NotImplementedError()
    
    @property
    def start_date(self) -> datetime:
        '''Gets event start date and time.'''
        raise NotImplementedError()
    
    @start_date.setter
    def start_date(self, value : datetime) -> None:
        '''Sets event start date and time.'''
        raise NotImplementedError()
    
    @property
    def end_date(self) -> Optional[datetime]:
        '''Gets event end date and time.'''
        raise NotImplementedError()
    
    @end_date.setter
    def end_date(self, value : Optional[datetime]) -> None:
        '''Sets event end date and time.'''
        raise NotImplementedError()
    

class FormatAttribute:
    '''Instructs objects serialization to serialize the member with the specified name and format'''
    
    @property
    def property_name(self) -> str:
        '''Gets the name of the property.'''
        raise NotImplementedError()
    
    @property_name.setter
    def property_name(self, value : str) -> None:
        '''Sets the name of the property.'''
        raise NotImplementedError()
    
    @property
    def property_format(self) -> str:
        '''Gets the serialization format of the property.'''
        raise NotImplementedError()
    
    @property_format.setter
    def property_format(self, value : str) -> None:
        '''Sets the serialization format of the property.'''
        raise NotImplementedError()
    

class HIBCLICCombinedData:
    '''Class for storing HIBC (Healthcare Industry Bar Code Council) LIC (Licensed Identification Code) combined data with primary and secondary data entities.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def primary_data(self) -> groupdocs.signature.domain.extensions.HIBCLICPrimaryData:
        '''HIBC LIC primary data structure'''
        raise NotImplementedError()
    
    @primary_data.setter
    def primary_data(self, value : groupdocs.signature.domain.extensions.HIBCLICPrimaryData) -> None:
        '''HIBC LIC primary data structure'''
        raise NotImplementedError()
    
    @property
    def secondary_additional_data(self) -> groupdocs.signature.domain.extensions.HIBCLICSecondaryAdditionalData:
        '''HIBC LIC secondary data structure'''
        raise NotImplementedError()
    
    @secondary_additional_data.setter
    def secondary_additional_data(self, value : groupdocs.signature.domain.extensions.HIBCLICSecondaryAdditionalData) -> None:
        '''HIBC LIC secondary data structure'''
        raise NotImplementedError()
    

class HIBCLICPrimaryData:
    '''Class for storing HIBC (Healthcare Industry Bar Code Council) LIC (Licensed Identification Code) primary data.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def labeler_identification_code(self) -> str:
        '''Identifies date of labeler identification code. Labeler identification code must
        be 4 symbols alphanumeric string, with first character always being alphabetic.'''
        raise NotImplementedError()
    
    @labeler_identification_code.setter
    def labeler_identification_code(self, value : str) -> None:
        '''Identifies date of labeler identification code. Labeler identification code must
        be 4 symbols alphanumeric string, with first character always being alphabetic.'''
        raise NotImplementedError()
    
    @property
    def product_or_catalog_number(self) -> str:
        '''Identifies product or catalog number. Product or catalog number must be alphanumeric
        string up to 18 symbols length.'''
        raise NotImplementedError()
    
    @product_or_catalog_number.setter
    def product_or_catalog_number(self, value : str) -> None:
        '''Identifies product or catalog number. Product or catalog number must be alphanumeric
        string up to 18 symbols length.'''
        raise NotImplementedError()
    
    @property
    def unit_of_measure_id(self) -> int:
        '''Identifies unit of measure ID. Unit of measure ID must be integer value from 0 to 9.'''
        raise NotImplementedError()
    
    @unit_of_measure_id.setter
    def unit_of_measure_id(self, value : int) -> None:
        '''Identifies unit of measure ID. Unit of measure ID must be integer value from 0 to 9.'''
        raise NotImplementedError()
    

class HIBCLICSecondaryAdditionalData:
    '''Class for storing HIBC (Healthcare Industry Bar Code Council) LIC (Licensed Identification Code) secondary and additional data.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def expiry_date_format(self) -> groupdocs.signature.domain.extensions.HIBCLICDateFormat:
        '''Identifies expiry date format.'''
        raise NotImplementedError()
    
    @expiry_date_format.setter
    def expiry_date_format(self, value : groupdocs.signature.domain.extensions.HIBCLICDateFormat) -> None:
        '''Identifies expiry date format.'''
        raise NotImplementedError()
    
    @property
    def expiry_date(self) -> datetime:
        '''Identifies expiry date. Will be used if ExpiryDateFormat is not set to None.'''
        raise NotImplementedError()
    
    @expiry_date.setter
    def expiry_date(self, value : datetime) -> None:
        '''Identifies expiry date. Will be used if ExpiryDateFormat is not set to None.'''
        raise NotImplementedError()
    
    @property
    def lot_number(self) -> str:
        '''Identifies lot or batch number.
        Lot/batch number must be alphanumeric string with up to 18 symbols length.'''
        raise NotImplementedError()
    
    @lot_number.setter
    def lot_number(self, value : str) -> None:
        '''Identifies lot or batch number.
        Lot/batch number must be alphanumeric string with up to 18 symbols length.'''
        raise NotImplementedError()
    
    @property
    def serial_number(self) -> str:
        '''Identifies serial number.
        Serial number must be alphanumeric string up to 18 symbols length.'''
        raise NotImplementedError()
    
    @serial_number.setter
    def serial_number(self, value : str) -> None:
        '''Identifies serial number.
        Serial number must be alphanumeric string up to 18 symbols length.'''
        raise NotImplementedError()
    
    @property
    def date_of_manufacture(self) -> datetime:
        '''Identifies date of manufacture.
        Date of manufacture can be set to DateTime.MinValue in order not to use this field.
        Default value: DateTime.MinValue'''
        raise NotImplementedError()
    
    @date_of_manufacture.setter
    def date_of_manufacture(self, value : datetime) -> None:
        '''Identifies date of manufacture.
        Date of manufacture can be set to DateTime.MinValue in order not to use this field.
        Default value: DateTime.MinValue'''
        raise NotImplementedError()
    
    @property
    def quantity(self) -> int:
        '''Identifies quantity, must be integer value from 0 to 500.
        Quantity can be set to -1 in order not to use this field. Default value: -1'''
        raise NotImplementedError()
    
    @quantity.setter
    def quantity(self, value : int) -> None:
        '''Identifies quantity, must be integer value from 0 to 500.
        Quantity can be set to -1 in order not to use this field. Default value: -1'''
        raise NotImplementedError()
    
    @property
    def link_character(self) -> str:
        '''Identifies link character in output string.'''
        raise NotImplementedError()
    
    @link_character.setter
    def link_character(self, value : str) -> None:
        '''Identifies link character in output string.'''
        raise NotImplementedError()
    

class HIBCPASData:
    '''Class for encoding and decoding the text embedded in the HIBC PAS code.'''
    
    @overload
    def add_record(self, data_type : groupdocs.signature.domain.extensions.HIBCPASDataType, data : str) -> groupdocs.signature.domain.extensions.HIBCPASData:
        '''Adds new record :py:class:`groupdocs.signature.domain.extensions.HIBCPASRecord` with given data type and data
        
        :param data_type: Record data type
        :param data: Record data'''
        raise NotImplementedError()
    
    @overload
    def add_record(self, record : groupdocs.signature.domain.extensions.HIBCPASRecord) -> groupdocs.signature.domain.extensions.HIBCPASData:
        '''Adds new record
        
        :param record: Record to be added
        :returns: Return reference on itself'''
        raise NotImplementedError()
    
    def clear(self) -> groupdocs.signature.domain.extensions.HIBCPASData:
        '''Clears records list
        
        :returns: Returns reference on itself'''
        raise NotImplementedError()
    
    @property
    def data_location(self) -> groupdocs.signature.domain.extensions.HIBCPASDataLocation:
        '''Identifies data location.'''
        raise NotImplementedError()
    
    @data_location.setter
    def data_location(self, value : groupdocs.signature.domain.extensions.HIBCPASDataLocation) -> None:
        '''Identifies data location.'''
        raise NotImplementedError()
    
    @property
    def records(self) -> List[groupdocs.signature.domain.extensions.HIBCPASRecord]:
        '''List of HIBCPASRecord records'''
        raise NotImplementedError()
    
    @records.setter
    def records(self, value : List[groupdocs.signature.domain.extensions.HIBCPASRecord]) -> None:
        '''List of HIBCPASRecord records'''
        raise NotImplementedError()
    

class HIBCPASRecord:
    '''Class for storing HIBC (Healthcare Industry Bar Code Council) PAS (Provider Applications Standard) Record'''
    
    @property
    def data_type(self) -> groupdocs.signature.domain.extensions.HIBCPASDataType:
        '''HIBC PAS record\'s data type.'''
        raise NotImplementedError()
    
    @data_type.setter
    def data_type(self, value : groupdocs.signature.domain.extensions.HIBCPASDataType) -> None:
        '''HIBC PAS record\'s data type.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> str:
        '''Identifies data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : str) -> None:
        '''Identifies data.'''
        raise NotImplementedError()
    

class IDataEncryption:
    '''Encryption interface to provide object encoding and decoding methods.'''
    
    def encode(self, source : str) -> str:
        '''Encode method to encrypt string.
        
        :param source: Source string to encode.
        :returns: Returns encrypted string'''
        raise NotImplementedError()
    
    def decode(self, source : str) -> str:
        '''Decode method to obtain decrypted string.
        
        :param source: Encrypted string to decode.
        :returns: Returns decrypted string'''
        raise NotImplementedError()
    

class IDataSerializer:
    '''Serialization interface to provide object serialization and deserialization methods.'''
    
    def serialize(self, data : Any) -> str:
        '''Serialize method to format object to string representing.
        
        :param data: Source object to serialize'''
        raise NotImplementedError()
    

class LinearGradientBrush(Brush):
    '''Represents linear gradient brush.'''
    
    @property
    def start_color(self) -> aspose.pydrawing.Color:
        '''Gets start gradient color.'''
        raise NotImplementedError()
    
    @start_color.setter
    def start_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets start gradient color.'''
        raise NotImplementedError()
    
    @property
    def end_color(self) -> aspose.pydrawing.Color:
        '''Gets finish gradient color.'''
        raise NotImplementedError()
    
    @end_color.setter
    def end_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets finish gradient color.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets gradient angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets gradient angle.'''
        raise NotImplementedError()
    

class Mailmark2D:
    '''Class for encoding and decoding the text embedded in the Royal Mail 2D Mailmark'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def upu_country_id(self) -> str:
        '''Identifies the UPU Country ID.Max length: 4 characters.'''
        raise NotImplementedError()
    
    @upu_country_id.setter
    def upu_country_id(self, value : str) -> None:
        '''Identifies the UPU Country ID.Max length: 4 characters.'''
        raise NotImplementedError()
    
    @property
    def information_type_id(self) -> str:
        '''Identifies the Royal Mail Mailmark barcode payload for each product type.'''
        raise NotImplementedError()
    
    @information_type_id.setter
    def information_type_id(self, value : str) -> None:
        '''Identifies the Royal Mail Mailmark barcode payload for each product type.'''
        raise NotImplementedError()
    
    @property
    def version_id(self) -> str:
        '''Identifies the barcode version as relevant to each Information Type ID.'''
        raise NotImplementedError()
    
    @property
    def supply_chain_id(self) -> int:
        '''Identifies the unique group of customers involved in the mailing.
        Max value: 9999999.'''
        raise NotImplementedError()
    
    @supply_chain_id.setter
    def supply_chain_id(self, value : int) -> None:
        '''Identifies the unique group of customers involved in the mailing.
        Max value: 9999999.'''
        raise NotImplementedError()
    
    @property
    def item_id(self) -> int:
        '''Identifies the unique item within the Supply Chain ID.
        Every Mailmark barcode is required to carry an ID so it can be uniquely identified for at least 90 days.
        Max value: 99999999.'''
        raise NotImplementedError()
    
    @item_id.setter
    def item_id(self, value : int) -> None:
        '''Identifies the unique item within the Supply Chain ID.
        Every Mailmark barcode is required to carry an ID so it can be uniquely identified for at least 90 days.
        Max value: 99999999.'''
        raise NotImplementedError()
    
    @property
    def destination_post_code_and_dps(self) -> str:
        '''Contains the Postcode of the Delivery Address with DPS
        If inland the Postcode/DP  contains the following number of characters.
        Area (1 or 2 characters)
        District(1 or 2 characters)
        Sector(1 character)
        Unit(2 characters)
        DPS (2 characters).
        The Postcode and DPS must comply with a valid PAF® format. Max length is 9.'''
        raise NotImplementedError()
    
    @destination_post_code_and_dps.setter
    def destination_post_code_and_dps(self, value : str) -> None:
        '''Contains the Postcode of the Delivery Address with DPS
        If inland the Postcode/DP  contains the following number of characters.
        Area (1 or 2 characters)
        District(1 or 2 characters)
        Sector(1 character)
        Unit(2 characters)
        DPS (2 characters).
        The Postcode and DPS must comply with a valid PAF® format. Max length is 9.'''
        raise NotImplementedError()
    
    @property
    def rts_flag(self) -> str:
        '''Flag which indicates what level of Return to Sender service is being requested. Max length is 1'''
        raise NotImplementedError()
    
    @rts_flag.setter
    def rts_flag(self, value : str) -> None:
        '''Flag which indicates what level of Return to Sender service is being requested. Max length is 1'''
        raise NotImplementedError()
    
    @property
    def return_to_sender_post_code(self) -> str:
        '''Contains the Return to Sender Post Code but no DPS.
        The PC(without DPS) must comply with a PAF® format.'''
        raise NotImplementedError()
    
    @return_to_sender_post_code.setter
    def return_to_sender_post_code(self, value : str) -> None:
        '''Contains the Return to Sender Post Code but no DPS.
        The PC(without DPS) must comply with a PAF® format.'''
        raise NotImplementedError()
    
    @property
    def customer_content(self) -> str:
        '''Optional space for use by customer.'''
        raise NotImplementedError()
    
    @customer_content.setter
    def customer_content(self, value : str) -> None:
        '''Optional space for use by customer.'''
        raise NotImplementedError()
    
    @property
    def customer_content_encode_mode(self) -> groupdocs.signature.domain.extensions.DataMatrixEncodeMode:
        '''Encode mode of DataMatrix barcode. Default value: DataMatrixEncodeMode.C40. :py:class:`groupdocs.signature.domain.extensions.DataMatrixEncodeMode`'''
        raise NotImplementedError()
    
    @customer_content_encode_mode.setter
    def customer_content_encode_mode(self, value : groupdocs.signature.domain.extensions.DataMatrixEncodeMode) -> None:
        '''Encode mode of DataMatrix barcode. Default value: DataMatrixEncodeMode.C40. :py:class:`groupdocs.signature.domain.extensions.DataMatrixEncodeMode`'''
        raise NotImplementedError()
    
    @property
    def data_matrix_type(self) -> groupdocs.signature.domain.extensions.Mailmark2DType:
        '''2D Mailmark Type defines size of Data Matrix barcode.'''
        raise NotImplementedError()
    
    @data_matrix_type.setter
    def data_matrix_type(self, value : groupdocs.signature.domain.extensions.Mailmark2DType) -> None:
        '''2D Mailmark Type defines size of Data Matrix barcode.'''
        raise NotImplementedError()
    

class MaxiCodeMode2:
    '''Class for encoding and decoding the text embedded in the MaxiCode code for modes'''
    
    @property
    def postal_code(self) -> str:
        '''Identifies the postal code. Must be 9 digits in mode 2 or 6 alphanumeric symbols in mode 3.'''
        raise NotImplementedError()
    
    @postal_code.setter
    def postal_code(self, value : str) -> None:
        '''Identifies the postal code. Must be 9 digits in mode 2 or 6 alphanumeric symbols in mode 3.'''
        raise NotImplementedError()
    
    @property
    def country_code(self) -> int:
        '''Identifies the 3-digit country code.'''
        raise NotImplementedError()
    
    @country_code.setter
    def country_code(self, value : int) -> None:
        '''Identifies the 3-digit country code.'''
        raise NotImplementedError()
    
    @property
    def service_category(self) -> int:
        '''Identifies the 3-digit service category.'''
        raise NotImplementedError()
    
    @service_category.setter
    def service_category(self, value : int) -> None:
        '''Identifies the 3-digit service category.'''
        raise NotImplementedError()
    
    @property
    def second_message(self) -> groupdocs.signature.domain.extensions.MaxiCodeSecondMessage:
        '''Identifies the second message of the barcode.'''
        raise NotImplementedError()
    
    @second_message.setter
    def second_message(self, value : groupdocs.signature.domain.extensions.MaxiCodeSecondMessage) -> None:
        '''Identifies the second message of the barcode.'''
        raise NotImplementedError()
    

class MaxiCodeSecondMessage:
    '''Class for encoding and decoding standart second message for MaxiCode barcode.'''
    
    @property
    def message(self) -> str:
        '''Gets the second message.'''
        raise NotImplementedError()
    
    @message.setter
    def message(self, value : str) -> None:
        '''Sets the second message.'''
        raise NotImplementedError()
    

class MeCard:
    '''Represents MeCard standard contact details.'''
    
    @property
    def name(self) -> str:
        '''Gets contact Name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets contact Name.'''
        raise NotImplementedError()
    
    @property
    def nickname(self) -> str:
        '''Gets contact Nickname.'''
        raise NotImplementedError()
    
    @nickname.setter
    def nickname(self, value : str) -> None:
        '''Sets contact Nickname.'''
        raise NotImplementedError()
    
    @property
    def phone(self) -> str:
        '''Gets phone number.'''
        raise NotImplementedError()
    
    @phone.setter
    def phone(self, value : str) -> None:
        '''Sets phone number.'''
        raise NotImplementedError()
    
    @property
    def alt_phone(self) -> str:
        '''Gets alternative phone number.'''
        raise NotImplementedError()
    
    @alt_phone.setter
    def alt_phone(self, value : str) -> None:
        '''Sets alternative phone number.'''
        raise NotImplementedError()
    
    @property
    def reading(self) -> str:
        '''Gets reading of name.'''
        raise NotImplementedError()
    
    @reading.setter
    def reading(self, value : str) -> None:
        '''Sets reading of name.'''
        raise NotImplementedError()
    
    @property
    def email(self) -> str:
        '''Gets contact email.'''
        raise NotImplementedError()
    
    @email.setter
    def email(self, value : str) -> None:
        '''Sets contact email.'''
        raise NotImplementedError()
    
    @property
    def note(self) -> str:
        '''Gets Note (Company) of contact.'''
        raise NotImplementedError()
    
    @note.setter
    def note(self, value : str) -> None:
        '''Sets Note (Company) of contact.'''
        raise NotImplementedError()
    
    @property
    def url(self) -> str:
        '''Gets URL.'''
        raise NotImplementedError()
    
    @url.setter
    def url(self, value : str) -> None:
        '''Sets URL.'''
        raise NotImplementedError()
    
    @property
    def address(self) -> groupdocs.signature.domain.extensions.Address:
        '''Gets Home Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @address.setter
    def address(self, value : groupdocs.signature.domain.extensions.Address) -> None:
        '''Sets Home Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @property
    def birth_day(self) -> Optional[datetime]:
        '''Gets contact birthday.'''
        raise NotImplementedError()
    
    @birth_day.setter
    def birth_day(self, value : Optional[datetime]) -> None:
        '''Sets contact birthday.'''
        raise NotImplementedError()
    

class RadialGradientBrush(Brush):
    '''Represents radial gradient brush.'''
    
    @property
    def inner_color(self) -> aspose.pydrawing.Color:
        '''Gets inner gradient color.'''
        raise NotImplementedError()
    
    @inner_color.setter
    def inner_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets inner gradient color.'''
        raise NotImplementedError()
    
    @property
    def outer_color(self) -> aspose.pydrawing.Color:
        '''Gets outer gradient color.'''
        raise NotImplementedError()
    
    @outer_color.setter
    def outer_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets outer gradient color.'''
        raise NotImplementedError()
    

class SMS:
    '''Represents SMS short message service details.'''
    
    @property
    def number(self) -> str:
        '''Gets SMS recipient phone number.'''
        raise NotImplementedError()
    
    @number.setter
    def number(self, value : str) -> None:
        '''Sets SMS recipient phone number.'''
        raise NotImplementedError()
    
    @property
    def message(self) -> str:
        '''Gets SMS message content.'''
        raise NotImplementedError()
    
    @message.setter
    def message(self, value : str) -> None:
        '''Sets SMS message content.'''
        raise NotImplementedError()
    

class SignatureExtension:
    '''Represents base class for signatures extensions.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    

class SkipSerializationAttribute:
    '''Instructs the serialization to skip the member.'''
    

class SolidBrush(Brush):
    '''Represents solid brush.
    It could be used instead background color property.'''
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets color of solid brush.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets color of solid brush.'''
        raise NotImplementedError()
    

class SpreadsheetPosition(SignatureExtension):
    '''Defines signature position for Spreadsheet documents.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def row(self) -> int:
        '''Gets the top row number of signature (min value is 0).'''
        raise NotImplementedError()
    
    @row.setter
    def row(self, value : int) -> None:
        '''Sets the top row number of signature (min value is 0).'''
        raise NotImplementedError()
    
    @property
    def column(self) -> int:
        '''Gets the left column number of signature (min value is 0).'''
        raise NotImplementedError()
    
    @column.setter
    def column(self, value : int) -> None:
        '''Sets the left column number of signature (min value is 0).'''
        raise NotImplementedError()
    

class SwissAddress:
    '''Represents the address of the creditor or debtor.
    You can either set street, house number, postal code, and town (structured address type)
    or address line 1 and 2 (combined address elements type).'''
    
    @property
    def name(self) -> str:
        '''Gets the name, either the first and last name of a natural person or
        the company name of a legal person.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name, either the first and last name of a natural person or
        the company name of a legal person.'''
        raise NotImplementedError()
    
    @property
    def address_line1(self) -> str:
        '''Gets the address line 1.
        Address line 1 contains street name, house number or P.O. box.
        This field is only used for combined elements addresses and is optional.'''
        raise NotImplementedError()
    
    @address_line1.setter
    def address_line1(self, value : str) -> None:
        '''Sets the address line 1.
        Address line 1 contains street name, house number or P.O. box.
        This field is only used for combined elements addresses and is optional.'''
        raise NotImplementedError()
    
    @property
    def address_line2(self) -> str:
        '''Gets the address line 2.
        Address line 2 contains postal code and town.
        This field is only used for combined elements addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @address_line2.setter
    def address_line2(self, value : str) -> None:
        '''Sets the address line 2.
        Address line 2 contains postal code and town.
        This field is only used for combined elements addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @property
    def street(self) -> str:
        '''Gets the street.
        The street must be specified without a house number.
        This field is only used for structured addresses and is optional.'''
        raise NotImplementedError()
    
    @street.setter
    def street(self, value : str) -> None:
        '''Sets the street.
        The street must be specified without a house number.
        This field is only used for structured addresses and is optional.'''
        raise NotImplementedError()
    
    @property
    def house_no(self) -> str:
        '''Gets the house number.
        This field is only used for structured addresses and is optional.'''
        raise NotImplementedError()
    
    @house_no.setter
    def house_no(self, value : str) -> None:
        '''Sets the house number.
        This field is only used for structured addresses and is optional.'''
        raise NotImplementedError()
    
    @property
    def postal_code(self) -> str:
        '''Gets the postal code.
        This field is only used for structured addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @postal_code.setter
    def postal_code(self, value : str) -> None:
        '''Sets the postal code.
        This field is only used for structured addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @property
    def town(self) -> str:
        '''Gets the town or city.
        This field is only used for structured addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @town.setter
    def town(self, value : str) -> None:
        '''Sets the town or city.
        This field is only used for structured addresses. For this type, it\'s mandatory.'''
        raise NotImplementedError()
    
    @property
    def country_code(self) -> str:
        '''Gets the two-letter ISO country code.
        The country code is mandatory unless the entire address contains null or empty values.'''
        raise NotImplementedError()
    
    @country_code.setter
    def country_code(self, value : str) -> None:
        '''Sets the two-letter ISO country code.
        The country code is mandatory unless the entire address contains null or empty values.'''
        raise NotImplementedError()
    

class SwissQR:
    '''Class for encoding and decoding the text embedded in the SwissQR code.'''
    
    @property
    def amount(self) -> float:
        '''Gets the payment amount.
        Valid values are between 0.01 and 999,999,999.99.'''
        raise NotImplementedError()
    
    @amount.setter
    def amount(self, value : float) -> None:
        '''Sets the payment amount.
        Valid values are between 0.01 and 999,999,999.99.'''
        raise NotImplementedError()
    
    @property
    def currency(self) -> str:
        '''Gets the payment currency.
        Valid values are "CHF" and "EUR".'''
        raise NotImplementedError()
    
    @currency.setter
    def currency(self, value : str) -> None:
        '''Sets the payment currency.
        Valid values are "CHF" and "EUR".'''
        raise NotImplementedError()
    
    @property
    def account(self) -> str:
        '''Gets the creditor\'s account number.
        Account numbers must be valid IBANs of a bank of Switzerland or Liechtenstein.
        Spaces are allowed in the account number.'''
        raise NotImplementedError()
    
    @account.setter
    def account(self, value : str) -> None:
        '''Sets the creditor\'s account number.
        Account numbers must be valid IBANs of a bank of Switzerland or Liechtenstein.
        Spaces are allowed in the account number.'''
        raise NotImplementedError()
    
    @property
    def creditor(self) -> groupdocs.signature.domain.extensions.SwissAddress:
        '''Gets the creditor address.'''
        raise NotImplementedError()
    
    @creditor.setter
    def creditor(self, value : groupdocs.signature.domain.extensions.SwissAddress) -> None:
        '''Sets the creditor address.'''
        raise NotImplementedError()
    
    @property
    def reference(self) -> str:
        '''Gets the creditor payment reference.
        The reference is mandatory for SwissQR IBANs, i.e. IBANs in the range CHxx30000xxxxxx
        through CHxx31999xxxxx.
        If specified, the reference must be either a valid SwissQR reference (corresponding
        to ISR reference form) or a valid creditor reference according to ISO 11649 ("RFxxxx").
        Both may contain spaces for formatting.'''
        raise NotImplementedError()
    
    @reference.setter
    def reference(self, value : str) -> None:
        '''Sets the creditor payment reference.
        The reference is mandatory for SwissQR IBANs, i.e. IBANs in the range CHxx30000xxxxxx
        through CHxx31999xxxxx.
        If specified, the reference must be either a valid SwissQR reference (corresponding
        to ISR reference form) or a valid creditor reference according to ISO 11649 ("RFxxxx").
        Both may contain spaces for formatting.'''
        raise NotImplementedError()
    
    @property
    def debtor(self) -> groupdocs.signature.domain.extensions.SwissAddress:
        '''Gets the debtor address.
        The debtor is optional. If it is omitted, both setting this field to null or
        setting an address with all null or empty values is ok.'''
        raise NotImplementedError()
    
    @debtor.setter
    def debtor(self, value : groupdocs.signature.domain.extensions.SwissAddress) -> None:
        '''Sets the debtor address.
        The debtor is optional. If it is omitted, both setting this field to null or
        setting an address with all null or empty values is ok.'''
        raise NotImplementedError()
    
    @property
    def unstructured_message(self) -> str:
        '''Gets the additional unstructured message.'''
        raise NotImplementedError()
    
    @unstructured_message.setter
    def unstructured_message(self, value : str) -> None:
        '''Sets the additional unstructured message.'''
        raise NotImplementedError()
    
    @property
    def bill_information(self) -> str:
        '''Gets the additional structured bill information.'''
        raise NotImplementedError()
    
    @bill_information.setter
    def bill_information(self, value : str) -> None:
        '''Sets the additional structured bill information.'''
        raise NotImplementedError()
    

class SymmetricEncryption(IDataEncryption):
    '''Implements standard symmetric algorithms for data encryption with single key and passphrase (salt).'''
    
    def encode(self, source : str) -> str:
        '''Encrypts string based on provided algorithm type, key and salt parameters
        
        :param source: Source string to encode.
        :returns: Returns encrypted string.'''
        raise NotImplementedError()
    
    def decode(self, source : str) -> str:
        '''Decrypts string based on provided algorithm type, key and salt parameters
        
        :param source: Encrypted string to decode.
        :returns: Returns decrypted string.'''
        raise NotImplementedError()
    
    @property
    def algorithm_type(self) -> groupdocs.signature.domain.extensions.SymmetricAlgorithmType:
        '''Gets type of symmetric algorithm.'''
        raise NotImplementedError()
    
    @algorithm_type.setter
    def algorithm_type(self, value : groupdocs.signature.domain.extensions.SymmetricAlgorithmType) -> None:
        '''Sets type of symmetric algorithm.'''
        raise NotImplementedError()
    
    @property
    def key(self) -> str:
        '''Gets key of encryption algorithm.'''
        raise NotImplementedError()
    
    @key.setter
    def key(self, value : str) -> None:
        '''Sets key of encryption algorithm.'''
        raise NotImplementedError()
    
    @property
    def salt(self) -> str:
        '''Gets passphrase of encryption algorithm.'''
        raise NotImplementedError()
    
    @salt.setter
    def salt(self, value : str) -> None:
        '''Sets passphrase of encryption algorithm.'''
        raise NotImplementedError()
    

class SymmetricEncryptionAttribute(IDataEncryption):
    '''Instructs instances serialization to encrypt / decrypt object serialization string.'''
    
    def encode(self, source : str) -> str:
        '''Encrypts string based on provided algorithm type, key and salt parameters
        
        :param source: Source string to encode
        :returns: Returns encoded string.'''
        raise NotImplementedError()
    
    def decode(self, source : str) -> str:
        '''Decrypts passed string based on algorithm type, key and salt parameters
        
        :param source: Encrypted string to decode.
        :returns: Returns decoded string.'''
        raise NotImplementedError()
    

class TextShadow(SignatureExtension):
    '''Represents text shadow properties for text signatures.
    The result may vary depending on the signature type and document format.
    TextShadow is recommended for using with TextAsImage signature for all supported document types,
    also with simple TextSignature and TextSignature as watermark for Spreadsheets (.xslx) and Presentations (.pptx).
    Simple TextSignature for Words (.docx) is recommended too, but has limited functionality.'''
    
    def clone(self) -> Any:
        '''Gets a copy of this object.'''
        raise NotImplementedError()
    
    @property
    def distance(self) -> float:
        '''Gets distance from text to shadow.
        Default value is 1.'''
        raise NotImplementedError()
    
    @distance.setter
    def distance(self, value : float) -> None:
        '''Sets distance from text to shadow.
        Default value is 1.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets angle for placing shadow relative to the text.
        Default value is 0.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets angle for placing shadow relative to the text.
        Default value is 0.'''
        raise NotImplementedError()
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets color of the shadow.
        Default value is Black.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets color of the shadow.
        Default value is Black.'''
        raise NotImplementedError()
    
    @property
    def transparency(self) -> float:
        '''Gets transparency of the shadow.
        Default value is 0.'''
        raise NotImplementedError()
    
    @transparency.setter
    def transparency(self, value : float) -> None:
        '''Sets transparency of the shadow.
        Default value is 0.'''
        raise NotImplementedError()
    
    @property
    def blur(self) -> float:
        '''Gets blur of the shadow.
        Default value is 4.'''
        raise NotImplementedError()
    
    @blur.setter
    def blur(self, value : float) -> None:
        '''Sets blur of the shadow.
        Default value is 4.'''
        raise NotImplementedError()
    

class TextureBrush(Brush):
    '''Represents texture brush.'''
    
    @property
    def image_file_path(self) -> str:
        '''Gets the texture image file path.
        This property is used only if ImageStream is not specified.'''
        raise NotImplementedError()
    
    @image_file_path.setter
    def image_file_path(self, value : str) -> None:
        '''Sets the texture image file path.
        This property is used only if ImageStream is not specified.'''
        raise NotImplementedError()
    
    @property
    def image_stream(self) -> io.RawIOBase:
        '''Gets the texture image stream.
        If this property is specified it is always used instead ImageFilePath.'''
        raise NotImplementedError()
    
    @image_stream.setter
    def image_stream(self, value : io.RawIOBase) -> None:
        '''Sets the texture image stream.
        If this property is specified it is always used instead ImageFilePath.'''
        raise NotImplementedError()
    

class VCard:
    '''Represents Electronic Business Card standard contact details.'''
    
    @property
    def first_name(self) -> str:
        '''Gets contact First Name.'''
        raise NotImplementedError()
    
    @first_name.setter
    def first_name(self, value : str) -> None:
        '''Sets contact First Name.'''
        raise NotImplementedError()
    
    @property
    def midddle_name(self) -> str:
        '''Gets contact Middle Name.'''
        raise NotImplementedError()
    
    @midddle_name.setter
    def midddle_name(self, value : str) -> None:
        '''Sets contact Middle Name.'''
        raise NotImplementedError()
    
    @property
    def last_name(self) -> str:
        '''Gets contact Last Name.'''
        raise NotImplementedError()
    
    @last_name.setter
    def last_name(self, value : str) -> None:
        '''Sets contact Last Name.'''
        raise NotImplementedError()
    
    @property
    def initials(self) -> str:
        '''Gets contact initials.'''
        raise NotImplementedError()
    
    @initials.setter
    def initials(self, value : str) -> None:
        '''Sets contact initials.'''
        raise NotImplementedError()
    
    @property
    def company(self) -> str:
        '''Gets Company of contact.'''
        raise NotImplementedError()
    
    @company.setter
    def company(self, value : str) -> None:
        '''Sets Company of contact.'''
        raise NotImplementedError()
    
    @property
    def job_title(self) -> str:
        '''Gets contact Job Title.'''
        raise NotImplementedError()
    
    @job_title.setter
    def job_title(self, value : str) -> None:
        '''Sets contact Job Title.'''
        raise NotImplementedError()
    
    @property
    def home_address(self) -> groupdocs.signature.domain.extensions.Address:
        '''Gets Home Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @home_address.setter
    def home_address(self, value : groupdocs.signature.domain.extensions.Address) -> None:
        '''Sets Home Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @property
    def work_address(self) -> groupdocs.signature.domain.extensions.Address:
        '''Gets Work Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @work_address.setter
    def work_address(self, value : groupdocs.signature.domain.extensions.Address) -> None:
        '''Sets Work Address properties. This property is not initialized by default.'''
        raise NotImplementedError()
    
    @property
    def home_phone(self) -> str:
        '''Gets home phone number.'''
        raise NotImplementedError()
    
    @home_phone.setter
    def home_phone(self, value : str) -> None:
        '''Sets home phone number.'''
        raise NotImplementedError()
    
    @property
    def work_phone(self) -> str:
        '''Gets work phone number.'''
        raise NotImplementedError()
    
    @work_phone.setter
    def work_phone(self, value : str) -> None:
        '''Sets work phone number.'''
        raise NotImplementedError()
    
    @property
    def cell_phone(self) -> str:
        '''Gets cellular phone number.'''
        raise NotImplementedError()
    
    @cell_phone.setter
    def cell_phone(self, value : str) -> None:
        '''Sets cellular phone number.'''
        raise NotImplementedError()
    
    @property
    def email(self) -> str:
        '''Gets contact email.'''
        raise NotImplementedError()
    
    @email.setter
    def email(self, value : str) -> None:
        '''Sets contact email.'''
        raise NotImplementedError()
    
    @property
    def url(self) -> str:
        '''Gets contact URL.'''
        raise NotImplementedError()
    
    @url.setter
    def url(self, value : str) -> None:
        '''Sets contact URL.'''
        raise NotImplementedError()
    
    @property
    def birth_day(self) -> Optional[datetime]:
        '''Gets contact birthday.'''
        raise NotImplementedError()
    
    @birth_day.setter
    def birth_day(self, value : Optional[datetime]) -> None:
        '''Sets contact birthday.'''
        raise NotImplementedError()
    

class WiFi:
    '''Represents WiFi network connection details.'''
    
    @property
    def ssid(self) -> str:
        '''Gets WiFi SSID Name.'''
        raise NotImplementedError()
    
    @ssid.setter
    def ssid(self, value : str) -> None:
        '''Sets WiFi SSID Name.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Gets WiFi Password.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Sets WiFi Password.'''
        raise NotImplementedError()
    
    @property
    def encryption(self) -> groupdocs.signature.domain.extensions.WiFiEncryptionType:
        '''Gets WiFi encryption :py:class:`groupdocs.signature.domain.extensions.WiFiEncryptionType`.'''
        raise NotImplementedError()
    
    @encryption.setter
    def encryption(self, value : groupdocs.signature.domain.extensions.WiFiEncryptionType) -> None:
        '''Sets WiFi encryption :py:class:`groupdocs.signature.domain.extensions.WiFiEncryptionType`.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets if WiFi is Hidden SSID.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets if WiFi is Hidden SSID.'''
        raise NotImplementedError()
    

class CryptoCurrencyType:
    '''Represents Cryptocurrency type.'''
    
    CUSTOM : CryptoCurrencyType
    '''Represents custom cryptocurrency type.'''
    BITCOIN : CryptoCurrencyType
    '''Represents Bitcoin cryptocurrency type.'''
    BITCOIN_CASH : CryptoCurrencyType
    '''Represents Bitcoin Cash cryptocurrency type.'''
    LITECOIN : CryptoCurrencyType
    '''Represents Litecoin cryptocurrency type.'''
    ETHEREUM : CryptoCurrencyType
    '''Represents Ethereum cryptocurrency type.'''
    DASH : CryptoCurrencyType
    '''Represents Dash cryptocurrency type.'''

class DataMatrixEncodeMode:
    '''DataMatrix encoder\'s encoding mode, default to Auto'''
    
    AUTO : DataMatrixEncodeMode
    '''Automatically pick up the best encode mode for DataMatrix encoding'''
    ASCII : DataMatrixEncodeMode
    '''Encodes one alphanumeric or two numeric characters per byte'''
    FULL : DataMatrixEncodeMode
    '''Encode 8 bit values'''
    CUSTOM : DataMatrixEncodeMode
    '''Encode with the encoding specified in BarcodeGenerator.Parameters.Barcode.DataMatrix.CodeTextEncoding'''
    C40 : DataMatrixEncodeMode
    '''Uses C40 encoding. Encodes Upper-case alphanumeric, Lower case and special characters'''
    TEXT : DataMatrixEncodeMode
    '''Uses Text encoding. Encodes Lower-case alphanumeric, Upper case and special characters.'''
    EDIFACT : DataMatrixEncodeMode
    '''Uses EDIFACT encoding. Uses six bits per character, encodes digits,
    upper-case letters, and many punctuation marks, but has no support for lower-case letters.'''
    ANSIX12 : DataMatrixEncodeMode
    '''Uses ANSI X12 encoding.'''
    EXTENDED_CODETEXT : DataMatrixEncodeMode
    '''ExtendedCodetext mode allows to manually switch encoding schemes in code-text.
    Format : "\Encodation_scheme_name:text\Encodation_scheme_name:text".
    Allowed encoding schemes are: EDIFACT, ANSIX12, ASCII, C40, Text, Auto.
    Extended code-text example: @"\ansix12:ANSIX12TEXT\ascii:backslash must be \\
    doubled\edifact:EdifactEncodedText"
    All backslashes (\) must be doubled in text.'''

class HIBCLICDateFormat:
    '''Specifies the different types of date formats for HIBC (Healthcare Industry Bar Code) LIC (Licensed Identification Code).'''
    
    YYYYMMDD : HIBCLICDateFormat
    '''YYYYMMDD format. Will be encoded in additional supplemental data.'''
    MMYY : HIBCLICDateFormat
    '''MMYY format.'''
    MMDDYY : HIBCLICDateFormat
    '''MMDDYY format.'''
    YYMMDD : HIBCLICDateFormat
    '''YYMMDD format.'''
    YYMMDDHH : HIBCLICDateFormat
    '''YYMMDDHH format.'''
    YYJJJ : HIBCLICDateFormat
    '''Julian date format.'''
    YYJJJHH : HIBCLICDateFormat
    '''Julian date format with hours.'''
    NONE : HIBCLICDateFormat
    '''Do not encode expiry date.'''

class HIBCPASDataLocation:
    '''Specifies HIBC PAS data location types.
    HIBC - Healthcare Industry Bar Code
    PAS - Provider Applications Standard'''
    
    PATIENT : HIBCPASDataLocation
    '''A - Patient'''
    PATIENT_CARE_RECORD : HIBCPASDataLocation
    '''B - Patient Care Record'''
    SPECIMEN_CONTAINER : HIBCPASDataLocation
    '''C - Specimen Container'''
    DIRECT_PATIENT_IMAGE_ITEM : HIBCPASDataLocation
    '''D - Direct Patient Image Item'''
    BUSINESS_RECORD : HIBCPASDataLocation
    '''E - Business Record'''
    MEDICAL_ADMINISTRATION_RECORD : HIBCPASDataLocation
    '''F - Medical Administration Record'''
    LIBRARY_REFERENCE_MATERIAL : HIBCPASDataLocation
    '''G - Library Reference Material'''
    DEVICES_AND_MATERIALS : HIBCPASDataLocation
    '''H - Devices and Materials'''
    IDENTIFICATION_CARD : HIBCPASDataLocation
    '''I - Identification Card'''
    PRODUCT_CONTAINER : HIBCPASDataLocation
    '''J - Product Container'''
    ASSET : HIBCPASDataLocation
    '''K - Asset data type'''
    SURGICAL_INSTRUMENT : HIBCPASDataLocation
    '''L - Surgical Instrument'''
    USER_DEFINED : HIBCPASDataLocation
    '''Z - User Defined'''

class HIBCPASDataType:
    '''Specifies the different data types of HIBC PAS record.
    HIBC - Healthcare Industry Bar Code
    PAS - Provider Applications Standard'''
    
    LABELER_IDENTIFICATION_CODE : HIBCPASDataType
    '''A - Labeler Identification Code'''
    SERVICE_IDENTIFICATION : HIBCPASDataType
    '''B - Service Identification'''
    PATIENT_IDENTIFICATION : HIBCPASDataType
    '''C - Patient Identification'''
    SPECIMEN_IDENTIFICATION : HIBCPASDataType
    '''D - Specimen Identification'''
    PERSONNEL_IDENTIFICATION : HIBCPASDataType
    '''E - Personnel Identification'''
    ADMINISTRABLE_PRODUCT_IDENTIFICATION : HIBCPASDataType
    '''F - Administrable Product Identification'''
    IMPLANTABLE_PRODUCT_INFORMATION : HIBCPASDataType
    '''G - Implantable Product Information'''
    HOSPITAL_ITEM_IDENTIFICATION : HIBCPASDataType
    '''H - Hospital Item Identification'''
    MEDICAL_PROCEDURE_IDENTIFICATION : HIBCPASDataType
    '''I - Medical Procedure Identification'''
    REIMBURSEMENT_CATEGORY : HIBCPASDataType
    '''J - Reimbursement Category'''
    BLOOD_PRODUCT_IDENTIFICATION : HIBCPASDataType
    '''K - Blood Product Identification'''
    DEMOGRAPHIC_DATA : HIBCPASDataType
    '''L - Demographic Data'''
    DATE_TIME : HIBCPASDataType
    '''M - DateTime in YYYDDDHHMMG format'''
    ASSET_IDENTIFICATION : HIBCPASDataType
    '''N - Asset Identification'''
    PURCHASE_ORDER_NUMBER : HIBCPASDataType
    '''O - Purchase Order Number'''
    DIETARY_ITEM_IDENTIFICATION : HIBCPASDataType
    '''P - Dietary Item Identification'''
    MANUFACTURER_SERIAL_NUMBER : HIBCPASDataType
    '''Q - Manufacturer Serial Number'''
    LIBRARY_MATERIALS_IDENTIFICATION : HIBCPASDataType
    '''R - Library Materials Identification'''
    BUSINESS_CONTROL_NUMBER : HIBCPASDataType
    '''S - Business Control Number'''
    EPISODE_OF_CARE_IDENTIFICATION : HIBCPASDataType
    '''T - Episode of Care Identification'''
    HEALTH_INDUSTRY_NUMBER : HIBCPASDataType
    '''U - Health Industry Number'''
    PATIENT_VISIT_ID : HIBCPASDataType
    '''V - Patient Visit ID'''
    XML_DOCUMENT : HIBCPASDataType
    '''X - XML Document'''
    USER_DEFINED : HIBCPASDataType
    '''Z - User Defined'''

class Mailmark2DType:
    '''2D Mailmark Type defines size of Data Matrix barcode'''
    
    AUTO : Mailmark2DType
    '''Auto determine'''
    TYPE_7 : Mailmark2DType
    '''24 x 24 modules'''
    TYPE_9 : Mailmark2DType
    '''32 x 32 modules'''
    TYPE_29 : Mailmark2DType
    '''16 x 48 modules'''

class SymmetricAlgorithmType:
    '''Represents symmetric encryption algorithm type.'''
    
    RIJNDAEL : SymmetricAlgorithmType
    '''Represents Rijndael symmetric encryption algorithm.'''
    AES_NEW : SymmetricAlgorithmType
    '''Represents improved AES (Advanced Encryption Standard) encryption algorithm.'''

class WiFiEncryptionType:
    '''Represents WiFi Encryption type.'''
    
    NONE : WiFiEncryptionType
    '''Represents no encryption WiFi type.'''
    WPA : WiFiEncryptionType
    '''Represents WiFi with the WPA encryption type.'''
    WPAEAP : WiFiEncryptionType
    '''Represents WiFi with the WPA-EAP encryption type.'''
    WPAWPA2 : WiFiEncryptionType
    '''Represents WiFi with the WPA/WPA2 encryption type.'''
    WEP : WiFiEncryptionType
    '''Represents WiFi with the WEP encryption type.'''

