#!/usr/bin/python
import os
import time
from pyinotify import WatchManager, Notifier, ProcessEvent,IN_DELETE,IN_CREATE,IN_MODIFY,IN_MOVED_TO

path=['/root/', '/bin/', '/etc/', '/lib/', 'boot', 'dev', 'lib64', 'sbin', 'srv', 'sys']
logfile='/var/log/inotify.log'

class EventHandler(ProcessEvent):
    def process_IN_CREATE(self, event):
        logstr= "\n%s create file: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),os.path.join(event.path,event.name))
        wlog(logfile, logstr)

    def process_IN_DELETE(self, event):
        logstr= "\n%s delete file: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),os.path.join(event.path,event.name))
        wlog(logfile, logstr)

    def process_IN_MODIFY(self, event):
        logstr= "\n%s modify file: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),os.path.join(event.path,event.name))
        wlog(logfile, logstr)

    def process_IN_MOVED_TO(self, event):
        logstr= "\n%s moved file: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),os.path.join(event.path,event.name))
        wlog(logfile, logstr)

def FSMonitor(path):
    wm = WatchManager()
    mask = IN_DELETE | IN_CREATE | IN_MODIFY | IN_MOVED_TO
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(path, mask, rec=True, auto_add=True)
    print 'now starting monitor %s ' % (path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break

def wlog(logfile, logstr):
    with open('%s' % (logfile), 'a') as f:
        f.write(logstr)

if __name__ == '__main__':
    FSMonitor(path)
