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

class DigitalSignatureAppearance(SignatureAppearance):
    '''Describes appearance of Signature Line for Digital Signature.
    One Signature Line could be applied for only one Digital Signature.
    Signature Line always is on the first page.
    This feature may be useful for .docx, .doc, .odt and .xlsx file formats.'''
    
    @property
    def signer(self) -> str:
        '''Gets signer name for signature line.'''
        raise NotImplementedError()
    
    @signer.setter
    def signer(self, value : str) -> None:
        '''Sets signer name for signature line.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets a title for signature line.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets a title for signature line.'''
        raise NotImplementedError()
    
    @property
    def email(self) -> str:
        '''Gets a email that will be displayed in signature line.'''
        raise NotImplementedError()
    
    @email.setter
    def email(self, value : str) -> None:
        '''Sets a email that will be displayed in signature line.'''
        raise NotImplementedError()
    

class ImageAppearance(SignatureAppearance):
    '''Describes extended appearance features for Image Signature.'''
    
    @property
    def grayscale(self) -> bool:
        '''Setup this flag to true if gray-scale filter is required.'''
        raise NotImplementedError()
    
    @grayscale.setter
    def grayscale(self, value : bool) -> None:
        '''Setup this flag to true if gray-scale filter is required.'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> float:
        '''Gets image brightness.
        Default value is 1 it corresponds to original brightness of image.'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : float) -> None:
        '''Sets image brightness.
        Default value is 1 it corresponds to original brightness of image.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> float:
        '''Gets image contrast.
        Default value is 1 it corresponds to original contrast of image.'''
        raise NotImplementedError()
    
    @contrast.setter
    def contrast(self, value : float) -> None:
        '''Sets image contrast.
        Default value is 1 it corresponds to original contrast of image.'''
        raise NotImplementedError()
    
    @property
    def gamma_correction(self) -> float:
        '''Gets image gamma.
        Default value is 1 it corresponds to original gamma of image.'''
        raise NotImplementedError()
    
    @gamma_correction.setter
    def gamma_correction(self, value : float) -> None:
        '''Sets image gamma.
        Default value is 1 it corresponds to original gamma of image.'''
        raise NotImplementedError()
    

class PdfDigitalSignatureAppearance(SignatureAppearance):
    '''Describes appearance of Digital Signature are on PDF documents.'''
    
    @property
    def contact_info_label(self) -> str:
        '''Gets contact info label. Default value: "Contact".
        if this value is empty then no contact label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @contact_info_label.setter
    def contact_info_label(self, value : str) -> None:
        '''Sets contact info label. Default value: "Contact".
        if this value is empty then no contact label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @property
    def reason_label(self) -> str:
        '''Gets reason label. Default value: "Reason".
        if this value is empty then no reason label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @reason_label.setter
    def reason_label(self, value : str) -> None:
        '''Sets reason label. Default value: "Reason".
        if this value is empty then no reason label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @property
    def location_label(self) -> str:
        '''Gets location label. Default value: "Location".
        if this value is empty then no location label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @location_label.setter
    def location_label(self, value : str) -> None:
        '''Sets location label. Default value: "Location".
        if this value is empty then no location label will appear on digital signature area.'''
        raise NotImplementedError()
    
    @property
    def digital_signed_label(self) -> str:
        '''Gets digital signed label. Default value: "Digitally signed by".'''
        raise NotImplementedError()
    
    @digital_signed_label.setter
    def digital_signed_label(self, value : str) -> None:
        '''Sets digital signed label. Default value: "Digitally signed by".'''
        raise NotImplementedError()
    
    @property
    def date_signed_at_label(self) -> str:
        '''Gets date signed label. Default value: "Date".'''
        raise NotImplementedError()
    
    @date_signed_at_label.setter
    def date_signed_at_label(self, value : str) -> None:
        '''Sets date signed label. Default value: "Date".'''
        raise NotImplementedError()
    
    @property
    def background(self) -> aspose.pydrawing.Color:
        '''Get or set background color of signature appearance.
        By default the value is SystemColors.Windows'''
        raise NotImplementedError()
    
    @background.setter
    def background(self, value : aspose.pydrawing.Color) -> None:
        '''Get or set background color of signature appearance.
        By default the value is SystemColors.Windows'''
        raise NotImplementedError()
    
    @property
    def font_family_name(self) -> str:
        '''Gets the Font family name to display the labels. Default value is "Arial".'''
        raise NotImplementedError()
    
    @font_family_name.setter
    def font_family_name(self, value : str) -> None:
        '''Sets the Font family name to display the labels. Default value is "Arial".'''
        raise NotImplementedError()
    
    @property
    def font_size(self) -> float:
        '''Gets the Font size to display the labels. Default value is 10.'''
        raise NotImplementedError()
    
    @font_size.setter
    def font_size(self, value : float) -> None:
        '''Sets the Font size to display the labels. Default value is 10.'''
        raise NotImplementedError()
    
    @property
    def foreground(self) -> aspose.pydrawing.Color:
        '''Get or set foreground text color of signature appearance.
        By default the value is Color.FromArgb(76, 100, 255)'''
        raise NotImplementedError()
    
    @foreground.setter
    def foreground(self, value : aspose.pydrawing.Color) -> None:
        '''Get or set foreground text color of signature appearance.
        By default the value is Color.FromArgb(76, 100, 255)'''
        raise NotImplementedError()
    

class PdfTextAnnotationAppearance(SignatureAppearance):
    '''Describes appearance of PDF text annotation object (Title, Subject, Content).'''
    
    @property
    def contents(self) -> str:
        '''Gets content of annotation object.'''
        raise NotImplementedError()
    
    @contents.setter
    def contents(self, value : str) -> None:
        '''Sets content of annotation object.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets Subject representing description of the object.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets Subject representing description of the object.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets a Title that will be displayed in title bar of annotation object.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets a Title that will be displayed in title bar of annotation object.'''
        raise NotImplementedError()
    
    @property
    def border(self) -> groupdocs.signature.domain.Border:
        '''Gets different border settings'''
        raise NotImplementedError()
    
    @border.setter
    def border(self, value : groupdocs.signature.domain.Border) -> None:
        '''Sets different border settings'''
        raise NotImplementedError()
    
    @property
    def border_effect(self) -> groupdocs.signature.domain.PdfTextAnnotationBorderEffect:
        '''Gets border effect.'''
        raise NotImplementedError()
    
    @border_effect.setter
    def border_effect(self, value : groupdocs.signature.domain.PdfTextAnnotationBorderEffect) -> None:
        '''Sets border effect.'''
        raise NotImplementedError()
    
    @property
    def border_effect_intensity(self) -> int:
        '''Gets border effect intensity. Valid range of value is [0..2].'''
        raise NotImplementedError()
    
    @border_effect_intensity.setter
    def border_effect_intensity(self, value : int) -> None:
        '''Sets border effect intensity. Valid range of value is [0..2].'''
        raise NotImplementedError()
    
    @property
    def h_corner_radius(self) -> int:
        '''Gets horizontal corner radius.'''
        raise NotImplementedError()
    
    @h_corner_radius.setter
    def h_corner_radius(self, value : int) -> None:
        '''Sets horizontal corner radius.'''
        raise NotImplementedError()
    
    @property
    def v_corner_radius(self) -> int:
        '''Gets vertical corner radius.'''
        raise NotImplementedError()
    
    @v_corner_radius.setter
    def v_corner_radius(self, value : int) -> None:
        '''Sets vertical corner radius.'''
        raise NotImplementedError()
    

class PdfTextStickerAppearance(SignatureAppearance):
    '''Describes appearance of PDF text annotation sticker object and pop-up window of sticker.'''
    
    @staticmethod
    def reset_default_appearance() -> None:
        '''Clears values of default appearance for sticker.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets title of pop-up window.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets title of pop-up window.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets subject.'''
        raise NotImplementedError()
    
    @property
    def contents(self) -> str:
        '''Gets the contents of pop-up window.'''
        raise NotImplementedError()
    
    @contents.setter
    def contents(self, value : str) -> None:
        '''Sets the contents of pop-up window.'''
        raise NotImplementedError()
    
    @property
    def opened(self) -> bool:
        '''Setup if sticker pop-up window will be opened by default.'''
        raise NotImplementedError()
    
    @opened.setter
    def opened(self, value : bool) -> None:
        '''Setup if sticker pop-up window will be opened by default.'''
        raise NotImplementedError()
    
    @property
    def icon(self) -> groupdocs.signature.domain.PdfTextStickerIcon:
        '''Gets the icon of sticker.'''
        raise NotImplementedError()
    
    @icon.setter
    def icon(self, value : groupdocs.signature.domain.PdfTextStickerIcon) -> None:
        '''Sets the icon of sticker.'''
        raise NotImplementedError()
    
    default_appearance : groupdocs.signature.options.appearances.PdfTextStickerAppearance
    '''Gets default appearance for sticker. These properties are applied as default if
    Options.SignatureAppearance property is not specified.
    The properties could be changed by user any time.'''

class SignatureAppearance:
    '''Represents the signature appearance - additional options for alternative implementations of sign on document page.'''
    

