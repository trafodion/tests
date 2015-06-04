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
    
def test001(desc="""inswghts"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # inswghts.sql
    # jclear
    # 1997-04-28
    # new aggregate tests
    # set up for the weights table
    stmt = """select count (*) from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/inswghtsexp""", 'inswghtsa')
    # expect count = 0
    
    stmt = """insert into weights values (1, 1332, 719665186, 4),
(2, 4911, 654275251, 0),
(3, 3528, 422088816, 4),
(4, 271, 954716137, 1),
(5, 2198, 1396880494, 3),
(6, 4266, 1098155791, 0),
(7, 4816, 610157468, 2),
(8, 1669, 459571621, 3),
(9, 4764, 1944693114, 4),
(10, 951, 444368171, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (11, 4513, 567934344, 4),
(12, 2692, 1950389025, 0),
(13, 4516, 1490608966, 5),
(14, 1592, 2008828167, 0),
(15, 185, 466971188, 2),
(16, 1848, 947011677, 5),
(17, 1666, 1026551250, 1),
(18, 1004, 1783262883, 3),
(19, 1758, 1685648800, 5),
(20, 129, 1008174425, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (21, 3331, 2088441118, 0),
(22, 4421, 1946898943, 2),
(23, 798, 101174220, 1),
(24, 571, 1563565589, 3),
(25, 650, 213869866, 4),
(26, 1467, 650972955, 2),
(27, 830, 164354232, 0),
(28, 1152, 505644689, 5),
(29, 862, 222734838, 3),
(30, 454, 421757431, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (31, 1654, 1103218788, 3),
(32, 257, 1810430669, 2),
(33, 2001, 1982558082, 0),
(34, 4053, 1292125843, 3),
(35, 4298, 17106640, 0),
(36, 4805, 202864329, 2),
(37, 788, 883229134, 4),
(38, 902, 1679997167, 3),
(39, 1744, 1861992444, 5),
(40, 4181, 1855436421, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (41, 35, 1075014874, 5),
(42, 3071, 1040971019, 2),
(43, 4390, 1631772648, 5),
(44, 1961, 1596077569, 1),
(45, 1103, 1942715558, 4),
(46, 4144, 1543689959, 2),
(47, 4629, 1750733460, 5),
(48, 125, 1383805245, 3),
(49, 3834, 966966578, 4),
(50, 744, 647756419, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (51, 357, 2064630784, 0),
(52, 2159, 1265542201, 3),
(53, 3863, 1362852478, 5),
(54, 4193, 1897511903, 3),
(55, 3277, 1823285292, 4),
(56, 440, 327961333, 0),
(57, 3790, 1074839690, 3),
(58, 1252, 1451767547, 0),
(59, 3516, 434246424, 2),
(60, 4671, 1134797169, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (61, 1465, 910318422, 0),
(62, 3242, 1285113815, 4),
(63, 1732, 2020690116, 2),
(64, 1678, 1476387757, 4),
(65, 1464, 1948309218, 3),
(66, 4448, 138447475, 5),
(67, 1620, 1973169456, 2),
(68, 4789, 1281625513, 1),
(69, 1562, 2088337198, 2),
(70, 3284, 269441743, 0);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (71, 1061, 1330572380, 4),
(72, 872, 2076629861, 5),
(73, 123, 530735162, 2),
(74, 560, 407950571, 4),
(75, 4446, 1410101832, 0),
(76, 3909, 1070516449, 2),
(77, 669, 726025734, 5),
(78, 2546, 82171079, 3),
(79, 466, 899312372, 4),
(80, 2947, 202248733, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (81, 3716, 1257290898, 1),
(82, 433, 752940643, 4),
(83, 553, 1517109856, 1),
(84, 3677, 16691993, 2),
(85, 2344, 1700401118, 3),
(86, 3910, 1004705215, 4),
(87, 3638, 1507075212, 2),
(88, 4438, 851339221, 5),
(89, 171, 41110506, 2),
(90, 310, 1295306459, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into weights values (91, 2714, 249888120, 4),
(92, 3188, 529181777, 5),
(93, 1518, 103955638, 4),
(94, 1938, 480738743, 1),
(95, 2865, 1848146212, 5),
(96, 3203, 301776013, 3),
(97, 3218, 1276997186, 1),
(98, 525, 1764507219, 3),
(99, 601, 168166288, 0),
(100, 4498, 1795527817, 3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/inswghtsexp""", 'inswghtsb')
    # expect count = 500
    
    stmt = """select
count (*) as CountStar,
sum (small500) as SumSmall,
sum (int500) as SumInt,
avg (small500) as AvgSmall,
avg (int500) as AvgInt
from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/inswghtsexp""", 'inswghtsc')
    # expect SumSmall = 299723, SumInt =  109216225342,
    #        AvgSmall = 2297.23, AvgInt = 1092162253.42
    
    stmt = """select
max (small500) as MaxSmall,
max (int500) as MaxInt,
min (small500) as MinSmall,
min (int500) as MinInt
from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/inswghtsexp""", 'inswghtsd')
    # expect MaxSmall = 4911, MaxInt = 2088441118,
    #        MinSmall = 35,   MinInt = 16691993
    
    _testmgr.testcase_end(desc)

