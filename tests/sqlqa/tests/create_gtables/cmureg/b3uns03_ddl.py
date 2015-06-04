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
    
    stmt = """CREATE TABLE B3UNS03 
(
VARCHAR0_AAZZ09BP_100          VARCHAR(8)
, CHAR0_ASCII_500                CHAR(8)
, UDEC0_UNIQ                     DECIMAL( 9, 0 ) UNSIGNED NOT NULL
, VARCHAR0_ISO_UNIQ              VARCHAR(8)
, CHAR0_ISOASC_UNIQ              CHAR(8)
, NVARCHAR1_09_UNIQ              VARCHAR(16)
, VARCHAR1_20                    VARCHAR(8)
, NCHAR1_AZ_20                   CHAR(16)
, NVARCHAR_AZAZ_100              VARCHAR(16)
, NCHAR1_UNIQ                    CHAR(16)
, PRIMARY KEY (UDEC0_UNIQ)
);"""
    output = _dci.cmdexec(stmt)
    
