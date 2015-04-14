#!/usr/bin/env python 

from debian import changelog
import logging
import sys
import subprocess
import os 

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def list_my_dirs():
    for d in os.listdir(os.path.abspath(os.path.split(__file__)[0])):
        if not os.path.isdir(d):
            continue
        yield d

def build(distro, arch, package=None):
    failed = []
    f = '/var/cache/pbuilder/base-%s-%s.cow' % (distro, arch)
    if not os.path.exists(f):
        log.info('Generating cowbuilder for building packages.')
        subprocess.check_call(['cowbuilder', '--create', '--distribution', distro, '--architecture', arch, '--basepath', f])

    log.info('Updating cow image.')
    subprocess.check_call(['cowbuilder', '--update', '--distribution', distro, '--architecture', arch, '--basepath', f])
    for d in list_my_dirs():
        if package is not None and d != package:
            log.warning('Skipping %s', d)
            continue
        log.info('Generating packages for %s' , d)
	version = '0.1'
	with open(os.path.join(d, 'debian/changelog')) as changefile:
		c = changelog.Changelog(changefile)
		version = '%s' % c.get_version()
        os.chdir(d)
        subprocess.check_call(['dpkg-source', '-b', '.'])
        os.chdir('../')
        try:
            subprocess.check_call(['cowbuilder', '--build', '%s_%s.dsc' % (d, version.replace('-', '_')), '--distribution', distro, '--architecture', arch, '--basepath', f, '--buildresult', '.'])
        except subprocess.CalledProcessError:
            log.exception('Failed to build %s', d)
            failed.append(d)

    return failed


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        failed = build('wheezy', 'amd64', sys.argv[1])
    else:
        failed = build('wheezy', 'amd64')

    if failed:
        log.critical('Some or all builds failed! %s', failed)
        sys.exit(1)
    # build('wheezy', 'i386')
