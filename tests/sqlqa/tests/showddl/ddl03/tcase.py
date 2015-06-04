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
# testunit ddl03
# data in /g_data/sqldopt

import time
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def save_ddl_to_obeyfile(objname1, objname2, filename, schema=''):

    tmpfile = defs.work_dir + """/pass1_tmpfile"""

    output = _testmgr.shell_call("""rm """ + tmpfile)
    output = _testmgr.shell_call("""rm """ + filename)

    stmt = """log """ + tmpfile + """ clear, cmdtext off;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl """ + objname1 + """;"""
    output = _dci.cmdexec(stmt)
    if objname2 != '':
        stmt = """showddl """ + objname2 + """;"""
        output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    if schema == '':
        schema = defs.my_schema
    output = _testmgr.shell_call("""echo 'set schema """ + schema + """;' > """ + filename)
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v 'showddl' | grep -v 'operation'  | grep -v '>>' | grep -v 'log'  >> """ + filename)
    # For triggers in case there is one
    output = _testmgr.shell_call("""echo '/' >> """ + filename)
    # IF the previous showddl got an error, the following ';' will make sure
    # that DCI does sit in a prompt when we feed this obey file to it.
    outout = _testmgr.shell_call("""echo ';' >> """ + filename)
    outout = _testmgr.shell_call("""echo 'exit;' >> """ + filename)

def save_ddl_to_obeyfile1(objname1, objname2, filename, schema=''):

    tmpfile = defs.work_dir + """/pass1_tmpfile"""

    output = _testmgr.shell_call("""rm """ + tmpfile)
    output = _testmgr.shell_call("""rm """ + filename)

    stmt = """log """ + tmpfile + """ clear, cmdtext off;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl """ + objname1 + """;"""
    output = _dci.cmdexec(stmt)
    if objname2 != '':
        stmt = """showddl """ + objname2 + """;"""
        output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    if schema == '':
        schema = defs.my_schema
    output = _testmgr.shell_call("""echo 'set schema """ + schema + """;' > """ + filename)
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v showddl | grep -v operation  | grep -v '>>' | grep -v log  >> """ + filename)
    # For triggers in case there is one
    output = _testmgr.shell_call("""echo '/' >> """ + filename)
    # IF the previous showddl got an error, the following ';' will make sure
    # that DCI does sit in a prompt when we feed this obey file to it.
    outout = _testmgr.shell_call("""echo ';' >> """ + filename)
    outout = _testmgr.shell_call("""echo 'exit;' >> """ + filename)
    
def save_ddl_to_obeyfile2(objname1, objname2, filename, schema=''):

    tmpfile = defs.work_dir + """/pass1_tmpfile"""

    output = _testmgr.shell_call("""rm """ + tmpfile)
    output = _testmgr.shell_call("""rm """ + filename)

    stmt = """log """ + tmpfile + """ clear, cmdtext off;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl """ + objname1 + """;"""
    output = _dci.cmdexec(stmt)
    if objname2 != '':
        stmt = """showddl """ + objname2 + """;"""
        output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    if schema == '':
        schema = defs.my_schema
    output = _testmgr.shell_call("""echo 'set schema """ + schema + """;' > """ + filename)
    output = _testmgr.shell_call("""cat """ + tmpfile + """ |  grep -v operation  | grep -v log  >> """ + filename)
    # For triggers in case there is one
    output = _testmgr.shell_call("""echo '/' >> """ + filename)
    # IF the previous showddl got an error, the following ';' will make sure
    # that DCI does sit in a prompt when we feed this obey file to it.
    outout = _testmgr.shell_call("""echo ';' >> """ + filename)
    outout = _testmgr.shell_call("""echo 'exit;' >> """ + filename)
    
def save_ddl_to_obeyfile3(objname1, objname2, filename, schema=''):

    tmpfile = defs.work_dir + """/pass1_tmpfile"""

    output = _testmgr.shell_call("""rm """ + tmpfile)
    output = _testmgr.shell_call("""rm """ + filename)

    stmt = """log """ + tmpfile + """ clear, cmdtext off;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl """ + objname1 + """;"""
    output = _dci.cmdexec(stmt)
    if objname2 != '':
        stmt = """showddl """ + objname2 + """;"""
        output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    if schema == '':
        schema = defs.my_schema
    output = _testmgr.shell_call("""echo 'set schema """ + schema + """;' > """ + filename)
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v log  >> """ + filename)
    # For triggers in case there is one
    output = _testmgr.shell_call("""echo '/' >> """ + filename)
    # IF the previous showddl got an error, the following ';' will make sure
    # that DCI does sit in a prompt when we feed this obey file to it.
    outout = _testmgr.shell_call("""echo ';' >> """ + filename)
    outout = _testmgr.shell_call("""echo 'exit;' >> """ + filename)
    
    
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()


# *****************************************************************************
#testcase a01 Hash partitioned tables with default attributes
# *****************************************************************************
#expect purge immediate
def test001(desc="""a01 Hash partitioned tables with default attributes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a01.1 small simple table with no pk specified and default attributes used.
    # catalog.schema.name
    stmt = """create table """ + defs.my_schema + """.t1a011(col1 int not null , col2 int)
store by (col1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl """ + defs.my_schema + """.t3a031;"""
    output = _dci.cmdexec(stmt)


    stmt = """create table t1a011_2(col1 int not null , col2 int) 
store by (col1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1a011_2 values (1,1), (2,1), (3,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """showddl t1a011_2;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t1a011_2;"""
    output = _dci.cmdexec(stmt)

    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    stmt = """create table t1a011_2new like t1a011_2 with constraints with headings with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1a011_2new values (1,1), (2,1), (3,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    save_ddl_to_obeyfile("""t1a011_2""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t1a011_2; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 

    stmt = """insert into t1a011_2 select * from t1a011_2new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """showddl t1a011_2;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t1a011_2;"""
    output = _dci.cmdexec(stmt)
    
    # a01.2 larger table with no pk specified default attribute used, location specified.

    # btuwl02
    stmt = """create table t1a012
  (
     sbin0_500        PIC S9(18) COMP   not null,
     char0_10         PIC X(4)          not null,
     udec0_2000       PIC 9(9)          not null,
     ubin0_1000       PIC 9(9) COMP     not null,
     sdec0_uniq       PIC S9(9)         not null,
     varchar0_4       varchar(8)   not null,

     sbin1_100        Numeric(9) signed     not null,
     char1_4          PIC X(5)   not null, -- len = 2,4
     udec1_10         PIC 9(9)              not null,
     ubin1_4          Numeric(9) unsigned   not null,
     sdec1_2          PIC S9(9)             not null,

     sbin2_2          PIC S9(2) COMP   not null,
     ubin2_4          PIC 9(2) COMP    not null,
     sdec2_10         PIC S9(2)        not null,
     char2_2          PIC X(2)         not null,
     udec2_100        PIC 9(2)         not null,

     sbin3_1000       Numeric(5) signed     not null,
     udec3_2000       PIC 9(5)              not null,
     char3_1000       PIC X(300)   not null, -- len = 64,300
     sdec3_500        PIC S9(5)             not null,
     ubin3_uniq       Numeric(5) unsigned   not null,

     sbin4_2          Numeric(1,1) signed     not null,
     ubin4_4          Numeric(1,1) unsigned   not null,
     char4_10         Character(5)   not null, -- len = 2,4
     sdec4_10         Decimal(1,1) signed     not null,
     udec4_2          Decimal(1,1) unsigned   not null,

     sbin5_4          Numeric(4) signed     not null,
     ubin5_20         Numeric(9) unsigned   not null,
     udec5_20         Decimal(4) unsigned   not null,
     varchar5_10      VarChar(8)       not null,
     sdec5_100        Decimal(18) signed    not null,

     sbin6_uniq       PIC S9(4) COMP   not null,
     sdec6_2000       PIC S9(4)        not null,
     udec6_500        PIC 9(4)         not null,
     char6_20         PIC X(8)         not null,
     ubin6_2          PIC 9(4) COMP    not null,

     sbin7_2          SMALLINT signed         not null,
     sdec7_10         Decimal(4,1) signed     not null,
     char7_uniq       Character(100)   not null, -- len = 16
     udec7_20         Decimal(4,1) unsigned   not null,
     ubin7_100        SMALLINT unsigned       not null,

     sbin8_1000       Numeric(18) signed      not null,
     char8_500        PIC X(100)   not null, -- len = 16
     sdec8_2000       PIC S9(3)V9             not null,
     udec8_500        PIC 9(3)V9              not null,
     ubin8_2          Numeric(4,1) unsigned   not null,

     sbin9_4          PIC S9(3)V9 COMP      not null,
     char9_uniq       Character(8)          not null,
     udec9_10         Decimal(5) unsigned   not null,
     sdec9_20         Decimal(5) signed     not null,
     ubin9_100        PIC 9(3)V9 COMP       not null,

     sbin10_uniq      PIC S9(9) COMP   not null,
     ubin10_1000      PIC 9(9) COMP    not null,
     char10_20        PIC X(5)   not null, -- len = 2,4
     udec10_2000      PIC 9(9)         not null,
     sdec10_500       PIC S9(18)       not null,

     sbin11_2000      PIC S9(5) COMP          not null,
     sdec11_20        Decimal(5,5) signed     not null,
     udec11_20        Decimal(5,5) unsigned   not null,
     ubin11_2         PIC 9(5) COMP           not null,
     char11_4         Character(2)            not null,

     sbin12_1000      Numeric(9) signed     not null,
     sdec12_100       PIC S9(9)             not null,
     char12_10        PIC X(2)              not null,
     ubin12_10        Numeric(9) unsigned   not null,
     udec12_1000      PIC 9(9)              not null,

     sbin13_uniq      PIC SV9(5) COMP       not null,
     char13_100       Character(5)   not null, -- len = 2,4
     sdec13_uniq      Decimal(9) signed     not null,
     ubin13_10        PIC V9(5) COMP        not null,
     udec13_500       Decimal(9) unsigned   not null,

     sbin14_100       Numeric(2) signed     not null,
     ubin14_2         Numeric(2) unsigned   not null,
     sdec14_20        Decimal(2) signed     not null,
     udec14_10        Decimal(2) unsigned   not null,
     char14_20        Character(2)          not null,

     sbin15_2         INTEGER signed          not null,
     udec15_4         Decimal(9,2) unsigned   not null,
     varchar15_uniq   VarChar(8)         not null,
     ubin15_uniq      INTEGER unsigned        not null,
     sdec15_10        Decimal(9,2) signed     not null,

     sbin16_20        Numeric(9,2) signed     not null,
     sdec16_100       PIC S9(7)V9(2)          not null,
     ubin16_1000      Numeric(9,2) unsigned   not null,
     udec16_1000      PIC 9(7)V9(2)           not null,
     char16_uniq      PIC X(8)                not null,

     sbin17_uniq      Numeric(10) signed    not null,
     sdec17_20        Decimal(2) signed     not null,
     ubin17_2000      PIC 9(7)V9(2) COMP    not null,
     char17_100       Character(100)   not null, -- len = 16
     udec17_100       Decimal(2) unsigned   not null,

     sbin18_uniq      Numeric(18) signed   not null,
     char18_20        PIC X(100)           not null, -- len = 16
     ubin18_20        PIC 9(2) COMP        not null,
     sdec18_4         PIC S9(2)            not null,
     udec18_4         PIC 9(2)             not null,

     sbin19_4         LARGEINT signed         not null,
     char19_2         Character(8)            not null,
     ubin19_10        SMALLINT unsigned       not null,
     udec19_100       Decimal(4,1) signed     not null,
     sdec19_1000      Decimal(4,1) unsigned   not null,

     sbin20_2000      PIC S9(16)V9(2) COMP   not null,
     udec20_uniq      PIC 9(9)               not null,
     ubin20_1000      PIC 9(3)V9 COMP        not null,
     char20_10        PIC X(300)   not null, -- len = 64,300
     sdec20_uniq      PIC S9(9)   not null -- range: 0-24999
   )
   store by ( sbin10_uniq )
   ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t1a012 -I $data_dir/btuwl02.dat

    stmt = """showddl t1a012;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t1a012;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile("""t1a012""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t1a012; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t1a012 -I $data_dir/btuwl02.dat

    stmt = """showddl t1a012;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t1a012;"""
    output = _dci.cmdexec(stmt)
        
    _testmgr.testcase_end(desc)
    
# *****************************************************************************
#testcase a02 Hash partitioned table with store by clause
# *****************************************************************************
#expect purge immediate

def test002(desc="""a02 Hash partitioned table with store by clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a02.1 create table with store by clause (ascending ) --local partitions only

    # b2unl11
    stmt = """Create Table t2a021
  (
     int0_yTOm_uniq      Interval year(5) to month  no default not null,
     sbin0_20p           Largeint                   no default not null,
     sdec0_nuniq         Decimal(18)                       default null,
     ts0_uniq            Timestamp               not null,
     char0_uniq          Character(8)            not null,

     udec1_n2            Decimal(4) unsigned             ,
     dt1_yTOmin_n100     Timestamp(0),
     real1_uniq          Real                       no default not null,
     ubin1_1000          Numeric(4) unsigned        no default not null,
     int1_dTOf6_n10      Interval day to second(6)         no default
  )
  store by ( ts0_uniq asc, int0_yTOm_uniq  ascending, real1_uniq asc )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t2a021 -I $data_dir/b2unl11.dat

    stmt = """showddl t2a021;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t2a021;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile1("""t2a021""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t2a021; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t2a021 -I $data_dir/b2unl11.dat

    stmt = """showddl t2a021;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t2a021;"""
    output = _dci.cmdexec(stmt)
    
    #  created_a02_2.txt is created dynamically.
    #  it will be empty if the system has only one segment.
    #  it will have a02_2.txt testcase if the system has more than one segment.
    #  this process is done in setup file.

    #  #runscript ${testdir}/a02_2.txt
    # a02.3 create large table with store by clause (ascending and descending)

    # b2uwl04
    stmt = """Create Table t2a023
   (
     sbin0_4             Integer                    default 3 not null,
     time0_uniq          Time                       not null,
     varchar0_uniq       VarChar(8)                 no default not null,
     sdec0_100           Decimal(9)                 no default not null,
     int0_dTOf6_4        Interval day to second(6)  not null,
     ts1_n100            Timestamp
                           heading 'ts1_n100 allowing nulls',
     sdec1_20            Decimal(5)                 no default not null,
     int1_yTOm_n100      Interval year(1) to month  no default,
     double1_2           Double Precision           not null,
     udec1_nuniq         Decimal(4) unsigned        ,
     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                   ,
     sdec2_500           Decimal(9) signed          no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)  no default,
     real2_500           Real                       not null,
     real3_n1000         Real                       ,
     int3_yTOm_4         Interval year(1) to month  no default not null,
     date3_n2000         Date                       no default,
     udec3_n100          Decimal(9) unsigned        ,
     ubin3_n2000         Numeric(4) unsigned        ,
     char3_4             Character(8)               no default not null,
     sdec4_n20           Decimal(4)                 no default,
     int4_yTOm_uniq      Interval year(5) to month  not null,
     sbin4_n1000         Smallint                   ,
     time4_1000          Time                       no default not null,
     char4_n10           Character(8)               no default,
     real4_2000          Real                       not null,
     char5_n20           Character(8)               ,
     sdec5_10            Decimal(9) signed          no default not null,
     ubin5_n500          Numeric(9) unsigned        no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)               ,
     int5_hTOs_500       Interval hour to second(0) no default not null,
     int6_dTOf6_nuniq    Interval day to second(6)  no default,
     sbin6_nuniq         Largeint                   no default,
     double6_n2          Float(23)                  ,
     sdec6_4             Decimal(4) signed          no default not null,
     char6_n100          Character(8)               no default,
     date6_100           Date                       not null,
     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                   no default,
     char7_500           Character(8)               no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0) ,
     udec7_n10           Decimal(4) unsigned        ,
     real7_n4            Real                       ,
     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)           ,
     date8_10            Date                       no default not null,
     char8_n1000         Character(8)               no default,
     double8_n10         Double Precision           no default,
     sdec8_4             Decimal(9) unsigned        not null,
     sdec9_uniq          Decimal(18) signed         no default not null,
     real9_n20           Real                       ,
     time9_n4            Time                       ,
     char9_100           Character(2)               no default not null,
     int9_dTOf6_2000     Interval day to second(6)  no default not null,
     ubin9_n4            Numeric(9) unsigned        no default,
     ubin10_n2           Numeric(4) unsigned        no default,
     char10_nuniq        Character(8)               ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                  ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned        no default not null,
     udec11_2000         Decimal(9) unsigned        no default not null,
     int11_h_n10         Interval hour(1)           no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision           ,
     real12_n20          Real                       ,
     ubin12_2            Numeric(4) unsigned        no default not null,
     dt12_mTOh_1000      Timestamp(0)               no default not null,
     sdec12_n1000        Decimal(18) signed         no default,
     char12_n2000        Character(8)               no default,
     int12_yTOm_100      Interval year to month     not null,
     int13_yTOm_n1000    Interval year to month     ,
     udec13_500          Decimal(9) unsigned        no default not null,
     sbin13_n100         PIC S9(8)V9 COMP           no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                       ,
     sbin14_1000         Integer                    no default not null,
     double14_nuniq      Float(23)                  no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)               ,
     int14_d_500         Interval day(3)            no default not null,
     ts14_n100           Timestamp                  no default,
     dt15_mTOh_n100      Timestamp(0)               no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                   ,
     sdecneg15_100       Decimal(9) signed          no default not null,
     int15_dTOf6_n100    Interval day to second(6)  no default,
     char15_100          Character(8)               not null,
     dt16_m_n10          Date                       ,
     int16_h_20          Interval hour              no default not null,
     ubin16_n10          Numeric(4) unsigned        no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)               ,   -- len = 2,4
     real16_10           Real                       no default not null,
     int17_y_n10         Interval year(1)           no default,
     dt17_yTOmin_uniq    Timestamp(0)               not null,
     real17_n100         Real                       ,
     sbin17_uniq         Largeint                   no default not null,
                                                    -- range: 0-149999
     sdec17_nuniq        Decimal(18)                no default,
     char17_2            Character(8)               not null
    )
    store by ( sdec9_uniq ASC, sdec0_100 DESC, sdec1_20  ASC)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t2a023 -I $data_dir/b2uwl04.dat

    stmt = """showddl t2a023;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t2a023;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile1("""t2a023""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t2a023; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t2a023 -I $data_dir/b2uwl04.dat
    
    stmt = """showddl t2a023;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t2a023;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
# *****************************************************************************
#testcase a03 Hash partitioned tables with pk column and table constraints
# *****************************************************************************

#expect purge immediate
def test003(desc=""" a03 Hash partitioned tables with pk column and table constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a03.1 create table with pk as column constraint

    # b2unl15
    stmt = """Create Table t3a031
  (
     char0_100           Character(8)  not null constraint a3t1_1 check(char0_100 <> 'Z'),
     -- sbin0_uniq          Integer  not null unique,
     sbin0_uniq          Integer  not null primary key asc not droppable,
     sdec0_n10           Decimal(4)           default 9 
                         constraint a3t1_2 check (sdec0_n10 between 0 and 15000),
     int0_yTOm_n1000     Interval year(2) to month         no default,
     date0_nuniq         Date no default check (date0_nuniq < date '3000-01-06'),

     -- real1_uniq          Real not null primary key asc not droppable,
     real1_uniq          Real not null ,
     ts1_n100            Timestamp                     ,
     ubin1_500           Numeric(4) unsigned      no default not null,
     int1_dTOf6_nuniq    Interval day to second(6)       no default,
     udec1_50p Decimal(9) unsigned not null 
  )
  ATTRIBUTES EXTENT (1024, 1024), MAXEXTENTS 160
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t3a031 -I $data_dir/b2unl15.dat

    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile1("""t3a031""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t3a031; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t3a031 -I $data_dir/b2unl15.dat

    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

# *****************************************************************************
#testcase a04 Hash partitioned table with primary key and store by specified
# *****************************************************************************
#expect purge immediate

def test004(desc=""" a04 Hash partitioned table with primary key and store by specified"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a04.1 create table with pk and store by ( same as pk)

    # b2unl17
    stmt = """Create Table t4a041
  (
     char0_100           Character(8)          not null,
     sbin0_uniq          Integer               not null,
     sdec0_n10           Decimal(4)                         default 9,
     int0_yTOm_n1000     Interval year(2) to month         no default,
     date0_n1000         Date                              no default,

     real1_uniq          Real                  not null,
     dt1_yTOmin_nuniq    Timestamp(0),
     ubin1_500           Numeric(4) unsigned      no default not null,
     int1_dTOf6_nuniq    Interval day(3) to second(6)    no default,
     udec1_50p           Decimal(9) unsigned   not null,

  primary key ( sbin0_uniq desc ) not droppable
  )
  attributes
  extent (1024, 1024)
  maxextents 760
  store by ( sbin0_uniq desc)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t4a041 -I $data_dir/b2unl17.dat

    stmt = """showddl t4a041;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile2("""t4a041""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t4a041; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t4a041 -I $data_dir/b2unl17.dat

    stmt = """showddl t4a041;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    #  created_a04_2.txt is created dynamically.
    #  it will be empty if the system has only one segment.
    #  it will have a04_2.txt testcase if the system has more than one segment.
    #  this process is done in setup file.

    #  #runscript ${testdir}/a04_2.txt

    #  created_a04_3.txt is created dynamically.
    #  it will be empty if the system has only one segment.
    #  it will have a04_3.txt testcase if the system has more than one segment.
    #  this process is done in setup file.

    #  #runscript ${testdir}/a04_3.txt

    _testmgr.testcase_end(desc)

# *****************************************************************************
#testcase a05 Hash partitioned table with attributes and locations
# *****************************************************************************
#expect purge immediate

def test005(desc=""" a05 Hash partitioned table with attributes and locations"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a05.1 create table with some attributes specified, volume specified

    # b2uns01
    stmt = """Create Table t5a051
  (
     char0_n10           Character(2)
                   default 'AD' heading 'char0_n10 with default AD',
     sbin0_uniq          Smallint              not null,
     sdec0_n500          Decimal(18)                   ,
     date0_uniq          Date                     no default not null,
     int0_yTOm_nuniq     Interval year(5) to month         no default,

     int1_hTOs_1000      Interval hour(2) to second  not null,
     date1_n4            Date                          ,
     real1_uniq          Real                     no default not null,
     ubin1_n2            Numeric(4) unsigned               no default,
     udec1_100           Decimal(2) unsigned    not null,
     primary key (sbin0_uniq)
  )
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (512, 512)
  maxextents 768
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t5a051 -I $data_dir/b2uns01.dat

    stmt = """showddl t5a051;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t5a051;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile2("""t5a051""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t5a051; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t5a051 -I $data_dir/b2uns01.dat

    stmt = """showddl t5a051;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t5a051;"""
    output = _dci.cmdexec(stmt)
    
    # a05.2 create table with all the attributes specified, node and volume specified

    # b2uwl14
    stmt = """Create Table t5a052
   (
     date0_n100          Date                                 default null,
     sbin0_4             Smallint                   not null,
     sdec0_n100          Decimal(2)                         ,
     int0_dTOf6_uniq     Interval day to second(6)    no default not null,
     varchar0_n1000      VarChar(8)                        no default,

     udec1_500           Decimal(9) unsigned        not null,
     real1_n100          Real                               ,
     ubin1_uniq          Numeric(9) unsigned           no default not null,
     ts1_nuniq           Timestamp                              no default,
     int1_yTOm_100       Interval year to month     not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_dTOf6_uniq ) not droppable
  )
  store by primary key
  attributes 
  allocate 1
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (64, 51200)
  maxextents 128 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t5a052 -I $data_dir/b2uwl14.dat

    stmt = """showddl t5a052;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t5a052;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile1("""t5a052""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t5a052; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t5a052 -I $data_dir/b2uwl14.dat
    
    stmt = """showddl t5a052;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t5a052;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

# *****************************************************************************
#testcase a06 Long table and column names -Hash partitioned table
# *****************************************************************************
#expect purge immediate

def test006(desc="""a06 Long table and column names -Hash partitioned table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a06.1 create table with long name
    # b2uns03
    stmt = """Create Table 
Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
  (
     sbin0_4             Integer                   default 3 not null,
     time0_uniq          Time                  not null,
     varchar0_uniq       varchar(8)          no default not null,
     sdec0_n1000         Decimal(9)                        no default,
     int0_dTOf6_4        Interval day to second(6)  not null,

     ts1_n100            Timestamp
                      heading 'ts1_n100 allowing nulls',
     ubin1_20            Numeric(9) unsigned      no default not null,
     int1_yTOm_n100      Interval year(1) to month         no default,
     double1_2           Double Precision      not null,
     udec1_nuniq         Decimal(4) unsigned           ,

  primary key ( time0_uniq  DESC) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    
    #expect purge immediate
    stmt = """drop table Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a06.2 create table with long schema and table name
    # 127 characters long
    stmt = """create schema """+ defs.w_catalog +""".Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M123456;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 128 characters long
    #stmt = """create schema $testcat.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    # set schema $testcat.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;
    
    # set schema $testcat.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;
 
    # b2uns03
    # #expect any *--- SQL operation complete.*
    # Create Table 
    # $testcat.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M123456.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
    #   (
    #      sbin0_4             Integer                   default 3 not null,
    #      time0_uniq          Time                  not null,
    #      varchar0_uniq       varchar(8)          no default not null,
    #      sdec0_n1000         Decimal(9)                        no default,
    #      int0_dTOf6_4        Interval day to second(6)  not null,
    # 
    #      ts1_n100            Timestamp
    #                       heading 'ts1_n100 allowing nulls',
    #      ubin1_20            Numeric(9) unsigned      no default not null,
    #      int1_yTOm_n100      Interval year(1) to month         no default,
    #      double1_2           Double Precision      not null,
    #      udec1_nuniq         Decimal(4) unsigned           ,
    # 
    #   primary key ( time0_uniq  DESC) not droppable
    #   )
    #   store by primary key
    #   ;

    # showddl 
    # Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
    # ;

    # a06.3 create table with long catalog, schema, and table name

    # 128 characters
    # #expect any *--- SQL operation complete.*
    #expect any *4222*
    stmt = """create schema PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    stmt = """set schema PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # b2uns03
    # #expect any *--- SQL operation complete.*
    stmt = """create table
PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
  (
     sbin0_4             Integer                   default 3 not null,
     time0_uniq          Time                  not null,
     varchar0_uniq       varchar(8)          no default not null,
     sdec0_n1000         Decimal(9)                        no default,
     int0_dTOf6_4        Interval day to second(6)  not null,

     ts1_n100            Timestamp
                      heading 'ts1_n100 allowing nulls',
     ubin1_20            Numeric(9) unsigned      no default not null,
     int1_yTOm_n100      Interval year(1) to month         no default,
     double1_2           Double Precision      not null,
     udec1_nuniq         Decimal(4) unsigned           ,

  primary key ( time0_uniq  DESC) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 -I $data_dir/b2uns03.dat

    
    stmt = """showddl Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel
Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile3("""Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567; """
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 -I $data_dir/b2uns03.dat

    stmt = """showddl Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel
Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567
;"""
    output = _dci.cmdexec(stmt)
    
    # a06.4 create table with long column names
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  #expect any *--- SQL operation complete.*
    stmt = """create table t6a064
(
a int not null,
b int not null not droppable,
Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 int not null,
primary key ( b desc, a))
store by (b desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'1193')
    
    stmt = """create table t6a064
(
a int not null,
b int not null not droppable,
Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 int not null,
primary key ( b desc, a))
store by (b desc,a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t6a064  values 
(1,1,11),(1,11,12),(1,12,13),
(1,2,21),(1,21,22),(1,22,23),
(2,1,31),(2,11,32),(2,12,33),
(2,2,41),(2,21,42),(2,22,43),
(3,1,51),(3,11,52),(3,12,53),
(3,2,61),(3,21,62),(3,22,63);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,18)
    
    stmt = """showddl t6a064;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t6a064;"""
    output = _dci.cmdexec(stmt)

    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    stmt = """create table t6a064new like t6a064 with constraints with headings with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t6a064new  values 
(1,1,11),(1,11,12),(1,12,13),
(1,2,21),(1,21,22),(1,22,23),
(2,1,31),(2,11,32),(2,12,33),
(2,2,41),(2,21,42),(2,22,43),
(3,1,51),(3,11,52),(3,12,53),
(3,2,61),(3,21,62),(3,22,63);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,18)
    
    save_ddl_to_obeyfile1("""t6a064""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t6a064; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """insert into t6a064  select * from t6a064new ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,18)
    
    stmt = """showddl t6a064;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t6a064;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema """ + defs.w_catalog +""".Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M123456 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567.Y123456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    stmt = """unregister catalog PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567 from $sysname_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'ERROR')
    
    stmt = """drop catalog PQ23456789B123456789C123456789D123456789E123456789F123456789G123456789H123456789I123456789J123456789K123456789L123456789M1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')

    _testmgr.testcase_end(desc)

# *******************************************************************************
# *****************************************************************************
#testcase a08 Column headings -Hash partitioned table
# *****************************************************************************
#expect purge immediate
def test008(desc="""a08 Column headings -Hash partitioned table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a08.1 create table with column headings different from column name
    # b2uns07
    # #expect any *SQL operation complete.
    stmt = """Create Table t8a081
  (
     sdec0_20            Decimal(4) not null heading 'ColumN_1' ,
     ts0_nuniq           Timestamp       heading 'ColumN_2'              ,
     sbin0_uniq          Smallint          no default not null heading 'column 3',
     int0_d_uniq         Interval day(6)          no default not null heading 'column 4',
     char0_n500          Character(8)                      no default heading 'column 5',

     double1_10          Double Precision   default 1.0004E1 not null heading 'column 6',
     ubin1_4             Numeric(4) unsigned      no default not null heading 'column 7',
     dt1_yTOmin_nuniq    Timestamp(0) heading 'column 8',
     udec1_500           Decimal(4) unsigned   not null heading 'column 9',
     int1_y_nuniq        Interval year(4)   heading 'column 10' ,

  primary key ( int0_d_uniq DESC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a081 -I $data_dir/b2uns07.dat
    
    stmt = """showddl t8a081;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t8a081;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile1("""t8a081""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t8a081;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a081 -I $data_dir/b2uns07.dat

    stmt = """showddl t8a081;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t8a081;;"""
    output = _dci.cmdexec(stmt) 

    # a08.2 create table wtih column headings same as column name

    # b2uns07
    stmt = """Create Table t8a082
  (
     sdec0_20            Decimal(4) not null heading 'SDEC0_20' ,
     ts0_nuniq           Timestamp       heading 'TS0_NUNIQ'    ,
     sbin0_uniq          Smallint      no default not null heading 'SBIN0_UNIQ',
     int0_d_uniq         Interval day(6) 
                                      no default not null heading 'INT0_D_UNIQ',
     char0_n500          Character(8)         no default heading 'CHAR0_N500',

     double1_10          Double Precision   
                                default 1.0004E1 not null heading 'DOUBLE1_10',
     ubin1_4             Numeric(4) unsigned      
                                       no default not null heading 'UBIN1_4',
     dt1_yTOmin_nuniq    Timestamp(0) heading 'DT1_YTOMIN_NUNIQ',
     udec1_500           Decimal(4) unsigned   not null heading 'UDEC1_500',
     int1_y_nuniq        Interval year(4)               heading 'INT1_Y_NUNIQ',

  primary key ( int0_d_uniq DESC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a082 -I $data_dir/b2uns07.dat

    stmt = """showddl t8a082;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showlabel t8a082;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile1("""t8a082""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t8a082;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a082 -I $data_dir/b2uns07.dat

    stmt = """showddl t8a082;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t8a082;"""
    output = _dci.cmdexec(stmt) 
    
    # a08.3 create table with column headings same as column name in lowercase

    # b2uns07
    stmt = """Create Table t8a083
  (
     sdec0_20            Decimal(4) not null heading 'sdec0_20' ,
     ts0_nuniq           Timestamp       heading 'ts0_nuniq'              ,
     sbin0_uniq          Smallint      no default not null heading 'sbin0_uniq',
     int0_d_uniq         Interval day(6)          no default not null,
     char0_n500          Character(8)                      no default,

     double1_10          Double Precision   default 1.0004E1 not null,
     ubin1_4             Numeric(4) unsigned      no default not null,
     dt1_yTOmin_nuniq    Timestamp(0),
     udec1_500           Decimal(4) unsigned   not null,
     int1_y_nuniq        Interval year(4)              ,

  primary key ( int0_d_uniq DESC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a083 -I $data_dir/b2uns07.dat
    
    stmt = """showddl t8a083;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showlabel t8a083;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t8a083""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t8a083;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t8a083 -I $data_dir/b2uns07.dat

    stmt = """showddl t8a083;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t8a083;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
    
# *****************************************************************************
#testcase a09 Hash partitioned table with unique index
# *****************************************************************************
#expect purge immediate
def test009(desc="""a09 Hash partitioned table with unique index"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table t9a091 cascade;"""
    output = _dci.cmdexec(stmt)
    
    # a09.1 create table with unique index (asceding and descending)
    # b2uwl10
    # #expect any *SQL operation complete.
    stmt = """Create Table t9a091
   (
     char0_100           Character(9)                  no default not null,
     sbin0_100           Integer                       no default not null,
     int0_dTOf6_n100     Interval day to second(6)            no default,
     sdec0_nuniq         Decimal(9)                             no default,
     time0_nuniq         Time                               ,

     dt1_mTOh_n20        Timestamp(0)             ,
     udec1_2             Decimal(9) unsigned        not null,
     int1_h_n10          Interval hour(1)     default interval '8' hour(1),
     ubin1_uniq          Numeric(9) unsigned        not null,
     real1_uniq          Real                          no default not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  ts13_uniq ) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #expect any *--- SQL operation complete.*
    stmt = """create unique index ixt09a091 on 
t9a091(ubin1_uniq asc, date2_uniq asc);"""
    output = _dci.cmdexec(stmt) 

    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a091 -I $data_dir/b2uwl10.dat

    stmt = """showddl t9a091;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a091;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t9a091""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t9a091;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a091 -I $data_dir/b2uwl10.dat

    stmt = """showddl t9a091;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a091;"""
    output = _dci.cmdexec(stmt) 

    stmt = """drop table t9a092 cascade;"""
    output = _dci.cmdexec(stmt) 
    
    # a09.2 create table with several unique indexes (asceding and descending)

    stmt = """Create Table t9a092
   (
     char0_100           Character(9)                  no default not null,
     sbin0_100           Integer                       no default not null,
     int0_dTOf6_n100     Interval day to second(6)            no default,
     sdec0_nuniq         Decimal(9)                             no default,
     time0_nuniq         Time                               ,

     dt1_mTOh_n20        Timestamp(0)             ,
     udec1_2             Decimal(9) unsigned        not null,
     int1_h_n10          Interval hour(1)     default interval '8' hour(1),
     ubin1_uniq          Numeric(9) unsigned        not null,
     real1_uniq          Real                          no default not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  ts13_uniq ) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a092_1 on 
t9a092(ubin1_uniq asc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a092_2 on 
t9a092(ubin1_uniq asc, date2_uniq asc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a092_3 on 
t9a092(int6_dTOf6_nuniq asc, time7_uniq desc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a092_4 on 
t9a092(int6_dTOf6_nuniq asc, time7_uniq desc, sdec9_uniq asc,char10_nuniq desc );"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a092 -I $data_dir/b2uwl10.dat

    stmt = """showddl t9a092;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a092;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t9a092""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t9a092;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a092 -I $data_dir/b2uwl10.dat
    
    stmt = """showddl t9a092;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a092;"""
    output = _dci.cmdexec(stmt) 
    
    # a09.3 create table with unpopulated indexes (ascending and descedning)
    stmt = """drop table t9a093 cascade;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """Create Table t9a093
   (
     char0_100           Character(9)                  no default not null,
     sbin0_100           Integer                       no default not null,
     int0_dTOf6_n100     Interval day to second(6)            no default,
     sdec0_nuniq         Decimal(9)                             no default,
     time0_nuniq         Time                               ,

     dt1_mTOh_n20        Timestamp(0)             ,
     udec1_2             Decimal(9) unsigned        not null,
     int1_h_n10          Interval hour(1)     default interval '8' hour(1),
     ubin1_uniq          Numeric(9) unsigned        not null,
     real1_uniq          Real                          no default not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
    char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  ts13_uniq ) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a093_1 on 
t9a093(ubin1_uniq asc, date2_uniq asc)
-- no populate
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a093_2 on 
t9a093(int6_dTOf6_nuniq asc, time7_uniq desc, sdec9_uniq asc,char10_nuniq desc ) 
-- no populate
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique  index ixt09a093_3 on 
t9a093(dt17_yTOmin_uniq asc,sbin17_uniq desc,  sdec16_uniq asc )
-- no populate
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a093_4 on 
t9a093(ts13_uniq asc)
-- no populate
; """
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a093 -I $data_dir/b2uwl10.dat

    stmt = """showddl t9a093;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a093;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t9a093""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t9a093;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t9a093 -I $data_dir/b2uwl10.dat

    stmt = """showddl t9a093;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a093;"""
    output = _dci.cmdexec(stmt) 
    
    # a09.4 create table with indexes that have attributes and locations specified
    stmt = """drop table t9a094 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table t9a094
   (
     char0_100           Character(9)                  no default not null,
     sbin0_100           Integer                       no default not null,
     int0_dTOf6_n100     Interval day to second(6)            no default,
     sdec0_nuniq         Decimal(9)                             no default,
     time0_nuniq         Time                               ,

     dt1_mTOh_n20        Timestamp(0)             ,
     udec1_2             Decimal(9) unsigned        not null,
     int1_h_n10          Interval hour(1)     default interval '8' hour(1),
     ubin1_uniq          Numeric(9) unsigned        not null,
     real1_uniq          Real                          no default not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

    int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  ts13_uniq ) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a094_1 on 
t9a094(ubin1_uniq asc, date2_uniq asc)
--   location $g_disc8
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (512, 512)
  maxextents 768
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a094_2 on 
t9a094(int6_dTOf6_nuniq asc, time7_uniq desc)
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (1024, 160)
  maxextents 16
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create  unique index ixt09a094_3 on 
t9a094(ts13_uniq asc)
  -- no populate
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (1024, 4)
  maxextents 768
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)

    stmt = """showddl t9a094;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a094;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t9a094""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t9a094;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t9a094;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t9a094;"""
    output = _dci.cmdexec(stmt) 
    
    # a09.5 create table and alter index
    stmt = """drop table t9a095 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table t9a095
   (
     char0_100           Character(9)                  no default not null,
     sbin0_100           Integer                       no default not null,
     int0_dTOf6_n100     Interval day to second(6)            no default,
     sdec0_nuniq         Decimal(9)                             no default,
     time0_nuniq         Time                               ,

     dt1_mTOh_n20        Timestamp(0)             ,
     udec1_2             Decimal(9) unsigned        not null,
     int1_h_n10          Interval hour(1)     default interval '8' hour(1),
     ubin1_uniq          Numeric(9) unsigned        not null,
     real1_uniq          Real                          no default not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  ts13_uniq ) not droppable
  )
  store by primary key
  ;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt09a095_1  attributes
  allocate 16
  auditcompress
  no clearonpurge
  maxextents 320
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create unique index ixt09a095_2 on 
t9a095(int6_dTOf6_nuniq asc, time7_uniq desc)
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (1024, 160)
  maxextents 16
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt09a095_2  attributes
  allocate 4
  auditcompress
  no clearonpurge
  maxextents 16
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create index ixt09a095_3 on 
t9a095(ts13_uniq asc, double15_uniq desc )
  -- no populate
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (1024, 4)
  maxextents 768
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt09a095_3  attributes
  allocate 24
  auditcompress
  no clearonpurge
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """showddl t9a095;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a095;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile1("""t9a095""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t9a095;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t9a095;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a095;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
# *****************************************************************************
#testcase a10 Hash partitioned table with non-unique index
# *****************************************************************************
#expect purge immediate
def test010(desc="""a10 Hash partitioned table with non-unique index"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # a10.1 create table with a index (asceding and descending)
    stmt = """drop table t10a101 cascade;"""
    output = _dci.cmdexec(stmt)
    
    # b2uwl12
    stmt = """Create Table t10a101
   (
     int0_yTOm_uniq      Interval year(5) to month     no default not null,
     sbin0_1000          Largeint                      no default not null,
     sdec0_nuniq         Decimal(18)                          default null,
     ts0_uniq            Timestamp                  not null,
     char0_uniq          Character(8)               not null,

     udec1_n2            Decimal(4) unsigned                ,
     time1_n100          Time                               ,
     double1_uniq        Double Precision              no default not null,
     ubin1_1000          Numeric(4) unsigned           no default not null,
     int1_dTOf6_n10      Interval day to second(6)            no default,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_yTOm_uniq ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    
    #expect any *--- SQL operation complete.*
    stmt = """create index ixt10a101_1 on 
t10a101(char2_2 asc, sdec4_n20 desc, double6_n2 desc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a101 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a101;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a101;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t10a101""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t10a101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a101 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a101;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a101;"""
    output = _dci.cmdexec(stmt) 

    # a10.2 create table with several indexes (asceding and descending)
    stmt = """drop table t10a102 cascade;"""
    output = _dci.cmdexec(stmt) 
    
    # a09.2 create table with several unique indexes (asceding and descending)
    # b2uwl12
    stmt = """Create Table t10a102
   (
     int0_yTOm_uniq      Interval year(5) to month     no default not null,
     sbin0_1000          Largeint                      no default not null,
     sdec0_nuniq         Decimal(18)                          default null,
     ts0_uniq            Timestamp                  not null,
     char0_uniq          Character(8)               not null,

     udec1_n2            Decimal(4) unsigned                ,
     time1_n100          Time                               ,
     double1_uniq        Double Precision              no default not null,
     ubin1_1000          Numeric(4) unsigned           no default not null,
     int1_dTOf6_n10      Interval day to second(6)            no default,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_yTOm_uniq ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create index ixt10a102_1 on t10a102(udec1_n2 asc,time1_n100 desc ,double1_uniq desc,ubin1_1000 desc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a102_2 on t10a102(real3_n1000 asc,int3_yTOm_4 desc ,date3_n2000 asc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a102_3 on t10a102(sdec4_n20 desc ,int4_yTOm_uniq asc,time4_1000 desc ,char4_n10 );"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a102_4 on t10a102( char5_n20   ,sdec5_10 desc , ubin5_n500 ,real5_uniq desc ,dt5_yTOmin_n500);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a102 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a102;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a102;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t10a102""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t10a102;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a102 -I $data_dir/b2uwl12.dat
    
    stmt = """showddl t10a102;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a102;"""
    output = _dci.cmdexec(stmt) 
    
    # a10.3 create table with unpopulated indexes (ascending and descedning)
    stmt = """drop table t10a103 cascade;"""
    output = _dci.cmdexec(stmt) 
    
    # b2uwl12
    stmt = """Create Table t10a103
   (
     int0_yTOm_uniq      Interval year(5) to month     no default not null,
     sbin0_1000          Largeint                      no default not null,
     sdec0_nuniq         Decimal(18)                          default null,
     ts0_uniq            Timestamp                  not null,
     char0_uniq          Character(8)               not null,

     udec1_n2            Decimal(4) unsigned                ,
     time1_n100          Time                               ,
     double1_uniq        Double Precision              no default not null,
     ubin1_1000          Numeric(4) unsigned           no default not null,
     int1_dTOf6_n10      Interval day to second(6)            no default,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_yTOm_uniq ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 

    
    stmt = """create index ixt10a103_1 on t10a103(int6_dTOf6_nuniq ,sbin6_nuniq  ,char6_n100  ,date6_100);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_2 on t10a103(time7_uniq,sbin7_n20 desc,char7_500,int7_hTOs_nuniq );"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_3 on t10a103(ubin3_n2000 desc ,char3_4,udec7_n10, real7_n4 desc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_4 on 
t10a103(sbin4_n1000  desc,double6_n2 desc ,sdec6_4 desc);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a103 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a103;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a103;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t10a103""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t10a103;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a103 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a103;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t10a103;"""
    output = _dci.cmdexec(stmt) 
    
    # a10.4 create table with indexes that have attributes and locations specified
    stmt = """drop table t10a104 cascade;"""
    output = _dci.cmdexec(stmt)

    # b2uwl12
    stmt = """Create Table t10a104
   (
     int0_yTOm_uniq      Interval year(5) to month     no default not null,
     sbin0_1000          Largeint                      no default not null,
     sdec0_nuniq         Decimal(18)                          default null,
     ts0_uniq            Timestamp                  not null,
     char0_uniq          Character(8)               not null,

     udec1_n2            Decimal(4) unsigned                ,
     time1_n100          Time                               ,
     double1_uniq        Double Precision              no default not null,
     ubin1_1000          Numeric(4) unsigned           no default not null,
     int1_dTOf6_n10      Interval day to second(6)            no default,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_yTOm_uniq ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create index ixt10a104_1 on 
t10a104(ubin3_n2000 ,char3_4 desc ,int4_yTOm_uniq desc,time4_1000)
--   location $sysname_2.$r2_disc11
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (16, 16)
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a104_2 on 
t10a104(ubin5_n500 ,real5_uniq desc,dt5_yTOmin_n500 desc,date6_100 desc)
--   location $sysname_2.$r2_disc11
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (812, 812)
  maxextents 320
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a104_3 on 
t10a104(dt15_mTOh_n100,double15_uniq desc,sbinneg15_nuniq )
--   location $g_disc4
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (16, 16)
  maxextents 16
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)

    stmt = """create index ixt10a104_4 on 
t10a104(sdecneg15_100 desc,int15_dTOf6_n100 ,char15_100 )
--   location $g_disc8
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (1024)
  maxextents 160
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a104 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a104;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a104;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t10a104""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t10a104;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """drop table t10a104;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a104 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a104;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a104;"""
    output = _dci.cmdexec(stmt) 
    
    # a10.5 create table and alter index
    stmt = """drop table t10a105;"""
    output = _dci.cmdexec(stmt)
    
    # b2uwl12
    stmt = """Create Table t10a105
   (
     int0_yTOm_uniq      Interval year(5) to month     no default not null,
     sbin0_1000          Largeint                      no default not null,
     sdec0_nuniq         Decimal(18)                          default null,
     ts0_uniq            Timestamp                  not null,
     char0_uniq          Character(8)               not null,

     udec1_n2            Decimal(4) unsigned                ,
     time1_n100          Time                               ,
     double1_uniq        Double Precision              no default not null,
     ubin1_1000          Numeric(4) unsigned           no default not null,
     int1_dTOf6_n10      Interval day to second(6)            no default,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,

     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          Date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  int0_yTOm_uniq ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create index ixt10a105_1 on 
t10a105(dt16_m_n10 desc,int16_h_20 ,ubin16_n10 desc ,char16_n20 ,real16_10)
--   location $sysname_2.$r2_disc11
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (51200, 16)
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt10a105_1  attributes
  allocate 24
  auditcompress
  no clearonpurge
  maxextents 260
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create index ixt10a105_2 on 
t10a105(int17_y_n10 desc,dt17_yTOmin_uniq desc ,real17_n100,sbin17_uniq )
--   location $sysname_3.$r3_disc17
  attributes 
  allocate 160
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (812, 812)
  maxextents 320
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt10a105_2  attributes
  allocate 34
  auditcompress
  no clearonpurge
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create index ixt10a105_3 on 
t10a105(int16_h_20 desc,sdec16_uniq desc,sbin17_uniq )
--   location $sysname_2.$r2_disc11
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (16, 16)
  maxextents 16
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)

    stmt = """alter index ixt10a105_3  attributes
  allocate 4
  auditcompress
  no clearonpurge
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create index ixt10a105_4 on 
t10a105(double15_uniq desc,sdec17_nuniq desc,char17_2)
--   location $sysname_3.$r3_disc19
  attributes 
  allocate 160
  auditcompress
  blocksize 4096
  no clearonpurge
  extent (1024)
  maxextents 160
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)

    stmt = """alter index ixt10a105_4  attributes
  allocate 24
  no auditcompress
  clearonpurge
  maxextents 240
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'4222')
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a105 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a105;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a105;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile1("""t10a105""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t10a105;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t10a105 -I $data_dir/b2uwl12.dat

    stmt = """showddl t10a105;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a105;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
# *****************************************************************************
#testcase a11 Hash partitioned table with check constraints
# *****************************************************************************
#expect purge immediate
def test011(desc="""a11 Hash partitioned table with check constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # a11.1 create table with check constraints (column constraints)
    stmt = """drop table t11a0111 ;"""
    output = _dci.cmdexec(stmt)
    
    # b2uns09
    stmt = """Create Table t11a0111
  (
     char0_100           Character(5)  no default not null 
                         constraint a11t11_1 check(char0_100 <> 'Zp'),
     sbin0_100           Integer  no default not null 
                         constraint a11t11_2 check(sbin0_100 < 2000000),
     int0_dTOf6_n100     Interval day to second(6)          no default,
     sdec0_nuniq         Decimal(9)                           no default,
     time0_nuniq         Time                             ,

     dt1_mTOh_n20        Timestamp(0),
     udec1_2             Decimal(9) unsigned      not null,
     int1_h_n10          Interval hour(1)   default interval '8' hour,
     ubin1_uniq          Numeric(9) unsigned      not null,
     real1_uniq          Real                        no default not null,

  primary key  ( ubin1_uniq) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t11a0111 -I $data_dir/b2uns09.dat

    stmt = """showddl t11a0111;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t11a0111;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t11a0111""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t11a0111;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t11a0111 -I $data_dir/b2uns09.dat

    stmt = """showddl t11a0111;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t11a0111;"""
    output = _dci.cmdexec(stmt)  

    # a11.2 create table with check constarints (table constraints)
    
    # b2uns09
    stmt = """Create Table t11a0112
  (
     char0_100           Character(5)  no default not null ,
     sbin0_100           Integer  no default not null ,
     int0_dTOf6_n100     Interval day to second(6)          no default,
     sdec0_nuniq         Decimal(9)                           no default,
     time0_nuniq         Time                             ,

     dt1_mTOh_n20        Timestamp(0),
     udec1_2             Decimal(9) unsigned      not null,
     int1_h_n10          Interval hour(1)   default interval '8' hour,
     ubin1_uniq          Numeric(9) unsigned      not null,
     real1_uniq          Real                        no default not null,

  primary key  ( ubin1_uniq ) not droppable,
  check (char0_100 <> 'Zp'),
  check(sbin0_100 < 2000000)

  )
  store by primary key
  ATTRIBUTES EXTENT (512, 512), MAXEXTENTS 160
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t11a0112 -I $data_dir/b2uns09.dat

    stmt = """showddl t11a0112;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t11a0112;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile1("""t11a0112""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t11a0112;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t11a0112 -I $data_dir/b2uns09.dat
    
    stmt = """showddl t11a0112;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t11a0112;"""
    output = _dci.cmdexec(stmt) 
  
    _testmgr.testcase_end(desc)
# *****************************************************************************
#testcase a12 Hash partitioned table with reference constraint
# *****************************************************************************
#expect purge immediate
def test012(desc="""a12 Hash partitioned table with reference constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # a12.1 create table with reference constraint (column constraint)
    # btuns09
    stmt = """Create Table t12a0121_a
  (
     ubin0_2             PIC 9(7)V9(2) COMP    not null,
     sbin0_100           Numeric(18) signed    not null,
     sdec0_10            PIC S9(9)             not null,
     varchar0_uniq       varchar(16)      not null unique,
     udec0_uniq          Decimal(9) unsigned   not null unique,
     char0_10            Character(8)          not null,
     char1_20            Character(32)         not null,
     varchar1_4          varchar(8)       not null,
     sdec1_uniq          Decimal(18) signed    not null unique,
     sbin1_100           Numeric(4) signed     not null,
     primary key  ( sbin1_100        ASC,
                    sdec1_uniq       ASC,
                    varchar1_4       DESC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # b2uns09
    stmt = """Create Table t12a0121
  (
     ubin0_2             PIC 9(7)V9(2) COMP    not null,
     sbin0_100           Numeric(18) signed    not null,
     sdec0_10            PIC S9(9)             not null,
     varchar0_uniq       varchar(16)      not null references t12a0121_a(varchar0_uniq),
     udec0_uniq          Decimal(9) unsigned   not null references t12a0121_a(udec0_uniq),
     char0_10            Character(8)          not null,
     char1_20            Character(32)         not null,
     varchar1_4          varchar(8)       not null,
     sdec1_uniq          Decimal(18) signed    not null
                         constraint cnsta12_2 references t12a0121_a(sdec1_uniq ),
     sbin1_100           Numeric(4) signed     not null,
     primary key  ( sbin1_100        ASC,
                    sdec1_uniq       ASC,
                    varchar1_4       DESC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0121_a -I $data_dir/btuns09.dat

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0121 -I $data_dir/btuns09.dat

    stmt = """showddl t12a0121;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t12a0121;"""
    output = _dci.cmdexec(stmt) 
    
    save_ddl_to_obeyfile1("""t12a0121""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t12a0121;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0121 -I $data_dir/btuns09.dat

    stmt = """showddl t12a0121;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t12a0121;"""
    output = _dci.cmdexec(stmt) 

    # a12.2 create table with reference constraint (table constraint)

    #btuns11
    stmt = """Create Table t12a0122_b
  (
     udec0_1000          Decimal(9) unsigned   not null,
     ubin0_uniq          PIC 9(7)V9(2) COMP    not null unique,
     sdec0_100           PIC S9(9)             not null,
     varchar0_500        varchar(16)      not null,
     char0_uniq          Character(8)          not null unique,
     sbin0_uniq          Numeric(18) signed    not null unique,
     sbin1_4             Numeric(4) signed     not null,
     char1_100           Character(64)         not null ,
     varchar1_uniq       varchar(8)       not null unique,
     sdec1_20            Decimal(18) signed    not null,
     primary key ( sdec1_20    ASC,
                   sbin0_uniq  DESC,
                   udec0_1000   ASC ) not droppable
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table t12a0122
  (
     udec0_1000          Decimal(9) unsigned   not null,
     ubin0_uniq          PIC 9(7)V9(2) COMP    not null,
     sdec0_100           PIC S9(9)             not null,
     varchar0_500        varchar(16)      not null,
     char0_uniq          Character(8)          not null,
     sbin0_uniq          Numeric(18) signed    not null,
     sbin1_4             Numeric(4) signed     not null,
     char1_100           Character(64)         not null,
     varchar1_uniq       varchar(8)       not null,
     sdec1_20            Decimal(18) signed    not null,
     primary key ( sdec1_20    ASC,
                   sbin0_uniq  DESC,
                   udec0_1000   ASC ) not droppable,
     constraint cnst12_1 foreign key (ubin0_uniq) references t12a0122_b (ubin0_uniq),
     constraint cnst12_2 foreign key (char0_uniq) references t12a0122_b (char0_uniq),
     constraint cnst12_3 foreign key (sbin0_uniq) references t12a0122_b (sbin0_uniq),
     constraint cnst12_4 foreign key (varchar1_uniq) references t12a0122_b (varchar1_uniq)
  )
  store by primary key
;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0122_b -I $data_dir/btuns11.dat

    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0122 -I $data_dir/btuns11.dat
    
    stmt = """showddl t12a0122;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t12a0122;"""
    output = _dci.cmdexec(stmt) 

    save_ddl_to_obeyfile3("""t12a0122""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t12a0122;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #unexpect any *ERROR*
    # #sh import $testcat.$testsch.t12a0122 -I $data_dir/btuns11.dat
    
    stmt = """showddl t12a0122;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t12a0122;"""
    output = _dci.cmdexec(stmt) 
  
    _testmgr.testcase_end(desc)
# -----------------------------------------------------------
#testcase a13 Hash partitioned table with unique constraints
# -----------------------------------------------------------

#expect purge immediate
def test013(desc="""a13 Hash partitioned table with unique constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  a13.1 create table with unique constraint (column constraint)
    stmt = """create Table tbl1
(
 col1 int not null not droppable primary key,
 col2 int not null,
 col3 int not null not droppable unique
) 
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    stmt = """insert into tbl1 values (1,1,1), (2,2,2), (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """delay 3;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tbl1 values (2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """showddl tbl1;"""
    output = _dci.cmdexec(stmt)

    save_ddl_to_obeyfile3("""tbl1""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table tbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """insert into tbl1 values (1,1,1), (2,2,2), (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """delay 3;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl1 values (2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """showddl tbl1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table tbl1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    #  a13.2 create table with unique constraint (table constraint)
    stmt = """create Table tbl1
(
 col1 int not null not droppable primary key,
 col2 int not null,
 col3 int not null not droppable,
 unique (col3)
) 
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    stmt = """insert into tbl1 values (1,1,1), (2,2,2), (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """insert into tbl1 values (2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """showddl tbl1;"""
    output = _dci.cmdexec(stmt)

    save_ddl_to_obeyfile3("""tbl1""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table tbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """insert into tbl1 values (1,1,1), (2,2,2), (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """insert into tbl1 values (2,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """showddl tbl1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
# ------------------------------------------------
#testcase a14 Hash partitioned table with triggers
# ------------------------------------------------

#expect purge immediate
def test014(desc="""a14 Hash partitioned table with triggers"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # a14.1 create table with a trigger
    stmt = """drop table t14a141 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t14a141 ( a int not null, b int, c int )
store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  #expect any *SQL operation complete.*
    #  create trigger tr2 before insert on t14a141
    #  REFERENCING NEW AS newR FOR EACH ROW SET newR.b = newR.b + 100;

    # activate trigger
    #expect any *18 row(s) inserted.*
    stmt = """insert into t14a141  values 
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 18)

    stmt = """showddl t14a141;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t14a141;"""
    output = _dci.cmdexec(stmt)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    stmt = """create table t14a141new like t14a141
with constraints
with headings
with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    save_ddl_to_obeyfile1("""t14a141""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t14a141 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    # #expect any *Exit Status: 0*
    # #sh import $testcat.$testsch.t13a0141 -I $data_dir/b2uwl16.dat
    #expect any *18 row(s) inserted.*
    stmt = """insert into t14a141  values 
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 18)

    stmt = """showddl t14a141;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t14a141;"""
    output = _dci.cmdexec(stmt)

    # a14.2 create table with a trigger, index, and constraints
    stmt = """drop table t14a143 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t14a142 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t14a143 
( 
 a int not null, 
 b int, 
 c int constraint ck14_3 check (c < 10000)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table t14a142 
( 
 a int not null, 
 b int, 
 c int constraint ck14_2 check (c < 10000)
) 
store by (a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t14a143 values 
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 18)

    stmt = """drop index ix1;"""
    output = _dci.cmdexec(stmt)
    
    # create unpopulated index
    stmt = """create index ix1  on t14a142 ( a,b,c) -- no populate
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create trigger
    #  #expect any *SQL operation complete.*
    #  create trigger tr3 after update on t14a142 insert into t14a142
    #  (select a,b,c as "c" from t14a143 where 
    #  a between 0 and 8
    #  and a > 4
    #  and b > 6
    #  and b < 20
    #  and b < 8
    #  and c between 6 and 8);
    
    stmt = """insert into t14a142  values 
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 18)
    
    stmt = """showddl t14a142;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t14a142;"""
    output = _dci.cmdexec(stmt)
    
    # create table like the original table, insert values,
    # recreate original table from showddl output and insert values.
    stmt = """create table t14a142new like t14a142
with constraints
with headings
with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    save_ddl_to_obeyfile1("""t14a142""", '', defs.work_dir + """/obeyfile""") 

    #stmt = """drop table t14a142;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #  debug:
    #  #sh cat $result_dir/a141
    #output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """insert into t14a142  values 
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 18)
    
    stmt = """showddl t14a142;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t14a142;"""
    output = _dci.cmdexec(stmt)
  
    _testmgr.testcase_end(desc)
