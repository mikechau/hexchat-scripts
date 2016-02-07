__module_name__ = 'Cinnamon Auto-Away (CinnAway)'
__module_version__ = '0.1'
__module_description__ = 'Checks if your cinnamon-screensaver is running and then sets your irc status to away'
__author__ = 'mikechau'

full_name = '{} v{} by {}'.format(__module_name__, __module_version__, __author__)

import hexchat
import subprocess

hook = None
away_cmd = 'away I am away right meow.'
back_cmd = 'back'
help_msg = \
    """\n"/cinnaway start"      start cinnaway.
"/cinnaway stop"       stop cinnaway.\n"""

def start_timer():
  global hook
  hook = hexchat.hook_timer(600000, auto_away_cb)

def end_timer():
  global hook
  hook = None

def set_timer(action):
  if action == 'stop':
    end_timer()
  elif action == 'start':
    start_timer()

def print_status(action=None):
  if action == 'stop':
    print('CinnAway has stopped.')
  elif action == 'start':
    print('CinnAway has started.')
  else:
    if hook == None:
      print('CinnAway is not running.')
    else:
      print('CinnAway is running.')

def cinnaway_cb(word, word_eol, userdata):
  global hook

  if len(word) > 2:
    action = word[1]
    set_timer(action)
    print_status(action)
  else:
    print_status()

  return hexchat.EAT_ALL

def auto_away_cb(userdata):
  stdout, stderr = (
    subprocess
    .Popen("/bin/bash -lc 'cinnamon-screensaver-command -q'", shell=True, stdout=subprocess.PIPE)
    .communicate()
  )

  if 'inactive' in stdout:
    exec_cmd('back')
  else:
    exec_cmd('away')

  return 1

def exec_cmd(cmd):
  global away_cmd
  global back_cmd

  channels = hexchat.get_list('channels')
  for channel in channels:
    if channel.type == 1: # channel for a server
      status = channel.context.get_info('away')

      if cmd == 'away' and status == None:
        channel.context.command(away_cmd)
      elif cmd == 'back' and status != None:
        channel.context.command(back_cmd)

start_timer()

hexchat.hook_command('cinnaway', cinnaway_cb, help=help_msg)

print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
