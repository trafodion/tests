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
(1,'1','aa','0001','ABCDEFGH','aaaa0001','A'),
(2,'1','bb','0002','BCDEFGHI','aaaa0002','B'),
(3,'1','cc','0003','CDEFGHIJ','cccc0003','C'),
(4,'1','dd','0004','DEFGHIJK','cccc0004','D'),
(5,'1','ee','0005','EFGHIJKL','eeee0005','E'),
(6,'2','ff','0006','FGHIJKLM','eeee0006','F'),
(7,'2','gg','0007','GHIJKLMN','gggg0007','G'),
(8,'2','hh','0008','HIJKLMNO','gggg0008','H'),
(9,'2','ii','0009','IJKLMNOP','iiii0009','I'),
(10,'2','jj','0010','JKLMNOPQ','iiii0010','J'),
(11,'3','kk','0011','KLMNOPQR','kkkk0011','K'),
(12,'3','ll','0012','LMNOPQRS','kkkk0012','L'),
(13,'3','mm','0013','MNOPQRST','mmmm0013','M'),
(14,'3','nn','0014','NOPQRSTU','mmmm0014','N'),
(15,'3','oo','0015','OPQRSTUV','oooo0015','O'),
(16,'4','pp','0016','PQRSTUVW','oooo0016','P'),
(17,'4','qq','0017','QRSTUVWX','qqqq0017','Q'),
(18,'4','rr','0018','RSTUVWXY','qqqq0018','R'),
(19,'4','ss','0019','STUVWXYZ','ssss0019','S'),
(20,'4','tt','0020','TUWVXYZA','ssss0020','T');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
