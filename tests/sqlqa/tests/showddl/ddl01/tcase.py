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
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v log >> """ + filename)
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


# ---------------------------------------------------------
#testcase a03 Tables with pk column and table constraints
# ---------------------------------------------------------
def test001(desc="""a03 Tables with pk column and table constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a03.1 create table with pk as column constraint
    stmt = """create Table t3a031
  (
     char0_100           Character(8)  not null constraint a3t1_1 check(char0_100 <> 'Z'),
     sbin0_uniq          Integer  not null unique,
     sdec0_n10           Decimal(4)           default 9 
                         constraint a3t1_2 check (sdec0_n10 between 0 and 15000),
     int0_yTOm_n1000     Interval year(2) to month         no default,
     date0_nuniq         Date no default check (date0_nuniq < date '3000-01-06'),

     real1_uniq          Integer not null primary key asc not droppable,
     ts1_n100            Timestamp                     ,
     ubin1_500           Numeric(4) unsigned      no default not null,
     int1_dTOf6_nuniq    Interval day to second(6)       no default,
     udec1_50p  Decimal(9) unsigned not null 
  )
  store by primary key
  attributes extent (16, 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)

    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    save_ddl_to_obeyfile("""t3a031""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t3a031; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 

    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)
    
    #  a03.2 create table with table constraints

    #  b2uwl06
    stmt = """Create Table t3a032
   (
     date0_n10           Date
       default date '01/09/2100' heading 'date0_n10 with default 01/09/2100',
     int0_dTOf6_uniq     Interval day to second(6)    no default not null,
     char0_n2            Character(8)                           no default,
     sbin0_10            Largeint                   not null,
     sdec0_nuniq         Decimal(4)                         ,

     ubin1_10            Numeric(4) unsigned           no default not null,
    udec1_nuniq         Decimal(9) unsigned                    no default,
     int1_d_100          Interval day               not null,
     dt1_m_n10           Date                     ,
     real1_500           Real                          no default not null,

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
     int7_hTOs_nuniq     Interval hour(2) to second(0)         ,
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

     dt15_mTOh_n100      Timestamp(0)               no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          date                       ,
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
     primary key (int4_yTOm_uniq)
     )
     attributes extent (16, 16)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a032;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t3a032;"""
    output = _dci.cmdexec(stmt)

    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    save_ddl_to_obeyfile("""t3a032""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a031
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t3a032;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t3a032;"""
    output = _dci.cmdexec(stmt)   
        
    _testmgr.testcase_end(desc)
    
# ----------------------------------------------------------
#testcase a04 Table with primary key and store by specified
# ----------------------------------------------------------

def test002(desc="""a04 Table with primary key and store by specified"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a04.1 create table with pk and store by ( same as pk)

    #  b2unl17
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
    
    stmt = """showddl t4a041;"""
    output = _dci.cmdexec(stmt)


    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t4a041""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop table t4a041; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t4a041;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    
    #  a04.2 create table with pk and store by ( prefix of pk)

    #  b2uwl08
    stmt = """Create Table t4a042
   (
     sdec0_20            Decimal(4)                 not null,
     ts0_nuniq           Timestamp                          ,
     sbin0_uniq          Smallint                      no default not null,
     int0_d_uniq         Interval day(6)               no default not null,
     char0_n500          Character(8)                           no default,

     double1_10          Double Precision        default 1.0004E1 not null,
     ubin1_4             Numeric(4) unsigned           no default not null,
     dt1_yTOmin_nuniq    Timestamp(0)            ,
     udec1_500           Decimal(4) unsigned        not null,
    int1_y_nuniq        Interval year(4)                   ,

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

     primary key  (  date2_uniq asc, sbin0_uniq, char11_uniq desc ) not droppable
  )
  store by ( date2_uniq asc, sbin0_uniq )
  attributes extent (16,16)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1193')
    
    
    #  b2uwl08
    stmt = """Create Table t4a042
   (
     sdec0_20            Decimal(4)                 not null,
     ts0_nuniq           Timestamp                          ,
     sbin0_uniq          Smallint                      no default not null,
     int0_d_uniq         Interval day(6)               no default not null,
     char0_n500          Character(8)                           no default,

     double1_10          Double Precision        default 1.0004E1 not null,
     ubin1_4             Numeric(4) unsigned           no default not null,
     dt1_yTOmin_nuniq    Timestamp(0)            ,
     udec1_500           Decimal(4) unsigned        not null,
    int1_y_nuniq        Interval year(4)                   ,

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

     primary key  (  date2_uniq asc, sbin0_uniq, char11_uniq desc ) not droppable
  )
  store by ( date2_uniq asc, sbin0_uniq, char11_uniq desc )
  attributes extent (16,16)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t4a042;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t4a042;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t4a042""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t4a042; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a041
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t4a042;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t4a042;"""
    output = _dci.cmdexec(stmt)
    
    #  a04.3 create table with droppable pk and store by 

    #  b2uwl08
    stmt = """Create Table t4a043
   (
     sdec0_20            Decimal(4)                 not null,
     ts0_nuniq           Timestamp                          ,
     sbin0_uniq          Smallint                      no default not null,
     int0_d_uniq         Interval day(6)               no default not null,
     char0_n500          Character(8)                           no default,

     double1_10          Double Precision        default 1.0004E1 not null,
     ubin1_4             Numeric(4) unsigned           no default not null,
     dt1_yTOmin_nuniq    Timestamp(0)            ,
     udec1_500           Decimal(4) unsigned        not null,
    int1_y_nuniq        Interval year(4)                   ,

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

     -- primary key  (  date2_uniq asc, sbin0_uniq,char11_uniq desc )  droppable
     primary key  ( sbin0_uniq desc,char11_uniq desc )  droppable
  )
  store by (sbin0_uniq desc,char11_uniq desc)
  attributes extent (16,16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t4a043;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t4a043;"""
    output = _dci.cmdexec(stmt)
    
    save_ddl_to_obeyfile("""t4a043""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t4a043; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a041
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t4a043;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t4a043;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test003(desc=""" a09 Table with unique index"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a09.1 create table with unique index (ascending and descending)

    #  b2uwl10
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a091 on 
t9a091(ubin1_uniq asc, date2_uniq asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t9a091;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a091;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t9a091""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t9a091; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a091
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t9a091;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t9a091;"""
    output = _dci.cmdexec(stmt)

    
    #  a09.2 create table with several unique indexes (ascending and descending)

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
  attributes extent (16,16)
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
    
    stmt = """showddl t9a092;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a092;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.

    save_ddl_to_obeyfile("""t9a092""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t9a092;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a091
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t9a092;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t9a092;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop index ixt09a093_1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index ixt09a093_2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index ixt09a093_3;"""
    output = _dci.cmdexec(stmt)
    
    #  a09.3 create table with unpopulated indexes (ascending and descedning)
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
  attributes extent (16,16)
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
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t9a093;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a093;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t9a093""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t9a093;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a091
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t9a093;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a093;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop index ixt09a094_1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index ixt09a094_2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index ixt09a094_3;"""
    output = _dci.cmdexec(stmt)
    
    #  a09.5 create table and alter index
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixt09a095_1 on 
t9a095(ubin1_uniq asc, date2_uniq asc)
  attributes 
  allocate 4
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (16, 16)
  maxextents 32
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt09a095_1  attributes
  allocate 16
  auditcompress
  no clearonpurge
  maxextents 64
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create unique index ixt09a095_2 on 
t9a095(int6_dTOf6_nuniq asc, time7_uniq desc)
  attributes 
  allocate 4
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (16, 16)
  maxextents 16
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter index ixt09a095_2  attributes
  allocate 4
  auditcompress
  no clearonpurge
  maxextents 32
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    
    stmt = """create index ixt09a095_3 on 
t9a095(ts13_uniq asc)
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
    
    stmt = """alter index ixt09a095_3  attributes
  allocate 32
  auditcompress
  no clearonpurge
  maxextents 32
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    stmt = """showddl t9a095;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t9a095;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    save_ddl_to_obeyfile("""t9a095""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t9a095;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a091
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t9a095;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t9a095;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc=""" a10 Table with non-unique index"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # #process lcl_node_1_part_mxci
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a10.1 create table with a index (ascending and descending)

    #  b2uwl12
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a101_1 on 
t10a101(char2_2 asc, sdec4_n20 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t10a101;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a101;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t10a101""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t10a101; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a101
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t10a101;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a101;"""
    output = _dci.cmdexec(stmt)

    
    #  a10.2 create table with several indexes (ascending and descending)

    #  b2uwl12
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
  attributes extent (16,16);"""
    output = _dci.cmdexec(stmt)

    stmt = """create index ixt10a102_1 on 
t10a102(udec1_n2 asc,time1_n100 desc , ubin1_1000 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a102_2 on 
t10a102(int3_yTOm_4 desc ,date3_n2000 asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a102_3 on 
t10a102(sdec4_n20 desc ,int4_yTOm_uniq asc,time4_1000 desc ,char4_n10 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """create index ixt10a102_4 on 
t10a102( char5_n20   ,sdec5_10 desc , ubin5_n500 ,dt5_yTOmin_n500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t10a102;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a102;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t10a102""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t10a102; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a101
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """showddl t10a102;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a102;"""
    output = _dci.cmdexec(stmt)
    
    #  a10.3 create table with unpopulated indexes (ascending and descedning)
    #  b2uwl12
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)

    stmt = """create index ixt10a103_1 on 
t10a103(int6_dTOf6_nuniq ,sbin6_nuniq  ,char6_n100  ,date6_100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_2 on 
t10a103(time7_uniq,sbin7_n20 desc,char7_500,int7_hTOs_nuniq );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_3 on 
t10a103(ubin3_n2000 desc ,char3_4,udec7_n10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a103_4 on 
t10a103(sbin4_n1000  desc,double6_n2 desc ,sdec6_4 desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t10a103;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t10a103;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.   
    save_ddl_to_obeyfile("""t10a103""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t10a103; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a101
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """showddl t10a103;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a103;"""
    output = _dci.cmdexec(stmt)
    
    #  a10.4 create table with indexes that have attributes and locations specified
        
    #  b2uwl12
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index ixt10a104_1 on 
t10a104(ubin3_n2000 ,char3_4 desc ,int4_yTOm_uniq desc,time4_1000)
  -- location $g_disc0
  attributes 
  allocate 16
  no auditcompress
  blocksize 4096
  clearonpurge
  extent (512, 16)
  maxextents 240
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixt10a104_2 on 
t10a104(ubin5_n500 ,dt5_yTOmin_n500 desc,date6_100 desc)
  -- location $g_disc0
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
t10a104(dt15_mTOh_n100,sbinneg15_nuniq )
  -- location $g_disc0
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
  -- location $g_disc0
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
    
    stmt = """showddl t10a104;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t10a104;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t10a104""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t10a104; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a101
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t10a104;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t10a104;"""
    output = _dci.cmdexec(stmt)

    #  a10.5 create table and alter index
    #  b2uwl12
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index ixt10a105_1 on 
t10a105(dt16_m_n10 desc,int16_h_20 ,ubin16_n10 desc ,char16_n20)
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
    
    stmt = """alter index ixt10a105_1  attributes
  allocate 24
  auditcompress
  no clearonpurge
  maxextents 260
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'4222')
    
    stmt = """create index ixt10a105_2 on 
t10a105(int17_y_n10 desc,dt17_yTOmin_uniq desc ,sbin17_uniq )
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
t10a105(sdec17_nuniq desc,char17_2)
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
    
    stmt = """showddl t10a105;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t10a105;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.

    save_ddl_to_obeyfile("""t10a105""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t10a105; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a101
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t10a105;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t10a105;"""
    output = _dci.cmdexec(stmt)

    #process mxci
    _testmgr.testcase_end(desc)
    
def test005(desc=""" a11 Table with check constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # #process lcl_node_1_part_mxci
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a11.1 create table with check constraints (column constraints)

    #  b2uns09
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
     real1_uniq          Integer    no default not null,

  primary key  ( real1_uniq) not droppable
  )
  store by primary key
  attributes extent (16,16)
 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t11a0111;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t11a0111;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    
    save_ddl_to_obeyfile("""t11a0111""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t11a0111;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a111
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t11a0111;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t11a0111;"""
    output = _dci.cmdexec(stmt)
    
    #  a11.2 create table with check constarints (table constraints)

    #  b2uns09
    stmt = """Create Table t11a0112
  (
     char0_100           Character(5)  no default not null ,
     sbin0_100           Integer  no default not null ,
     int0_dTOf6_n100     Interval day to second(6) no default,
     sdec0_nuniq         Decimal(9)                no default,
     time0_nuniq         Time                      ,

     dt1_mTOh_n20        Timestamp(0),
     udec1_2             Decimal(9) unsigned      not null,
     int1_h_n10          Interval hour(1)   default interval '8' hour,
     ubin1_uniq          Numeric(9) unsigned      not null,
     real1_uniq          Integer        no default not null,

  primary key  ( real1_uniq) not droppable,
  check (char0_100 <> 'Zp'),
 check(sbin0_100 < 2000000)
 
  )
  store by primary key
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t11a0112;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t11a0112;"""
    output = _dci.cmdexec(stmt)

    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
    save_ddl_to_obeyfile("""t11a0112""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t11a0112;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a111
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t11a0112;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t11a0112;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test006(desc="""a12 Table with reference constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # #process lcl_node_1_part_mxci
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a12.1 create table with reference constraint (column constraint)

    #  b2uns09
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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

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
  attributes extent (16,16)
  ;"""
    output = _dci.cmdexec(stmt)

    # Susan
    stmt = """showddl t12a0121;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showddl t12a0121;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t12a0121;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.

    save_ddl_to_obeyfile("""t12a0121""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t12a0121;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a121
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t12a0121;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t12a0121;"""
    output = _dci.cmdexec(stmt)

    #  a12.2 create table with reference constraint (table constraint)

    #  btuns11
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
  attributes extent (16,16)
;"""
    output = _dci.cmdexec(stmt)

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
  attributes extent (16,16)
;"""
    output = _dci.cmdexec(stmt)

    stmt = """showddl t12a0122;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t12a0122;"""
    output = _dci.cmdexec(stmt)

    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.
 
    save_ddl_to_obeyfile("""t12a0122""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t12a0122;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a121
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t12a0122;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t12a0122;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
def test007(desc="""a13 Table with unique constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  a13.1 create table with unique constraint (column constraint)

    #  b2uwl16
    stmt = """Create Table t13a0131
(
     char0_100           Character(8)               not null,
     sbin0_uniq          Integer                    not null unique,
     sdec0_n10           Decimal(4)                              default 9,
     int0_yTOm_n1000     Interval year(2) to month              no default,
     date0_nuniq         Date                                   no default,

     real1_uniq          Integer                   not null ,
     ts1_n100            Timestamp                          ,
     ubin1_500           Numeric(4) unsigned           no default not null,
     int1_dTOf6_nuniq    Interval day to second(6)            no default,
     udec1_2000          Decimal(9) unsigned        not null,

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
     int4_yTOm_uniq      Interval year(5) to month   not null unique,
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

     time7_uniq          Time                       not null unique,
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

     sdec9_uniq          Decimal(18) signed            no default not null unique,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null unique,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null unique,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null unique,
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
     ts13_uniq           Timestamp                  not null unique,
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
     sdec16_uniq         Decimal(18) signed         not null unique,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null unique,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null unique,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null,

     primary key  (  real1_uniq ) not droppable
  )
store by primary key
attributes extent (16,16)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t13a0131;"""
    output = _dci.cmdexec(stmt) 

    stmt = """showlabel t13a0131;"""
    output = _dci.cmdexec(stmt)
    
    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.

    save_ddl_to_obeyfile("""t13a0131""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t13a0131;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a131
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    stmt = """showddl t13a0131;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t13a0131;"""
    output = _dci.cmdexec(stmt)
    
    #  a13.2 create table with unique constraint (table constraint)

    #  b2uwl16
    stmt = """Create Table t13a0132
   (
     char0_100           Character(8)               not null,
     sbin0_uniq          Integer                    not null,
     sdec0_n10           Decimal(4)                              default 9,
     int0_yTOm_n1000     Interval year(2) to month              no default,
     date0_nuniq         Date                                   no default,

     real1_uniq          Integer                not null,
     ts1_n100            Timestamp                          ,
     ubin1_500           Numeric(4) unsigned           no default not null,
     int1_dTOf6_nuniq    Interval day to second(6)            no default,
     udec1_2000          Decimal(9) unsigned        not null,

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
     real5_uniq          Integer                   not null,
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

     primary key  (  sbin0_uniq ) not droppable,
     unique (sbin0_uniq, date2_uniq, int4_yTOm_uniq),
     unique (time7_uniq, sdec9_uniq, int10_d_uniq ),
     unique (udec10_uniq, char11_uniq, ts13_uniq, sdec16_uniq, sbin17_uniq )
  )
  store by primary key
  attributes extent (16,16)
 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t13a0132;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t13a0132;"""
    output = _dci.cmdexec(stmt)

    #  create table like the original table, insert values,
    #  recreate original table from showddl output and insert values.

    save_ddl_to_obeyfile("""t13a0132""", '', defs.work_dir + """/obeyfile""") 
    stmt = """drop table t13a0132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #runscript $result_dir/a131
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")

    stmt = """showddl t13a0132;"""
    output = _dci.cmdexec(stmt)

    stmt = """showlabel t13a0132;"""
    output = _dci.cmdexec(stmt)

    #process mxci
    
    _testmgr.testcase_end(desc) 
