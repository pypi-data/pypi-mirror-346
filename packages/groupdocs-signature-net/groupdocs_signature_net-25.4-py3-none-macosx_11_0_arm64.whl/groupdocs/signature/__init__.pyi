
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

class GroupDocsSignatureException:
    '''Represents the generic errors that occur during document processing.'''
    

class IncorrectPasswordException(GroupDocsSignatureException):
    '''The exception that is thrown when specified password is incorrect.'''
    

class License:
    '''Provides methods to license the component. Learn more about licensing `here <https://purchase.groupdocs.com/faqs/licensing>`.'''
    
    @overload
    def set_license(self, license_path : str) -> None:
        '''Licenses the component.
        
        :param license_path: The license path.'''
        raise NotImplementedError()
    
    @overload
    def set_license(self, license_stream : io.RawIOBase) -> None:
        '''Licenses the component.
        
        :param license_stream: The license stream.'''
        raise NotImplementedError()
    

class Metered:
    '''Provides methods for applying `Metered <https://purchase.groupdocs.com/faqs/licensing/metered>` license.'''
    
    def set_metered_key(self, public_key : str, private_key : str) -> None:
        '''Activates product with Metered keys.
        
        :param public_key: The public key.
        :param private_key: The private key.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_quantity() -> float:
        '''Retrieves amount of MBs processed.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_credit() -> float:
        '''Retrieves count of credits consumed.'''
        raise NotImplementedError()
    

class PasswordRequiredException(GroupDocsSignatureException):
    '''The exception that is thrown when password is required to load the document.'''
    

class ProcessCompleteEventArgs(ProcessEventArgs):
    '''Provides data on complete event of signing, verification and search processes.'''
    
    @property
    def status(self) -> groupdocs.signature.domain.ProcessStatus:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @status.setter
    def status(self, value : groupdocs.signature.domain.ProcessStatus) -> None:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @property
    def completed(self) -> datetime:
        '''Represents the time mark of process completion.'''
        raise NotImplementedError()
    
    @completed.setter
    def completed(self, value : datetime) -> None:
        '''Represents the time mark of process completion.'''
        raise NotImplementedError()
    
    @property
    def ticks(self) -> int:
        '''Represents the time in milliseconds spent since process Start event.'''
        raise NotImplementedError()
    
    @ticks.setter
    def ticks(self, value : int) -> None:
        '''Represents the time in milliseconds spent since process Start event.'''
        raise NotImplementedError()
    
    @property
    def total_signatures(self) -> int:
        '''Represents the total quantity of processed signatures.'''
        raise NotImplementedError()
    
    @total_signatures.setter
    def total_signatures(self, value : int) -> None:
        '''Represents the total quantity of processed signatures.'''
        raise NotImplementedError()
    
    @property
    def canceled(self) -> bool:
        '''Indicates whether process was canceled.'''
        raise NotImplementedError()
    

class ProcessEventArgs:
    '''Provides data for different events of signature, verification and search processes.'''
    
    @property
    def status(self) -> groupdocs.signature.domain.ProcessStatus:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @status.setter
    def status(self, value : groupdocs.signature.domain.ProcessStatus) -> None:
        '''Indicates current process state.'''
        raise NotImplementedError()
    

class ProcessProgressEventArgs(ProcessEventArgs):
    '''Provides data for OnProgress event of signing, verification and search processes.'''
    
    @property
    def status(self) -> groupdocs.signature.domain.ProcessStatus:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @status.setter
    def status(self, value : groupdocs.signature.domain.ProcessStatus) -> None:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @property
    def progress(self) -> int:
        '''Represents the progress in percents. Value range is from 0 to 100.'''
        raise NotImplementedError()
    
    @progress.setter
    def progress(self, value : int) -> None:
        '''Represents the progress in percents. Value range is from 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def ticks(self) -> int:
        '''Represents the time spent in milliseconds since process Start event.'''
        raise NotImplementedError()
    
    @ticks.setter
    def ticks(self, value : int) -> None:
        '''Represents the time spent in milliseconds since process Start event.'''
        raise NotImplementedError()
    
    @property
    def processed_signatures(self) -> int:
        '''Represents the quantity of processed signatures.'''
        raise NotImplementedError()
    
    @processed_signatures.setter
    def processed_signatures(self, value : int) -> None:
        '''Represents the quantity of processed signatures.'''
        raise NotImplementedError()
    
    @property
    def cancel(self) -> bool:
        '''Indicates whether process should be canceled.'''
        raise NotImplementedError()
    
    @cancel.setter
    def cancel(self, value : bool) -> None:
        '''Indicates whether process should be canceled.'''
        raise NotImplementedError()
    

class ProcessStartEventArgs(ProcessEventArgs):
    '''Provides data for Start event of signing, verification and search process'''
    
    @property
    def status(self) -> groupdocs.signature.domain.ProcessStatus:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @status.setter
    def status(self, value : groupdocs.signature.domain.ProcessStatus) -> None:
        '''Indicates current process state.'''
        raise NotImplementedError()
    
    @property
    def started(self) -> datetime:
        '''Represents the time mark of process start.'''
        raise NotImplementedError()
    
    @started.setter
    def started(self, value : datetime) -> None:
        '''Represents the time mark of process start.'''
        raise NotImplementedError()
    
    @property
    def total_signatures(self) -> int:
        '''Represents the total quantity of signatures to be processed.'''
        raise NotImplementedError()
    
    @total_signatures.setter
    def total_signatures(self, value : int) -> None:
        '''Represents the total quantity of signatures to be processed.'''
        raise NotImplementedError()
    

class Signature:
    '''Represents main class that controls document signing process.'''
    
    @overload
    def sign(self, document : io.RawIOBase, sign_options : groupdocs.signature.options.SignOptions) -> groupdocs.signature.domain.SignResult:
        '''Signs document with :py:class:`groupdocs.signature.options.SignOptions` and saves result to a stream.
        
        :param document: The output document stream.
        :param sign_options: The signature options.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.SignResult` with list of newly created signatures.'''
        raise NotImplementedError()
    
    @overload
    def sign(self, document : io.RawIOBase, sign_options : groupdocs.signature.options.SignOptions, save_options : groupdocs.signature.options.SaveOptions) -> groupdocs.signature.domain.SignResult:
        '''Signs document with :py:class:`groupdocs.signature.options.SignOptions` and saves result to a stream with predefined :py:class:`groupdocs.signature.options.SaveOptions`.
        
        :param document: The output document stream.
        :param sign_options: The signature options.
        :param save_options: The save options.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.SignResult` with list of newly created signatures.'''
        raise NotImplementedError()
    
    @overload
    def sign(self, document : io.RawIOBase, sign_options_list : List[groupdocs.signature.options.SignOptions]) -> groupdocs.signature.domain.SignResult:
        raise NotImplementedError()
    
    @overload
    def sign(self, document : io.RawIOBase, sign_options_list : List[groupdocs.signature.options.SignOptions], save_options : groupdocs.signature.options.SaveOptions) -> groupdocs.signature.domain.SignResult:
        raise NotImplementedError()
    
    @overload
    def sign(self, file_path : str, sign_options : groupdocs.signature.options.SignOptions) -> groupdocs.signature.domain.SignResult:
        '''Signs document with :py:class:`groupdocs.signature.options.SignOptions` and saves result to specified file path.
        
        :param file_path: The output file path.
        :param sign_options: The signature options.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.SignResult` with list of newly created signatures.'''
        raise NotImplementedError()
    
    @overload
    def sign(self, file_path : str, sign_options : groupdocs.signature.options.SignOptions, save_options : groupdocs.signature.options.SaveOptions) -> groupdocs.signature.domain.SignResult:
        '''Signs document with :py:class:`groupdocs.signature.options.SignOptions` and saves result to specified file path with predefined :py:class:`groupdocs.signature.options.SaveOptions`.
        
        :param file_path: The output file path.
        :param sign_options: The signature options.
        :param save_options: The save options.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.SignResult` with list of newly created signatures.'''
        raise NotImplementedError()
    
    @overload
    def sign(self, file_path : str, sign_options_list : List[groupdocs.signature.options.SignOptions]) -> groupdocs.signature.domain.SignResult:
        raise NotImplementedError()
    
    @overload
    def sign(self, file_path : str, sign_options_list : List[groupdocs.signature.options.SignOptions], save_options : groupdocs.signature.options.SaveOptions) -> groupdocs.signature.domain.SignResult:
        raise NotImplementedError()
    
    @overload
    def verify(self, verify_options : groupdocs.signature.options.VerifyOptions) -> groupdocs.signature.domain.VerificationResult:
        '''Verifies the document signatures with given VerifyOptions data.
        
        :param verify_options: The signature verification options.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.VerificationResult`. Property VerificationResult.IsValid returns true if verification process was successful.'''
        raise NotImplementedError()
    
    @overload
    def verify(self, verify_options_list : List[groupdocs.signature.options.VerifyOptions]) -> groupdocs.signature.domain.VerificationResult:
        raise NotImplementedError()
    
    @overload
    def search(self, search_options_list : List[groupdocs.signature.options.SearchOptions]) -> groupdocs.signature.domain.SearchResult:
        raise NotImplementedError()
    
    @overload
    def search(self, signature_types : List[groupdocs.signature.domain.SignatureType]) -> groupdocs.signature.domain.SearchResult:
        '''Searches for specified signature types in the document by :py:class:`groupdocs.signature.domain.SignatureType` value.
        
        :param signature_types: One or several types of signatures to find.
        :returns: Returns instance of :py:class:`groupdocs.signature.domain.SearchResult` with list of found signatures.'''
        raise NotImplementedError()
    
    @overload
    def update(self, signature : groupdocs.signature.domain.BaseSignature) -> bool:
        '''Updates passed signature :py:class:`groupdocs.signature.domain.BaseSignature` in the document.
        
        :param signature: Signature object to be updated in the document.
        :returns: Returns true if operation was successful.'''
        raise NotImplementedError()
    
    @overload
    def update(self, signatures : List[groupdocs.signature.domain.BaseSignature]) -> groupdocs.signature.domain.UpdateResult:
        raise NotImplementedError()
    
    @overload
    def delete(self, signature : groupdocs.signature.domain.BaseSignature) -> bool:
        '''Deletes passed signature :py:class:`groupdocs.signature.domain.BaseSignature` from the document.
        
        :param signature: Signature object to be removed from the document.
        :returns: Returns true if operation was successful.'''
        raise NotImplementedError()
    
    @overload
    def delete(self, signatures : List[groupdocs.signature.domain.BaseSignature]) -> groupdocs.signature.domain.DeleteResult:
        raise NotImplementedError()
    
    @overload
    def delete(self, signature_type : groupdocs.signature.domain.SignatureType) -> groupdocs.signature.domain.DeleteResult:
        '''Deletes signatures of the certain type :py:class:`groupdocs.signature.domain.SignatureType` from the document.
        Only signatures that were added by Sign method and marked as Signatures :py:attr:`groupdocs.signature.domain.BaseSignature.is_signature`  will be removed.
        Following signature types are supported: Text, Image, Digital, Barcode, QR-Code
        
        :param signature_type: The type of signatures to be removed from the document.
        :returns: Returns DeleteResult :py:class:`groupdocs.signature.domain.DeleteResult` with list of successfully deleted signatures and failed ones.'''
        raise NotImplementedError()
    
    @overload
    def delete(self, signature_types : List[groupdocs.signature.domain.SignatureType]) -> groupdocs.signature.domain.DeleteResult:
        raise NotImplementedError()
    
    @overload
    def delete(self, signature_id : str) -> bool:
        '''Deletes signature by its specific signature Id from the document.
        
        :param signature_id: The Id of the signature to be removed from the document.
        :returns: Returns true if operation was successful.'''
        raise NotImplementedError()
    
    @overload
    def delete(self, signature_ids : List[str]) -> groupdocs.signature.domain.DeleteResult:
        raise NotImplementedError()
    
    def get_document_info(self) -> groupdocs.signature.domain.IDocumentInfo:
        '''Gets information about document pages: their sizes,
        maximum page height, the width of a page with the maximum height.
        
        :returns: Information about document.'''
        raise NotImplementedError()
    
    def generate_preview(self, preview_options : groupdocs.signature.options.PreviewOptions) -> None:
        '''Generates document pages preview.
        
        :param preview_options: The preview options.'''
        raise NotImplementedError()
    
    @staticmethod
    def generate_signature_preview(preview_options : groupdocs.signature.options.PreviewSignatureOptions) -> None:
        '''Generates Signature preview based on given SignOptions. :py:class:`groupdocs.signature.options.SignOptions`
        
        :param preview_options: The preview signature with given SignOptions. :py:class:`groupdocs.signature.options.PreviewSignatureOptions`'''
        raise NotImplementedError()
    

class SignatureSettings:
    '''Defines settings for customizing :py:class:`groupdocs.signature.Signature` behavior.'''
    
    @property
    def show_deleted_signatures_info(self) -> bool:
        '''Gets flag that includes deleted signatures into Document Info result.
        Each Signature :py:class:`groupdocs.signature.domain.BaseSignature` has Deleted flag :py:attr:`groupdocs.signature.domain.BaseSignature.deleted` to detect if it was deleted.'''
        raise NotImplementedError()
    
    @show_deleted_signatures_info.setter
    def show_deleted_signatures_info(self, value : bool) -> None:
        '''Sets flag that includes deleted signatures into Document Info result.
        Each Signature :py:class:`groupdocs.signature.domain.BaseSignature` has Deleted flag :py:attr:`groupdocs.signature.domain.BaseSignature.deleted` to detect if it was deleted.'''
        raise NotImplementedError()
    
    @property
    def save_document_on_empty_update(self) -> bool:
        '''Gets flag to re-save source document when Update method has no signatures to update.
        If this flag is set to true (by default) document will be saving with corresponding history process log (date and operation type) even if Update method has no signatures to update.
        When this flat is set to false source document will not be modified at all.'''
        raise NotImplementedError()
    
    @save_document_on_empty_update.setter
    def save_document_on_empty_update(self, value : bool) -> None:
        '''Sets flag to re-save source document when Update method has no signatures to update.
        If this flag is set to true (by default) document will be saving with corresponding history process log (date and operation type) even if Update method has no signatures to update.
        When this flat is set to false source document will not be modified at all.'''
        raise NotImplementedError()
    
    @property
    def save_document_on_empty_delete(self) -> bool:
        '''Gets flag to re-save source document when Delete method has no affected signatures to remove.
        If this flag is set to true (by default) document will be saving with corresponding history process log (date and operation type) even if Delete method has no signatures to remove.
        When this flat is set to false source document will not be modified at all.'''
        raise NotImplementedError()
    
    @save_document_on_empty_delete.setter
    def save_document_on_empty_delete(self, value : bool) -> None:
        '''Sets flag to re-save source document when Delete method has no affected signatures to remove.
        If this flag is set to true (by default) document will be saving with corresponding history process log (date and operation type) even if Delete method has no signatures to remove.
        When this flat is set to false source document will not be modified at all.'''
        raise NotImplementedError()
    
    @property
    def include_standard_metadata_signatures(self) -> bool:
        '''Gets flag to include into the Metadata List the embedded standard document metadata signatures like Author, Owner, document creation date, modified date, etc.
        If this flag is set to false (by default) the GetDocumentInfo will not include these metadata signatures.
        When this flag is set to true the document information will include these standard metadata signatures.'''
        raise NotImplementedError()
    
    @include_standard_metadata_signatures.setter
    def include_standard_metadata_signatures(self, value : bool) -> None:
        '''Sets flag to include into the Metadata List the embedded standard document metadata signatures like Author, Owner, document creation date, modified date, etc.
        If this flag is set to false (by default) the GetDocumentInfo will not include these metadata signatures.
        When this flag is set to true the document information will include these standard metadata signatures.'''
        raise NotImplementedError()
    
    @property
    def logger(self) -> groupdocs.signature.logging.ILogger:
        '''The logger implementation used for logging (Errors, Warnings, Traces). :py:class:`groupdocs.signature.logging.ILogger`.'''
        raise NotImplementedError()
    
    @property
    def log_level(self) -> groupdocs.signature.logging.LogLevel:
        '''The level of the logging to limit the messages (All, Traces, Warnings, Errors). :py:attr:`groupdocs.signature.SignatureSettings.log_level`.
        BY default the All level type is set.'''
        raise NotImplementedError()
    
    @log_level.setter
    def log_level(self, value : groupdocs.signature.logging.LogLevel) -> None:
        '''The level of the logging to limit the messages (All, Traces, Warnings, Errors). :py:attr:`groupdocs.signature.SignatureSettings.log_level`.
        BY default the All level type is set.'''
        raise NotImplementedError()
    

