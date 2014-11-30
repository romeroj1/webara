from fabric.api import *
from fabric.colors import *
import datetime


@task
def getdate():
    '''Returns date'''
    today = datetime.datetime.strftime(datetime.datetime.now(), '%m%d%Y%H%M%S%f')
    return today

@task 
def getSMBStatus():
    ''' Returns the Samba Status, includes shares and PIDs'''
    out = sudo('smbstatus')
    return out

@task
def getSMBServiceStatus():
    ''' Returns the Samba Service Status'''
    out = sudo('service smb status')
    return out

@task
def stopSamba():
    ''' Stops the Samba Service '''
    sudo('service smb stop')

@task
def startSamba():
    ''' Starts the Samba Service'''
    sudo('service smb start')
