#!/usr/bin/python


from os import environ

from libsan.host.cmdline import run
from libsan.host.linux import is_module_loaded, load_module, unload_module

from stqe.host.atomic_run import atomic_run, parse_ret


def kvdo():
    # Tries to load/unload kvdo kernel module.
    errors = []
    arguments = []

    # clean up modules first, to be sure (kvdo blocks uds)
    for module in ["kvdo", "uds"]:
        _, data = run(cmd="lsmod | grep %s" % module, return_output=True)
        if data != "":
            arguments += [
                {
                    "message": "Unloading module '%s'." % module,
                    "command": unload_module,
                    "module_name": module,
                },
            ]

    arguments += [
        {"message": "Loading module 'kvdo'.", "command": load_module, "module": "kvdo"},
        {
            "message": "Checking if 'kvdo' is loaded.",
            "command": is_module_loaded,
            "module_name": "kvdo",
        },
        # kvdo requires uds
        {
            "message": "Checking if 'uds' is loaded.",
            "command": is_module_loaded,
            "module_name": "kvdo",
        },
        {
            "message": "Unloading module 'kvdo'.",
            "command": unload_module,
            "module_name": "kvdo",
        },
        {
            "message": "Unloading module 'uds'.",
            "command": unload_module,
            "module_name": "uds",
        },
    ]

    for argument in arguments:
        atomic_run(errors=errors, **argument)

    return errors


if __name__ == "__main__":
    if int(environ["fmf_tier"]) == 1:
        errs = kvdo()
    exit(parse_ret(errs))
