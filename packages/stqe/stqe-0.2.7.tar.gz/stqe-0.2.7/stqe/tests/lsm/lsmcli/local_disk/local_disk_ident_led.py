#!/usr/bin/python


from os import environ

from libsan.host.lsm import LibStorageMgmt

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import get_local_disk_data, yield_lsm_config


def local_disk_ident_led_success():
    errors = []

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])
    _, disks = atomic_run(
        "Listing local disks",
        command=lsm.local_disk_list,
        return_output=True,
        script=True,
        errors=errors,
    )
    data = get_local_disk_data(disks)
    if not data:
        print("WARN: Could not find any local disks, skipping.")
        return errors

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        for disk in data:
            if data[disk]["LED Status"] == "Unknown":
                print("WARN: Disk %s does not support LED changes." % disk)
                continue
            status = data[disk]["LED Status"]
            arguments = [
                {
                    "message": "Switching identification LED ON with protocol %s" % config["protocol"],
                    "command": lsm.local_disk_ident_led_on,
                },
                {
                    "message": "Switching identification LED OFF with protocol %s" % config["protocol"],
                    "command": lsm.local_disk_ident_led_off,
                },
            ]
            if status == "ON":
                arguments = reversed(arguments)
            for argument in arguments:
                atomic_run(path=disk, errors=errors, **argument)
    return errors


def local_disk_ident_led_on_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {
                "message": "Trying to fail to set ident led ON without path with protocol %s" % config["protocol"],
                "command": lsm.local_disk_ident_led_on,
            },
            {
                "message": "Trying to fail to set ident led ON with wrong path with protocol %s" % config["protocol"],
                "command": lsm.local_disk_ident_led_on,
                "path": "WRONG",
            },
        ]
        for argument in arguments:
            atomic_run(expected_ret=2, errors=errors, **argument)
    return errors


def local_disk_ident_led_off_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {
                "message": "Trying to fail to set ident led OFF without path with protocol %s" % config["protocol"],
                "command": lsm.local_disk_ident_led_off,
            },
            {
                "message": "Trying to fail to set ident led OFF with wrong path with protocol %s" % config["protocol"],
                "command": lsm.local_disk_ident_led_off,
                "path": "WRONG",
            },
        ]
        for argument in arguments:
            atomic_run(expected_ret=2, errors=errors, **argument)
    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 1:
        errs = local_disk_ident_led_success()
    if int(environ["fmf_tier"]) == 2:
        errs = local_disk_ident_led_on_fail()
        errs += local_disk_ident_led_off_fail()
    exit(parse_ret(errs))
