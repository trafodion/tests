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
 
    stmt = """create table "t6a" (
char_len1            char character set ISO88591 upshift not null,
pic_char_2           pic x display upshift not null heading 'picture2',
char_vary_3          character varying (100) upshift not null,
var_char_4           varchar  (220) upshift not null check (var_char_4 <> 'richard nixon'),
numeric_5            numeric (9,5) unsigned not null not droppable,
small_6	      smallint unsigned not null,
int_7                integer unsigned not null check (int_7 < dec_9),
large_8              largeint not null,
dec_9                dec(9,3) unsigned not null no heading,
pic_10               picture s9(6)V99 display sign is leading not null not droppable,
float_11             float(11) not null unique,
real_12              real not null,
double_13            double precision not null,
date_14              date not null heading 'd',
"time6_()"             time not null unique,
timestamp_16         timestamp(6) not null unique,
int_17               interval year to month not null,
-- primary key (timestamp_16, var_char_4, int_17) droppable,
constraint "ct6a" check (large_8 > 0),
unique  (char_len1, pic_char_2, char_vary_3,numeric_5),
unique  (small_6, int_7, large_8, dec_9, pic_10, float_11,real_12),
unique  (double_13, date_14, "time6_()", timestamp_16, int_17)
) store by (numeric_5, pic_10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """showlabel "t6a";"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """insert into "t6a" values
('a','a','a03','a20',2222.11111,1,1,1,111111.111,-1111.33,11.11E-40,11.12E-12, 13.13e-13,
date '2001-01-23', time '12:01:01.111111', timestamp '2001-01-01:01:01:01.111111',
interval '99-01' year to month),
('b','b','b03','b20',2111.11111,2,2,2,211111.111,-2111.11,21.11E-11,21.12E-12, 14.13e-14,
date '2001-01-02', time '12:02:01.111111', timestamp '2001-01-02:01:01:01.222222',
interval '02-02' year to month);"""
    output = _dci.cmdexec(stmt)
    
    # from b2pwl24
    stmt = """create table t6b
(
sbin0_4             Integer                    default 3 not null,
time0_uniq          Time                       not null not droppable
references "t6a"("time6_()"),
varchar0_500        VarChar(11)
default 'GDAAIAAA' not null
heading 'varchar0_500 with default GDAAIAAA',
real0_20            Real                          no default not null,
int0_dTOf6_4        Interval day to second(6)  not null,    

ts1_n100            Timestamp
heading 'ts1_n100 allowing nulls',
ubin1_20            Numeric(9,5) unsigned        no default not null,
int1_yTOm_n100      Interval year(1) to month              no default,
double1_uniq        Double Precision           not null,
udec1_nuniq         Decimal(4) unsigned                ,    

char2_2             Character(2)               not null,
--     sbin2_uniq          Largeint                no default not null not droppable -updated 20040329
sbin2_uniq          Largeint              no default not null not droppable
primary key droppable,
sdec2_500           Decimal(9) signed             no default not null,
date2_uniq          Date                       not null,
int2_dTOf6_n2       Interval day to second(6)            no default,
real2_500           Real                       not null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index it6b on t6b
(sdec2_500, date2_uniq desc, ts1_n100, time0_uniq desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vt6b as select udec1_nuniq, char2_2 from t6b
where char2_2 <> 'me';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    _testmgr.testcase_end(desc)
 
