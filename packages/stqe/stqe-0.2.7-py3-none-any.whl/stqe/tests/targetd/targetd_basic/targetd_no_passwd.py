#!/usr/bin/python


from time import sleep

from libsan.host import linux, targetd
from libsan.host.cmdline import run

from stqe.host.atomic_run import atomic_run, parse_ret


def targetd_no_passwd_test():
    errors = []

    atomic_run("Disabling SSL", command=targetd.ssl_change, errors=errors)

    atomic_run("Removing password from config", command=targetd.set_password, errors=errors)

    atomic_run(
        "Restarting targetd service",
        service_name="targetd",
        command=linux.service_restart,
        errors=errors,
    )

    print("Waiting 10 seconds for the service to restart")
    sleep(10)

    atomic_run(
        "Checking retcode of targetd",
        retcode=3,
        command=targetd.targetd_status,
        errors=errors,
    )

    cmd = "systemctl status targetd"
    has_systemctl = True

    if run("which systemctl", verbose=False) != 0:
        has_systemctl = False
    if not has_systemctl:
        cmd = "service targetd status"

    _, data = run(cmd, return_output=True)

    for line in data.splitlines():
        if "CRITICAL:root:password" in line:
            return errors

    print("FAIL: Service has failed with different error than expected or service is running!")
    errors.append("FAIL: Service has failed with different error than expected or service is running!")
    return errors


if __name__ == "__main__":
    errs = targetd_no_passwd_test()
    exit(parse_ret(errs))
