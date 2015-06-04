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
    
    stmt = """insert into t002t1 values
(1,'A','aa','ABCDEFGH','0001'),
(2,'B','bb','BCDEFGHI','0002'),
(3,'C','cc','CDEFGHIJ','0003'),
(4,'D','dd','DEFGHIJK','0004'),
(5,'E','ee','EFGHIJKL','0005'),
(6,'F','ff','FGHIJKLM','0006'),
(7,'G','gg','GHIJKLMN','0007'),
(8,'H','hh','HIJKLMNO','0008'),
(9,'I','ii','IJKLMNOP','0009'),
(10,'J','jj','JKLMNOPQ','0010'),
(11,'K','kk','KLMNOPQR','0011'),
(12,'L','ll','LMNOPQRS','0012'),
(13,'M','mm','MNOPQRST','0013'),
(14,'N','nn','NOPQRSTU','0014'),
(15,'O','oo','OPQRSTUV','0015'),
(16,'P','pp','PQRSTUVW','0016'),
(17,'Q','qq','QRSTUVWX','0017'),
(18,'R','rr','RSTUVWXY','0018'),
(19,'S','ss','STUVWXYZ','0019'),
(20,'T','tt','TUWVXYZA','0020');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
