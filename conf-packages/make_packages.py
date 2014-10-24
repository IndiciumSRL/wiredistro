#!/usr/bin/env python 

import subprocess
import os 

def list_my_dirs():
    for d in os.listdir(os.path.abspath(os.path.split(__file__)[0])):
        if not os.path.isdir(d):
            continue
        yield d

def build(distro, arch):
    f = '/var/cache/pbuilder/base-%s-%s.cow' % (distro, arch)
    if not os.path.exists(f):
        print 'Generating cowbuilder for building packages.'
        subprocess.check_call(['cowbuilder', '--create', '--distribution', distro, '--architecture', arch, '--basepath', f])

    print 'Updating cow image.'
    subprocess.check_call(['cowbuilder', '--update', '--distribution', distro, '--architecture', arch, '--basepath', f])
    for d in list_my_dirs():
        print 'Generating packages for %s' % d
        os.chdir(d)
        subprocess.check_call(['dpkg-source', '-b', '.'])
        os.chdir('../')
        subprocess.check_call(['cowbuilder', '--build', '%s_0.1.dsc' % (d), '--distribution', distro, '--architecture', arch, '--basepath', f, '--buildresult', '.'])

if __name__ == "__main__":
    build('wheezy', 'amd64')
    # build('wheezy', 'i386')