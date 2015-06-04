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
    
def test001(desc="""indec100"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # indec.sql
    # jclear
    # 1997-04-30
    # setup for the new aggregate tests
    #
    # create table dec (
    #     counter int,
    #     num     decimal (10, 5) signed
    #     );
    
    stmt = """insert into dec100 values
(1, 2644426372.303),
(2, -218225135.18253),
(3, 440124552.31098),
(4, 3166826641.24139),
(5, 1586229813.24919),
(6, -1140018514.11282),
(7, 2812819634.20213),
(8, 426525440.7895),
(9, -1816912348.21650),
(10, 1230032723.26051),
(11, -151428730.16146),
(12, 1226311251.4682),
(13, 229086683.26287),
(14, -217027893.11161),
(15, 1789410276.17164),
(16, 348420129.9005),
(17, -1721610232.11036),
(18, 1624926.17922),
(19, -1521011358.32407),
(20, 2919711745.18386),
(21, 359432437.14833),
(22, -2956627876.28253),
(23, 312143159.30483),
(24, 1916414009.16563),
(25, -3233727985.27714),
(26, 147312694.756),
(27, -2673526722.26615),
(28, 3084422247.16649),
(29, 141231600.25504),
(30, 261801805.19257),
(31, 2501331372.24695),
(32, -51048273.23983),
(33, 1214829446.10480),
(34, -133230964.18500),
(35, 3241419930.5751),
(36, 1044317834.24119),
(37, null),
(38, 2102727862.19853),
(39, -1937320935.6836),
(40, -803523653.19533),
(41, 298283832.16645),
(42, 2480031526.24037),
(43, -137781532.23087),
(44, 213354062.23884),
(45, -46075256.13514),
(46, -424418324.2234),
(47, 1497014929.6365),
(48, -467612742.4638),
(49, 295496574.22742),
(50, -438525741.17291),
(51, 99467940.20877),
(52, -3245121455.10584),
(53, 1329416433.32333),
(54, 252703603.31657),
(55, -293038504.10009),
(56, 502922169.16277),
(57, null),
(58, 1119018366.23599),
(59, -24920400.21200),
(60, 172666619.14866),
(61, -356314242.27977),
(62, 20310770.1091),
(63, -2232017356.15394),
(64, 2870214805.22410),
(65, 225086062.24634),
(66, -3155727395.10638),
(67, 394319139.9612),
(68, 140931524.852),
(69, -2397322731.15428),
(70, -1477528102.25336),
(71, -637619234.6854),
(72, 197857366.18106),
(73, 1619517592.28727),
(74, -994026073.6056),
(75, 37918836.3115),
(76, -2662622817.29851),
(77, null),
(78, 883822869.20027),
(79, -1281830610.17256),
(80, -2797431886.27459),
(81, 22262774.23493),
(82, -269603698.22595),
(83, 2120015422.7528),
(84, 2688017147.2185),
(85, 2437720981.32336),
(86, -2198912378.5634),
(87, 1353023611.13694),
(88, 56619361.11306),
(89, -2146216591.28667),
(90, 2279214130.20071),
(91, 1523121439.28115),
(92, -27774818.25701),
(93, 1717528235.26864),
(94, -1731724422.22345),
(95, 2677910876.274),
(96, -454531559.8407),
(97, null),
(98, -1617615412.2530),
(99, 314583803.2386),
(100, -2872423304.1944);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    
    stmt = """select
count (*) as CountStar,
cast (sum (num) as dec (18,5)) as SumTotal,
cast (avg (num) as dec (18,5)) as Average
from dec100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/indec100exp""", 'indec100b')
    # expect values 100, 14025330181.37770, 140253301.81377
    
    stmt = """select
cast (max (num) as dec (18,5)) as Maximum_Num,
cast (min (num) as dec (18,5)) as Minimum
from dec100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/indec100exp""", 'indec100c')
    # expect values 3241419930.57510, -3245121455.10584
    
    _testmgr.testcase_end(desc)

