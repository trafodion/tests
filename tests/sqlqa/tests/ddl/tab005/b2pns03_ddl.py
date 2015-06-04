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

# Single column datetime TIME key 1500 recs

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table b2pns03
(
sbin0_4             Integer                       default 3 not null,
time0_uniq          Time                          not null,
varchar0_uniq       VarChar(8)                    no default not null,
sdec0_n1000         Decimal(9)                    no default,
int0_dTOf6_4        Interval day to second(6)     not null,
ts1_n100            Timestamp     heading 'ts1_n100 allowing nulls',
ubin1_20            Numeric(9) unsigned           no default not null,
int1_yTOm_n100      Interval year(1) to month     no default,
double1_2           Double Precision              not null,
udec1_nuniq         Decimal(4) unsigned           ,
primary key ( time0_uniq  DESC)
)
;"""
# location """ + gvars.g_disc1 + """
# store by primary key
# range partition
# (
# add first key time '00:16:39' location """ + gvars.g_disc2 + """,
# add first key time '00:08:19' location """ + gvars.g_disc3 + """
# )
# ;"""
    output = _dci.cmdexec(stmt)
