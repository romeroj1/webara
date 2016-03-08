from fabric.api import *
from fabric.colors import *
import datetime

@task
def startvm(name=None):
    '''Starts a virtual machine. need to pass the name of the VM'''
    if name == None:
        print('pls enter a valid virtual machine name to modify')
        return
    local('VBoxManage startvm "' + name + '" --type headless')

@task
def stopvm(name=None):
    '''Stops a vrtual Machine, need to pass the name of the VM'''
    if name == None:
        print('pls enter a valid virtual machine name to modify')
        return
    local('VBoxManage controlvm "' + name + '" poweroff')

@task
def restartvm(name=None):
    '''Restarts a vrtual Machine, need to pass the name of the VM'''
    if name == None:
        print('pls enter a valid virtual machine name')
        return
    local('VBoxManage controlvm "' + name + '" reset')
        
@task
def showvminfo(name=None):
    ''' Display information configuration about the VM '''
    local('VBoxManage showvminfo "' + name + '"')

@task
def status():
    ''' Shows status of all vms'''
    out = local('VBoxManage list vms -l | grep -e ^Name: -e ^State', capture=True) #'VBoxManage list runningvms', capture=True)
    return out

@task
def exportvm_ovf(name=None):
    now = datetime.datetime.now()
    strtoday = now.strftime('%Y%m%d%H%M')
    strfilename = 'sunnyx02_' + strtoday + '.ova'
    local('VBoxManage export "' + name + '" --output /apps/backups/vms/' + strfilename)
