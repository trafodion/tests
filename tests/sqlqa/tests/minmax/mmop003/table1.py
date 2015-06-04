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
    
    stmt = """insert into table1
values
('kUYm', 190641683, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '30:39' HOUR(2) TO MINUTE,
1102836828, -1321787539);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('6ecDPehyZ', -400538679, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '1:53' HOUR(2) TO MINUTE,
523007018, 1839056054);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('M', 517384848, INTERVAL '39-7' YEAR(2) TO MONTH, INTERVAL '8:16' HOUR(2) TO MINUTE,
-880576225, -1067122833);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('L9jNuCbd', -763657792, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '6:55' HOUR(2) TO MINUTE,
NULL, -1097124470);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('N', -423147649, INTERVAL '79-1' YEAR(2) TO MONTH, INTERVAL '28:37' HOUR(2) TO MINUTE,
NULL, -2089622456);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('mdJRBg7oqH', 511432662, NULL, INTERVAL '8:17' HOUR(2) TO MINUTE, 1895714486, -1526181985
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('2nWNrIU', 059108505, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '8:05' HOUR(2) TO MINUTE,
-234038213, 924008536);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('qRsuc', 659109838, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '16:28' HOUR(2) TO MINUTE,
1616353683, 1814891532);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('ZKt6RWk6', 482020214, INTERVAL '51-6' YEAR(2) TO MONTH, INTERVAL '7:29' HOUR(2) TO MINUTE,
28780996, -768068570);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('lX', NULL, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '2:33' HOUR(2) TO MINUTE,
1519220102, -672654581);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('g', -514417202, NULL, INTERVAL '7:29' HOUR(2) TO MINUTE, 1669375894, 1977594200
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('I0CJ9Hh', 261685905, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '3:36' HOUR(2) TO MINUTE,
-1656199612, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('DJ', 523712420, INTERVAL '23-7' YEAR(2) TO MONTH, INTERVAL '1:52' HOUR(2) TO MINUTE,
1737977310, 1409999233);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('c5', -865749274, NULL, NULL, -1378078324, 759093722);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Is', NULL, INTERVAL '11-5' YEAR(2) TO MONTH, INTERVAL '12:30' HOUR(2) TO MINUTE,
NULL, -1688063259);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('d5Aq', -873368690, INTERVAL '00-5' YEAR(2) TO MONTH, INTERVAL '15:09' HOUR(2) TO MINUTE,
-336463627, 594344536);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('aVI', -601358542, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '49:16' HOUR(2) TO MINUTE,
-1040890366, 812541308);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('0ALiU', 674836291, INTERVAL '12-5' YEAR(2) TO MONTH, INTERVAL '3:03' HOUR(2) TO MINUTE,
340405290, 1915984113);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('OymG', -397006801, INTERVAL '1-6' YEAR(2) TO MONTH, INTERVAL '32:58' HOUR(2) TO MINUTE,
-1671177392, -2046946591);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('h4Q', -914168945, INTERVAL '3-6' YEAR(2) TO MONTH, INTERVAL '37:02' HOUR(2) TO MINUTE,
775714580, 1826559375);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('sa4', -420100046, INTERVAL '9-2' YEAR(2) TO MONTH, INTERVAL '0:47' HOUR(2) TO MINUTE,
-1626742353, 896651251);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('nsThilfh', -687293553, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '2:46' HOUR(2) TO MINUTE,
1693692177, 433672345);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Mw', 586486998, INTERVAL '40-8' YEAR(2) TO MONTH, INTERVAL '19:36' HOUR(2) TO MINUTE,
155732715, -2018799930);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('LhY', 921538717, INTERVAL '22-11' YEAR(2) TO MONTH, NULL, NULL, -1332918087);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('RnAvp', -485881792, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '7:41' HOUR(2) TO MINUTE,
-2065720469, -1337812683);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('X', -947110709, INTERVAL '77-2' YEAR(2) TO MONTH, INTERVAL '69:09' HOUR(2) TO MINUTE,
-22369726, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('05kXmoq8DD', 185516326, INTERVAL '68-8' YEAR(2) TO MONTH, INTERVAL '33:49' HOUR(2) TO MINUTE,
-913863534, 1167615774);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('tgv', -039480304, INTERVAL '3-8' YEAR(2) TO MONTH, INTERVAL '83:31' HOUR(2) TO MINUTE,
356498597, -542893629);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('JH', 100423051, INTERVAL '30-5' YEAR(2) TO MONTH, INTERVAL '53:06' HOUR(2) TO MINUTE,
NULL, 1402278323);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Hxr8FwZW', -688882867, INTERVAL '42-7' YEAR(2) TO MONTH, INTERVAL '4:20' HOUR(2) TO MINUTE,
560190040, 1278974370);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('a', 729915143, INTERVAL '5-8' YEAR(2) TO MONTH, INTERVAL '34:04' HOUR(2) TO MINUTE,
421930502, 838328837);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('8GhGJ9TCv5', -678983277, INTERVAL '72-11' YEAR(2) TO MONTH, INTERVAL '4:38' HOUR(2) TO MINUTE,
-883077926, -493846129);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('IaPUlH', 008077055, INTERVAL '72-10' YEAR(2) TO MONTH, INTERVAL '31:29' HOUR(2) TO MINUTE,
1239127268, -1565381242);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('JRtZf', NULL, INTERVAL '9-11' YEAR(2) TO MONTH, INTERVAL '9:00' HOUR(2) TO MINUTE,
-1557695961, 1576779957);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('K', 736935374, INTERVAL '63-11' YEAR(2) TO MONTH, INTERVAL '39:47' HOUR(2) TO MINUTE,
728113442, -707193359);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('f2', 582401261, INTERVAL '53-9' YEAR(2) TO MONTH, NULL, 1751262538, 150240070);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('zwzHLQ', -895746679, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '29:37' HOUR(2) TO MINUTE,
1192851505, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('MXQRX', 407091199, INTERVAL '5-0' YEAR(2) TO MONTH, NULL, -903153601, -2081311267
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('i', NULL, NULL, INTERVAL '92:10' HOUR(2) TO MINUTE, NULL, -86095575);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('qpBC6UF', 965330016, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '21:11' HOUR(2) TO MINUTE,
538506558, 1065837614);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('VXfRPav', 010271282, INTERVAL '2-11' YEAR(2) TO MONTH, INTERVAL '03:39' HOUR(2) TO MINUTE,
-1840336698, 1717062902);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('wktf7X', 961818966, INTERVAL '03-1' YEAR(2) TO MONTH, NULL, -1136596928, 195301141
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('kbAPNjW', -318042473, INTERVAL '2-2' YEAR(2) TO MONTH, INTERVAL '8:26' HOUR(2) TO MINUTE,
385104124, 841150218);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('gXemak', -537153234, INTERVAL '4-0' YEAR(2) TO MONTH, INTERVAL '0:17' HOUR(2) TO MINUTE,
NULL, 419267315);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('3Th1EHIohs', -681310354, INTERVAL '4-11' YEAR(2) TO MONTH, INTERVAL '4:23' HOUR(2) TO MINUTE,
-609534270, -1782785802);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('sYM9', 877996832, INTERVAL '8-2' YEAR(2) TO MONTH, INTERVAL '93:07' HOUR(2) TO MINUTE,
NULL, -622372758);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('fbQJkVnI', 909299882, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '75:20' HOUR(2) TO MINUTE,
-104171422, -1589547632);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('mnmh', NULL, INTERVAL '7-5' YEAR(2) TO MONTH, NULL, NULL, -1298841906);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('tDSt8', 321316591, INTERVAL '26-6' YEAR(2) TO MONTH, INTERVAL '5:27' HOUR(2) TO MINUTE,
1939455651, -1310890007);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('CPowoZmy', 764932122, INTERVAL '64-7' YEAR(2) TO MONTH, INTERVAL '3:46' HOUR(2) TO MINUTE,
-1163952662, -1833943181);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('nTuCrBFqr', 267948753, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '7:09' HOUR(2) TO MINUTE,
-382486062, -189750188);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('XMLlhCvOH', 141852530, INTERVAL '55-2' YEAR(2) TO MONTH, INTERVAL '2:05' HOUR(2) TO MINUTE,
-1783313451, -1790685319);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('2hcjdx94KE', -118633235, NULL, INTERVAL '80:04' HOUR(2) TO MINUTE, NULL, 1466027262
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('tWXk', 486388637, INTERVAL '90-10' YEAR(2) TO MONTH, INTERVAL '6:49' HOUR(2) TO MINUTE,
-231809823, 1217727421);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('91UUyBFJ60', NULL, INTERVAL '8-11' YEAR(2) TO MONTH, INTERVAL '00:08' HOUR(2) TO MINUTE,
-905987092, -749828052);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('8MdUUik3', -474607918, NULL, NULL, 1580128705, 377303096);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('b7mB8SL3z', -904467129, INTERVAL '39-6' YEAR(2) TO MONTH, INTERVAL '4:33' HOUR(2) TO MINUTE,
1068138640, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('7UJs3', -986023539, INTERVAL '7-2' YEAR(2) TO MONTH, INTERVAL '34:39' HOUR(2) TO MINUTE,
-1417809823, 582210947);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('nv0Z', -023445040, INTERVAL '0-6' YEAR(2) TO MONTH, INTERVAL '0:14' HOUR(2) TO MINUTE,
-1210852665, 1903417890);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('uwI', NULL, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '19:27' HOUR(2) TO MINUTE,
-496304558, -1375495560);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('zRZqOxbpDI', -994957909, INTERVAL '1-4' YEAR(2) TO MONTH, NULL, 1993609602, -16347340
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('r', -515198180, INTERVAL '86-8' YEAR(2) TO MONTH, INTERVAL '6:59' HOUR(2) TO MINUTE,
1906249784, 1370862714);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('OK4CS0', -746787627, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '87:07' HOUR(2) TO MINUTE,
-908653605, -1788738440);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('9I', -170808286, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '93:34' HOUR(2) TO MINUTE,
-146230965, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('TpXoZiY', -184527579, INTERVAL '68-0' YEAR(2) TO MONTH, NULL, 374389410, -210742281
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('A46mglyQil', 132062444, INTERVAL '5-11' YEAR(2) TO MONTH, INTERVAL '28:59' HOUR(2) TO MINUTE,
-435235301, -1831036621);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Rafx', -159211959, INTERVAL '16-4' YEAR(2) TO MONTH, INTERVAL '62:56' HOUR(2) TO MINUTE,
19933837, 18415714);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('WH', 182998842, INTERVAL '80-4' YEAR(2) TO MONTH, INTERVAL '59:02' HOUR(2) TO MINUTE,
-1819898745, -234287023);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('3', 152247628, INTERVAL '73-2' YEAR(2) TO MONTH, INTERVAL '77:18' HOUR(2) TO MINUTE,
NULL, -572280271);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('NY', NULL, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '7:10' HOUR(2) TO MINUTE,
NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('ris', -882664033, INTERVAL '8-4' YEAR(2) TO MONTH, INTERVAL '09:08' HOUR(2) TO MINUTE,
-144343981, -731679498);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('m1e', 103942166, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '4:25' HOUR(2) TO MINUTE,
365159561, 986671880);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('L', 179227883, INTERVAL '02-9' YEAR(2) TO MONTH, INTERVAL '7:07' HOUR(2) TO MINUTE,
1703787809, 195288234);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('ST3m', 470035440, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '9:50' HOUR(2) TO MINUTE,
NULL, -2085010186);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('LBMNP0', 962225668, INTERVAL '93-7' YEAR(2) TO MONTH, INTERVAL '5:16' HOUR(2) TO MINUTE,
35794862, -27937023);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('6mAwFUPwVy', 865414392, NULL, INTERVAL '06:53' HOUR(2) TO MINUTE, -1015125607,
700324736);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('dJKl', NULL, INTERVAL '52-0' YEAR(2) TO MONTH, INTERVAL '18:54' HOUR(2) TO MINUTE,
1617742622, -1748715929);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('i', 067351752, INTERVAL '5-0' YEAR(2) TO MONTH, INTERVAL '05:05' HOUR(2) TO MINUTE,
-2137771885, -61936232);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('GUOghJ7', -457828745, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '77:23' HOUR(2) TO MINUTE,
1828780676, 1671839194);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('xn', 973798789, INTERVAL '8-9' YEAR(2) TO MONTH, INTERVAL '6:51' HOUR(2) TO MINUTE,
1831456315, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('8y2vp', 580890948, INTERVAL '70-2' YEAR(2) TO MONTH, INTERVAL '42:43' HOUR(2) TO MINUTE,
117949372, -485438150);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('k62c3PzK', 262242555, INTERVAL '0-8' YEAR(2) TO MONTH, INTERVAL '79:58' HOUR(2) TO MINUTE,
-356536617, -1997813929);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('o', NULL, INTERVAL '5-1' YEAR(2) TO MONTH, INTERVAL '40:55' HOUR(2) TO MINUTE,
1419095396, 941462286);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('OSf', 906253576, INTERVAL '41-2' YEAR(2) TO MONTH, INTERVAL '23:25' HOUR(2) TO MINUTE,
46588798, 837806688);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Hd', 026572115, INTERVAL '0-10' YEAR(2) TO MONTH, INTERVAL '9:22' HOUR(2) TO MINUTE,
1208708207, -1996947849);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('xYhg1W4GH', 620398029, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '29:39' HOUR(2) TO MINUTE,
NULL, 2051423052);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('b13duY5B', -886422759, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '33:25' HOUR(2) TO MINUTE,
928964245, 1699881177);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('O4CWr', 608573062, INTERVAL '76-4' YEAR(2) TO MONTH, INTERVAL '01:57' HOUR(2) TO MINUTE,
-982559744, 391642015);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('eagn1', 113226870, INTERVAL '8-1' YEAR(2) TO MONTH, INTERVAL '53:29' HOUR(2) TO MINUTE,
1452525, -597395713);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('EYEjq9', 328493934, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '69:54' HOUR(2) TO MINUTE,
542045502, 1523823444);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('Vk3Q', -279571390, INTERVAL '76-5' YEAR(2) TO MONTH, INTERVAL '2:01' HOUR(2) TO MINUTE,
NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('iENyDO2967', 814085496, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '8:24' HOUR(2) TO MINUTE,
-1007424115, 1802309145);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('pOOpALsLw5', NULL, INTERVAL '53-8' YEAR(2) TO MONTH, INTERVAL '6:46' HOUR(2) TO MINUTE,
NULL, -909691150);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('5m8sx', 398902902, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '57:37' HOUR(2) TO MINUTE,
NULL, -1312403887);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('tFv21OiwY', -940724783, INTERVAL '49-11' YEAR(2) TO MONTH, INTERVAL '05:02' HOUR(2) TO MINUTE,
-129840282, -347526131);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('4DVSwXO', NULL, INTERVAL '11-1' YEAR(2) TO MONTH, INTERVAL '79:30' HOUR(2) TO MINUTE,
1895539793, 513082050);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('X', -182410246, NULL, INTERVAL '12:58' HOUR(2) TO MINUTE, -192330393, -747614603
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('z5hAF6ftk', -592454430, INTERVAL '99-11' YEAR(2) TO MONTH, INTERVAL '28:01' HOUR(2) TO MINUTE,
838326383, 954363767);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('UXhpE', 717832594, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '86:03' HOUR(2) TO MINUTE,
-768869517, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1
values
('VUE', -277691255, NULL, INTERVAL '93:04' HOUR(2) TO MINUTE, 316146035, 1604030147
)
;"""
    output = _dci.cmdexec(stmt)
