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
    
def test001(desc="""insflt100"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # insflt100.sql
    # jclear
    # 1997-04-30
    # setup for the new aggregate tests
    # create table float100 (
    #     counter int,
    #     flt100  float (5)
    #     );
    #
    stmt = """insert into float100 values (1, 923.165),
(2, -23402.29813),
(3, -1099.17907),
(4, -16426.31447),
(5, 20213.31810),
(6, 29818.85),
(7, -22996.12590),
(8, 3978.1295),
(9, 23973.6270),
(10, 14638.8859),
(11, 13055.7429),
(12, -4563.17409),
(13, 6631.30917),
(14, 22200.7946),
(15, -8096.6235),
(16, 5723.21179),
(17, null),
(18, -2353.20252),
(19, 21897.5482),
(20, 25241.27198),
(21, 11893.29957),
(22, -11795.18043),
(23, 22291.12863),
(24, -3245.28160),
(25, 12562.27447),
(26, 26303.18313),
(27, 10651.20795),
(28, -26072.18540),
(29, -8933.2793),
(30, 19192.2009),
(31, 7171.404),
(32, 29952.5984),
(33, 2816.7658),
(34, 11110.17587),
(35, -7469.14291),
(36, -301.10414),
(37, 20922.15772),
(38, -25621.10132),
(39, 8836.22100),
(40, 11279.18076),
(41, 12078.886),
(42, 16115.31404),
(43, 7795.1481),
(44, 7285.21604),
(45, 10682.2437),
(46, -26198.11614),
(47, 1771.23991),
(48, 14551.15028),
(49, 9346.15078),
(50, 26483.10435);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 50)
    
    stmt = """insert into float100 values
(51, 27618.23799),
(52, 29133.9263),
(53, -32235.29774),
(54, 17640.29736),
(55, -7630.12854),
(56, 7318.2539),
(57, 15904.29827),
(58, 6451.10635),
(59, 25646.21622),
(60, 23954.4081),
(61, -21905.7392),
(62, 18744.14881),
(63, -17410.27530),
(64, 8904.12736),
(65, 27503.469),
(66, 18111.723),
(67, null),
(68, 11873.16074),
(69, -15409.19300),
(70, 25332.12477),
(71, -11930.11949),
(72, -12587.9973),
(73, null),
(74, -12517.30126),
(75, 20853.11017),
(76, 29976.5915),
(77, 4496.323),
(78, 30727.3243),
(79, -15085.15831),
(80, -6076.25995),
(81, 11246.25597),
(82, -14002.3692),
(83, 29977.4751),
(84, 21714.20102),
(85, -22963.2342),
(86, 13472.5597),
(87, 16016.2177),
(88, -24759.195),
(89, 31529.4646),
(90, 9587.13470),
(91, 16623.19275),
(92, 21229.31211),
(93, -3295.1782),
(94, -23340.14211),
(95, -22359.15204),
(96, 8345.13085),
(97, 30248.26280),
(98, 2228.15125),
(99, 25836.9876),
(100, -9990.7532);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 50)
    
    stmt = """select
count (*) as CountStar,
cast (sum (flt100) as dec (18,5)) as SumTotal,
cast (avg (flt100) as dec (18,5)) as Average
from float100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insflt100exp""", 'insflt100c')
    # expect values 100, 615559.49587, 6155.59495
    
    stmt = """select
cast (max (flt100) as dec (18,5)) as M1,
cast (min (flt100) as dec (18,5)) as M2
from float100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insflt100exp""", 'insflt100d')
    # expect values 31529.46460, -32235.29774
    
    _testmgr.testcase_end(desc)

