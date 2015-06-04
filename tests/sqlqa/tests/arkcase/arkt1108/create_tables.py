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
    stmt = """create table TAB1 (vc varchar(9) ) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table TAB4 (vc9 varchar(9)
,vc7 varchar(7)
,vc5 varchar(5)
,vc3 varchar(3)
)  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table TEMPT ( c3 char(3), vc5 varchar(5) )  no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table BTRead5 
(
char0_n10           Char(2)
,
sbin0_uniq          Smallint not null,
sdec0_n500          Numeric(18,0) ,    

ubin1_n2            Numeric(4,0) unsigned
,
udec1_100           Numeric(2,0) unsigned        not null,    

char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                           ,
sdec2_500           Numeric(9,0) signed          not null,    

udec3_n100          Numeric(9,0) unsigned                ,
ubin3_n2000         Numeric(4,0) unsigned                ,
char3_4             Char(8)                   not null
,    

sdec4_n20           Numeric(4,0)                             ,
sbin4_n1000         Smallint                           ,
char4_n10           Char(8)                           ,    

char5_n20           Char(8)                       ,
sdec5_10            Numeric(9,0) signed          not null,
ubin5_n500          Numeric(9,0) unsigned
,    

sbin6_nuniq         Largeint                               ,
sdec6_4             Numeric(4,0) signed          not null,
char6_n100          Char(8)                           ,    

sbin7_n20           Smallint                               ,
char7_500           Char(8)                   not null,
udec7_n10           Numeric(4,0) unsigned
,    

ubin8_10            Numeric(4,0) unsigned        not null,
char8_n1000         Char(8)                           ,
sdec8_4             Numeric(9,0) unsigned        not null,    

sdec9_uniq          Numeric(18,0) signed         not null,
char9_100           Char(2)                   not null,
ubin9_n4            Numeric(9,0) unsigned
,    

ubin10_n2           Numeric(4,0) unsigned                    ,
char10_nuniq        Char(8)                       ,
udec10_uniq         Numeric(9,0) unsigned        not null,    

udec11_2000         Numeric(9,0) unsigned        not null,
sbin11_100          Integer                      not null,
char11_uniq         Char(8)               not null
,    

ubin12_2            Numeric(4,0) unsigned        not null
,
sdec12_n1000        Numeric(18,0) signed                     ,
char12_n2000        Char(8)
,    

udec13_500          Numeric(9,0) unsigned        not null,
char13_1000         Char(8)                      not null
,    

sbin14_1000         Integer                      not null,
udec14_100          Numeric(4,0) unsigned        not null,
char14_n500         Char(8)                       ,    

sbinneg15_nuniq     Largeint                           ,
sdecneg15_100       Numeric(9,0) signed          not null,
char15_100          Char(8)               not null
,    

ubin16_n10          Numeric(4,0) unsigned
,
sdec16_uniq         Numeric(18,0) signed         not null,
char16_n20          Char(5)
,   -- len = 2,4    

sbin17_uniq         Largeint   not null,
sdec17_nuniq        Numeric(18,0)
,
char17_2            Char(8)               not null    

, primary key ( sbin0_uniq )
)
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    #
    stmt = """Insert Into BTRead5 
Values ( NULL , -200, -266,
NULL , 60,
'AA', -3766, -266,
44, 344, 'BA',
-9, -509, NULL ,
'AAAAAAAA', -0, 60, -- (5)
-3766, -2, 'CQAAAAAA',
-4, 'EAAAGAAA', NULL ,
9, 'DBAAAAAA', 1,
-60, 'AK', NULL ,
NULL , 'AEAAJAAB', 3766, -- (10)
344, -44, 'EKAACAAE',
1, -509, 'DBAAAAAB',
60, 'EFAAIAAA',
-766, 66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA', -- (15)
NULL , -2509, 'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert Into BTRead5 
Values ( NULL , -201, -266,
NULL , 60,
'AA', -3766, -266,
44, 344, 'BA',
-9, -509, NULL     ,
'AAAAAAAA', -0, 60, -- (5)
-3766, -2, 'CQAAAAAA',
-4, 'EAAAGAAA', NULL ,
9, 'DBAAAAAA', 1,
-60, 'AK', NULL ,
NULL , 'AEAAJAAB', 3766, -- (10)
344, -44, 'EKAACAAE',
1, -509, 'DBAAAAAB',
60, 'EFAAIAAA',
-766, 66, 'AGAAEAAA',
-4344, -44, 'ATAAAAAA', -- (15)
NULL , -2509, 'BE   ',
-37055, -60, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert Into BTRead5 
Values ( NULL , -101, -272,
NULL , 86,
'BA', -772, -272,
52, 1552, 'AA',
-18, -678, NULL ,
'CBAAAAAA', -6, 86, -- (5)
-772, -0, 'AWAAAAAA',
-12, 'DAAAGAAA', NULL ,
8, 'DEAAMAAA', 2,
-2086, 'CL', NULL ,
NULL , 'CCAAFAAC', 772, -- (10)
1552, -52, 'DKAADAAC',
0, -678, 'DEAAMAAA',
86, 'AHAAGAAA',
-772, 72, 'CEAAHAAA',
-3552, -52, 'ACAAAAAA', -- (15)
NULL , -3678, 'ADAA ',
-49700, -2086, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert Into BTRead5 
Values ( NULL , -100, -65,
NULL , 12,
'BA', -2065, -65,
89, 389, 'CA',
-14, -594, NULL ,
'ACAAAAAA', -2, 312, -- (5)
-2065, -1, 'BPAAAAAA',
-9, 'CFAAEAAA', NULL ,
4, 'FKAAIAAA', 2,
-812, 'AM', NULL ,
NULL , 'AIAALAAA', 2065, -- (10)
389, -89, 'CCAAKAAE',
0, -594, 'FKAAIAAA',
312, 'AJAAGAAA',
-65, 65, 'ABAAEAAA',
-2389, -89, 'BOAAAAAA', -- (15)
NULL , -1594, 'AE   ',
-15935, -812, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert Into BTRead5 
Values ( NULL , -1, -36,
NULL , 95,
'DA', -2536, -36,
89, 789, 'CA',
-17, -417, NULL     ,
'DAAAAAAA', -5, 495, -- (5)
-2536, -0, 'ALAAAAAA',
-9, 'DFAAIAAA', NULL ,
7, 'AGAAKAAA', 1,
-4495, 'DU', NULL     ,
NULL , 'CGAABAAB', 2536, -- (10)
789, -89, 'DGAAHAAE',
1, -417, 'AGAAKAAB',
495, 'BHAAKAAA',
-536, 36, 'CAAAHAAA',
-2789, -89, 'BOAAAAAA', -- (15)
NULL , -4417, 'BCAA ',
-81017, -4495, 'BAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Insert Into BTRead5 
Values ( NULL , -0, -284,
NULL , 2,
'EA', -284, -284,
50, 1950, 'DA',
-6, -866, NULL ,
'CCAAAAAA', -2, 302, -- (5)
-284, -0, 'AJAAAAAA',
-10, 'EGAAGAAA', NULL ,
6, 'FIAAIAAA', 2,
-1802, 'CC', NULL ,
NULL , 'EJAALAAE', 284, -- (10)
1950, -50, 'EDAAAAAA',
0, -866, 'FIAAIAAA',
302, 'DJAAIAAA',
-284, 84, 'EEAAFAAA',
-1950, -50, 'CAAAAAAA', -- (15)
NULL , -866, 'AB   ',
-48764, -1802, 'AAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view  VNRead5 ( n1, c2, c3, c4 ) as
select cast( max(t1.sbinneg15_nuniq) as smallint signed )
, min(t1.char2_2)
, min(t2.char2_2)
, max(t3.char3_4)
from BTRead5 t1
right join BTRead5 t2 on t1.char2_2   = t2.char3_4
left  join BTRead5 t3 on t2.char2_2   = t3.char3_4
group by t1.sbinneg15_nuniq , t1.char2_2 , t2.char2_2 , t3.char3_4
;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

