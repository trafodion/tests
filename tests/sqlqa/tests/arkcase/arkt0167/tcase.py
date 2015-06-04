# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""a00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table a1dtyf3 (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1itym  (a interval year to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1ity4m (a interval year(4) to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1itdf3 (a interval DAY TO second(3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #create table a1itdf3 (a interval DAY TO fraction(3));
    
    stmt = """create table a2dt1 (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #create table a2dt1 (a datetime year to fraction(3));
    
    stmt = """create table a2dt2 (b timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #create table a2dt2 (b datetime year to fraction(3));
    
    stmt = """create table a2dt1k 
(c timestamp  NOT NULL, primary key (c));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #    (c datetime year to fraction(3) NOT NULL, primary key (c));
    
    stmt = """create table a2dt2k 
(d timestamp  NOT NULL, primary key (d));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #    (d datetime year to fraction(3) NOT NULL, primary key (d));
    
    stmt = """create table a2dtup (a timestamp, b timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #create table a2dtup (a datetime year to fraction(3),
    #      b datetime year to fraction(3));
    
    stmt = """create table a2dt1d (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #create table a2dt1d (a datetime year to fraction(3));
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0167 : testA01
    #  Description:        Param assignment for datetime and interval
    #                      datatypes.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # set parameter to be used in these tests
    #   set param ?y_f3 '1989-03-25:08:43:23.123';
    stmt = """set param ?y_f3 '1989-03-25 08:43:23.123';"""
    output = _dci.cmdexec(stmt)
    
    #    show param ?y_f3;
    
    # DEFAULT DATETIME PARAM SPECIFICATION IN THE INSERT VALUE LIST
    
    stmt = """insert into a1dtyf3 values (?y_f3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  DEFAULT DATETIME PARAM SPECIFICATION IN THE SELECT LIST
    
    stmt = """select cast(?y_f3 as timestamp(3)) from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #   CAN'T CAST A TIMESTAMP PARAM as date or time
    #    select cast(?y_f3 as date)       from a1dtyf3;
    #    select cast(?y_f3 as time(3)) from a1dtyf3;
    
    #  Okay:
    stmt = """select cast(?y_f3 as timestamp) + interval '0' hour from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select cast(?y_f3 as timestamp) - interval '0' hour from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """select interval '0' hour + cast(?y_f3 as timestamp) from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select * from a1dtyf3 where a = ?y_f3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select * from a1dtyf3 where a = cast(?y_f3 as timestamp)+ interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """select * from a1dtyf3 where a = cast(?y_f3 as timestamp)- interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select * from a1dtyf3 where a = interval '0' hour + cast(?y_f3 as timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """insert into a1dtyf3 values (cast(?y_f3  AS TIMESTAMP(3)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  DATETIME PARAM SPECIFICATION WITH TYPE AS IN THE SELECT LIST
    
    stmt = """select cast(?y_f3  AS TIMESTAMP(3)) from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    stmt = """select cast(?y_f3 AS TIMESTAMP(3)) + interval '0' hour from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select cast(?y_f3  AS TIMESTAMP(3)) - interval '0' hour from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select interval '0' hour + cast(?y_f3 AS TIMESTAMP(3)) from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select * from a1dtyf3 where a = cast(?y_f3 AS TIMESTAMP(3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """select * from a1dtyf3 where a = cast(?y_f3 AS TIMESTAMP(3))
+ interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select * from a1dtyf3 where a = cast(?y_f3 AS TIMESTAMP(3))
- interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    stmt = """select * from a1dtyf3 where a = interval '0' hour + cast(?y_f3  AS
TIMESTAMP(3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    # interval fraction is not supported.
    #    select * from a1dtyf3 where cast(?y_f3  AS TIMESTAMP(3))
    #       - a = interval '0' fraction(3);
    
    stmt = """delete from a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0167 : testA02.sql
    #  Description:        Params in INSERT, UPDATE, and SELECT
    #                      - datetime values.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # SET PARAM to be used in all the tests
    #   set param ?p '1989-03-17:08:45:58.123';
    stmt = """set param ?p '1989-03-17 08:45:58.123';"""
    output = _dci.cmdexec(stmt)
    #    show param ?p;
    
    # INSERT into DATETIME tables
    stmt = """insert into a2dt1 values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a2dt2 values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a2dt1k values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a2dt2k values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Simple SELECTs: expect 1989-03-17 08:45:58.123  from each
    
    stmt = """select * from a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """select * from a2dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    stmt = """select * from a2dt1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select * from a2dt2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """select a + interval '0' hour from a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  WHERE predicates on DATETIME values
    stmt = """select * from a2dt1 where a = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """select * from a2dt1 where a + interval '0' hour = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select * from a2dt1 where a = cast(?p as timestamp(3)) + interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """select * from a2dt1k where c = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    stmt = """select * from a2dt1k where c + interval '0' hour = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    stmt = """select * from a2dt1k where c = cast(?p as timestamp(3))+ interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    #  JOIN tests
    stmt = """select * from a2dt1,  a2dt2 where a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    stmt = """select * from a2dt1k, a2dt2k where c = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    stmt = """select * from a2dt1, a2dt1k where a = c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """select * from a2dt1,  a2dt2  where a + interval '0' hour = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    stmt = """select * from a2dt1k, a2dt2k where c + interval '0' hour = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    #  SUBQUERY tests: returning one value
    stmt = """select * from a2dt1 where a = (   select * from a2dt1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """select * from a2dt1 where a = (   select * from a2dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    stmt = """select * from a2dt1k where c = (   select * from a2dt1k);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """select * from a2dt1k where c = (   select * from a2dt2k);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  SUBQUERY tests: ANY, ALL type
    stmt = """select * from a2dt1 where a in (   select * from a2dt1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    stmt = """select * from a2dt1 where a in (   select * from a2dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    # update tests
    stmt = """insert into a2dtup values (?p, ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    stmt = """show param ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update a2dtup set a = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    stmt = """update a2dtup set a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    stmt = """update a2dtup set a = a + interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    
    stmt = """update a2dtup set a = cast(?p as timestamp(3))+ interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    # insert from select
    stmt = """insert into a2dt1d select * from a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a2dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    stmt = """delete from a2dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into a2dt1d select a + interval '0' hour from a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from a2dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    
    #
    
    # cleanup the tables
    stmt = """delete from a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from a2dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from a2dt1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from a2dt2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from a2dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a1dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1itym;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1ity4m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1itdf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dt1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dt2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a2dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

