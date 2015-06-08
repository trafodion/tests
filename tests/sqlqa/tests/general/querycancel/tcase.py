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

import subprocess
import time
import os.path

from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dbrootdci = _testmgr.get_dbroot_dci_proc()
def test0001(desc="select from table"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c1.sql", "test001.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test001.log")

    _testmgr.testcase_end(desc)

def test0002(desc="select table with index"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c2.sql", "test002.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test002.log")

    time.sleep(50)

    _testmgr.testcase_end(desc)

def test0003(desc="select from view"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid_1 = exec_obeyfile("c3.sql", "test003.log")
    time.sleep(1)

    stmt = 'control query cancel qid "' + qid_1 + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test003.log")
    time.sleep(5)

    _testmgr.testcase_end(desc)
    
def test0004(desc="select from volatile table"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c4.sql", "test004.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test004.log")

    _testmgr.testcase_end(desc)
    
def test0005(desc="select first(n) where"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c5.sql", "test005.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test005.log")

    _testmgr.testcase_end(desc)
    
def test0006(desc="select last(n) with olap window"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c6.sql", "test006.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test006.log")

    _testmgr.testcase_end(desc)
    
def test0007(desc="select with sql functions, distinct aggregates"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c7.sql", "test007.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test007.log")

    _testmgr.testcase_end(desc)

def test0008(desc="select with sql functions"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c8.sql", "test008.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test008.log")

    _testmgr.testcase_end(desc)

def test0009(desc="select with subqueries"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c9.sql", "test009.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test009.log")

    _testmgr.testcase_end(desc)

def test0010(desc="select with deep joins"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c10.sql", "test010.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test010.log")

    _testmgr.testcase_end(desc)

def test0011(desc="cancel delete from a table"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c11.sql", "test011.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test011.log")

    stmt = 'select count(*) from partsupp;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1600000')

    _testmgr.testcase_end(desc)

def test0012(desc="cancel insert into a table"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c12.sql", "test012.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test012.log")

    stmt = 'select count(*) from part12;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    stmt = 'drop table part12 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0013(desc="cancel update where..."):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c13.sql", "test013.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test013.log")

    stmt = 'select count(*) from f13 where colkey=12345;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1')

    stmt = 'drop table f13 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0014(desc="cancel update with case statement"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c14.sql", "test014.log")

    time.sleep(1)

    stmt = 'select count(*) from f02 where colintn < 40000 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '40000')

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test014.log")

    stmt = 'select count(*) from f02 where colintn < 40000 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '40000')

    stmt = 'drop table f02 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0015(desc="cancel upsert using load"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'create table f02 like f00;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    qid = exec_obeyfile("c15.sql", "test015.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test015.log")

    stmt = 'drop table f02 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test0016(desc="cancel merge match then update"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c16.sql", "test016.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'

    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test016.log")

    _testmgr.testcase_end(desc)

def test0017(desc="cancel table"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c17.sql", "test017.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test017.log")

    _testmgr.testcase_end(desc)

def test0018(desc="cancel values"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c18.sql", "test018.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test018.log")

    _testmgr.testcase_end(desc)

def test0019(desc="cancel upsert"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c19.sql", "test019.log")

    time.sleep(1)

    stmt = 'select count(*) from f02 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test019.log")

    stmt = 'select count(*) from f02 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    stmt = 'drop table f02 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0020(desc="cancel transaction"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c20.sql", "test020.log")

    time.sleep(1)

    stmt = 'select count(*) from part20 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test020.log")

    stmt = 'select count(*) from part20 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    stmt = 'drop table part20 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0021(desc="create table as"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'select count(*) from f21 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')
    
    qid = exec_obeyfile("c21.sql", "test021.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test021.log")

    stmt = 'select count(*) from f21;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'4082')

    stmt = 'drop table f21 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


def test0022(desc="drop table(100000)"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'Create table f22 as select * from f00;'
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f22 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000')

    qid = exec_obeyfile("c22.sql", "test022.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test022.log")

    stmt = 'select count(*) from f22;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '100000')

    stmt = 'drop table f22 cascade;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    

def test0023(desc="drop table for view"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'create table f23 as select * from f00;'
    output = _dci.cmdexec(stmt)
    
    stmt = 'select count(*) from f23 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000')

    qid = exec_obeyfile("c23.sql", "test023.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test023.log")

    stmt = 'select count(*) from f23;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '100000')

    stmt = 'drop table f23 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0025(desc="alter table drop column"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    stmt = 'create table f25 as select * from f00;'
    output = _dci.cmdexec(stmt)
    
    stmt = 'showddl f25 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """COLINTN""")

    qid = exec_obeyfile("c25.sql", "test025.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test025.log")

    stmt = 'showddl f25 ;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_any_substr(output, """COLINTN""")

    stmt = 'drop table f25 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
def test0026(desc="create index"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'create table f26 as select * from f00;'
    output = _dci.cmdexec(stmt)

    stmt = 'showddl f26 ;'
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """IDX26""")

    qid = exec_obeyfile("c26.sql", "test026.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test026.log")

    stmt = 'showddl f26 ;'
    output = _dci.cmdexec(stmt)
    #_dci.unexpect_any_substr(output, """IDX26""")

    stmt = 'drop table f26 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0027(desc="drop index"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'create table f27 as select * from f00;'
    output = _dci.cmdexec(stmt) 
        
    stmt = 'create index idx27 on f27 (colnum, colchariso);'
    output = _dci.cmdexec(stmt) 

    stmt = 'showddl f27 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """IDX27""")

    qid = exec_obeyfile("c27.sql", "test027.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test027.log")

    stmt = 'showddl f27 ;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_any_substr(output, """IDX27""")

    stmt = 'drop table f27 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    ### test028

def test0028(desc="update statistics for f00"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c28.sql", "test028.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test028.log")

    _testmgr.testcase_end(desc)

def test0029(desc="load into f01 "):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'create table f29 like f00;'
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f29;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    qid = exec_obeyfile("c29.sql", "test029.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test029.log")

    stmt = 'select count(*) from f29;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '0')

    stmt = 'drop table f29 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0030(desc="unload into '/bulkload'"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    qid = exec_obeyfile("c30.sql", "test030.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test030.log")

    _testmgr.testcase_end(desc)

def test0031(desc="create as some field"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'select count(*) from f31_lineitem1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')

    qid = exec_obeyfile("c31.sql", "test031.log")
    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test031.log")

    stmt = 'select count(*) from f31_lineitem1;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'4082')

    stmt = 'drop table f31_lineitem1 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    

def test0032(desc="create unique index"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
        
    stmt = 'drop table f32_lineitem cascade;'
    output = _dci.cmdexec(stmt)
    
    stmt = 'create table f32_lineitem like  '+ gvars.g_schema_tpch2x+'.lineitem;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'cleanup index TRAFODION.GENERAL_QUERYCANCEL.LORDERLINEX_q2p;'
    output = _dci.cmdexec(stmt)

    stmt = 'showddl f32_lineitem;'
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """LORDERLINEX_Q2P""")

    qid = exec_obeyfile("c32.sql", "test032.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test032.log")

    stmt = 'showddl f32_lineitem;'
    output = _dci.cmdexec(stmt)
    #_dci.unexpect_any_substr(output, """LORDERLINEX_Q2P""")

    #need cleanup
    stmt = 'drop index TRAFODION.GENERAL_QUERYCANCEL.LORDERLINEX_q2p;'
    output = _dci.cmdexec(stmt)

    #stmt = 'cleanup index TRAFODION.GENERAL_QUERYCANCEL.LORDERLINEX_q2p;'
    #output = _dci.cmdexec(stmt)

    stmt = 'drop table f32_lineitem cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
def test0033(desc="create table like"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    stmt = 'select count(*) from f33_lineitem;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')

    qid = exec_obeyfile("c33.sql", "test033.log")

    #time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test033.log")

    stmt = 'select count(*) from f33_lineitem;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'4082')

    stmt = 'drop table f33_lineitem cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test0034(desc="create table like as"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'select count(*) from f34_lineitem;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')

    qid = exec_obeyfile("c34.sql", "test034.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test034.log")

    stmt = 'select count(*) from f34_lineitem;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'4082')

    stmt = 'drop table f34_lineitem cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
def test0035(desc="load into all"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

        
    stmt = 'drop table f35 cascade;'
    output = _dci.cmdexec(stmt)
    stmt = 'create table f35 like f00;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'select count(*) from f35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
        
    qid = exec_obeyfile("c35.sql", "test035.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test035.log")

    stmt = 'select count(*) from f35;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '0')

    stmt = 'drop table f35 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0036(desc="load 100000 with truncate table(90000)"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
        
    stmt = 'drop table f36 cascade;'
    output = _dci.cmdexec(stmt)
    stmt = 'create table f36 as select * from f00 where colint between 10000 and 100000; '
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '90000')
    
    qid = exec_obeyfile("c36.sql", "test036.log")

    time.sleep(1)
    
    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test036.log")
    
    #need cleanup
    stmt = 'drop table f36 cascade ;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0037(desc="load 90000 with truncate table(100000)"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
        
    stmt = 'drop table f37 cascade;'
    output = _dci.cmdexec(stmt)
    stmt = 'create table f37 as select * from f00 ;'
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f37;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000')

    qid = exec_obeyfile("c37.sql", "test037.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test037.log")

    #need cleanup
    stmt = 'drop table f37 cascade;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test0038(desc="load with NO RECOVERY into"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    stmt = 'drop table f38 cascade;'
    output = _dci.cmdexec(stmt)
    stmt = 'create table f38 like f00 ;'
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f38;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    qid = exec_obeyfile("c38.sql", "test038.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test038.log")

    stmt = 'select count(*) from f38;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '0')

    stmt = 'drop table f38 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


def test0040(desc="load with NO DUPLICATE CHECK into"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    stmt = 'drop table f40 cascade;'
    output = _dci.cmdexec(stmt)
    stmt = 'create table f40 like f00 ;'
    output = _dci.cmdexec(stmt)

    stmt = 'select count(*) from f40;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')

    qid = exec_obeyfile("c40.sql", "test040.log")

    time.sleep(1)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test040.log")

    stmt = 'select count(*) from f40;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '0')

    stmt = 'drop table f40 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test0046_1(desc="drop view quickly"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return  
    stmt = 'create view v_o_46 as select o_totalprice,O_ORDERSTATUS,O_ORDERDATE from ' + gvars.g_schema_tpch2x+'.orders ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = 'select count(*) from v_o_46 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3000000')     
    
    qid = exec_obeyfile("c46.sql", "test046_1.log")

    time.sleep(1);
    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test046_1.log")

    stmt = 'get views;'
    output = _dci.cmdexec(stmt)
    #_dci.unexpect_any_substr(output, """v_o_46""")

    stmt = 'drop view v_o_46 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
def test0046_2(desc="drop view after 2 seconds"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return  
    stmt = 'create view v_o_46 as select o_totalprice,O_ORDERSTATUS,O_ORDERDATE from ' + gvars.g_schema_tpch2x+'.orders ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = 'select count(*) from v_o_46 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3000000')     
    
    qid = exec_obeyfile("c46.sql", "test046_2.log")

    time.sleep(2);

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test046_2.log")

    stmt = 'get views;'
    output = _dci.cmdexec(stmt)
    #_dci.unexpect_any_substr(output, """v_o_46""")

    stmt = 'drop view v_o_46 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
    # create view from two tables need manul

def test0048(desc="cancel upsert using load after 2 mins"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return  
    stmt = 'create table lineitem_48 like ' + gvars.g_schema_tpch2x+'.lineitem;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    qid = exec_obeyfile("c48.sql", "test048.log")

    time.sleep(120);
    
    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    check_logfile("test048.log")

    stmt = 'select count(*) from lineitem_48 ;'
    output = _dci.cmdexec(stmt)
    #_dci.expect_str_token(output, '0')  

    stmt = 'drop table lineitem_48 cascade;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
def testn001(desc="negative test ,cancel wrong qid"):

    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = 'control query cancel qid "0000x";'
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_error_msg(output,'8919')

    stmt = 'control query cancel qid 0000x;'
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_error_msg(output,'15001')

    _testmgr.testcase_end(desc)

def testn002(desc="negative test, cancel qid that no longer exist & query not in execute state"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # cancel qid that no longer exist
    qid = exec_obeyfile("cn002.sql", "testn002.log")
    time.sleep(10)

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8026')

    # query not in execute state
    stmt = """prepare xx from select [last 1] * from f00 order by colchariso desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """infostats xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    for line in output.splitlines():
        if line.startswith('MXID'):
            token = line.split()
            qid = token[0]

    stmt = 'control query cancel qid "' + qid + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8031')

    _testmgr.testcase_end(desc)
    
def exec_obeyfile(f1, f2):
    classpath = '.:' + defs._jdbc_classpath + ':' + defs._hpdci_classpath
    sqlfile = defs.work_dir + '/' + f1
    logfile = defs.work_dir + '/' + f2
    cmd = 'java -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + defs._target + ' -u ' + defs._user + ' -p ' + defs._pw
    cmd = cmd + ' -s ' + sqlfile + ' >' + logfile + ' &'
    _testmgr.log_write(cmd + '\n\n')
    subprocess.call(cmd, shell=True)

    # check for qid
    qid = ''
    for num in range(1, 200):
        # check if file exists
        if os.path.exists(logfile):
            # read Qid
            with open(logfile, 'r') as f:
                data = f.readlines()
                for line in data:
                    if line.startswith('MXID'):
                        token = line.split()
                        qid = token[0]
        if qid != '':
            break
        time.sleep(1)

    return qid

def check_logfile(f1):
    logfile = defs.work_dir + '/' + f1

    # check for command completed
    done = False
    data = ''
    for num in range(1, 200):
        # read Qid
        with open(logfile, 'r') as f:
            data = f.readlines()
            for line in data:
                if line.startswith('SQL>exit'):
                    done = True
        if done:
            break
        time.sleep(1)

    cancelMsg = False
    cancelTime = False
    for line in data:
        _testmgr.log_write(line)
        if line.startswith('*** ERROR[8007]'):
            cancelMsg = True
        if line.startswith('Cancel Time'):
            _dci.unexpect_any_substr(line, "Cancel Time*-1*")
            cancelTime = True

    if not cancelMsg:
            _testmgr.mismatch_record("Cancel message not found")

    if not cancelTime:
            _testmgr.mismatch_record("Cancel Time not found")


