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
    
    stmt = """insert into t002t2 values
(21,'A','aa','ABCDEFGH','0021'),
(22,'B','bb','BCDEFGHI','0022'),
(23,'C','cc','CDEFGHIJ','0023'),
(24,'D','dd','DEFGHIJK','0024'),
(25,'E','ee','EFGHIJKL','0025'),
(26,'F','ff','FGHIJKLM','0026'),
(27,'G','gg','GHIJKLMN','0027'),
(28,'H','hh','HIJKLMNO','0028'),
(29,'I','ii','IJKLMNOP','0029'),
(30,'J','jj','JKLMNOPQ','0030'),
(31,'K','kk','KLMNOPQR','0031'),
(32,'L','ll','LMNOPQRS','0032'),
(33,'M','mm','MNOPQRST','0033'),
(34,'N','nn','NOPQRSTU','0034'),
(35,'O','oo','OPQRSTUV','0035'),
(36,'P','pp','PQRSTUVW','0036'),
(37,'Q','qq','QRSTUVWX','0037'),
(38,'R','rr','RSTUVWXY','0038'),
(39,'S','ss','STUVWXYZ','0039'),
(40,'T','tt','TUWVXYZA','0040');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
