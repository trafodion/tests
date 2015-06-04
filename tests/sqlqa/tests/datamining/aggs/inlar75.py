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
    
def test001(desc="""inlar75"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """insert into lar75 values
(1,  7192270),
(2,  699611642),
(3,  2105732741),
(4,  200833125),
(5,  28190139),
(6,  174123317),
(7,  137631906),
(8,  1692512277),
(9,  324236364),
(10, 251341692),
(11, 505831097),
(12, 96356904),
(13, 943573),
(14, 191949886),
(15, 294513418),
(16, 1687918933),
(17, 436726058),
(18, 810823601),
(19, 13907900),
(20, 27531873),
(21, 410917701),
(22, 1745321910),
(23, 1237814519),
(24, 2085518206),
(25, 915312139),
(26, 503525624),
(27, 1155211592),
(28, 66766765),
(29, 74415857),
(30, 2024229943),
(31, 81030669),
(32, 233604180),
(33, 548425266),
(34, 1921727822),
(35, 264964485),
(36, 1373819377),
(37, 1416025784),
(38, 915127698),
(39, 252429708),
(40, 1825027105),
(41, 12345064),
(42, 1686810796),
(43, 1668623648),
(44, 1904710861),
(45, 9034950),
(46, 501517563),
(47, 431618092),
(48, 328819062),
(49, 60214368),
(50, 652411069),
(51, 1550613942),
(52, 310565777),
(53, 115847633),
(54, 267687820),
(55, 273469479),
(56, 286389401),
(57, 20645071),
(58, 1006631358),
(59, 206928404),
(60, 1152330362),
(61, 1881013521),
(62, 273417854),
(63, 900231039),
(64, 972223702),
(65, 402422339),
(66, 297725434),
(67, 167576836),
(68, 263608250),
(69, 120519508),
(70, 118628630),
(71, 1566030716),
(72, 1147529988),
(73, 551530113),
(74, 1615121664),
(75, 1384015358);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 75)
    _testmgr.testcase_end(desc)

