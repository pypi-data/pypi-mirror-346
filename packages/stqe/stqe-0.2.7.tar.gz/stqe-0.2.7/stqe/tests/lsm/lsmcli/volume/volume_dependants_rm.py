#!/usr/bin/python


from os import environ

from libsan.host.lsm import LibStorageMgmt

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from stqe.host.persistent_vars import read_var


def volume_dependants_rm_success():
    errors = []

    src_vol = read_var("LSM_VOL_ID")
    dst_vol = read_var("LSM_VOL_ID_2")
    rep_type = "CLONE"

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run(
            "Replicating volume %s to volume %s with type %s to create dependency with protocol %s."
            % (src_vol, dst_vol, rep_type, config["protocol"]),
            command=lsm.volume_replicate_range,
            src_vol=src_vol,
            dst_vol=dst_vol,
            rep_type=rep_type,
            src_start=0,
            dst_start=0,
            count=100,
            force=True,
            errors=errors,
        )

        for vol in [src_vol, dst_vol]:
            _, data = atomic_run(
                "Checking for dependants of volume %s." % vol,
                command=lsm.volume_dependants,
                vol=vol,
                return_output=True,
                errors=errors,
            )
            if data != "False" and vol == dst_vol:
                msg = "FAIL: Volume %s should have no dependants." % vol
                print(msg)
                errors.append(msg)

            elif data != "True" and vol == src_vol:
                msg = "FAIL: Volume %s should have dependants." % vol
                print(msg)
                errors.append(msg)

        atomic_run(
            f"Removing dependency between replicated volumes {src_vol} and {dst_vol}",
            command=lsm.volume_dependants_rm,
            vol=src_vol,
            errors=errors,
        )

        for vol in [src_vol, dst_vol]:
            _, data = atomic_run(
                "Checking for dependants of volume %s." % vol,
                command=lsm.volume_dependants,
                vol=vol,
                return_output=True,
                errors=errors,
            )
            if data != "False":
                msg = "FAIL: Volume %s should have no dependants." % vol
                print(msg)
                errors.append(msg)

    return errors


def volume_dependants_rm_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {
                "message": "Trying to fail getting dependants of volume without any paramethers with protocol %s"
                % config["protocol"],
                "command": lsm.volume_dependants_rm,
            },
            {
                "message": "Trying to fail replicating volume range with WRONG volume with protocol %s"
                % config["protocol"],
                "vol": "WRONG",
                "command": lsm.volume_dependants_rm,
            },
        ]
        for argument in arguments:
            atomic_run(expected_ret=2, errors=errors, **argument)
    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 1:
        errs = volume_dependants_rm_success()
    if int(environ["fmf_tier"]) == 2:
        errs = volume_dependants_rm_fail()
    exit(parse_ret(errs))
