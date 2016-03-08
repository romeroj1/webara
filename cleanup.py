#! /usr/bin/python
 
''' 
Title:    cleanup.py
Author:   Johann Romero (johann.romero@gmail.com)
Date:     Mar052016
update:   
'''
 
import ConfigParser
import os
import tarfile
import logging
import logging.handlers
import datetime
import time

##########################
# Setup logging
##########################

logfile = '/apps/backups/logs/cleanup.log'
logsize = '2097152' 
numlogs = 5
strBkploc = '/apps/backups/vms/'
backup_retention = 30

# Log Level Info
# Level		Numeric value
# CRITICAL	50
# ERROR		40
# WARNING	30
# INFO		20
# DEBUG		10
# NOTSET	0
loglevel = 20

# Setup handler
handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=logsize, backupCount=numlogs)
handler.setLevel(loglevel)
# Logging Format
formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(formatter)
# create logger
my_logger = logging.getLogger(__name__)
my_logger.setLevel(loglevel)
# Add handler to logger
my_logger.addHandler(handler)

now = time.time()
cutoff = now - (backup_retention * 86400)


def cleanup_Backups(strBkploc):
    '''
    Deletes old backups
    '''
    # Do the job
    
    for dirname, dirnames, filenames in os.walk(strBkploc):
        for name in filenames:
            #Get file extension
            (base, ext)=os.path.splitext(name)
            bkpFile = os.path.join(dirname, name)
            stats = os.stat(bkpFile)  
            lastmodDate = stats.st_mtime
            #modDate = time.localtime(stats[8])
            #lastmodDate = time.strftime("%m-%d-%Y", modDate)
            #expDate = returnRetentionperiod(backup_retention)
            my_logger.debug('function="cleanup_Backups" file="{0}" backup_retention="{1} days" lastmodDate="{2}" expiration_date="{3}" loglevel="{4}"'.format(bkpFile,backup_retention,lastmodDate,cutoff,loglevel_mapping_tostring(loglevel))) 
            if  lastmodDate < cutoff:
                delete_Oldbackups(bkpFile)                                        
    
    my_logger.info('function="cleanup_Backups" message="Completed Cleaning up old Backups" loglevel="{0}"'.format(loglevel_mapping_tostring(loglevel)))

def delete_Oldbackups(strPath):
    '''
    It executes the actual deletion
    '''
    try:
        if  os.path.exists(strPath):
            #uncomment after test
            os.remove(strPath)
            my_logger.info('function="delete_Oldbackups" action="deleting" path="{0}" loglevel={1}'.format(loglevel_mapping_tostring(loglevel))) 
    except OSError:
        my_logger.error('exception="Error deleting file" file="{0}" loglevel="{1}"'.format(strPath,loglevel_mapping_tostring(loglevel)))
        
def returnRetentionperiod(bkpretention):
    '''
    Substract the delta from current date and returns it
    '''
    today = datetime.date.today()
    DD = datetime.timedelta(days=bkpretention)
    olderthandate = today - DD
    #padded the day to be a two digit int so that it would match the day digits on file modtime
    day = '%02d' % olderthandate.day
    month = '%02d' % olderthandate.month
    year = olderthandate.year
    
    #filterDate = str(year) + '-' + str(month) + '-' + str(day)
    filterDate = str(month) + '-' + str(day) + '-' + str(year)
    return  filterDate

def showAffecteditems(strName):
    '''
    Just list files or folders that will be affected
    '''              
    my_logger.debug('Working on: %s' % strName)
    my_logger.debug('The following files or folders will be affected:')
    my_logger.debug(strName)

def loglevel_mapping_tostring(loglevelint):
    ''' Returns the loglevel as a string'''
    switcher = {
        50:  "CRITICAL",
        40:  "ERROR",
        30:  "WARNING", 
        20:  "INFO", 
        10:  "DEBUG",   
        0:   "NOTSET",  
    }
    return switcher.get(loglevelint, "nothing")

def main():
    '''
    Main Module
    '''

    my_logger.info('function="main" message="Start Clean Up of Old Backups" loglevel="{0}"'.format(loglevel_mapping_tostring(loglevel)))

    cleanup_Backups(strBkploc)


if __name__ == '__main__':
    main()
