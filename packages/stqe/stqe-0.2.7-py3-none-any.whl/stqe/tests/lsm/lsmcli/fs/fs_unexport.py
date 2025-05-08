#!/usr/bin/python


from os import environ

from libsan.host.lsm import LibStorageMgmt

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from stqe.host.persistent_vars import read_var

# fs_unexport_success is part of fs_export_success() in this same directory


def fs_unexport_fail():
    errors = []

    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {
                "message": "Trying to fail deleting export without name with protocol %s" % config["protocol"],
                "command": lsm.fs_unexport,
            },
            {
                "message": "Trying to fail deleting export with WRONG name with protocol %s" % config["protocol"],
                "command": lsm.fs_unexport,
                "export": "WRONG",
            },
            {
                "message": "Trying to fail deleting export with fs_id instead of export_id with protocol %s"
                % config["protocol"],
                "command": lsm.fs_unexport,
                "export": fs_id,
            },
        ]
        for argument in arguments:
            atomic_run(expected_ret=2, errors=errors, **argument)
    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 2:
        errs = fs_unexport_fail()
    exit(parse_ret(errs))
