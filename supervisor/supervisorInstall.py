# -*- coding: utf-8 -*-
# author: hiro
import configparser
import os
import subprocess

from kill_process_by_name import kill_process_by_name

def install_supervisor():
    # kill old salt-minion
    kill_process_by_name('salt-minion')

    # install supervisor
    subprocess.Popen('/application/python/bin/easy_install supervisor',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    # generate supervisord.conf
    with open('/etc/supervisord.conf', 'w') as sv:
        with open('supervisord.conf', 'r') as sv1:
            for line in sv1:
                sv.write(line)

    # make supervisord.conf.d
    subprocess.Popen('mkdir /etc/supervisord.conf.d',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def config_supervisor_salt(configFilePath):
    # create salt-minion.ini
    # with open('/etc/supervisord.conf.d/salt-minion.ini', 'w') as sm:
    with open('%s/salt-minion.ini' % configFilePath, 'w') as sm:

        with open('salt-minion.ini', 'r') as sm1:
            for line in sm1:
                sm1.write(line)

def onboot_supervisor():
    # create /etc/init.d/supervisord
    with open('/etc/init.d/supervisord', 'w') as sm:
        with open('supervisord', 'r') as sm1:
            for line in sm1:
                sm1.write(line)

    # onboot and start supervisord
    subprocess.Popen('chmod +x /etc/init.d/supervisord',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    subprocess.Popen('chkconfig --add supervisord',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    subprocess.Popen('chkconfig supervisord off',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    subprocess.Popen('chkconfig supervisord on',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    subprocess.Popen('/etc/init.d/supervisord start',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def check_supervisord_yum():
    # values = subprocess.Popen('ps -ef |grep "/usr/bin/python /usr/bin/supervisord" |grep -v grep',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    values = os.popen('ps -ef |grep "/usr/bin/python /usr/bin/supervisord" |grep -v "grep" ')
    values = values.readlines()
    if len(values) and 'supervisord' in values[1]:
        subprocess.Popen('/etc/init.d/supervisord stop',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print("supervisord is stopped.")

def parse_supervisor_config_file():
    cf = configparser.ConfigParser()
    cf.read('/etc/supervisord.conf')

    configFilePath= cf.get('include', 'files')
    # if configFilePath == '/etc/supervisord.conf.d/*.ini':
    if configFilePath is not None:
        config_supervisor_salt(configFilePath)
        subprocess.Popen('/application/python/bin/supervisorctl reread',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subprocess.Popen('/application/python/bin/supervisorctl update',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        print('supervisor config path is none.')


if __name__ == "__main__":
    if os.path.isfile('/etc/init.d/supervisord'):
        check_supervisord_yum()
    elif os.path.isfile('/etc/supervisord.conf'):
        parse_supervisor_config_file()
    else:
        install_supervisor()
        config_supervisor_salt('/etc/supervisord.conf.d')
        onboot_supervisor()
