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
import defs

_testmgr = None
_testlist = []
_dci = None

# single column char key
# 5000 recs
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """Create Table btpwl14
(
ubin0_1000       PIC 9(9) COMP     not null,
sdec0_uniq       PIC S9(9)         not null,
varchar0_4       varchar(8)   not null,
char0_500        PIC X(515)        not null,
sbin0_500        PIC S9(9) COMP    not null,
udec0_2000       PIC 9(9)          not null,    

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
char9_uniq       Character(8)   not null,
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
char18_20        PIC X(100)   not null, -- len = 16
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
sdec20_uniq      PIC S9(9)   not null, -- range: 0-24999    

primary key ( char9_uniq   ASC ) not droppable
)
attributes extent(1024,1024), maxextents 512
;"""
    output = _dci.cmdexec(stmt)
