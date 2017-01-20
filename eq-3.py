#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect # install with: pip install pexpect
import sys

bluetooth_adr = sys.argv[1]
#bluetooth_adr = '00:1A:22:07:70:DA'
gatt_handle = sys.argv[2]
gatt_value = sys.argv[3]

# start and connect gatttool
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
tool.sendline('connect')
tool.expect('Connection successful')
# write to the handle
tool.sendline('char-write-req ' + gatt_handle + ' ' + gatt_value)
# get back notifications
tool.expect('Notification handle = .*')
# make some nicer output
handle = tool.after.split('\n')[0].split(': ')[0].split()[3]
values = tool.after.split('\n')[0].split(': ')[1]
print handle + ': ' + values
print '   dec:',
for value in values.split():
    print str(int(value, 16)),
print ''
print '-----------------------'

# play with the values
mode = values.split()[2]
vent = int(values.split()[3], 16)
temp = int(values.split()[5], 16) / 2.0
modestr = 'Unbekannt'
if mode == '08':
    modestr = 'Automatik'
if mode == '09':
    modestr = 'Manuell'
if mode == '0a':
    modestr = 'Urlaub'
if mode == '0c':
    modestr = 'Boost'
if mode == '18':
    modestr = 'Fenster auf'
if mode == '28':
    modestr = 'Locked'
print ' Modus: ' + modestr
if not modestr == 'Unbekannt':
    print 'Ventil: ' + str(vent) + '%'
    print ' Temp.: ' + str(temp) + '°C'

# disconnect gatttool
tool.sendline('disconnect')
tool.sendline('quit')
