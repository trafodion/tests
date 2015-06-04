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
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v log | grep -v 'SQL operation complete' >> """ + filename)
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
    
def test001(desc="""Create View Syntax"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #-------------------------------
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a01.1 create view with column names and default headings
    
    stmt = """create view vopt12 (datecol1, datecol2, interval1, interval2)
as select DT16_M_N10, DATE8_10, INT3_YTOM_4, INT1_DTOF6_N10
from b2pwl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12
where interval2 is NULL
and interval1 = interval '0-00' year(1) to month
and datecol1 > date '1997-07-01'
order by datecol2 desc, datecol1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""vopt12""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12
where interval2 is NULL
and interval1 = interval '0-00' year(1) to month
and datecol1 > date '1997-07-01'
order by datecol2 desc, datecol1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #a01.2 create view with explicit headings
    
    stmt = """create view vopt12a ("maxcol" heading 'maxcol?', "mincol" heading 'Less%&()',
regcol)
as select max(ubin1_1000), min(udec1_n2), sdec2_500 as groupcol
from b2pwl12
group by sdec2_500
having sdec2_500 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12a
order by regcol;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""vopt12a""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a01.3 create view with explicit 'no heading'
    
    stmt = """create view vopt12b (
a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567 no heading, "vcol2" no heading)
as select char2_2, sbin2_nuniq
from b2pwl12
where sbin2_nuniq < 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12b
order by "vcol2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""vopt12b""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12b
order by "vcol2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #a01.4 create view with delimited columns and maxlength headings
    
    stmt = """create view vopt12c
("my_ubin1_1000" heading
'myubin11000a123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456'
, "my_date8_10" heading
'myubin11000a123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456'
)
as
select avg(ubin1_1000), date8_10 from b2pwl12
group by date8_10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12c
order by "my_date8_10" ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""vopt12c""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vopt12c
order by "my_date8_10";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #a01.5 create view with reserved word as delimited view name
    
    stmt = """create view "RESIGNAL" ("prepare" heading 'prepare', "INTERVAL",
"describe" no heading, "MONTH")
as select  time7_uniq,
sbin7_n20,
char7_500,
int7_hTOs_nuniq from b2pwl12
where char7_500 in ('AAAADAAA','AAAAEAAA','AAAAFAAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select max("prepare") as "false",min("INTERVAL") as "indicator",
"describe", min("MONTH") as "NATIONAL"
from "RESIGNAL"
group by "describe"
order by "describe";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select max("prepare") as "false",min("INTERVAL") as "indicator",
"describe", min("MONTH") as "NATIONAL"
from "RESIGNAL"
group by "describe"
order by "describe";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
   
    save_ddl_to_obeyfile('"RESIGNAL"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a01.6 create view with default column names on column select "AS"
    
    stmt = """create view
v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
(c123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567)
as select max(int8_y_n1000) from b2pwl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a01.7 Create view with default column names on columns selected AS
    
    stmt = """create view vopt12d
as select min(time7_uniq) as lowtime, max(char5_n20) as
t123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567,
count(*) as howmanytimes, char3_4 as alphagroup
from b2pwl12
group by char3_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""vopt12d""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl  vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    stmt = """drop view vopt12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vopt12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vopt12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vopt12c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "RESIGNAL";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view
v123456789b123456789c123456789d123456789e12345678f123456789g123456789h123456789i123456789j123456789k123456789l123456789m1234567
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vopt12d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Create View Catalog Issues"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #a02.1 create view as join on tables on two different catalogs
    
    stmt = """set schema """ + defs.my_schema2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #create table b2pwl28 like $popsch.b2pwl28;
    # multi-column non-contiguous primary key
    # non-unique Numeric lead-off column
    # 5000 recs
    stmt = """Create Table b2pwl28
(
int0_yTOm_uniq      Interval year(5) to month     no default not null,
sbin0_500           Largeint                      no default not null,
sdec0_nuniq         Decimal(18)                          default null,
ts0_uniq            Timestamp                  not null,
char0_uniq          Character(8)               not null,    

udec1_n2            Decimal(4) unsigned                ,
time1_uniq          Time                       not null,
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

primary key  (  sbin0_500, time1_uniq) not droppable
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    #insert into b2pwl28 (select * from $popsch.b2pwl28);
    # R2.5 NCI #sh import $my_schema2.b2pwl28 -I $gdata/b2pwl28.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema2 + """.b2pwl28
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl28);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #create table b2pwl14 like $popsch.b2pwl14;
    # Interval day to second(6) primary key
    # 5000 recs
    stmt = """Create Table b2pwl14
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
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    #insert into b2pwl14 (select * from $popsch.b2pwl14);
    # R2.5 NCI #sh import $my_schema2.b2pwl14 -I $gdata/b2pwl14.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema2 + """.b2pwl14
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl14);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view """ + defs.my_schema + """.v1opt28 (expression1, expression2, joincol1, joincol2)
location """ + gvars.g_disc4 + """
as select a.ubin5_n500,
b.real5_uniq,
a.dt5_yTOmin_n500,
b.int5_hTOs_500
from """ + defs.my_schema + """.b2pwl28 a left join """ + defs.my_schema2 + """.b2pwl28 b
on a.ubin5_n500 = b.ubin5_n500
where a.sbin6_nuniq < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v1opt28 order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl """ + defs.my_schema + """.v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel """ + defs.my_schema + """.v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile(defs.my_schema + """.v1opt28""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  """ + defs.my_schema + """.v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl  """ + defs.my_schema + """.v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  """ + defs.my_schema + """.v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    
    # now do it the other way
    stmt = """create view """ + defs.my_schema2 + """.v2opt28
(expression1, expression2, joincol1, joincol2)
location """ + gvars.g_disc4 + """
as select a.ubin5_n500,
b.real5_uniq,
a.dt5_yTOmin_n500,
b.int5_hTOs_500
from """ + defs.my_schema + """.b2pwl28 a left join """ + defs.my_schema2 + """.b2pwl28 b
on a.ubin5_n500 = b.ubin5_n500
where a.sbin6_nuniq < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # use same expectfile
    stmt = """select * from """ + defs.my_schema2 + """.v2opt28 order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile(defs.my_schema2 + """.v2opt28""", '', defs.work_dir + """/obeyfile""") 

    stmt = """drop view  """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema """ + defs.my_schema2 + """;"""
    output = _dci.cmdexec(stmt)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl  """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  """ + defs.my_schema2 + """.v2opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.2 create view on single table, different catalog
    
    stmt = """create view """ + defs.my_schema + """.v2opt14("mycol1", "mycol2")
as select max(date0_n100 ),  sbin0_4 from """ + defs.my_schema2 + """.b2pwl14
group by sbin0_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + defs.my_schema + """.v2opt14 order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl """ + defs.my_schema + """.v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel """ + defs.my_schema + """.v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile(defs.my_schema + """.v2opt14""", '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  """ + defs.my_schema + """.v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")    
    stmt = """showddl """ + defs.my_schema + """.v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  """ + defs.my_schema + """.v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.3 create same view name on two different schemas, same catalog

    stmt = """create view """ + defs.my_schema + """.v2opt14b (\"c**(forty)\", \"b-c*43\")
as select udec1_500,real1_n100 from """ + defs.my_schema2 + """.b2pwl14
where  date2_uniq < date '2003-01-30' +interval '97' year(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view """ + defs.my_schema2 + """.v2opt14b (\"c**(forty)\", \"b-c*43\")
as select udec1_500,real1_n100 from """ + defs.my_schema2 + """.b2pwl14
where  date2_uniq < date '2003-01-30' +interval '97' year(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + defs.my_schema + """.v2opt14b order by \"c**(forty)\" desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select * from """ + defs.my_schema2 + """.v2opt14b order by \"c**(forty)\" desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    save_ddl_to_obeyfile(defs.my_schema + """.v2opt14b;""",  defs.my_schema2 + """.v2opt14b;""", defs.work_dir + """/obeyfile""")
 
    stmt = """drop view  """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view  """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel   """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.4 create view as select *, add column to table
    
    stmt = """create table "month" ("natural" int, "current_date" date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into "month" values (2, date '2001-02-01'),
(5, date '2001-03-01'),(7, date '2001-04-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """create view "newmonth" as select * from "month";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "newmonth" order by "current_date";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """alter table "month" add column holiday char(10) default 'workday';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "newmonth" order by "current_date";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"newmonth"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.5 create view with explicit columns, add column to table
    
    stmt = """create view "leapyearmonth" ("n","current_date","h") as select * from "month";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "leapyearmonth" order by "current_date";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """alter table "month" add column weekend char(10) default 'sunday';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "month" order by "current_date";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from "leapyearmonth" order by "current_date";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"newmonth"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    stmt = """drop view v1opt28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v2opt14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view """ + defs.my_schema2 + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view  """ + defs.my_schema + """.v2opt14b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view  "newmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view  "leapyearmonth";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table "month";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #--------------------------------------
    _testmgr.testcase_end(desc)

def test003(desc="""Create Non-Updateable View"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #--------------------------------------
    
    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a03.1 create view with union
    
    stmt = """create view v3a1 (y1) as
SELECT WEEK(date3_n2000)
from b2pwl06
UNION ALL
SELECT EXTRACT(YEAR from date2_uniq) + YEAR(date3_n2000)
from """ + defs.my_schema + """.b2pwl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a1', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.2 create view with join
    
    stmt = """create view v3a2 (x, y, z) as
select b6.int4_ytom_uniq, b6.time4_1000, b12.int0_yTOm_uniq
from b2pwl06 b6 left join """ + defs.my_schema + """.b2pwl12 b12 on b6.int4_ytom_uniq = b12.int0_yTOm_uniq
where b12.int0_yTOm_uniq < interval '05-04' year(5) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a2', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view  v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a03.3 create view with except - not implemented
    
    # a03.4 create view with groupby
    
    stmt = """create view v3a4 (udec1_n2, time1_n100, avg2cols, int1_dtof6_n10)
as
select
max(udec1_n2),
min(time1_n100),
avg(double1_uniq+ubin1_1000),
int1_dTOf6_n10
from """ + defs.my_schema + """.b2pwl12
group by int1_dTOf6_n10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a4', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.5 create view with groupby and having
    stmt = """create view v3a5 (udec1_n2, time1_n100, avg2cols, int1_dtof6_n10)
as
select
max(udec1_n2),
min(time1_n100),
avg(double1_uniq+ubin1_1000),
int1_dTOf6_n10
from """ + defs.my_schema + """.b2pwl12
group by int1_dTOf6_n10
having int1_dTOf6_n10 > interval '0 00:00:07.875000' day to second(6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a5', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.6 create view with distinct
    stmt = """create view v3a6 (date1,date2,date3,number4)
as
select  distinct(dt1_m_n10), max(date3_n2000),
min(date6_100), count(*)
from b2pwl06
group by dt1_m_n10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a6', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.7 create view on non-updataeable view
    
    stmt = """create view v3a7 (a,b) as
select date3,number4 from v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a7', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.8 create view with all aggregates
    
    stmt = """create view v3a8 (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12) as
select
max(ubin10_n2),
min(char10_nuniq),
max(int10_d_uniq),
min(ts10_n2),
sum(real10_100),
avg(udec10_uniq),
sum(udec11_2000),
min(int11_h_n10),
avg(sbin11_100),
max(time11_20),
min(char11_uniq),
avg(double11_n100)
from b2pwl06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a8', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.9 create view with expressions
    stmt = """create view v3a9 (d1,mx1,mx2,s1,h1,s2)
as
select
day(min(ts10_n2)),
max(ubin10_n2)+avg(udec10_uniq),
max(int10_d_uniq)+min(int11_h_n10),
sum(udec11_2000)/avg(sbin11_100),
hour(max(time11_20)),
sum(real10_100)-avg(double11_n100)
from b2pwl06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a9', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.10 create view with subquery
    stmt = """create view v3a10 (a1,m1)
as
select char12_n2000,
int12_yTOm_100
from b2pwl06
where char12_n2000 < (select max(char0_uniq) from """ + defs.my_schema + """.b2pwl12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a10 where a1 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a10', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.11 create view with duplicate column references
    stmt = """create view v3a11 (a1,m1,a2)
as
select char12_n2000,
int12_yTOm_100,
char12_n2000
from b2pwl06
where int12_ytom_100 < interval '6-02' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from v3a11 where a1 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('v3a11', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    stmt = """drop view v3a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v3a11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-----------------------------------
    _testmgr.testcase_end(desc)

def test004(desc="""Create Updateable View"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #-----------------------------------
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table "everydatatype"
(
char_len1            char character set ISO88591 upshift  default 't' not null ,
pic_char_2           pic x display upshift default 't' not null,
char_vary_3          character varying (100) upshift default 'ttttt' not null,
var_char_4           varchar  (20) upshift default 'thunder' not null,
numeric_5            numeric (9,5) unsigned default 43.55 not null not droppable,
"small_6"	      smallint unsigned default 43 not null,
int_7                integer unsigned default 143 not null,
large_8              largeint default 11111143 not null,
dec_9                dec(9,3) unsigned default 43.43 not null,
pic_10               picture s9(6)V99 display sign is leading default 666643.43 not null not droppable,
float_11             float(11) default 1.43E43 not null,
real_12              real default 1.00E38 not null,
double_13            double precision default 1.43E1 not null,
"date_14"              date default date '1943-10-10' not null,
"time6_15"             time(6) default time '12:43:43.111111' not null unique,
timestamp_16         timestamp(6) default timestamp '1943-12-12 10:10:43.101010' not null unique,
int_17               interval year to month default interval '43-05' year to month not null,
primary key (var_char_4, int_17) not droppable,
unique  (char_len1, pic_char_2, char_vary_3, var_char_4),
unique  ("small_6", int_7, large_8, dec_9),
unique  ("date_14", "time6_15", timestamp_16, int_17)
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into "everydatatype" values
('a','a','a03','a20',1111.11111,1,1,1,111111.111,-1111.11,11.11E-11,11.12E-12, 13.13e-13,
date '2001-01-01', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '01-01' year to month),
('z','z','z03','z20',2111.11111,2,2,2,211111.111,-2111.11,21.11E-11,21.12E-12, 14.13e-14,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #a04.1 create view with check option
    stmt = """create view "a4t1" ("first*col", "seco(nd)col","third?col")
as
select "time6_15","date_14", large_8 from "everydatatype"
where large_8 > 1
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"a4t1"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""")
    
    stmt = """showddl "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.2 create view with cascaded check option
    stmt = """create view "a4t2" (generic_int, best_time, "birthday")
as
select "small_6",timestamp_16, "date_14" from "everydatatype"
where dayofmonth("date_14") = 1
with cascaded check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"a4t2"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.3 create view on updateable view with check option
    stmt = """create view "newview43" ("onedigits*10","four+1=digits", "any#of chars","int(17)")
as
select pic_10, numeric_5, char_vary_3, int_17 from "everydatatype"
where pic_10 < numeric_5 and char_vary_3  not like '%T%'
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view "newview_on_newview43"
as
select * from "newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"newview_on_newview43"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.4 create view without check option, update with row
    #that violates where clause
    stmt = """create view "noupdatechecking" (c1, c2)
as
select int_7, large_8 from "everydatatype"
where int_7 <> 43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"noupdatechecking"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.5 create view without check option, insert with row
    #that violates where clause
    stmt = """create view "nocheckingallowed" ("anyval1", "anyval2", "anyval3")
as
select var_char_4,
numeric_5,
"small_6"
from "everydatatype"
where numeric_5 + "small_6" < 43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"nocheckingallowed"', '', defs.work_dir + """/obeyfile""") 
    stmt = """drop view "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "nocheckingallowed";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.6 create view with check option, update with row
    #that violates view predicate, but doesn't select any rows
    stmt = """create view "ZeroRowsExpected" (noval1, noval2)
as
select "date_14", "time6_15" from "everydatatype"
where "date_14" > date '2002-07-23'
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """showddl "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile('"ZeroRowsExpected"', '', defs.work_dir + """/obeyfile""") 
    
    stmt = """drop view "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel  "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    stmt = """drop view "a4t1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "a4t2";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "newview_on_newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "newview43";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "noupdatechecking";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view "ZeroRowsExpected";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table "everydatatype" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema """ + defs.my_schema + """ CASCADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

