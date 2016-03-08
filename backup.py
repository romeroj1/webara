from fabric.api import *
from fabric.colors import *
import datetime
import common
import sendemail
import vboxmgmt
import os

@task
def avimark():
    ''' Runs the compres avimark and gets the gz from remote server and puts it locally'''
    compress_avimark()
    cleanup_oldbackups()

@task
def compress_avimark():
    ''' Backs up Avimark Share, excluding *.zip files'''
    out = common.getSMBStatus() #sudo('smbstatus')
    if 'No locked files' in out:
        do_avimarkTar()
    else:
        sendemail.sendmail('Avimark Backup could not be started', 'Possible reasons are: There are open files or could not connect to Sunnyx02 \n ' + out + ' \n Will try to Stop Samba to Start backup')
        smbstatus = common.getSMBServiceStatus()
        if 'running' in smbstatus:
            #print red('Testing ...')
            common.stopSamba()
            #common.getSMBStatus()
            do_avimarkTar()
            common.startSamba()

def do_avimarkTar():
    ''' Performs the actual TAR of the avimark folder. Can't call as a single task. Must be call from within file'''
    bkpfolder = '/apps/backups/'
    bkpname = 'avimark_fullbackup_' + common.getdate() + '.tgz'
    with cd('/apps/shares'):
        sudo("tar cvfz " + bkpfolder + bkpname + " avimark/ --exclude=avimark/*.zip --exclude=avimark/Backup")
        get_avimarkTar()

@task
def get_avimarkTar():
    '''Gets the compress avimark backup files'''
    get('/apps/backups/*.tgz', '/apps/backups/avimark/', use_sudo=True)
    get('/apps/backups/*.tgz', '/removableUsb/portablebackups/', use_sudo=True)
    out = local('ls -lah /apps/backups/avimark/', capture=True)
    smbstatus = common.getSMBStatus()
    smbservicestatus = common.getSMBServiceStatus()
    sendemail.sendmail('Avimark Backup', 'Avimark has been completed, please verify at your earliest convenience \n ' + out + '\n Samba Service Status: ' + smbservicestatus + '\n Samba Shares Satus: ' + smbstatus)
    with cd('/apps/backups/'):
        sudo('rm *.tgz')

@task
def cleanup_oldbackups():
   ''' Deletes backup files older than 5 days'''
   local('find /apps/backups/avimark/*.tgz -mtime +10 -delete')

@task
def backup_vm(All=True):
    ''' Backs up virtual machines. Could be one or all. Defaults to True meaning All VMs will be back up '''
    #status = vboxmgmt.status()
    #Still need to work on the boolean check for single or all vms
    vms = '/apps/vms'
    vmstatus = vboxmgmt.status()
    for d in os.listdir(vms):
       if d in vmstatus and 'running' in vmstatus:
           print red('VM with Name=' + d + ' is still running... Will try to perform action=poweroff now') 
           vboxmgmt.stopvm(d)
           vboxmgmt.exportvm_ovf(d)
           copy_tar_vm(d)
       else:
           print green('VM with Name=' + d + ' seems to be poweroff, starting VM backup now...')
           vboxmgmt.stopvm(d)
           vboxmgmt.exportvm_ovf(d)
           copy_tar_vm(d)

@task
def copy_tar_vm(svrname=None):
    ''' Performs the actual tar of the VM folder and copies file to backup folder. Can't call directly. Must be call from a defined task'''
    
    sendemail.sendmail('function="Sunnyx02 Backup"', 'message="Starting Sunnyx02 backup now"')

    with lcd('/apps/vms'):
        vboxmgmt.startvm(svrname)
        vmstatus = vboxmgmt.status()
        sendemail.sendmail('Sunny Hills VMs Backup', 'Completed Backup for Sunny Hills VMs. Find VMs status below: \n' + vmstatus)

    strdest= '/removableUsb/vms/'
    strsrc= '/apps/backups/vms/'

    with lcd(strdest):
        local('[[ -d /removableUsb/vms/"$(date +"%m%d%Y")" ]] || mkdir "$(date +"%m%d%Y")"')
        local('find /apps/backups/vms/ -mtime -1 -exec cp {} /removableUsb/vms/"$(date +"%m%d%Y")" \;')
        
