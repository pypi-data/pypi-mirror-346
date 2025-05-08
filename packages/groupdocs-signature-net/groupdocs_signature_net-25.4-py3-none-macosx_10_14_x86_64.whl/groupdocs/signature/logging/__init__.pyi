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

class ConsoleLogger(ILogger):
    '''Writes log messages to the file.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace message to the console.
        Trace log messages provide generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning message to the console;
        Warning log messages provide information about the unexpected and recoverable event in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    

class FileLogger(ILogger):
    '''Writes log messages to the file.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace message to the console.
        Trace log messages provide generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning message to the console;
        Warning log messages provide information about the unexpected and recoverable event in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    

class ILogger:
    '''Defines the methods that are used to perform logging.'''
    
    def trace(self, message : str) -> None:
        '''Writes a trace message. Trace log messages provide generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message; Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    

class LogLevel:
    '''Specifies the available Log Level types.
    This enumeration can be used as flags to set several possible values as enabled bits
    Example: LogLevel.Error | LogLevel.Warning or LogLevel.Error | LogLevel.Trace'''
    
    NONE : LogLevel
    '''No logging limitation all information will be logged from trace, warning to errors'''
    ERROR : LogLevel
    '''No logging limitation all information will be logged from trace, warning to errors'''
    WARNING : LogLevel
    '''Same as All level, all messages including the Trace level will be logged'''
    TRACE : LogLevel
    '''The logging level to include messages from the Warning to Error level'''
    ALL : LogLevel
    '''All Log level events (Error, Warning, Trace) will be included into the logging'''

