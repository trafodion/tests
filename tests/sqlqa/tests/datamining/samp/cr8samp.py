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
    
def test001(desc="""cr8samp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # cr8samp
    # jclear
    # 1998-10-27
    # setup for the sampling tests
    #
    # a plain table
    stmt = """create table samptb1 (
a int not null primary key,
b int,
c int,
d int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb1 
as select a, b, c
from samptb1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb1 values
(1, 250, 18237, 2761),
(2, 26456, 23942, 4890),
(3, 14066, 5852, 2359),
(4, 24204, 29007, 30964),
(5, 31145, 27216, 21236),
(6, 28785, 15410, 11508),
(7, 23689, 3687, 9320),
(8, 22344, 14579, 23103),
(9, 17379, 32016, 4913),
(10, 24584, 3908, 13819),
(11, 899, 30990, 21621),
(12, 19161, 22482, 686),
(13, 26163, 17160, 15180),
(14, 30568, 8394, 26159),
(15, 335, 7734, 11296),
(16, 1583, 6024, 17436),
(17, 7925, 9559, 25436),
(18, 13313, 26473, 19672),
(19, 3718, 24765, 7359),
(20, 10104, 1794, 30067),
(21, 7776, 13450, 13866),
(22, 16417, 9251, 10013),
(23, 13088, 10869, 9163),
(24, 17780, 29803, 13539),
(25, 12242, 23734, 17637),
(26, 10228, 13157, 7399),
(27, 32724, 28641, 12207),
(28, 28951, 22615, 22112),
(29, 24154, 10201, 12292),
(30, 3774, 23891, 32759),
(31, 16591, 18478, 18382),
(32, 28004, 7725, 14945),
(33, 24715, 10866, 20858),
(34, 24662, 12631, 26949),
(35, 5528, 21876, 17365),
(36, 14728, 30170, 2262),
(37, 22398, 30302, 21536),
(38, 15078, 14567, 20636),
(39, 6723, 31021, 7746),
(40, 18741, 6835, 3177),
(41, 11560, 12278, 25694),
(42, 3296, 3478, 31347),
(43, 3540, 4341, 11829),
(44, 1857, 15273, 10745),
(45, 7646, 8549, 26139),
(46, 9027, 7773, 22541),
(47, 8693, 14211, 21621),
(48, 32382, 28852, 12371),
(49, 14629, 26702, 23527),
(50, 9231, 12330, 13779),
(51, 24540, 17895, 26565),
(52, 17627, 27000, 31794),
(53, 26046, 6557, 27495),
(54, 12549, 26025, 21488),
(55, 20086, 4357, 27752),
(56, 1211, 16700, 11385),
(57, 13553, 30637, 11008),
(58, 11940, 23122, 17710),
(59, 17879, 8017, 25330),
(60, 16533, 9229, 25263),
(61, 4377, 5787, 9414),
(62, 27487, 7346, 12303),
(63, 7141, 21196, 14928),
(64, 11468, 12589, 19387),
(65, 4976, 2793, 15014),
(66, 8995, 5118, 20015),
(67, 5699, 17214, 12570),
(68, 15312, 18113, 27872),
(69, 3355, 32341, 22482),
(70, 6920, 7380, 17881),
(71, 19835, 17588, 12823),
(72, 14453, 8891, 28922),
(73, 3960, 18171, 7021),
(74, 20821, 26963, 14823),
(75, 28015, 22077, 30737),
(76, 2706, 1284, 29178),
(77, 32678, 23721, 26743),
(78, 32185, 28766, 11230),
(79, 32514, 29920, 1242),
(80, 477, 16109, 31391),
(81, 341, 18562, 1786),
(82, 24007, 30765, 3145),
(83, 9985, 3808, 14238),
(84, 17158, 23512, 15478),
(85, 17616, 27350, 17013),
(86, 2483, 2068, 5461),
(87, 1623, 4915, 3690),
(88, 13073, 20258, 13843),
(89, 1096, 13119, 12681),
(90, 19787, 19862, 19373),
(91, 10096, 22846, 24317),
(92, 31992, 21330, 17808),
(93, 15457, 9983, 4833),
(94, 16696, 16556, 16791),
(95, 9453, 23766, 4814),
(96, 3457, 26247, 25414),
(97, 27650, 20889, 27494),
(98, 8309, 4946, 30799),
(99, 30090, 2675, 12893),
(100, 8539, 4126, 202);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb1;"""
    output = _dci.cmdexec(stmt)
    # expect count = 100
    
    # an empty table & view
    stmt = """create table samptb2 (
a int not null primary key,
b char (9),
c varchar (9),
d smallint
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb2 
as select a, b, c
from samptb2;"""
    output = _dci.cmdexec(stmt)
    
    # a vertically partitioned table
    stmt = """create table samptb3 (
a int not null primary key,
b int,
c int,
d int
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb3 
as select a, b, c
from samptb3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb3 values
(1, 250, 18237, 2761),
(2, 26456, 23942, 4890),
(3, 14066, 5852, 2359),
(4, 24204, 29007, 30964),
(5, 31145, 27216, 21236),
(6, 28785, 15410, 11508),
(7, 23689, 3687, 9320),
(8, 22344, 14579, 23103),
(9, 17379, 32016, 4913),
(10, 24584, 3908, 13819),
(11, 899, 30990, 21621),
(12, 19161, 22482, 686),
(13, 26163, 17160, 15180),
(14, 30568, 8394, 26159),
(15, 335, 7734, 11296),
(16, 1583, 6024, 17436),
(17, 7925, 9559, 25436),
(18, 13313, 26473, 19672),
(19, 3718, 24765, 7359),
(20, 10104, 1794, 30067),
(21, 7776, 13450, 13866),
(22, 16417, 9251, 10013),
(23, 13088, 10869, 9163),
(24, 17780, 29803, 13539),
(25, 12242, 23734, 17637),
(26, 10228, 13157, 7399),
(27, 32724, 28641, 12207),
(28, 28951, 22615, 22112),
(29, 24154, 10201, 12292),
(30, 3774, 23891, 32759),
(31, 16591, 18478, 18382),
(32, 28004, 7725, 14945),
(33, 24715, 10866, 20858),
(34, 24662, 12631, 26949),
(35, 5528, 21876, 17365),
(36, 14728, 30170, 2262),
(37, 22398, 30302, 21536),
(38, 15078, 14567, 20636),
(39, 6723, 31021, 7746),
(40, 18741, 6835, 3177),
(41, 11560, 12278, 25694),
(42, 3296, 3478, 31347),
(43, 3540, 4341, 11829),
(44, 1857, 15273, 10745),
(45, 7646, 8549, 26139),
(46, 9027, 7773, 22541),
(47, 8693, 14211, 21621),
(48, 32382, 28852, 12371),
(49, 14629, 26702, 23527),
(50, 9231, 12330, 13779),
(51, 24540, 17895, 26565),
(52, 17627, 27000, 31794),
(53, 26046, 6557, 27495),
(54, 12549, 26025, 21488),
(55, 20086, 4357, 27752),
(56, 1211, 16700, 11385),
(57, 13553, 30637, 11008),
(58, 11940, 23122, 17710),
(59, 17879, 8017, 25330),
(60, 16533, 9229, 25263),
(61, 4377, 5787, 9414),
(62, 27487, 7346, 12303),
(63, 7141, 21196, 14928),
(64, 11468, 12589, 19387),
(65, 4976, 2793, 15014),
(66, 8995, 5118, 20015),
(67, 5699, 17214, 12570),
(68, 15312, 18113, 27872),
(69, 3355, 32341, 22482),
(70, 6920, 7380, 17881),
(71, 19835, 17588, 12823),
(72, 14453, 8891, 28922),
(73, 3960, 18171, 7021),
(74, 20821, 26963, 14823),
(75, 28015, 22077, 30737),
(76, 2706, 1284, 29178),
(77, 32678, 23721, 26743),
(78, 32185, 28766, 11230),
(79, 32514, 29920, 1242),
(80, 477, 16109, 31391),
(81, 341, 18562, 1786),
(82, 24007, 30765, 3145),
(83, 9985, 3808, 14238),
(84, 17158, 23512, 15478),
(85, 17616, 27350, 17013),
(86, 2483, 2068, 5461),
(87, 1623, 4915, 3690),
(88, 13073, 20258, 13843),
(89, 1096, 13119, 12681),
(90, 19787, 19862, 19373),
(91, 10096, 22846, 24317),
(92, 31992, 21330, 17808),
(93, 15457, 9983, 4833),
(94, 16696, 16556, 16791),
(95, 9453, 23766, 4814),
(96, 3457, 26247, 25414),
(97, 27650, 20889, 27494),
(98, 8309, 4946, 30799),
(99, 30090, 2675, 12893),
(100, 8539, 4126, 202);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb3;"""
    output = _dci.cmdexec(stmt)
    # expect count = 100
    
    # a hash partitioned table
    stmt = """create table samptb4 (
a int not null,
b int,
c int,
d int,
primary key (a))
STORE BY (a)
HASH PARTITION (add location """ + gvars.g_disc1 + """, add location """ + gvars.g_disc2 + """)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb4 
as select a, b, c
from samptb4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb4 values
(1, 250, 18237, 2761),
(2, 26456, 23942, 4890),
(3, 14066, 5852, 2359),
(4, 24204, 29007, 30964),
(5, 31145, 27216, 21236),
(6, 28785, 15410, 11508),
(7, 23689, 3687, 9320),
(8, 22344, 14579, 23103),
(9, 17379, 32016, 4913),
(10, 24584, 3908, 13819),
(11, 899, 30990, 21621),
(12, 19161, 22482, 686),
(13, 26163, 17160, 15180),
(14, 30568, 8394, 26159),
(15, 335, 7734, 11296),
(16, 1583, 6024, 17436),
(17, 7925, 9559, 25436),
(18, 13313, 26473, 19672),
(19, 3718, 24765, 7359),
(20, 10104, 1794, 30067),
(21, 7776, 13450, 13866),
(22, 16417, 9251, 10013),
(23, 13088, 10869, 9163),
(24, 17780, 29803, 13539),
(25, 12242, 23734, 17637),
(26, 10228, 13157, 7399),
(27, 32724, 28641, 12207),
(28, 28951, 22615, 22112),
(29, 24154, 10201, 12292),
(30, 3774, 23891, 32759),
(31, 16591, 18478, 18382),
(32, 28004, 7725, 14945),
(33, 24715, 10866, 20858),
(34, 24662, 12631, 26949),
(35, 5528, 21876, 17365),
(36, 14728, 30170, 2262),
(37, 22398, 30302, 21536),
(38, 15078, 14567, 20636),
(39, 6723, 31021, 7746),
(40, 18741, 6835, 3177),
(41, 11560, 12278, 25694),
(42, 3296, 3478, 31347),
(43, 3540, 4341, 11829),
(44, 1857, 15273, 10745),
(45, 7646, 8549, 26139),
(46, 9027, 7773, 22541),
(47, 8693, 14211, 21621),
(48, 32382, 28852, 12371),
(49, 14629, 26702, 23527),
(50, 9231, 12330, 13779),
(51, 24540, 17895, 26565),
(52, 17627, 27000, 31794),
(53, 26046, 6557, 27495),
(54, 12549, 26025, 21488),
(55, 20086, 4357, 27752),
(56, 1211, 16700, 11385),
(57, 13553, 30637, 11008),
(58, 11940, 23122, 17710),
(59, 17879, 8017, 25330),
(60, 16533, 9229, 25263),
(61, 4377, 5787, 9414),
(62, 27487, 7346, 12303),
(63, 7141, 21196, 14928),
(64, 11468, 12589, 19387),
(65, 4976, 2793, 15014),
(66, 8995, 5118, 20015),
(67, 5699, 17214, 12570),
(68, 15312, 18113, 27872),
(69, 3355, 32341, 22482),
(70, 6920, 7380, 17881),
(71, 19835, 17588, 12823),
(72, 14453, 8891, 28922),
(73, 3960, 18171, 7021),
(74, 20821, 26963, 14823),
(75, 28015, 22077, 30737),
(76, 2706, 1284, 29178),
(77, 32678, 23721, 26743),
(78, 32185, 28766, 11230),
(79, 32514, 29920, 1242),
(80, 477, 16109, 31391),
(81, 341, 18562, 1786),
(82, 24007, 30765, 3145),
(83, 9985, 3808, 14238),
(84, 17158, 23512, 15478),
(85, 17616, 27350, 17013),
(86, 2483, 2068, 5461),
(87, 1623, 4915, 3690),
(88, 13073, 20258, 13843),
(89, 1096, 13119, 12681),
(90, 19787, 19862, 19373),
(91, 10096, 22846, 24317),
(92, 31992, 21330, 17808),
(93, 15457, 9983, 4833),
(94, 16696, 16556, 16791),
(95, 9453, 23766, 4814),
(96, 3457, 26247, 25414),
(97, 27650, 20889, 27494),
(98, 8309, 4946, 30799),
(99, 30090, 2675, 12893),
(100, 8539, 4126, 202);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb4;"""
    output = _dci.cmdexec(stmt)
    # expect count = 100
    
    stmt = """create table samptb31 (
a int not null, b int,
primary key (a))
STORE BY (a)
RANGE PARTITION (add first key (1) location """ + gvars.g_disc1 + """)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb31 as
select * from samptb31 where a <> 666;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vwsamptb31 values
(1, 94),
(2, 26602),
(3, 30017),
(4, 18297),
(5, 20363),
(6, 13015),
(7, 28509),
(8, 15290),
(9, 29003),
(10, 24399),
(11, 3339),
(12, 28849),
(13, 17055),
(14, 19424),
(15, 4588),
(16, 15756),
(17, 6098),
(18, 11834),
(19, 1351),
(20, 21383),
(21, 18431),
(22, 155),
(23, 14763),
(24, 14082),
(25, 4564),
(26, 25482),
(27, 30678),
(28, 20183),
(29, 15765),
(30, 18376);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb32 (
numb varchar (3),
upperc char not null,
lowerc char (1) not null,
lname varchar (10),
primary key (upperc, lowerc)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb32 
as select upperc, lowerc, numb, lname
from samptb32 
where numb between '0' and '99'
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb32 values
('13', 'C', 'c', 'Hvwce'),
('25', 'O', 'o', null),
('36', 'Z', 'z', 'Ysqwtbixs'),
('4', '3', '3', null),
('34', 'X', 'x', 'Rppohkce'),
('30', 'T', 't', null),
('8', '7', '7', 'Zekxmy'),
('15', 'E', 'e', 'Zfglnxtloe'),
('3', '2', '2', 'Tlkyvlj'),
('18', 'H', 'h', 'Yfmx'),
('7', '6', '6', 'Trkahdnjqg'),
('9', '8', '8', 'Ydtdcuua'),
('6', '5', '5', 'Ddqxqfece'),
('28', 'R', 'r', null),
('23', 'M', 'm', 'Zaxk'),
('20', 'J', 'j', 'Onhlrgniu'),
('19', 'I', 'i', 'Hiixrnohfb'),
('21', 'K', 'k', 'Nerep'),
('10', '9', '9', 'Lacfjdp'),
('33', 'W', 'w', 'Zhiur'),
('17', 'G', 'g', null),
('5', '4', '4', 'Qpvetf'),
('32', 'V', 'v', 'Pvrkfi'),
('26', 'P', 'p', 'Auuqfw'),
('1', '0', '0', null),
('29', 'S', 's', 'Ekhsgvrf'),
('11', 'A', 'a', null),
('16', 'F', 'f', 'Uthsypa'),
('35', 'Y', 'y', 'Clxn'),
('2', '1', '1', 'Qvrtymg'),
('31', 'U', 'u', 'Jvk'),
('12', 'B', 'b', 'Rsfcmwmqkh'),
('24', 'N', 'n', 'Old'),
('27', 'Q', 'q', 'Brxvba'),
('22', 'L', 'l', 'Vro'),
('14', 'D', 'd', null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb32;"""
    output = _dci.cmdexec(stmt)
    # expect count = 36
    
    stmt = """create table samptb33 (
a char not null primary key,
b varchar (7),
c decimal,
d float,
e interval hour
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb33 
as select b, e, a, d from samptb33 
where c > -666;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb050 (
name   char(20) no default not null,
salary numeric no default not null,
gender char(1) no default not null,
primary key (name)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb050 values
('Debbie', 500000, 'F'),
('David' , 300000, 'M'),
('Abbie' , 90000 , 'F'),
('Iris'  , 100000, 'F'),
('Melody', 90000 , 'F'),
('Sydney', 500000, 'F'),
('Nikki' , 60000 , 'F'),
('Jane'  , 70000 , 'F'),
('Donna' , 100000, 'F'),
('Larry' , 80000 , 'M'),
('Hema'  , 100000, 'F'),
('Chris' ,  2000 , 'M');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb051 (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb051 values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9018, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE'),
(4567, 4444, 30000.00, 23, 'FEMALE'),
(8901, 5555, 40000.00, 56, 'MALE'),
(2345, 5555, 36000.00, 29, 'FEMALE'),
(6799, 5555, 60000.00, 100, 'MALE'),
(9123, 3333, 20050.00, 18, 'MALE'),
(4900, 3333, 45000.00, 34, 'FEMALE'),
(6234, 3333, 20000.00, 60, 'MALE'),
(6678, 3333, 50000.00, 59, 'FEMALE'),
(6012, 3333, 40000.00, 49, 'MALE'),
(6455, 4444, 45000.00, 39, 'FEMALE'),
(7789, 4444, 55000.00, 38, 'MALE'),
(6123, 3333, 25000.00, 37, 'MALE'),
(6567, 4444, 30000.00, 24, 'FEMALE'),
(6901, 5555, 40000.00, 22, 'MALE'),
(6345, 5555, 36000.00, 21, 'FEMALE'),
(6798, 5555, 60000.00, 19, 'MALE'),
(6133, 3333, 20050.00, 80, 'MALE'),
(6900, 3333, 45000.00, 61, 'FEMALE'),
(4907, 3333, 45000.00, 74, 'FEMALE'),
(9234, 3333, 20000.00, 62, 'MALE'),
(9678, 3333, 50000.00, 99, 'FEMALE'),
(9012, 3333, 40000.00,  1, 'MALE'),
(9455, 4444, 45000.00,  2, 'FEMALE'),
(9789, 4444, 55000.00,  3, 'MALE'),
(9193, 3333, 25000.00,  4, 'MALE'),
(9567, 4444, 30000.00,  5, 'FEMALE'),
(9901, 5555, 40000.00,  6, 'MALE'),
(9345, 5555, 36000.00,  7, 'FEMALE'),
(9798, 5555, 60000.00,  8, 'MALE'),
(9143, 3333, 20050.00,  9, 'MALE'),
(9900, 3333, 45000.00, 69, 'FEMALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb054 (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb054 values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9019, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE'),
(4567, 4444, 30000.00, 23, 'FEMALE'),
(8901, 5555, 40000.00, 56, 'MALE'),
(2345, 5555, 36000.00, 29, 'FEMALE'),
(6799, 5555, 60000.00, 60, 'MALE'),
(9123, 3333, 20050.00, 18, 'MALE'),
(4900, 3333, 45000.00, 34, 'FEMALE'),
(6234, 3333, 20000.00, 60, 'MALE'),
(6678, 3333, 50000.00, 59, 'FEMALE'),
(6012, 3333, 40000.00, 49, 'MALE'),
(6455, 4444, 45000.00, 39, 'FEMALE'),
(7789, 4444, 55000.00, 38, 'MALE'),
(6123, 3333, 25000.00, 37, 'MALE'),
(6567, 4444, 30000.00, 24, 'FEMALE'),
(6901, 5555, 40000.00, 22, 'MALE'),
(6345, 5555, 36000.00, 21, 'FEMALE'),
(6798, 5555, 60000.00, 19, 'MALE'),
(6133, 3333, 20050.00, 80, 'MALE'),
(6900, 3333, 45000.00, 61, 'FEMALE'),
(4909, 3333, 45000.00, 74, 'FEMALE'),
(9234, 3333, 20000.00, 62, 'MALE'),
(9678, 3333, 50000.00, 99, 'FEMALE'),
(9012, 3333, 40000.00,  1, 'MALE'),
(9455, 4444, 45000.00,  2, 'FEMALE'),
(9789, 4444, 55000.00,  3, 'MALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb058 (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb058 values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9012, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE'),
(4567, 4444, 30000.00, 23, 'FEMALE'),
(8901, 5555, 40000.00, 56, 'MALE'),
(2345, 5555, 36000.00, 29, 'FEMALE'),
(6798, 5555, 60000.00, 60, 'MALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb060 (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb060 values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9012, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb062 (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb062 values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9012, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE'),
(4567, 4444, 30000.00, 23, 'FEMALE'),
(8901, 5555, 40000.00, 56, 'MALE'),
(2345, 5555, 36000.00, 29, 'FEMALE'),
(6798, 5555, 60000.00, 60, 'MALE'),
(9123, 3333, 20050.00, 18, 'MALE'),
(4900, 3333, 45000.00, 34, 'FEMALE'),
(6234, 3333, 20000.00, 60, 'MALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb066a (
empid   numeric (4) unsigned not null not droppable,
dnum    numeric (4) unsigned not null not droppable,
salary numeric (8,2) unsigned,
age     integer,
sex     char (6),
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb066a values
(1234, 3333, 20000.00, 16, 'MALE'),
(5678, 3333, 50000.00, 35, 'FEMALE'),
(9012, 3333, 40000.00, 30, 'MALE'),
(3455, 4444, 45000.00, 31, 'FEMALE'),
(6789, 4444, 55000.00, 36, 'MALE'),
(0123, 3333, 25000.00, 20, 'MALE'),
(4567, 4444, 30000.00, 23, 'FEMALE'),
(8901, 5555, 40000.00, 56, 'MALE'),
(2345, 5555, 36000.00, 29, 'FEMALE'),
(6798, 5555, 60000.00, 60, 'MALE'),
(9123, 3333, 20050.00, 18, 'MALE'),
(4900, 3333, 45000.00, 34, 'FEMALE'),
(6234, 3333, 20000.00, 60, 'MALE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb066b (
empid numeric (4) unsigned not null not droppable,
dnum numeric (4) unsigned not null not droppable,
datehired date,
primary key (empid) not droppable
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb066b values
(1234, 3333, date '1979-12-12'),
(5678, 3333, date '1983-12-01'),
(9012, 3333, date '1940-10-04'),
(3455, 4444, date '1991-01-01'),
(6789, 4444, date '1990-09-07'),
(0123, 3333, date '1999-01-01'),
(4567, 4444, date '2000-09-08'),
(8901, 5555, date '1993-04-05'),
(2345, 5555, date '1987-07-29'),
(6798, 5555, date '1986-03-04'),
(9123, 3333, date '1995-01-15'),
(4900, 3333, date '1997-03-06'),
(6234, 3333, date '1976-04-04');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb066c (
id          int not null primary key,
pay         float,
hiredate    date
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb075 (
name    char (20) no default not null,
salary  numeric no default not null,
gender  char no default not null,
primary key (name)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb075 values
('Debbie', 500000, 'F'),
('David' , 300000, 'M'),
('Abbie' , 90000 , 'F'),
('Iris'  , 100000, 'F'),
('Melody', 90000 , 'F'),
('Sydney', 500000, 'F'),
('Nikki' , 60000 , 'F'),
('Jane'  , 70000 , 'F'),
('Donna' , 100000, 'F'),
('Larry' , 80000 , 'M'),
('Hema'  , 100000, 'F'),
('Chris' ,  2000 , 'M'),
('Ellie' , 100000, 'F'),
('Elory' ,  2000 , 'F');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb077 (
name    varchar (20) no default not null primary key,
salary  numeric no default,
gender  char no default
)
location """ + gvars.g_disc2 + """;"""
    output = _dci.cmdexec(stmt)
    #     RANGE PARTITION (add first key (_ISO88591'Adams') location ${g_disc1});
    
    stmt = """insert into samptb077 values
('Debbie', 500000, 'F'),
('David' , 300000, 'M'),
('Abbie' , 90000 , 'F'),
('Iris'  , 100000, 'F'),
('Melody', 90000 , 'F'),
('Sydney', 500000, 'F'),
('Nikki' , 60000 , 'F'),
('Jane'  , 70000 , 'F'),
('Donna' , 100000, 'F'),
('Larry' , 80000 , 'M'),
('Hema'  , 100000, 'F'),
('Chris' ,  2000 , 'M'),
('Ellie' , 100000, 'F'),
('Elory' ,  2000 , 'F');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb082 (I1 INTEGER, I2 INTEGER, I3 INTEGER not null primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb082 values
(NULL, 500000, 1),
(NULL, 300000,2),
(10, 90000, 3),
(9, 100000, 4),
(8, 90000, 5),
(7, 500000, 6),
(6, 60000, 7),
(5, 70000, 8),
(4, 100000, 9),
(3, 80000, 10),
(2, 100000, 11),
(1, 2000, 12);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tempt1 (
intcol  int default null,
numcol  numeric (15,2) default null,
cnt int default 1 not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tempt2 (
intcol  int default null,
numcol  numeric (15,2) default null,
cnt int default 1 not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tempt3 (
gender  char no default,
name    varchar (20) no default not null primary key,
salary  numeric no default
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table samptb085a (
a int not null primary key,
b int,
c int,
d int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb085a 
as select a, b, c
from samptb085a;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into samptb085a values
(1, 250, 18237, 2761),
(2, 26456, 23942, 4890),
(3, 14066, 5852, 2359),
(4, 24204, 29007, 30964),
(5, null, 27216, 21236),
(6, 28785, 15410, 11508),
(7, 23689, 3687, 9320),
(8, 22344, 14579, 23103),
(9, 17379, null, 4913),
(10, 24584, 3908, 13819),
(11, 899, 30990, 21621),
(12, 19161, 22482, 686),
(13, 26163, 17160, 15180),
(14, 30568, 8394, null),
(15, 335, 7734, 11296),
(16, 1583, 6024, 17436),
(17, 7925, 9559, 25436),
(18, 13313, 26473, 19672),
(19, 3718, null, 7359),
(20, 10104, 1794, 30067),
(21, 7776, 13450, 13866),
(22, 16417, 9251, 10013),
(23, 13088, 10869, 9163),
(24, null, 29803, 13539),
(25, 12242, 23734, 17637);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb085a;"""
    output = _dci.cmdexec(stmt)
    # expect count = 25
    
    stmt = """create table samptb085b (
x int not null primary key,
y int,
z int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vwsamptb085b 
as select x, y, z
from samptb085b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vwsamptb085b values    

(100, -74, -27648),
(101, -21136, -4989),
(102, -24011, -22223),
(103, -9834, -85),
(104, null, -28519),
(105, -4226, -28585),
(106, -15294, -18450),
(107, -2507, -10032),
(108, -9031, null),
(109, -23134, -11307),
(110, -15474, -5573),
(111, -22978, -4763),
(112, -15250, -24665),
(113, null, -19633),
(114, -21344, -27138),
(115, -2688, -3718),
(116, -23010, -6585),
(117, -15330, -6668),
(118, -13457, null),
(119, -30057, -1861),
(120, -20410, -29298),
(121, -29553, -23730),
(122, -9509, -9303),
(123, -11669, -3087),
(124, -5621, -3193);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from vwsamptb085b;"""
    output = _dci.cmdexec(stmt)
    # expect count = 25
    
    _testmgr.testcase_end(desc)

