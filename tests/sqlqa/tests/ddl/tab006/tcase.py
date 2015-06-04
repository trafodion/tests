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
import defs

_testmgr = None
_testlist = []
_dci = None

# Testunit TAB006 CREATE LIKE tests
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Create TABLE like"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #A001.1 Create table A6t1 like "t6a" -no WITH clauses
    stmt = """create table a6t1 like "t6a";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.2 Create table A1t2 like "t6a" with partitions, constraints and headings
    #attributes and store by should be copied from the source table
    stmt = """create table "a6t2" like "t6a"
with partitions
with constraints
with headings;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl "a6t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.3 Create table A1t3 like t6b no WITH clauses
    stmt = """create table a6t3 like t6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.4 Create table a6t4 like t6b  with partitions, constraints and headings
    stmt = """create table a6t4 like t6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.5 Create table like one in a different schema
    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a6t5 like """ + defs.my_schema + """.t6b
with partitions
with headings;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Reset the schema
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A001.6 Create table like t6a specifying different attributes
    stmt = """create table """ + defs.my_schema1 + """.a6t6 like T6B
attributes clearonpurge, no auditcompress
-- extent (1012,1012), maxextents 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl """ + defs.my_schema1 + """.a6t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.7 Create table like t6a specifying different partition locations
    stmt = 'create table a6t7 like "t6a"'
    if hpdci.tgtSQ():
        stmt += """ range partition
(          add first key 250 location """ + gvars.g_disc8 + """,
add first key 500 location """ + gvars.g_disc9 + """,
add first key 750 location """ + gvars.g_disc10 + """,
add first key 1000 location """ + gvars.g_disc3 + """);"""
    elif hpdci.tgtTR():
        stmt += """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.8 Create table like t6a specifying different store-by order
    stmt = 'create table a6t8 like "t6a"'
    if hpdci.tgtSQ():
        stmt += """ store by ( "time6_()", dec_9)
range partition (add first key time '12:40:44' location """ + gvars.g_disc0 + """);"""
    elif hpdci.tgtTR():
        stmt += """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.9 Create table like t6a after t6a has been altered to have partitioned
    #       unique index constraint
    stmt = """create unique index ut6a on "t6a" (small_6)
range partition (
add first key 55 location """ + gvars.g_disc0 + """,
add first key 155 location """ + gvars.g_disc6 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table "t6a" add unique(small_6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    #A001.10 Create table like hash-partitioned table, specifying range partitions
    stmt = """create table a6t10 like t6b with headings"""
    if hpdci.tgtSQ():
        stmt += """ range partition
(add first key date '2002-05-01' location """ + gvars.g_disc6 + """);"""
    elif hpdci.tgtTR():
        stmt += """;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A001.11 Create table like 
    stmt = """create table a6t11 like "t6a"
with headings
location """ + gvars.g_disc9 + """
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a6t11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Create TABLE like"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Create Table btpnl21_2
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
range partition (add first key  (33,0,'DAAAAAAA') location """ + gvars.g_disc2 + """,
add first key  (67,0,'DAAAAAAA') location """ + gvars.g_disc3 + """)
attributes    

extent(1024,1024),
maxextents 700
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.1 create table like by specifying extent and maxextents
    stmt = """create table t1206 like btpnl21_2
location """ + gvars.g_disc2 + """
attribute extent(512,512),maxextents 768;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.2 create table like with no extent and maxextents specified
    stmt = """create table t1216 like btpnl21_2
location """ + gvars.g_disc2 + """
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table T1206;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table T1216;"""
    output = _dci.cmdexec(stmt)
    
    #A002.3 create table like with long tab name.
    stmt = """create table
Z123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
like "t6a";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.4 delimited tab name.
    stmt = """create table
"z123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567"
like "t6a";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.5 create table like with attribute allocate
    stmt = """create table """ + defs.my_schema1 + """.a62t5 like btpnl21_2
--create table a62t5 like btpnl21_2
attributes clearonpurge, no auditcompress
, allocate 12
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A002.6 create table like with out of range maxextent
    stmt = """create table t12061 like btpnl21_2
location """ + gvars.g_disc2 + """
attribute extent(512,512),maxextents 769;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop table t12061;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btpnl21_2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + defs.my_schema1 + """.a62t5;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Negative CREATE table LIKE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #N001.1 Create table like index
    stmt = """create table N1t1 like it6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N001.2 Create table like MP table
    stmt = """create table n1t2 like """ + gvars.g_disc9 + """.kate.n1t2mp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #N001.3 Create table like t6b with partitions, specifying new partitions
    stmt = """create table clone6b like t6b
with partitions
hash partition by (sbin0_4)
(add location """ + gvars.g_disc0 + """, add location """ + gvars.g_disc9 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N001.4 Create table like t6b with partitions and store-by order
    stmt = """create table n1t7 like "t6a"
with headings
with partitions
store by (real_12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N001.5 Create table like view.
    #In trafodion, create a table like a view is allowed.
    stmt = """create table n1t5 like vt6b;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1127')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)

    #N001.6 Create view like view
    stmt = """create view vt699 like v6tb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Tests for fixes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #A003.1 Create table a3t1 like "t6a" with partitions, constraints and headings
    #attributes and store by should be copied from the source table
    
    stmt = """create table "a3t1" like "t6a"
with partitions
with constraints
with headings;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "a3t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl "a3t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """STORE BY (NUMERIC_5 ASC, PIC_10 ASC)""")
    
    #A003.2 create table with constraint should copy the not null
    #constraint from the original table
    
    stmt = """create table a3t2
(
c int not null not droppable primary key
)
attributes extent (16,16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a3t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showcontrol default "NOT_NULL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showcontrol all;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a3t22 like a3t2 with constraints;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a3t22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default NOT_NULL_CONSTRAINT_DROPPABLE_OPTION 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a3t23;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a3t23 like a3t2 with constraints;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl a3t23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Table created in setup
    #A003.3 create table like with heading where the heading has
    #two single quotes returns an error
    
    stmt = """drop table a3t3b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a3t3b
like a3t3a with headings;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

