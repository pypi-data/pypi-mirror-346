# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 11:54:32 2022

This is helper function for printing to console and logging

@author: user
"""
import os,sys
from datetime import datetime
import uuid
import random
import hashlib
import inspect

FORCE_LOG_SUFFIX = False
LOG_SUFFIX = None
ENABLE_LOG = True
LOG_DIR = None
FLUSH_PRINT = False

def set_log_suffix(log_suffix:str):
    """
    Set logging suffix  
    log format : [datetime]_[log_suffix].txt  
    Default format of log_suffix is random generated uuid for the program
    that called the print_debug function. Once it existed, same uuid will be 
    used everytime the program is called/run.

    Parameters
    ----------    
    log_suffix : str  
        Any string text, suppose to identify the program that calls the
        print_debug function and save logs.
    
    Returns
    -------
    None.

    """
    global LOG_SUFFIX
    LOG_SUFFIX = log_suffix
    _set_force_log_suffix()
    
def _set_force_log_suffix(force=True):
    global FORCE_LOG_SUFFIX 
    FORCE_LOG_SUFFIX = force
    
def set_print_flush_mode(flush=True):
    global FLUSH_PRINT
    FLUSH_PRINT = flush

def set_log_dir(log_dir:str):
    """
    Set directory to store logs  
    Default is store at 'logs' folder where the program is called (not the
    script called directory)

    Parameters
    ----------    
    log_dir : str  
        Directory string.
    
    Returns
    -------
    None.

    """
    global LOG_DIR
    LOG_DIR = log_dir
    
def enable_log():
    """
    Enable log saving. Different form log printing in console. This save
    log to file.  
    Default printing is True.

    Returns
    -------
    None.

    """
    global ENABLE_LOG
    ENABLE_LOG = True

def disable_log():
    """
    Disable log saving.

    Returns
    -------
    None.

    """
    global ENABLE_LOG
    ENABLE_LOG = False
        
def _call_source():
    result = inspect.getouterframes(inspect.currentframe(), 2)
    return str(result[0][1])     

def _string_to_seed(seed_string):
    return int(hashlib.sha256(seed_string.encode()).hexdigest(), 16)

def _generate_uuid4(seed_string):
    seed = _string_to_seed(seed_string)
    random.seed(seed)

    random_bytes = random.getrandbits(128).to_bytes(16, 'big')
    # Set the UUID version to 4 (UUID4)
    random_bytes = (random_bytes[:6] + bytes([random_bytes[6] & 0x0f | 0x40]) + random_bytes[7:])
    key = uuid.UUID(bytes=random_bytes) 
    
    random.seed(None)  
    return key

    # reset random seed
           
def _get_logging_info():
    if LOG_DIR is not None:
        logdir = os.path.join(LOG_DIR,'logs')
    else:
        logdir = os.path.join(os.getcwd(),'logs')
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except Exception as e:
            print(e)
        
    seedstring = _call_source()
    suffix_uuid = _generate_uuid4(seedstring.lower())

    return logdir,suffix_uuid  
        
def save_log(logdir:str,log_suffix:str,text:str):
    """
    Save single line of log to log file at [datetime]_[log_suffix].txt  

    Parameters
    ----------    
    logdir : str  
        Directory to store log.  
    log_suffix : str  
        Suffix set for log.  
    text : str  
        Log line to save. 
    
    Returns
    -------
    None.

    """
    dt = f"{datetime.now().strftime('%Y%m%d')}"  
    savename = f"{dt}_{log_suffix}.txt"
    
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except Exception as e:
            print(e)
            
    savepath = os.path.join(logdir,savename)
    if not os.path.exists(savepath):
        with open(savepath,'w') as fid:
            fid.write(f"Created time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    with open(savepath,'a') as fid:
        fid.write('%s\n'%text)
    
def print_debug(*arg,**kwargs):
    """
    Main print function to replace native print in Python.  
    If enable_log is active, this will also save log to file.  
    arg is basically anything print does and support. 
    
    Supported kwargs:  
        'force_print' : bool  
            In the event of print option is disable, force_print overwrite
            the condition.  
        'disable_timepath' : bool  
            Supress prefix for time and date printing  
        'disable_log' : bool  
            Disable log printing to file, supersede global setting  
        'log_suffix' : str or None  
            Write log with own suffix, supersede global setting  
    
    Parameters
    ----------    
    *arg : print_statement  
        Print content.  
    **kwargs : keyword value pair  
        Optional/additional argument.
    
    Raises
    ------    
    KeyError
        Unknown error in getting calling source meta.
    
    Returns
    -------
    None.

    """
    try:
        text = ' '.join(arg)
    except:
        text = arg
    
    force_print = kwargs.get('force_print',False)
    disable_timepath = kwargs.get('disable_timepath',False)
    disable_log = kwargs.get('disable_log',False)
    log_suffix = kwargs.get('log_suffix',None)
    
    logdir,suffix_uuid = _get_logging_info()
    if log_suffix is None:
        log_suffix = suffix_uuid
    
    if FORCE_LOG_SUFFIX:
        if LOG_SUFFIX is not None:
            log_suffix = LOG_SUFFIX
            
    if ENABLE_LOG:
        enable_log_system = True
    else:
        enable_log_system = False
        
    # if (os.environ.get("NEUON_DEBUG") == '1') or force_print:
    if disable_timepath:
        text_to_print = text
        
        # [print(text)]
    else:
        try:
            text_to_print = '[%s][%s] %s [%s]'%(
                datetime.now().strftime('%y%m%d%H%M%S'),
                os.path.basename(''.join((sys._getframe().f_back.f_globals['__file__']).split('.')[0:-1])),
                text,
                sys._getframe().f_back.f_code.co_name
                )
            # print('[%s][%s] %s [%s]'%(
            #     datetime.now().strftime('%y%m%d%H%M%S'),
            #     os.path.basename(''.join((sys._getframe().f_back.f_globals['__file__']).split('.')[0:-1])),
            #     text,
            #     sys._getframe().f_back.f_code.co_name
            #     ))
        except KeyError as e:
            if e.args[0] == '__file__':
                text_to_print = '[%s] %s [%s]'%(
                    datetime.now().strftime('%y%m%d%H%M%S'),
                    text,
                    sys._getframe().f_back.f_code.co_name
                    )
                
                # print('[%s] %s [%s]'%(
                #     datetime.now().strftime('%y%m%d%H%M%S'),
                #     text,
                #     sys._getframe().f_back.f_code.co_name
                #     ))   

            else:
                raise KeyError(str(e))  
                    
    if (not disable_log) and enable_log_system:
        save_log(logdir,log_suffix,text_to_print)
        
    if (os.environ.get("NEUON_DEBUG") == '1') or force_print: 
        print(text_to_print,flush=FLUSH_PRINT)
            
            
def enable_debug_print():
    """
    Enable console printing  
    Default is not enabled.

    Returns
    -------
    None.

    """
    os.environ["NEUON_DEBUG"] = '1'
    
def disable_debug_print():
    """
    Disable console printing

    Returns
    -------
    None.

    """
    os.environ["NEUON_DEBUG"] = ''
    
if __name__ == '__main__': 
    print_debug("Test print")
    
