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

from ...lib import hpdci
from ...lib import gvars

_testmgr = None
_testlist = []
_dci = None

work_dir = None

qi_rvkobj_sleeptime = 6
qi_rvkrole_sleeptime = 6

# global funcions to be defined
user1_grant_all_privs_to_all = None
user1_revoke_all_privs_from_all = None
verify_aqr_counters = None

class TestVars():
    test_schema_full = None
    test_schema_partial = None

    testobj = None
    testop1 = None
    testop = None
    testquery = None

    myrole1 = None
    myrole2 = None

    # WST what do we do with the user stuff?

    # Start different mxci sessions using different users so that
    # the tests can switch between users
    # LDAP users were maintained by Paul Low.  Here is the list of users that
    # the QI project has asked him for execlusive usage:
    # register user qa080;
    # register user qa081;
    # register user qa082;
    # register user qa083;
    # register user qa084;
    # register user qa085;
    # register user qa086;
    # register user qa087;
    # register user qa088;
    # register user qa089;
    qi_user1 = "qa080"
    qi_pw1 = "QAPassword"
    qi_role1 = ""

    qi_user2 = "qa081"
    qi_pw2 = "QAPassword"
    qi_role2 = ""

    qi_user3 = "qa082"
    qi_pw3 = "QAPassword"
    qi_role3 = ""

    conn_user = 'qauser_execs'
    # gvars.NVS_USER
    conn_pw = 'QAPassword'
    # gvars.NVS_PW
    conn_role = 'ROLE.EXECS'
    # gvars.NVS_ROLE

    # The following works only for dev workstation
    # #sh export NVS_USER="sql_user"
    # The following works only for dev cluster
    # #sh . $TEST_ROOT/bin/export_users supermxci
    super_user = 'trafodion'
    # gvars.NVS_USER
    super_pw = 'traf123'
    # gvars.NVS_PW
    super_role = ''
    #gvars.NVS_ROLE


# Sleep time after each revoke, so that other sessions can
# detect the effect.
def _init(test_schema_full, test_schema_partial, hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
   
    TestVars.test_schema_full = test_schema_full
    TestVars.test_schema_partial = test_schema_partial

    _testmgr.clone_dci_proc_with_id('supermxci', _dci, TestVars.super_user, TestVars.super_pw, TestVars.super_role)
    # Use the users/pws/roles defined in testunit.
    _testmgr.clone_dci_proc_with_id('qi_mxci1', _dci, TestVars.qi_user1, TestVars.qi_pw1, TestVars.qi_role1)
    _testmgr.clone_dci_proc_with_id('qi_mxci2', _dci, TestVars.qi_user2, TestVars.qi_pw2, TestVars.qi_role2)
    _testmgr.clone_dci_proc_with_id('qi_mxci3', _dci, TestVars.qi_user3, TestVars.qi_pw3, TestVars.qi_role3)

    # Call all users to get some info, the rest of the setup is done
    # under user1.
    mydci = switch_session_conn_user()
    # who am i
    # WST crash trafci
    stmt = """get current_user;"""
    # WST crash trafci
    output = mydci.cmdexec(stmt)
    stmt = """get roles for user """ + TestVars.conn_user + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)

    mydci = switch_session_super_user()
    # who am i
    # WST crash trafci
    stmt = """get current_user;"""
    # WST crash trafci
    output = mydci.cmdexec(stmt)
    stmt = """get roles for user """ + TestVars.super_user + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)

    mydci = switch_session_qi_user2()
    # who am i
    # WST crash trafci
    stmt = """get current_user;"""
    # WST crash trafci
    output = mydci.cmdexec(stmt)
    stmt = """get roles for user """ + TestVars.qi_user2 + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)

    mydci = switch_session_qi_user3()
    # who am i
    # WST crash trafci
    stmt = """get current_user;"""
    # WST crash trafci
    output = mydci.cmdexec(stmt)
    stmt = """get roles for user """ + TestVars.qi_user3 + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)

    mydci = switch_session_qi_user1()
    # who am i
    # WST crash trafci
    stmt = """get current_user;"""
    # WST crash trafci
    output = mydci.cmdexec(stmt)
    stmt = """get roles for user """ + TestVars.qi_user1 + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)

def switch_session_conn_user():
    global _testmgr
    mydci = _testmgr.get_default_dci_proc()
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)
    return mydci

def switch_session_super_user():
    global _testmgr
    mydci = _testmgr.get_dci_proc('supermxci')
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)
    return mydci

def switch_session_qi_user1():
    global _testmgr
    mydci = _testmgr.get_dci_proc('qi_mxci1')
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)
    return mydci

def switch_session_qi_user2():
    global _testmgr
    mydci = _testmgr.get_dci_proc('qi_mxci2')
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)
    return mydci

def switch_session_qi_user3():
    global _testmgr
    mydci = _testmgr.get_dci_proc('qi_mxci3')
    stmt = """set schema """ + TestVars.test_schema_full + """;"""
    output = mydci.cmdexec(stmt)
    return mydci

def verify_cache_empty(mydci):
    stmt = """select count(*) from table(querycacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output, """*0*""")
    stmt = """select count(*) from table(natablecacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """') and object_name = upper('""" + TestVars.testobj + """');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output, """*0*""")

def verify_cache_nonempty(mydci):
    #AQRTODO We may not be able to verify this.  A query may or
    #may not be inserted into the cache in the first place, depeing on a lot of
    #rules.  Here we want to verify that the cache is not cleared, but the entry
    #may not be there even after it is first prepared!
    #AQRTODO #unexpect any *0*
    stmt = """select count(*) from table(querycacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """');"""
    output = mydci.cmdexec(stmt)
    #AQRTODO #unexpect any *0*
    stmt = """select count(*) from table(natablecacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """') and object_name = upper('""" + TestVars.testobj + """');"""
    output = mydci.cmdexec(stmt)

def verify_cache_nd(mydci):
    # behavior non-deterministic.  Informational only, no verification
    stmt = """select count(*) from table(querycacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """');"""
    output = mydci.cmdexec(stmt)
    # behavior non-deterministic.  Informational only, no verification
    stmt = """select count(*) from table(natablecacheentries()) where schema_name = upper('""" + TestVars.test_schema_partial + """') and object_name = upper('""" + TestVars.testobj + """');"""
    output = mydci.cmdexec(stmt)

def notverify_cache_nd(mydci):
     pass

def noverify_cache_nonempty(mydci):
    pass
	

def get_cur_qryqid(mydci):
    stmt = """log """ + work_dir + """/qidout clear;"""
    output = mydci.cmdexec(stmt)
    stmt = """get statistics for qid current;"""
    output = mydci.cmdexec(stmt)
    stmt = """log off;"""
    output = mydci.cmdexec(stmt)
    cur_qryqid = _testmgr.shell_call("""grep ^Qid """ + work_dir + """/qidout|awk '{print $2}'""")
    return cur_qryqid

def check_rms_aqr(mydci, qryqid,
                  expect_aqrerr, unexpect_aqrerr,
                  expect_aqrnumtry, unexpect_aqrnumtry,
                  expect_aqrdelay, unexpect_aqrdelay):
    global _testmgr
    # WST TODO: do we want to keep this as informational only?
    stmt = """get statistics for rms all;"""
    output = mydci.cmdexec(stmt)

    stmt = """log """ + work_dir + """/rmsqid.log clear;"""
    output = mydci.cmdexec(stmt)
    stmt = """get statistics for qid """ + qryqid + """;"""
    output = mydci.cmdexec(stmt)
    stmt = """log off;"""
    output = mydci.cmdexec(stmt)
    # Don't really care which error causes AQR, just make sure that it is not 0.
    output = _testmgr.shell_call("""grep 'Last Error before AQR' """ + work_dir + """/rmsqid.log | awk '{print $5}'""")
    if expect_aqrerr:
        mydci.expect_str_token(output, expect_aqrerr)
    if unexpect_aqrerr:
        mydci.unexpect_any_substr(output, unexpect_aqrerr)

    output = _testmgr.shell_call("""grep 'Number of AQR retries' """ + work_dir + """/rmsqid.log | awk '{print $5}'""")
    if expect_aqrnumtry:
        mydci.expect_str_token(output, expect_aqrnumtry)
    if unexpect_aqrnumtry:
        mydci.unexpect_any_substr(output, unexpect_aqrnumtry)

    output = _testmgr.shell_call("""grep 'Delay before AQR' """ + work_dir + """/rmsqid.log | awk '{print $4}'""")
    if expect_aqrdelay:
        mydci.expect_str_token(output, expect_aqrdelay)
    if unexpect_aqrdelay:
        mydci.unexpect_any_substr(output, unexpect_aqrdelay)

def verify_rms_aqr_counters_retry(mydci, qryqid):
    check_rms_aqr(mydci, qryqid, '', '0', '1', '', '0', '')

def verify_rms_aqr_counters_no_retry(mydci, qryqid):
    #AQRTODO TODO: Is 0 we should be expecting for aqrdelay?
    check_rms_aqr(mydci, qryqid, '0', '', '0', '', '0', '')

def verify_rms_aqr_counters_nd(mydci, qryqid):
    #AQRTODO check_rms_aqr(mydci, qryqid, '', '0', '1', '', '0', '')
    pass

def exec_expect_error_and_warning(mydci, output):
    global verify_aqr_counters
    verify_aqr_counters = verify_rms_aqr_counters_retry
    mydci.expect_any_substr(output, """*WARNING[8597]*""")
    mydci.expect_any_substr(output, """*ERROR*""")

def exec_expect_no_error_and_nd_warning(mydci, output):
    global verify_aqr_counters
    verify_aqr_counters = verify_rms_aqr_counters_nd
    #AQRTODO #expect any *WARNING[8597]*
    mydci.unexpect_any_substr(output, """ERROR""")

def exec_expect_no_error_and_no_warning(mydci, output):
    global verify_aqr_counters
    #AQRTODO TODO Hope this is OK
    verify_aqr_counters = verify_rms_aqr_counters_no_retry
    mydci.unexpect_any_substr(output, """WARNING[8597]""")
    mydci.unexpect_any_substr(output, """ERROR""")

def clear_cache(mydci):
    # clear the query cache
    stmt = """cqd query_cache '0';"""
    output = mydci.cmdexec(stmt)
    stmt = """cqd query_cache reset;"""
    output = mydci.cmdexec(stmt)
    # clear the NATable cache
    stmt = """cqd metadata_cache_size '0';"""
    output = mydci.cmdexec(stmt)
    stmt = """cqd metadata_cache_size reset;"""
    output = mydci.cmdexec(stmt)
    verify_cache_empty(mydci)

def turn_on_aqr_settings(mydci):
    # should be on by default: cqd auto_query_retry 'on';
    stmt = """cqd auto_query_retry_warnings 'on';"""
    output = mydci.cmdexec(stmt)

def turn_off_aqr_settings(mydci):
    stmt = """cqd auto_query_retry 'off';"""
    output = mydci.cmdexec(stmt)
    stmt = """cqd auto_query_retry_warnings 'on';"""
    output = mydci.cmdexec(stmt)

def turn_on_aqr_all_users():
    mydci = switch_session_qi_user1()
    turn_on_aqr_settings(mydci)
    mydci = switch_session_qi_user2()
    turn_on_aqr_settings(mydci)
    mydci = switch_session_qi_user3()
    turn_on_aqr_settings(mydci)

def turn_off_aqr_all_users():
    mydci = switch_session_qi_user1()
    turn_off_aqr_settings(mydci)
    mydci = switch_session_qi_user2()
    turn_off_aqr_settings(mydci)
    mydci = switch_session_qi_user3()
    turn_off_aqr_settings(mydci)

def super_create_all_roles():
    mydci = switch_session_super_user()
    # this test may not use all of them, but create them anyway.
    stmt = """create role \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """create role \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def super_drop_all_roles():
    mydci = switch_session_super_user()
    stmt = """drop role \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """drop role \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def prepare_test_query(mydci):
    clear_cache(mydci)
    stmt = """prepare xx from """ + TestVars.testquery + """;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_prepared_msg(output)
    # A query prepared by a non-super ID should see this new field in the
    # explain output.
    stmt = """explain xx;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output, """*Query_Invalidation_Keys*""")
    return get_cur_qryqid(mydci)

# Schema privs are separete from object privs.  You can do "grant schema S"
# and "grant object S.O" at the same time.  As long as one of them is there,
# you will have the priv on S.O.  You can view "grant schema S" as a special
# way of granting privs to all objects in S all at once.  You can't do
# "revoke S.O" just to take the privs of S.O back either.  The only way
# to revoke "grant schema S" is to "revoke schema S".
# That's why we need seprate sets of routines here.  Otherwise, they may
# interfer with each other.
#
# Object privs, on the other hand, need to work with the column privs.
# To simplfy the tests, they are also separated.

def user1_grant_all_obj_privs_to_all_a():
    mydci = switch_session_qi_user1()
    stmt = """grant all on mytable1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.qi_user2 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def user1_revoke_all_obj_privs_from_all_a():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke all on myview1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.qi_user2 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)

def user1_grant_all_obj_privs_to_all_b():
    mydci = switch_session_qi_user1()
    stmt = """grant all on mytable1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to PUBLIC;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant all on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant all on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

def user1_revoke_all_obj_privs_from_all_b():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke all on myview1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mymv1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke all on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke all on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)

# Can't use $testop on MV, since table/view objects call this function for
# update/insert as $testop and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_a():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user2 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

# Can't use $testop on MV, since table/view objects call this function for
# update/insert as $testop and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_a():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user2 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

# Can't use $testop on MV, since table/view objects call this function for
# update/insert as $testop and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_b():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop + """ on mytable1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to PUBLIC;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

# Can't use $testop on MV, since table/view objects call this function for
# update/insert as $testop and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_b():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from PUBLIC;"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    #output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    #stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    #output = mydci.cmdexec(stmt)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_a1():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_a2():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_a1():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_a2():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_b1():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select (a,b,c,d,e) on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_grant_all_col_privs_to_all_b2():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on mytable1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on mytable2 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop1 + """ on myview1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant select on mymv1 to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_b1():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select (a,b,c,d,e) on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

# Can't use $testop1 on MV, since table/view objects call this function for
# update/insert as $testop1 and they don't apply to MV.  Only select applies
# to MV, so the function just hardcodes it.

def user1_revoke_all_col_privs_from_all_b2():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on mytable1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on mytable2 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop1 + """ on myview1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke select on mymv1 from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

def user1_grant_all_sch_privs_to_all_a():
    mydci = switch_session_qi_user1()
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def user1_revoke_all_sch_privs_from_all_a():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

def user1_grant_all_sch_privs_to_all_b():
    mydci = switch_session_qi_user1()
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant all on schema """ + TestVars.test_schema_full + """ to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def user1_revoke_all_sch_privs_from_all_b():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke all on schema """ + TestVars.test_schema_full + """ from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

def user1_grant_all_spj_privs_to_all_a():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def user1_revoke_all_spj_privs_from_all_a():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.qi_user2 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

def user1_grant_all_spj_privs_to_all_b():
    mydci = switch_session_qi_user1()
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """grant """ + TestVars.testop + """ on """ + TestVars.testobj + """ to \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

def user1_revoke_all_spj_privs_from_all_b():
    mydci = switch_session_qi_user1()
    # ignore errors; some may have been revoked earlier in the test.
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.qi_user3 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.myrole1 + """\";"""
    output = mydci.cmdexec(stmt)
    stmt = """revoke """ + TestVars.testop + """ on """ + TestVars.testobj + """ from \"""" + TestVars.myrole2 + """\";"""
    output = mydci.cmdexec(stmt)

# The following routines define the queries and operator that
# are used in the tests.

def def_tbl_del_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """delete"""
    TestVars.testquery = """delete from mytable1 where a = (select min(a) from mytable2)"""

def def_tbl_ins_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """insert"""
    TestVars.testquery = """insert into mytable1 values (6,6,6,'F','F')"""

def def_tbl_sel_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_tbl_upd_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """update"""
    TestVars.testquery = """update mytable1 set b = a where a <> b"""

def def_tbl_all_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """all"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_view_del_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """delete"""
    TestVars.testquery = """delete from myview1 where a = (select min(a) from mytable2)"""

def def_view_ins_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """insert"""
    TestVars.testquery = """insert into myview1 values (6,6,6,'F','F')"""

def def_view_sel_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from myview1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_view_upd_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """update"""
    TestVars.testquery = """update myview1 set b = a where a <> b"""

def def_view_all_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """all"""
    TestVars.testquery = """select * from myview1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

# insert/update do not apply to MV.

def def_mv_del_query():
    TestVars.testobj = """mymv1"""
    TestVars.testop = """delete"""
    TestVars.testquery = """delete from mymv1 where a = (select min(a) from mytable2)"""

def def_mv_sel_query():
    TestVars.testobj = """mymv1"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from mymv1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_mv_all_query():
    TestVars.testobj = """mymv1"""
    TestVars.testop = """all"""
    TestVars.testquery = """select * from mymv1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

# delete/all do not apply to object column priv.

def def_tblcol_ins_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """insert (a,b,c,d,e)"""
    TestVars.testquery = """insert into mytable1 values (6,6,6,'F','F')"""

def def_tblcol_sel_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_tblcol_upd_query():
    TestVars.testobj = """mytable1"""
    TestVars.testop = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testquery = """update mytable1 set b = a where a <> b"""

def def_tblcol_ins_query_1():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """insert (a,b,c,d,e)"""
    TestVars.testop = """insert"""
    TestVars.testquery = """insert into mytable1 values (6,6,6,'F','F')"""

def def_tblcol_sel_query_1():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """select (a,b,c,d,e)"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_tblcol_upd_query_1():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testop = """update,select"""
    TestVars.testquery = """update mytable1 set b = a where a <> b"""

def def_tblcol_ins_query_2():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """insert"""
    TestVars.testop = """insert (a,b,c,d,e)"""
    TestVars.testquery = """insert into mytable1 values (6,6,6,'F','F')"""

def def_tblcol_sel_query_2():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """select"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_tblcol_upd_query_2():
    TestVars.testobj = """mytable1"""
    TestVars.testop1 = """update,select"""
    TestVars.testop = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testquery = """update mytable1 set b = a where a <> b"""

# delete/all do not apply to object column priv.

def def_viewcol_ins_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """insert (a,b,c,d,e)"""
    TestVars.testquery = """insert into myview1 values (6,6,6,'F','F')"""

def def_viewcol_sel_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from myview1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_viewcol_upd_query():
    TestVars.testobj = """myview1"""
    TestVars.testop = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testquery = """update myview1 set b = a where a <> b"""

def def_viewcol_ins_query_1():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """insert (a,b,c,d,e)"""
    TestVars.testop = """insert"""
    TestVars.testquery = """insert into myview1 values (6,6,6,'F','F')"""

def def_viewcol_sel_query_1():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """select (a,b,c,d,e)"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from myview1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_viewcol_upd_query_1():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testop = """update,select"""
    TestVars.testquery = """update myview1 set b = a where a <> b"""

def def_viewcol_ins_query_2():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """insert"""
    TestVars.testop = """insert (a,b,c,d,e)"""
    TestVars.testquery = """insert into myview1 values (6,6,6,'F','F')"""

def def_viewcol_sel_query_2():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """select"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from myview1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_viewcol_upd_query_2():
    TestVars.testobj = """myview1"""
    TestVars.testop1 = """update,select"""
    TestVars.testop = """update (a,b,c,d,e),select (a,b,c,d,e)"""
    TestVars.testquery = """update myview1 set b = a where a <> b"""

# insert/update do not apply to MV.
# delete/all do not apply to object column priv.

def def_mvcol_sel_query():
    TestVars.testobj = """mymv1"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from mymv1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_mvcol_sel_query_1():
    TestVars.testobj = """mymv1"""
    TestVars.testop1 = """select (a,b,c,d,e)"""
    TestVars.testop = """select"""
    TestVars.testquery = """select * from mymv1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_mvcol_sel_query_2():
    TestVars.testobj = """mymv1"""
    TestVars.testop1 = """select"""
    TestVars.testop = """select (a,b,c,d,e)"""
    TestVars.testquery = """select * from mymv1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_sch_del_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """delete"""
    TestVars.testquery = """delete from mytable1 where a = (select min(a) from mytable2)"""

def def_sch_ins_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """insert"""
    TestVars.testquery = """insert into mytable1 values (6,6,6,'F','F')"""

def def_sch_sel_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """select"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_sch_upd_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """update"""
    TestVars.testquery = """update mytable1 set b = a where a <> b"""

def def_sch_all_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """all"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_sch_dml_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """all_dml"""
    TestVars.testquery = """select * from mytable1 t1, mytable2 t2 where t1.a=t2.a order by t1.a"""

def def_sch_exe_query():
    TestVars.testobj = """schema """ + TestVars.test_schema_full
    TestVars.testop = """execute"""
    TestVars.testquery = """call QIN0001()"""

def def_spj_exe_query():
    TestVars.testobj = """procedure QIN0001"""
    TestVars.testop = """execute"""
    TestVars.testquery = """call QIN0001()"""

