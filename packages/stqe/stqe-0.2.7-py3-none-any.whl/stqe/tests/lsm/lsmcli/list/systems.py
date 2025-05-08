#!/usr/bin/python


from os import environ

from libsan.host.lsm import LibStorageMgmt

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config


def systems_success():
    errors = []
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        atomic_run(
            "Using LSM to list SYSTEMS with protocol %s" % config["protocol"],
            command=lsm.list,
            lsm_type="SYSTEMS",
            errors=errors,
        )
    return errors


def systems_fail():
    errors = []
    arguments = [
        {"sys": "false_id"},
        {"pool": "false_id"},
        {"vol": "false_id"},
        {"disk": "false_id"},
        {"ag": "false_id"},
        {"fs": "false_id"},
        {"nfs_export": "false_id"},
        {"tgt": "false_id"},
    ]
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        for argument in arguments:
            atomic_run(
                "Trying to fail using LSM to list SYSTEMS with protocol %s" % config["protocol"],
                errors=errors,
                command=lsm.list,
                lsm_type="SYSTEMS",
                success=False,
                expected_ret=2,
                **argument,
            )
    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 1:
        errs = systems_success()
    if int(environ["fmf_tier"]) == 2:
        errs = systems_fail()
    exit(parse_ret(errs))
