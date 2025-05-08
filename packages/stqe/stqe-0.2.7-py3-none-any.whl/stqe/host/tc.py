"""tc.py: Module to help on test case execution."""

# Copyright (C) 2016 Red Hat, Inc.
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

__author__ = "Bruno Goncalves"
__copyright__ = "Copyright (c) 2015 Red Hat, Inc. All rights reserved."

import os
import re  # regex
import sys

from libsan.host import linux, mp
from libsan.host.cmdline import run

import stqe.host.logchecker
import stqe.host.restraint


def show_sys_info():
    print("### Kernel Info: ###")
    _, kernel = run("uname -a", return_output=True, verbose=False)
    _, taint_val = run("cat /proc/sys/kernel/tainted", return_output=True, verbose=False)
    print("Kernel version: %s" % kernel)
    print("Kernel tainted: %s" % taint_val)
    print("### IP settings: ###")
    run("ip a")
    print("### File system disk space usage: ###")
    run("df -h")

    if run("rpm -q device-mapper-multipath") == 0 and linux.service_status("multipathd") == 0:
        # Abort test execution if multipath is not working well
        if run("multipath -l 2>/dev/null") != 0:
            sys.exit(1)
        # Flush all unused multipath devices before starting the test
        mp.flush_all()
        mp.multipath_reload()


class TestClass:
    # we currently support these exit code for a test case
    tc_sup_status = {"pass": "PASS: ", "fail": "ERROR: ", "skip": "SKIP: "}
    initial_loaded_modules: list
    final_loaded_modules: list

    test_dir = "%s/.stqe-test" % os.path.expanduser("~")
    test_log = "%s/test.log" % test_dir

    def __init__(self):
        self.tc_pass = []
        self.tc_fail = []
        self.tc_skip = []  # For some reason it did not execute
        self.tc_results = []  # Test results stored in a list
        f = None
        print("################################## Test Init ###################################")
        stqe.host.logchecker.check_all()
        if not os.path.isdir(self.test_dir):
            linux.mkdir(self.test_dir)
        # read entries on test.log, there will be entries if tend was not called
        # before starting a TC class again, usually if the test case reboots the server
        if not os.path.isfile(self.test_log):
            # running the test for the first time
            show_sys_info()
            # Track memory usage during test
            run("free -b > init_mem.txt", verbose=False)
            run("top -b -n 1 > init_top.txt", verbose=False)
        else:
            try:
                with open(self.test_log) as f:
                    file_data = f.read()
            except Exception as e:
                print(e)
                print("FAIL: TestClass() could not read %s" % self.test_log)
                return
            log_entries = file_data.split("\n")
            # remove the file, once tlog is ran it will add the entries again...
            run("rm -f %s" % self.test_log, verbose=False)
            if log_entries:
                print("INFO: Loading test result from previous test run...")
                for entry in log_entries:
                    self.tlog(entry)
        print("################################################################################")
        self.initial_loaded_modules = linux.get_all_loaded_modules()
        return

    def tlog(self, string):
        """print message, if message begins with supported message status
        the test message will be added to specific test result array
        """
        print(string)
        if re.match(self.tc_sup_status["pass"], string):
            self.tc_pass.append(string)
            self.tc_results.append(string)
            run(f"echo '{string}' >> {self.test_log}", verbose=False)
        if re.match(self.tc_sup_status["fail"], string):
            self.tc_fail.append(string)
            self.tc_results.append(string)
            run(f"echo '{string}' >> {self.test_log}", verbose=False)
        if re.match(self.tc_sup_status["skip"], string):
            self.tc_skip.append(string)
            self.tc_results.append(string)
            run(f"echo '{string}' >> {self.test_log}", verbose=False)
        return

    @staticmethod
    def trun(cmd, return_output=False):
        """Run the cmd and format the log. return the exitint status of cmd
        The arguments are:
        \tCommand to run
        \treturn_output: if should return command output as well (Boolean)
        Returns:
        \tint: Command exit code
        \tstr: command output (optional)
        """
        return run(cmd, return_output)

    def tok(self, cmd, return_output=False):
        """Run the cmd and expect it to pass.
        The arguments are:
        \tCommand to run
        \treturn_output: if should return command output as well (Boolean)
        Returns:
        \tBoolean: return_code
        \t\tTrue: If command excuted successfully
        \t\tFalse: Something went wrong
        \tstr: command output (optional)
        """
        output = None
        if not return_output:
            cmd_code = run(cmd)
        else:
            cmd_code, output = run(cmd, return_output)

        if cmd_code == 0:
            self.tpass(cmd)
            ret_code = True
        else:
            self.tfail(cmd)
            ret_code = False

        if return_output:
            return ret_code, output
        else:
            return ret_code

    def tnok(self, cmd, return_output=False):
        """Run the cmd and expect it to fail.
        The arguments are:
        \tCommand to run
        \treturn_output: if should return command output as well (Boolean)
        Returns:
        \tBoolean: return_code
        \t\tFalse: If command excuted successfully
        \t\tTrue: Something went wrong
        \tstr: command output (optional)
        """
        output = None
        if not return_output:
            cmd_code = run(cmd)
        else:
            cmd_code, output = run(cmd, return_output)

        if cmd_code != 0:
            self.tpass(cmd + " [exited with error, as expected]")
            ret_code = True
        else:
            self.tfail(cmd + " [expected to fail, but it did not]")
            ret_code = False

        if return_output:
            return ret_code, output
        else:
            return ret_code

    def tpass(self, string):
        """Will add PASS + string to test log summary"""
        self.tlog(self.tc_sup_status["pass"] + string)
        return

    def tfail(self, string):
        """Will add ERROR + string to test log summary"""
        self.tlog(self.tc_sup_status["fail"] + string)
        return

    def tskip(self, string):
        """Will add SKIP + string to test log summary"""
        self.tlog(self.tc_sup_status["skip"] + string)
        return

    def tend(self):
        """It checks for error in the system and print test summary
        Returns:
        \tBoolean
        \t\tTrue if all test passed and no error was found on server
        \t\tFalse if some test failed or found error on server
        """
        if stqe.host.logchecker.check_all():
            self.tpass("Search for error on the server")
        else:
            self.tfail("Search for error on the server")

        self.final_loaded_modules = linux.get_all_loaded_modules()
        if self.final_loaded_modules:
            for module in self.final_loaded_modules:
                if module not in self.initial_loaded_modules:
                    # in case the module was unloaded already, like via dependency...
                    if not linux.is_module_loaded(module):
                        continue
                    self.tlog("module '%s' was loaded during the test. Unloading it..." % module)
                    if not linux.unload_module(module, remove_dependent=True):
                        # some modules like ext4, seems load some module dependencies that
                        # make very hard to unload it again.
                        self.tlog("INFO: Couldn't unload module '%s', ignoring it..." % module)

        print("################################ Test Summary ##################################")
        # for tc in self.tc_pass:
        #    print tc
        # for tc in self.tc_fail:
        #    print tc
        # for tc in self.tc_skip:
        #    print tc
        # Will print test results in order and not by test result order
        for tc in self.tc_results:
            print(tc)

        n_tc_pass = len(self.tc_pass)
        n_tc_fail = len(self.tc_fail)
        n_tc_skip = len(self.tc_skip)
        print("#############################")
        print("Total tests that passed: " + str(n_tc_pass))
        print("Total tests that failed: " + str(n_tc_fail))
        print("Total tests that skipped: " + str(n_tc_skip))
        print("################################################################################")
        sys.stdout.flush()
        # Added this sleep otherwise some of the prints were not being shown....
        linux.sleep(1)
        run("rm -f %s" % self.test_log, verbose=False)
        run("rmdir %s" % self.test_dir, verbose=False)

        # If at least one test failed, return error
        if n_tc_fail > 0:
            return False

        return True

    def log_submit(self, log_file):
        """It will upload logs depending on environment used to run the test"""
        if not log_file:
            self.tfail("log_submit: log_file parameter not set")
            return False

        if stqe.host.restraint.is_restraint_job():
            stqe.host.restraint.log_submit(log_file)

        self.tlog("doesn't know how to upload log in this environment. Skipping...")
        return True
