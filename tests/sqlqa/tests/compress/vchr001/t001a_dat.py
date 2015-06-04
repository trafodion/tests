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
    
    stmt = """insert into t001t1 values
(1,'A','aa','0001','ABCDEFGH'),
(2,'B','bb','0002','BCDEFGHI'),
(3,'C','cc','0003','CDEFGHIJ'),
(4,'D','dd','0004','DEFGHIJK'),
(5,'E','ee','0005','EFGHIJKL'),
(6,'F','ff','0006','FGHIJKLM'),
(7,'G','gg','0007','GHIJKLMN'),
(8,'H','hh','0008','HIJKLMNO'),
(9,'I','ii','0009','IJKLMNOP'),
(10,'J','jj','0010','JKLMNOPQ'),
(11,'K','kk','0011','KLMNOPQR'),
(12,'L','ll','0012','LMNOPQRS'),
(13,'M','mm','0013','MNOPQRST'),
(14,'N','nn','0014','NOPQRSTU'),
(15,'O','oo','0015','OPQRSTUV'),
(16,'P','pp','0016','PQRSTUVW'),
(17,'Q','qq','0017','QRSTUVWX'),
(18,'R','rr','0018','RSTUVWXY'),
(19,'S','ss','0019','STUVWXYZ'),
(20,'T','tt','0020','TUWVXYZA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)

