## working 2020-03-08
### prereqs:
    $ snap list
    Name                Version    Rev    Tracking  Publisher     Notes
    core                16-2.43.3  8689   stable    canonical✓    core
    core18              20200124   1668   stable    canonical✓    base
    snapcraft           3.10.1     4201   stable    canonical✓    classic

    $ lsb_release -a
    Description:	Ubuntu 18.04.4 LTS

### build
    snapcraft --use-lxd --debug

### install
    snap install --dangerous igotu_0.3.90+y2016_amd64.snap --devmode

### permissions
#### temporary variant
    # after plugging i-gotU:
    $ find /dev/bus/usb/ -mmin -1 -ls
      143      0 drwxr-xr-x   2 root     root          140 Mär  8 14:06 /dev/bus/usb/003
      931      0 crw-rw-r--   1 root     root     189, 260 Mär  8 14:06 /dev/bus/usb/003/005
    $ sudo chgrp plugdev /dev/bus/usb/003/005

#### permanent variant
Add the file `/lib/udev/rules.d/51-igotu2gpx.rules` to your fs as root:

    SUBSYSTEMS=="usb", ATTRS{idVendor}=="0df7", ATTRS{idProduct}=="0900", GROUP="plugdev", MODE="0664"

Reload for testing without reboot:

    $ sudo udevadm control --reload-rules && sudo udevadm trigger

### start
    $ igotu.igotugui
