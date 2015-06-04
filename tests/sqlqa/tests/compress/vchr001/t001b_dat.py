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
    
    stmt = """insert into t001t2 values
(21,'A','aa','0021','ABCDEFGH'),
(22,'B','bb','0022','BCDEFGHI'),
(23,'C','cc','0023','CDEFGHIJ'),
(24,'D','dd','0024','DEFGHIJK'),
(25,'E','ee','0025','EFGHIJKL'),
(26,'F','ff','0026','FGHIJKLM'),
(27,'G','gg','0027','GHIJKLMN'),
(28,'H','hh','0028','HIJKLMNO'),
(29,'I','ii','0029','IJKLMNOP'),
(30,'J','jj','0030','JKLMNOPQ'),
(31,'K','kk','0031','KLMNOPQR'),
(32,'L','ll','0032','LMNOPQRS'),
(33,'M','mm','0033','MNOPQRST'),
(34,'N','nn','0034','NOPQRSTU'),
(35,'O','oo','0035','OPQRSTUV'),
(36,'P','pp','0036','PQRSTUVW'),
(37,'Q','qq','0037','QRSTUVWX'),
(38,'R','rr','0038','RSTUVWXY'),
(39,'S','ss','0039','STUVWXYZ'),
(40,'T','tt','0040','TUWVXYZA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
