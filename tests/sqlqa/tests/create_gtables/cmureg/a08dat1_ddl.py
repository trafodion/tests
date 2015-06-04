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
    
    stmt = """create table a08dat1 (
 orders int no default not null
, ch1 char(1)
, num1 NUMERIC (9,2) UNSIGNED default null no heading
, vch1 char varying(1) heading ''
, sma1 SMALLINT UNSIGNED DEFAULT NULL  heading 'SmallInt'
, vch2 CHARACTER VARYING(255)
, int1 int unsigned constraint int_uniq_cmureg_a08dat1 check (int1 < 10000)
, vch3 CHARACTER VARYING(2) heading 'VARYING(2)'
, dec1 DEC(9,2) UNSIGNED
, num10 NUMERIC (9,2) SIGNED default 7.2 heading 'num_10'
, vch11 char varying(1) heading 'col11'
, sma12 SMALLINT SIGNED default -1 check (sma12 < 65535 and sma12 > -100)
, vch13 CHARACTER VARYING(255) default 'xxx'
, int14 int signed default -100 constraint int14_c_cmureg_a08dat1 check (int14 < 1234567890)
, vch15 CHARACTER VARYING(2) default 'zz'
, dec16 DEC(9,7) SIGNED default -9.99
, vch17 varchar(80) upshift default 'vch17'
, ch18 char(512)
, int19 int default 191919
, vch20 varchar(1024)
, primary key (orders ASC) not droppable
)
;"""
    output = _dci.cmdexec(stmt)
