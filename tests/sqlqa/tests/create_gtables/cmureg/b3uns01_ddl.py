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
    
    stmt = """CREATE TABLE B3UNS01 
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
