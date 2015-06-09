# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

import time
from ...lib import hpdci
from ...lib import gvars
import basic_test
import basic_defs

_testmgr = None
_testlist = []
_dci = None

# Tests using qi_user2 for privilege granting/revoking.

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    basic_test._init(hptestmgr, testlist)
    
def test001(desc="""Y/Vwc-Upd/U1,U2,U3 P:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        pass

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test002(desc="""Y/Vwc-Upd/U1,U2,U3,R1 P:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test003(desc="""Y/Vwc-Upd/U1,U2,U3,R1 P:R1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test004(desc="""Y/Vwc-Upd/U1,U2,U3,R1 R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        pass

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test005(desc="""Y/Vwc-Upd/U1,U2,U3,R1 P:U2,P:R1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test006(desc="""Y/Vwc-Upd/U1,U2,U3,R1 P:U2,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test007(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test008(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test009(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test010(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        pass

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test011(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        pass

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test012(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test013(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test014(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test015(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test016(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,P:R2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test017(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test018(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test019(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R2,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test020(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test021(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 R1:U2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        pass

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test022(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R1,P:R2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        pass

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test023(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R1,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test024(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R1,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test025(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R2,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test026(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,P:R2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test027(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:U2,R1:U2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_empty
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_error_and_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test028(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,P:R2,R1:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test029(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,P:R2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test030(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R1,R1:U2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole1 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

def test031(desc="""Y/Vwc-Upd/U1,U2,U3,R1,R2 P:R2,R1:U2,R2:U2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    def super_grant_test_roles():
        mydci = basic_defs.switch_session_super_user()
        stmt = """grant role \"""" + basic_defs.TestVars.myrole1 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        stmt = """grant role \"""" + basic_defs.TestVars.myrole2 + """\" to \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)

    def super_revoke_test_roles():
        pass

    def user1_revoke_test_privs():
        mydci = basic_defs.switch_session_qi_user1()
        stmt = """revoke """ + basic_defs.TestVars.testop + """ on """ + basic_defs.TestVars.testobj + """ from \"""" + basic_defs.TestVars.myrole2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkobj_sleeptime)

    def super_revoke_test_privs():
        mydci = basic_defs.switch_session_super_user()
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)
        stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
        output = mydci.cmdexec(stmt)
        mydci.expect_complete_msg(output)
        time.sleep(basic_defs.qi_rvkrole_sleeptime)

    user2_check_cache = basic_defs.verify_cache_nd
    user3_check_cache = basic_defs.verify_cache_nonempty
    user2_exec_expect_what = basic_defs.exec_expect_no_error_and_nd_warning
    user3_exec_expect_what = basic_defs.exec_expect_no_error_and_no_warning
    basic_test.mytest(super_grant_test_roles, super_revoke_test_roles,
                      user1_revoke_test_privs, super_revoke_test_privs,
                      user2_check_cache, user3_check_cache,
                      user2_exec_expect_what, user3_exec_expect_what)

    _testmgr.testcase_end(desc)

