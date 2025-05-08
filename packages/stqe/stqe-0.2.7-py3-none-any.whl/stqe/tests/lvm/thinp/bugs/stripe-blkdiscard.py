#!/usr/bin/python3 -u
# -u is for unbuffered stdout
# Copyright (C) 2023 Red Hat, Inc.
# python-stqe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-stqe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-stqe.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Filip Suba   <fsuba@redhat.com>


import sys
import traceback

from libsan.host import linux, loopdev, lvm
from libsan.host.cmdline import run

import stqe.host.tc

TestObj = None

loop_dev = {}

vg_name = "testvg"


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Provisioning Stripe test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=40)
        if not new_dev:
            TestObj.tfail("Could not create loop device to be used as dev%s" % dev_num)
            return False
        loop_dev["dev%s" % dev_num] = new_dev

    pvs = ""
    for dev in loop_dev:
        pvs += " %s" % (loop_dev[dev])
    if not lvm.vg_create(vg_name, pvs, force=True):
        TestObj.tfail("Could not create VG")
        return False

    lv_name = "lv"
    if not lvm.lv_create(vg_name, lv_name, options=["-l 100%VG", "--stripes=2"]):
        TestObj.tfail("Could not create lv!")
        return False

    cmd = "blkdiscard /dev/testvg/lv"
    ret, data = run(cmd, return_output=True)
    if ret != 0:
        TestObj.tfail(data)
        return False

    return True


def _clean_up():
    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail('Could not delete VG "%s"' % vg_name)

    if loop_dev:
        for dev in loop_dev:
            if not lvm.pv_remove(loop_dev[dev]):
                TestObj.tfail('Could not delete PV "%s"' % loop_dev[dev])
            linux.sleep(1)
            if not loopdev.delete_loopdev(loop_dev[dev]):
                TestObj.tfail("Could not remove loop device %s" % loop_dev[dev])


def main():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    linux.install_package("lvm2")

    try:
        start_test()
    except Exception as e:
        traceback.print_exc()
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
