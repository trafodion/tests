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
(1,'a','0021','0001',21,'0021ABCD','00210021','A'),
(2,'b','0022','0002',22,'0022ABCD','00220022','B'),
(3,'c','0023','0003',23,'0023ABCD','00230023','C'),
(4,'d','0024','0004',24,'0024ABCD','00240024','D'),
(5,'e','0025','0005',25,'0025ABCD','00250025','E'),
(6,'f','0026','0006',26,'0026ABCD','00260026','F'),
(7,'g','0027','0007',27,'0027ABCD','00270027','G'),
(8,'h','0028','0008',28,'0028ABCD','00280028','H'),
(9,'i','0029','0009',29,'0029ABCD','00290029','I'),
(10,'j','0030','0010',30,'ABCD0030','00300130','J'),
(11,'k','0031','0011',31,'ABCD0031','00310131','K'),
(12,'l','0032','0012',32,'ABCD0032','00320132','L'),
(13,'m','0033','0013',33,'ABCD0033','00330133','M'),
(14,'n','0034','0014',34,'ABCD0034','00340134','N'),
(15,'o','0035','0015',35,'ABCD0035','00350135','O'),
(16,'p','0036','0016',36,'ABCD0036','00360136','P'),
(17,'q','0037','0017',37,'ABCD0037','00370137','Q'),
(18,'r','0038','0018',38,'ABCD0038','00380138','R'),
(19,'s','0039','0019',39,'ABCD0039','00390139','S'),
(20,'t','0040','0020',40,'ABCD0040','00400140','T');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
