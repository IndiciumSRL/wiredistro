from contextlib import closing
from subprocess import call
import datetime
import tarfile
import os
import socket

def make_tarfile(output_filename, source_dir):
	with closing(tarfile.open(output_filename, "w:gz")) as tar:
		tar.add(source_dir)

host = socket.gethostname()
Server1 = Wolverine
Server2 = Superbowl

bkpath = '/root/backups/files/'
fecha = datetime.datetime.now().strftime("%Y-%m-%d")
dbfile = bkpath + 'freeswitch-db-'+ fecha +'.tar.gz'
conffile = bkpath + 'freeswitch-conf-'+ fecha +'.tar.gz'
psdaily = bkpath + fecha + '-daily'
psweekly = bkpath + fecha + '-weekly'

make_tarfile(dbfile, "/var/lib/freeswitch/db/")
make_tarfile(conffile, "/etc/freeswitch/")
if os.path.isfile(psweekly):
	call(["rsync", "-aze", "ssh", dbfile, conffile, psdaily, psweekly, Server1 +":~/backups-clientes/"+ host +"/"])
	call(["rsync", "-aze", "ssh", dbfile, conffile, psdaily, psweekly, Server2 +":~/backups-clientes/"+ host +"/"])
else:
	call(["rsync", "-aze", "ssh", dbfile, conffile, psdaily, Server1 +":~/backups-clientes/"+ host +"/"])
	call(["rsync", "-aze", "ssh", dbfile, conffile, psdaily, Server2 +":~/backups-clientes/"+ host +"/"])

call(["rsync", "-aze", "ssh", "/var/lib/wirephone/provisioning/", Server1 +":~/backups-clientes/"+ host +"/provision-files/var/"])
call(["rsync", "-aze", "ssh", "/var/lib/wirephone/provisioning/", Server2 +":~/backups-clientes/"+ host +"/provision-files/var/"])
call(["rsync", "-aze", "ssh", "/etc/wirephone/provisioning/", Server1 +":~/backups-clientes/"+ host +"/provision-files/etc/"])
call(["rsync", "-aze", "ssh", "/etc/wirephone/provisioning/", Server2 +":~/backups-clientes/"+ host +"/provision-files/etc/"])

