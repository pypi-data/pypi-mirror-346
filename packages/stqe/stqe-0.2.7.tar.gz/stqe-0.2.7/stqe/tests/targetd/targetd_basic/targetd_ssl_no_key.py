#!/usr/bin/python


import os
from time import sleep

from libsan.host import linux, targetd
from libsan.host.cmdline import run

from stqe.host.atomic_run import atomic_run, parse_ret


def targetd_ssl_func_test():
    errors = []

    password = os.environ["fmf_ssl_password"]

    atomic_run(
        "Starting targetd SSL NO KEY test",
        enable=True,
        command=targetd.ssl_change,
        errors=errors,
    )

    atomic_run(
        "Adding password to the config",
        password=password,
        command=targetd.set_password,
        errors=errors,
    )

    atomic_run(
        "Trying to start targetd without SSL key, it should fail!",
        service_name="targetd",
        command=linux.service_restart,
        errors=errors,
    )

    print("Waiting 10 seconds for the service to restart")
    sleep(10)

    atomic_run(
        "Getting targetd service status",
        retcode=3,
        command=targetd.targetd_status,
        errors=errors,
    )

    atomic_run("Removing password from config", command=targetd.set_password, errors=errors)

    cmd = "systemctl status targetd -l"
    has_systemctl = True

    if run("which systemctl", verbose=False) != 0:
        has_systemctl = False
    if not has_systemctl:
        cmd = "service targetd status -l"

    _, data = run(cmd, return_output=True)
    for line in data.splitlines():
        if "ERROR:root:SSL file: '/etc/target/targetd_key.pem' does not exist" in line:
            return errors

    print("FAIL: Service has failed with different error than expected or service is running!")
    errors.append("FAIL: Service has failed with different error than expected or service is running!")

    return errors


if __name__ == "__main__":
    errs = targetd_ssl_func_test()
    exit(parse_ret(errs))
