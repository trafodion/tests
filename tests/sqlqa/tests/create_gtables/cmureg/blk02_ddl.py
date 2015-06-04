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
    
    stmt = """CREATE TABLE blk02 
(
UNIQUE1           INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE2           INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWO               INT NO DEFAULT NOT NULL NOT DROPPABLE
, FOUR              INT NO DEFAULT NOT NULL NOT DROPPABLE
, TEN               INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTY            INT NO DEFAULT NOT NULL NOT DROPPABLE
, ONEPERCENT        INT NO DEFAULT NOT NULL NOT DROPPABLE
, TENPERCENT        INT NO DEFAULT NOT NULL NOT DROPPABLE
, TWENTYPERCENT     INT NO DEFAULT NOT NULL NOT DROPPABLE
, FIFTYPERCENT      INT NO DEFAULT NOT NULL NOT DROPPABLE
, UNIQUE3           INT NO DEFAULT NOT NULL NOT DROPPABLE
, EVENONEPERCENT    INT NO DEFAULT NOT NULL NOT DROPPABLE
, ODDONEPERCENT     INT NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU1          VARCHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRINGU2          VARCHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, STRING4           VARCHAR(52) NO DEFAULT NOT NULL NOT DROPPABLE
, a1                char(1) default 'a' not null
, a2                char(2) default 'bb'
, PRIMARY KEY (UNIQUE2) not droppable
)
attribute blocksize 4096, extent (20480, 20480)
;"""
    output = _dci.cmdexec(stmt)
