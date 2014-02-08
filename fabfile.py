from fabric.api import *
from fabric.contrib import files
import os
import os.path
from binascii import b2a_hex
import re
import urllib

env.user = "root"
env.shell="/bin/ash -c"

def copy_id():
    """
    Copy our public SSH key to node, so we can log in without password
    """
    files.append("/etc/dropbear/authorized_keys", open(os.path.expanduser("~/.ssh/id_rsa.pub")).read())

def set_random_password():
    """
    Change node password to a long random password.
    The password is kept in a local file nodes/<hostname> should you ever
    need it.
    """
    new_password = b2a_hex(os.urandom(16))
    with hide('running', 'stdout', 'stderr'):
        run('echo -e "%s\\n%s" | passwd' % (new_password, new_password))

    if not os.path.exists("nodes"):
        os.makedirs("nodes")
    text_file = open(os.path.join("nodes", env.host_string), "w")
    text_file.write(new_password)
    text_file.close()
    os.chmod(os.path.join("nodes", env.host_string), 0600)

def lock_down():
    """
    Set up authorisation on a fresh node:
    Copy our SSH public key and change the password.
    """
    copy_id()
    set_random_password()

def set_hostname():
    """
    Set the system hostname to match the fabric hostname
    (most likely taken from your local /etc/hosts).
    This will only be in effect after a reboot.
    """
    run("uci set system.@system[0].hostname=%s" % env.host_string)
    run("uci commit system")

def download_firmware(sysinfo_model):
    """
    Download the firmware image for the given router model
    to a local directory.
    """
    url = _model_to_firmware_url(sysinfo_model)

    if not os.path.exists("firmware_images"):
        os.makedirs("firmware_images")

    with lcd("firmware_images"):
        local("wget -q --timestamping %s" % url)

def _model_to_firmware_url(sysinfo_model):
    """
    Translate the model string as read from /var/sysinfo/model
    into a download URL for the matching firmware update image
    """
    community = "duesseldorf"
    base_url = "http://images.freifunk-rheinland.net/images/fsm/current/%s-ar71xx-attitude_adjustment/" % community

    revision = re.findall(r"v.", sysinfo_model)[0]
    model = re.findall(r"TL\-\S*", sysinfo_model)[0].lower()
    model = model.replace("n/nd", "nd")

    return "%sopenwrt-ar71xx-generic-%s-%s-squashfs-sysupgrade.bin" % (base_url, model, revision)
