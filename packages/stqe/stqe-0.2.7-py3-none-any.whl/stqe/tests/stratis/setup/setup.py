#!/usr/bin/python


from time import sleep

from libsan.host.stratis import Stratis

from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.fmf_tools import get_env_args, get_func_from_string, read_env
from stqe.host.persistent_vars import read_var, write_var
from stqe.host.stratis import get_stratis_args


def write_data(args, errors):
    name = read_env("fmf_name")
    if "fs_create" in name:
        atomic_run(
            "Writing var STRATIS_FS",
            command=write_var,
            var={"STRATIS_FS": args["fs_name"]},
            errors=errors,
        )

    if "snapshot_create" in name:
        atomic_run(
            "Writing var STRATIS_SNAPSHOT",
            command=write_var,
            var={"STRATIS_SNAPSHOT": args["snapshot_name"]},
            errors=errors,
        )

    if "mkdir" in name:
        atomic_run(
            "Writing var FS_DIR",
            command=write_var,
            var={"FS_DIR": args["cmd"].split()[-1]},
            errors=errors,
        )
    return


def setup():
    errors = []

    stratis = Stratis(disable_check=True)
    args = get_stratis_args(stratis_object=stratis)

    name = read_env("fmf_name")
    if "fs/destroy" in name:
        print("INFO: Waiting 2 seconds before destroying filesystem.")
        sleep(2)

    # some extra args for some setup
    args.update(get_env_args(["id", "cmd", "path"], read_var("FILE_NAMES")))
    command = args.pop("command")

    args["command"] = get_func_from_string(stratis, command)
    atomic_run(errors=errors, **args)
    print("the second args %s" % args)
    write_data(args, errors)

    return errors


if __name__ == "__main__":
    errs = setup()
    exit(parse_ret(errs))
