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
    
    stmt = """create table  """ + defs.my_schema + """.timetable
(query           int not null,
cardinal         real default null,
T1_cost          real default null,
T1_cmp_time      time default null,
T1_time          time default null,
T2_cost          real default null,
T2_cmp_time      time default null,
T2_time          time default null,
--T3_cost          real default null,
--T3_cmp_time      time default null,
--T3_time          time default null,
--T4_cost          real default null,
--T4_cmp_time      time default null,
--T4_time          time default null,
low_time         time default null,
low_type         char(5) default null,
T1_vs_T2_plan    char(6) default null,
primary key (query))
attributes extent(16,64)
no partition
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + defs.my_schema + """.plantable
(
QUERY_NO                         SMALLINT NO DEFAULT NOT NULL NOT DROPPABLE
, MODEL                            CHAR(8)  NO DEFAULT NOT NULL NOT DROPPABLE
, SEQ_NUM                          SMALLINT NO DEFAULT NOT NULL NOT DROPPABLE
, LEFT_CHILD                       SMALLINT DEFAULT NULL
, RIGHT_CHILD                      SMALLINT DEFAULT NULL
, OPERATOR                         CHAR(30) DEFAULT NULL
, primary key (query_no, model,seq_num)
)
attributes extent (16,64)
no partition;"""
    output = _dci.cmdexec(stmt)
    
