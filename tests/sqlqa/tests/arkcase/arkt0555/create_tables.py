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


def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)
    
    stmt = """drop table b2uns01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table b2uns01 
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
udec1_100           Decimal(2) unsigned    not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btuns07;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table btuns07 
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,
varchar2_uniq       varchar(64)      not null,
-- length = 8
primary key ( varchar2_uniq ASC ) not droppable
)
store by primary key
--  attributes audit
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b2pwl02;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table b2pwl02 
(
char0_n10           Character(2)
default 'AD' heading 'char0_n10 with default AD',
sbin0_uniq          Smallint                   not null,
sdec0_n500          Decimal(18)                        ,
date0_uniq          Date                  no default not null,
int0_yTOm_nuniq     Interval year(5) to month       no default,    
    
int1_hTOs_1000      Interval hour(2) to second(0)   not null,
date1_n4            Date                               ,
real1_uniq          Real                no default not null,
ubin1_n2            Numeric(4) unsigned      no default,
udec1_100           Decimal(2) unsigned        not null,    

char2_2             Character(2)               not null,
sbin2_nuniq         Largeint                           ,
sdec2_500           Decimal(9) signed    no default not null,
date2_uniq          Date                       not null,
int2_dTOf6_n2       Interval day to second(6)      no default,
real2_500           Real                       not null,    

real3_n1000         Real                               ,
int3_yTOm_4         Interval year(1) to month no default not null,
date3_n2000         Date                            no default,
udec3_n100          Decimal(9) unsigned                ,
ubin3_n2000         Numeric(4) unsigned                ,
char3_4             Character(8)             no default not null,
sdec4_n20           Decimal(4)                       no default,
int4_yTOm_uniq      Interval year(5) to month   not null,
sbin4_n1000         Smallint                           ,
time4_1000          Time                     no default not null,
char4_n10           Character(8)               no default,
real4_2000          Real                       not null,    

char5_n20           Character(8)                       ,
sdec5_10            Decimal(9) signed        no default not null,
ubin5_n500          Numeric(9) unsigned              no default,
real5_uniq          Real                       not null,
dt5_yTOmin_n500     Timestamp(0)            ,
int5_hTOs_500       Interval hour to second(0)  no default not null,    

int6_dTOf6_nuniq    Interval day to second(6)     no default,
sbin6_nuniq         Largeint                      no default,
double6_n2          Float(23)                          ,
sdec6_4             Decimal(4) signed        no default not null,
char6_n100          Character(8)               no default,
date6_100           Date                       not null,    

time7_uniq          Time                       not null,
sbin7_n20           Smallint                   no default,
char7_500           Character(8)             no default not null,
int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
udec7_n10           Decimal(4) unsigned                ,
real7_n4            Real                               ,
ubin8_10            Numeric(4) unsigned        not null,
int8_y_n1000        Interval year(3)                   ,
date8_10            Date                     no default not null,
char8_n1000         Character(8)                no default,
double8_n10         Double Precision           no default,
sdec8_4             Decimal(9) unsigned        not null,    

sdec9_uniq          Decimal(18) signed       no default not null,
real9_n20           Real                               ,
time9_n4            Time                               ,
char9_100           Character(2)             no default not null,
int9_dTOf6_2000     Interval day to second(6)   no default not null,
ubin9_n4            Numeric(9) unsigned            no default,    

ubin10_n2           Numeric(4) unsigned            no default,
char10_nuniq        Character(8)                       ,
int10_d_uniq        Interval day(6)            not null,
ts10_n2             Timestamp                          ,
real10_100          Real                       not null,
udec10_uniq         Decimal(9) unsigned      no default not null,    

udec11_2000         Decimal(9) unsigned      no default not null,
int11_h_n10         Interval hour(1)                no default,
sbin11_100          Integer                    not null,
time11_20           Time                       not null,
char11_uniq         Character(8)               not null,
double11_n100       Double Precision                   ,
real12_n20          Real                               ,
ubin12_2            Numeric(4) unsigned      no default not null,
dt12_mTOh_1000      Timestamp(0)        no default not null,
sdec12_n1000        Decimal(18) signed            no default,
char12_n2000        Character(8)                  no default,
int12_yTOm_100      Interval year to month     not null,    

int13_yTOm_n1000    Interval year to month             ,
udec13_500          Decimal(9) unsigned      no default not null,
sbin13_n100         PIC S9(9)V9 COMP           no default,
ts13_uniq           Timestamp                  not null,
char13_1000         Character(8)               not null,
real13_n1000        Real                               ,    

sbin14_1000         Integer                  no default not null,
double14_nuniq      Float(23)                   no default,
udec14_100          Decimal(4) unsigned        not null,
char14_n500         Character(8)                       ,
int14_d_500         Interval day(3)          no default not null,
ts14_n100           Timestamp                    no default,    

dt15_mTOh_n100      Timestamp(0)                 no default,
double15_uniq       Double Precision           not null,
sbinneg15_nuniq     Largeint                           ,
sdecneg15_100       Decimal(9) signed        no default not null,
int15_dTOf6_n100    Interval day to second(6)   no default,
char15_100          Character(8)               not null,
dt16_m_n10          Date                     ,
int16_h_20          Interval hour            no default not null,
ubin16_n10          Numeric(4) unsigned         no default,
sdec16_uniq         Decimal(18) signed         not null,
char16_n20          Character(5)        ,   -- len = 2,4
real16_10           Real                     no default not null,    

int17_y_n10         Interval year(1)            no default,
dt17_yTOmin_uniq    Timestamp(0)    not null,
real17_n100         Real                               ,
sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
sdec17_nuniq        Decimal(18)                no default,
char17_2            Character(8)               not null    

) number of partitions 3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table btpwl08;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table btpwl08 
(
varchar0_100     VarChar(1000)   not null,
-- len = 16,1000
char0_1000       PIC x(32)        not null,
sbin0_500        PIC S9(9) COMP   not null,
udec0_2000       PIC 9(9)         not null,
ubin0_1000       PIC 9(9) COMP    not null,
sdec0_uniq       PIC S9(9)        not null,    

sbin1_100        Numeric(9) signed     not null,
char1_4          PIC x(5)   not null, -- len = 2,4
udec1_10         PIC 9(9)              not null,
ubin1_4          Numeric(9) unsigned   not null,
sdec1_2          PIC S9(9)             not null,    

sbin2_2          PIC S9(2) COMP     not null,
ubin2_4          PIC 9(2) COMP      not null,
sdec2_10         PIC S9(2)          not null,
varchar2_10      VarChar(15)   not null, -- len = 2
varchar2_100     VarChar(25)   not null, -- len = 16    

sbin3_1000       Numeric(5) signed     not null,
udec3_2000       PIC 9(5)              not null,
char3_1000       PIC x(300)   not null, -- len = 64,300
sdec3_500        PIC S9(5)             not null,
ubin3_uniq       Numeric(5) unsigned   not null,
sbin4_2          Numeric(1,1) signed     not null,
ubin4_4          Numeric(1,1) unsigned   not null,
varchar4_1000    VarChar(16)   not null, -- len = 16
sdec4_10         Decimal(1,1) signed     not null,
udec4_2          Decimal(1,1) unsigned   not null,    

sbin5_4          Numeric(4) signed     not null,
ubin5_20         Numeric(9) unsigned   not null,
udec5_20         Decimal(4) unsigned   not null,
varchar5_4       VarChar(8)   not null, -- len = 8
sdec5_100        Decimal(18) signed    not null,    

sbin6_uniq       PIC S9(4) COMP     not null,
sdec6_2000       PIC S9(4)          not null,
udec6_500        PIC 9(4)           not null,
varchar6_20      VarChar(32)   not null, -- len = 32
ubin6_2          PIC  9(4) COMP     not null,    

sbin7_2          SMALLINT signed         not null,
sdec7_10         Decimal(4,1) signed     not null,
char7_uniq       Character(100)   not null, -- len = 16
udec7_20         Decimal(4,1) unsigned   not null,
ubin7_100        SMALLINT unsigned       not null,    

sbin8_1000       Numeric(18) signed      not null,
varchar8_uniq    VarChar(32)   not null, -- len = 16
sdec8_2000       PIC S9(3)V9             not null,
udec8_500        PIC 9(3)V9              not null,
ubin8_2          Numeric(4,1) unsigned   not null,
sbin9_4          PIC S9(3)V9 COMP      not null,
char9_uniq       Character(8)          not null,
udec9_10         Decimal(5) unsigned   not null,
sdec9_20         Decimal(5) signed     not null,
ubin9_100        PIC 9(3)V9 COMP       not null,    

sbin10_uniq       PIC S9(9) COMP     not null,
ubin10_1000       PIC 9(9) COMP      not null,
varchar10_20      VarChar(32)   not null, -- len = 8
udec10_2000       PIC 9(9)           not null,
sdec10_500        PIC S9(18)         not null,    

sbin11_2000      PIC S9(5) COMP        not null,
sdec11_20        Decimal(5,5) signed   not null,
varchar11_2      VarChar(32)   not null, -- len = 4
ubin11_2         PIC 9(5) COMP         not null,
char11_4         Character(2)          not null,    

sbin12_1000      Numeric(9) signed     not null,
sdec12_100       PIC S9(9)             not null,
varchar12_4      VarChar(32)   not null, -- len = 16
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
varchar14_2000   VarChar(64)   not null, -- len = 16,64    

sbin15_2         INTEGER signed          not null,
udec15_4         Decimal(9,2) unsigned   not null,
varchar15_uniq   VarChar(8)   not null, -- len = 8
ubin15_uniq      INTEGER unsigned        not null,
sdec15_10        Decimal(9,2) signed     not null,    

sbin16_20        Numeric(9,2) signed     not null,
sdec16_100       PIC S9(7)V9(2)          not null,
ubin16_1000      Numeric(9,2) unsigned   not null,
udec16_1000      PIC 9(7)V9(2)           not null,
varchar16_100    VarChar(128)       not null,
-- len = 16,64    

sbin17_uniq      Numeric(10) signed   not null,
sdec17_20        Decimal(2) signed    not null,
ubin17_2000      PIC 9(7)V9(2) COMP   not null,
char17_100       Character(100)   not null, -- len = 16
varchar17_20     VarChar(256)   not null, -- len = 64    

sbin18_uniq      Numeric(18) signed   not null,
varchar18_uniq   VarChar(60)   not null, -- len = 8
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
varchar20_1000   VarChar(100)   not null,
-- len = 16,64
sdec20_uniq      PIC S9(9)   not null, -- range: 0-24999    

primary key  ( varchar2_10    DESC,
varchar11_2    ASC,
ubin11_2       ASC,
varchar15_uniq ASC ) not droppable
) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns01 
(
CHAR0_09_UNIQ                  CHAR(8) NOT NULL
, VARCHAR0_MONEY_100             VARCHAR(8)
, CHAR0_AZ_UNIQ                  CHAR(8)
, VARCHAR0_AZAZ_20               VARCHAR(15)
, CHAR0_AAZY_UNIQ                CHAR(8)
, VARCHAR1_AAZZB_500             VARCHAR(8)
, CHAR1_AAZZ09BP_UNIQ            CHAR(8)
, UDEC1_UNIQ                     DECIMAL( 9, 0 ) UNSIGNED
, VARCHAR1_ASCII_UNIQ            VARCHAR(8)
, VARCHAR1_UNIQ                  VARCHAR(8)
, PRIMARY KEY (CHAR0_09_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns05 
(
CHAR0_AAZY_20                  CHAR(1)
, NCHAR0_UNIQ                    CHAR(16)
, CHAR0_09_COLDESCAN_100         CHAR(8)
, SBIN0_UNIQ                     NUMERIC( 18, 0) NOT NULL
, CHAR0_AAZZ09BP_COLDESCAN_100   CHAR(8)
, NCHAR1_UNIQ                    CHAR(16)
, NVARCHAR1_AZAZ_10              VARCHAR(16)
, CHAR1_AZ_2                     CHAR(8)
, CHAR1_COLCHSET_4               CHAR(8)
, CHAR1_AAZZB_COLCASEINS_500     CHAR(8)
, PRIMARY KEY (SBIN0_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns07;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns07 
(
NVARCHAR0_4                    VARCHAR(16)
, NCHAR0_AZAZ_10                 CHAR(16)
, CHAR0_AZAZ_20                  CHAR(8)
, CHAR0_COLBIN_100               CHAR(8)
, CHAR0_AAZZ09BP_COLDESC_500     CHAR(8)
, SDEC1_UNIQ                     PIC S9(9) NOT NULL
, CHAR1_AAZZ09BP_UNIQ            CHAR(8)
, VARCHAR1_AZAZ_COLBCSAME_20     VARCHAR(8)
, CHAR1_AAZY_COLBCSAME_100       CHAR(8)
, CHAR1_AAZZB_COLCASEINS_UNIQ    CHAR(8)
, PRIMARY KEY (SDEC1_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table b3uns09;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE b3uns09 
(
CHAR0_ISO_COLISOASC_100        CHAR(8)
, CHAR0_ISOASC_COLDESC_UNIQ      CHAR(8)
, NCHAR0_AZ_UNIQ                 CHAR(16)
, NVARCHAR0_AZ_1000              VARCHAR(16)
, CHAR0_AAZY_500                 CHAR(8)
, CHAR1_100                      CHAR(8)
, CHAR1_COLDESCAN_20             CHAR(8)
, CHAR1_ASCII_COLDESC_500        CHAR(8)
, SDEC1_UNIQ                     DECIMAL( 18, 0 ) NOT NULL
, CHAR1_ISOASC_UNIQ              CHAR(8)
, PRIMARY KEY (SDEC1_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *Exit Status: 0*

    tablelist = [['b2uns01', '1500'], ['btuns07', '1500'], ['b2pwl02', '5000'],
                 ['btpwl08', '5000'], ['b3uns01', '1500'], ['b3uns05', '1500'],
                 ['b3uns07', '1500'], ['b3uns09', '1500']]
    delim = ','
    for t in tablelist:
        name = t[0]
        row_count = t[1]
        table = name
        data_file = defs.test_dir + '/' + name + '.dat'
        output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, delim)
        _dci.expect_loaded_msg(output)

        stmt = """select count(*) from """ + name + """;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_str_token(output, row_count)

    _testmgr.testcase_end(desc)

