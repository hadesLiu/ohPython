# -*- coding: utf-8 -*-
# author: hiro
#import configparser
import ConfigParser
import os
import subprocess

from kill_process_by_name import kill_process_by_name

curDir = '/tmp/ohPython/supervisor'

def install_supervisor():
    # kill old salt-minion
    kill_process_by_name('salt-minion')

    # install supervisor
    # subprocess.Popen('/application/python/bin/easy_install supervisor',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    values = os.popen('/application/python/bin/easy_install supervisor')
    print(values.readlines())

    # generate supervisord.conf
    with open('/etc/supervisord.conf', 'w') as sv:
        with open('%s/supervisord.conf' % curDir, 'r') as sv1:
            for line in sv1:
                sv.write(line)

    # make supervisord.conf.d
    #subprocess.Popen('mkdir /etc/supervisord.conf.d',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.popen('mkdir /etc/supervisord.conf.d')

def config_supervisor_salt(configFilePath):
    # create salt-minion.ini
    # with open('/etc/supervisord.conf.d/salt-minion.ini', 'w') as sm:
    with open('%s/salt-minion.ini' % configFilePath, 'w') as sm:

        with open('%s/salt-minion.ini' % curDir, 'r') as sm1:
            for line in sm1:
                sm.write(line)

def onboot_supervisor():
    # create /etc/init.d/supervisord
    with open('/etc/init.d/supervisord', 'w') as sm:
        with open('%s/supervisord' % curDir, 'r') as sm1:
            for line in sm1:
                sm.write(line)

    # onboot and start supervisord
    values1 = subprocess.Popen('chmod +x /etc/init.d/supervisord',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(values1.stderr.readline())
    values2 = subprocess.Popen('chkconfig --add supervisord',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(values2.stderr.readline())
    values3 = subprocess.Popen('chkconfig supervisord off',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(values3.stderr.readline())
    values4 = subprocess.Popen('chkconfig supervisord on',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(values4.stderr.readline())
    values5 = subprocess.Popen('/etc/init.d/supervisord start',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(values5.stderr.readline())

def check_supervisord_yum():
    # values = subprocess.Popen('ps -ef |grep "/usr/bin/python /usr/bin/supervisord" |grep -v grep',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    values = os.popen('ps -ef |grep "/usr/bin/python /usr/bin/supervisord" |grep -v "grep" ')
    values = values.readlines()
    if len(values) and 'supervisord' in values[0]:
        values = subprocess.Popen('sudo /etc/init.d/supervisord stop',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(values.stdout.readline())
        print(values.stderr.readline())
        print("supervisord is stopped.")

def parse_supervisor_config_file():
    #cf = configparser.ConfigParser()
    cf = ConfigParser.ConfigParser()
    cf.read('/etc/supervisord.conf')

    configFilePath = cf.get('include', 'files')
    configFilePath = os.path.dirname(configFilePath)
    # if configFilePath == '/etc/supervisord.conf.d/*.ini':
    if configFilePath is not None:
        config_supervisor_salt(configFilePath)
        values6 = subprocess.Popen('/application/python/bin/supervisorctl reread',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(values6.stderr.readline())
        values7 = subprocess.Popen('/application/python/bin/supervisorctl update',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(values7.stderr.readline())
    else:
        print('supervisor config path is none.')


if __name__ == "__main__":
    if os.path.isfile('/etc/init.d/supervisord'):
        check_supervisord_yum()
    elif os.path.isfile('/etc/supervisord.conf'):
        kill_process_by_name('salt-minion')
        parse_supervisor_config_file()

        values_super = os.popen('ps -ef |grep "/application/python/bin/python /application/python/bin/supervisord -c /etc/supervisord.conf" |grep -v "grep" ')
        values_super = values_super.readlines()
        if len(values_super):
            kill_process_by_name('supervisord')

        onboot_supervisor()
    else:
        install_supervisor()
        config_supervisor_salt('/etc/supervisord.conf.d')
        onboot_supervisor()

