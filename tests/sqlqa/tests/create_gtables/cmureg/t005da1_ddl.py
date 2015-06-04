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
    
    stmt = """Create Table t005da1 
(
col01    varchar(4)       not null heading 'k1',
col02    varchar(4)       ,
col03    varchar(2)       not null,
col04    varchar(16)      not null,
col05    varchar(8)       not null,
col06    varchar(4)       not null heading 'k2',
col07    varchar(4)       not null,
col08    varchar(64)      ,
col09    varchar(8)       not null,
col10    varchar(2)       not null heading 'k3',
col11    char (1) default 'a',
col12    char(2) upshift,
col13    char(3) default '000',
col14    character (3) default null,
col15    char(1) default 'b' heading 'b',
primary key (    col01 ASC,
col06 DESC,
col10 ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition
(add location """ + gvars.g_disc2 + """)
attribute extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)
    stmt = """;"""
    output = _dci.cmdexec(stmt)
