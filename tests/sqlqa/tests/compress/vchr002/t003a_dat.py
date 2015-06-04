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
    
    stmt = """insert into t003t1 values
(1,'A','0001','NULL',101,'ABCDEFGH','00010001','a'),
(2,'B','0002','NULL',102,'ABCDEFGH','00020002','b'),
(3,'C','0003','NULL',103,'ABCDEFGH','00030003','c'),
(4,'D','0004','NULL',104,'ABCDEFGH','00040004','d'),
(5,'E','0005','NULL',105,'ABCDEFGH','00050005','e'),
(6,'F','0006','NULL',106,'ABCDEFGH','00060006','f'),
(7,'G','0007','NULL',107,'ABCDEFGH','00070007','g'),
(8,'H','0008','NULL',108,'ABCDEFGH','00080008','h'),
(9,'I','0009','NULL',109,'ABCDEFGH','00090009','i'),
(10,'J','0010','NULL',110,'ABCDEFGH','00100010','j'),
(11,'K','0011','NULL',111,'ABCDEFGH','00110111','k'),
(12,'L','0012','NULL',112,'ABCDEFGH','00120112','l'),
(13,'M','0013','NULL',113,'ABCDEFGH','00130113','m'),
(14,'N','0014','NULL',114,'ABCDEFGH','00140114','n'),
(15,'O','0015','NULL',115,'ABCDEFGH','00150115','o'),
(16,'P','0016','NULL',116,'ABCDEFGH','00160116','p'),
(17,'Q','0017','NULL',117,'ABCDEFGH','00170117','q'),
(18,'R','0018','NULL',118,'ABCDEFGH','00180118','r'),
(19,'S','0019','NULL',119,'ABCDEFGH','00190119','s'),
(20,'T','0020','NULL',120,'ABCDEFGH','00200120','t');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
