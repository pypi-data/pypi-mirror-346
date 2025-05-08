#!/usr/bin/python


from os import environ

from libsan.host.lsm import LibStorageMgmt

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import translate_cache_policy, yield_lsm_config
from stqe.host.persistent_vars import read_var


def volume_write_cache_policy_update_success():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        _, data = atomic_run(
            "Getting write cache policy of volume %s." % vol,
            command=lsm.volume_cache_info,
            vol=vol,
            return_output=True,
            script=True,
            errors=errors,
        )
        old_policy = None
        for line in data.splitlines():
            if "Write Cache Policy" in line:
                old_policy = translate_cache_policy(line.split().pop().strip())

        for policy in ["WB", "AUTO", "WT", "wb", "auto", "wt"]:
            atomic_run(
                "Updating policy of volume {} to be {} with protocol {}.".format(vol, policy, config["protocol"]),
                command=lsm.volume_write_cache_policy_update,
                vol=vol,
                policy=policy,
                errors=errors,
            )

        atomic_run(
            "Returning write policy of volume %s to former state '%s' with protocol %s."
            % (vol, old_policy, config["protocol"]),
            command=lsm.volume_write_cache_policy_update,
            vol=vol,
            policy=old_policy,
            errors=errors,
        )
    return errors


def volume_write_cache_policy_update_fail():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {
                "message": "Trying to fail changing write policy of volume without any paramethers with protocol %s"
                % config["protocol"],
                "command": lsm.volume_write_cache_policy_update,
            },
            {
                "message": "Trying to fail changing write policy of volume with WRONG volume with protocol %s"
                % config["protocol"],
                "vol": "WRONG",
                "policy": "auto",
                "command": lsm.volume_write_cache_policy_update,
            },
            {
                "message": "Trying to fail changing write policy of volume with WRONG policy with protocol %s"
                % config["protocol"],
                "vol": vol,
                "policy": "WRONG",
                "command": lsm.volume_write_cache_policy_update,
            },
        ]
        for argument in arguments:
            atomic_run(expected_ret=2, errors=errors, **argument)
    return errors


def volume_write_cache_policy_update_offline():
    errors = []
    # TODO: Check updating policy of offline volume, create test
    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 1:
        errs = volume_write_cache_policy_update_success()
    if int(environ["fmf_tier"]) == 2:
        errs = volume_write_cache_policy_update_fail()
    exit(parse_ret(errs))
