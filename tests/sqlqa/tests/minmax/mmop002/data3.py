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
    
    stmt = """insert into tab1
values
(INTERVAL '46-6' YEAR(2) TO MONTH, -1.953381e+020, -1954514522, 'K7', NULL, 406462164
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '08-10' YEAR(2) TO MONTH, 4.649565e-008, 1879150029, 'Qif8Y', DATE '3533-04-25',
130336033);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '28-7' YEAR(2) TO MONTH, 2.122527e+004, -1980083414, 'PKaG', DATE '2772-07-17',
568299440);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '51-5' YEAR(2) TO MONTH, 4.582298e+015, 1380384130, 'G', DATE '1993-07-28',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '34-7' YEAR(2) TO MONTH, -2.984996e+004, -870712018, 'WB', DATE '2760-03-07',
361383569);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-4' YEAR(2) TO MONTH, 3.817541e+003, 195195475, '9bm', DATE '4454-10-29',
073002718);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-4' YEAR(2) TO MONTH, NULL, 266039172, NULL, DATE '2255-12-22', 316894925
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-2' YEAR(2) TO MONTH, 1.659973e+010, 1386760814, 'd', DATE '1560-05-20',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-11' YEAR(2) TO MONTH, -3.493364e+019, NULL, 'TgnAw', NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '83-7' YEAR(2) TO MONTH, -2.201589e+008, 1245249248, 'Ey', DATE '3003-01-07',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '67-7' YEAR(2) TO MONTH, 1.911067e-003, NULL, 's', DATE '2959-06-14', 608532487
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-4' YEAR(2) TO MONTH, -9.654563e-016, 1593619416, 'q09f', DATE '3832-11-04',
660380197);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '84-7' YEAR(2) TO MONTH, 5.086762e-014, -1720316443, '6C', DATE '2162-03-12',
962803152);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '47-9' YEAR(2) TO MONTH, -7.485656e+031, 859604292, 'Wc2', DATE '1802-06-26',
401801307);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-2' YEAR(2) TO MONTH, -3.762119e+017, -63187637, 'JRl', DATE '3166-02-22',
437713863);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '97-1' YEAR(2) TO MONTH, 6.184852e-014, 31096110, 'kbfb', DATE '2950-04-08',
796037697);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-5' YEAR(2) TO MONTH, 6.741914e-015, 1372933685, '0E3na', DATE '2732-12-25',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '93-5' YEAR(2) TO MONTH, 4.426437e-001, NULL, 'AV5a0', DATE '3583-07-16',
711166042);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-1' YEAR(2) TO MONTH, 3.635244e-023, 436095129, NULL, DATE '1539-01-06',
000369025);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-1' YEAR(2) TO MONTH, -3.754503e-005, -1842849333, 'T', DATE '3315-05-23',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-11' YEAR(2) TO MONTH, -4.807071e+006, NULL, 'Dd', DATE '2195-08-13',
984483947);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '09-1' YEAR(2) TO MONTH, 7.750308e+002, 1802068648, '7veea', NULL, 140397177
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, 1.637445e+029, NULL, '17oj5', NULL, 000112879);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-0' YEAR(2) TO MONTH, NULL, -293833104, '17vh', DATE '4289-09-19', 816674511
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-4' YEAR(2) TO MONTH, -1.798134e-024, NULL, 'M', DATE '2996-07-29', 144672649
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-1' YEAR(2) TO MONTH, 1.013834e+000, 68909707, NULL, DATE '2080-03-01',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-2' YEAR(2) TO MONTH, NULL, 12651311, 'O', DATE '3125-11-25', 615663475
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-5' YEAR(2) TO MONTH, -9.169355e+000, -853852155, 'VZr', DATE '2097-02-12',
426493321);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-7' YEAR(2) TO MONTH, 4.265141e-010, 39096375, 'o4in9', DATE '4261-02-19',
724700433);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '48-8' YEAR(2) TO MONTH, 6.320414e-009, 52415901, 'fzoN', DATE '3464-02-16',
362855889);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '91-0' YEAR(2) TO MONTH, 9.123468e-019, -29774905, 'M', DATE '2529-06-19',
948611212);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-9' YEAR(2) TO MONTH, 4.638541e+012, 1499520449, 'HL8Ae', DATE '2689-01-10',
546560684);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, -9.876543e-005, 688459296, 'ek', DATE '3229-01-13',
211943504);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '08-5' YEAR(2) TO MONTH, -1.089135e-018, 846798555, 'wyas7', DATE '4069-08-25',
390675083);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-10' YEAR(2) TO MONTH, 4.883533e-028, 213639479, 'd4M1V', DATE '2130-07-14',
953228637);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-8' YEAR(2) TO MONTH, -7.520463e+007, 185195672, 'rZ', DATE '2246-08-25',
768480504);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-6' YEAR(2) TO MONTH, 2.965379e-013, 421727649, 'U8', DATE '4127-09-27',
295728003);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '27-10' YEAR(2) TO MONTH, -3.853640e-035, 123617589, 'mx', DATE '2316-04-20',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '56-11' YEAR(2) TO MONTH, -2.325896e-035, NULL, 'fRE', DATE '2400-06-14',
302989951);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-5' YEAR(2) TO MONTH, 1.173135e+003, 1175995114, 'R', DATE '3028-05-10',
398614848);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '61-8' YEAR(2) TO MONTH, 3.783201e+011, -674334040, '8jc7V', DATE '3163-09-02',
158297151);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '71-7' YEAR(2) TO MONTH, -9.066428e-029, 392760674, '8qZm', DATE '2469-03-25',
064662693);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-3' YEAR(2) TO MONTH, 4.617865e-001, -774672752, 'Gjqct', DATE '4443-08-05',
527421473);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '04-10' YEAR(2) TO MONTH, -6.246218e-004, 2065600481, NULL, NULL, 640956705
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-11' YEAR(2) TO MONTH, -2.933496e+018, -1572423738, 'x2', DATE '4182-01-04',
521635763);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-1' YEAR(2) TO MONTH, -9.439885e+008, -2079710669, 'cG', DATE '1938-08-24',
646739472);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-2' YEAR(2) TO MONTH, -8.621630e-034, -2123935532, 'z', NULL, 353358886
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '12-11' YEAR(2) TO MONTH, -1.570786e-029, NULL, NULL, DATE '4249-10-13',
366318017);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '10-5' YEAR(2) TO MONTH, 2.073161e+004, 614576077, 'Wp', DATE '4328-09-05',
501282620);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '52-0' YEAR(2) TO MONTH, 2.287513e+008, 771172625, 'e7W', DATE '1593-11-06',
528748538);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '39-1' YEAR(2) TO MONTH, 1.000000e+000, -933552403, '9l', NULL, 776196301
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, 6.520046e-015, 666940150, 'aN', DATE '1773-11-07',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-10' YEAR(2) TO MONTH, -1.699636e+001, 1585255426, 'kFuae', DATE '2277-08-10',
987778015);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-6' YEAR(2) TO MONTH, NULL, 954069479, 'b0nu', DATE '4225-01-18', 918349686
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-10' YEAR(2) TO MONTH, -1.274931e+021, NULL, 'z', DATE '4323-04-18',
494681434);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '13-2' YEAR(2) TO MONTH, 3.317849e+028, 1369353937, 'FA', DATE '1683-02-05',
685457424);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '20-8' YEAR(2) TO MONTH, -2.759896e+023, -1404261400, 'MSyRY', NULL, 362561351
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '49-8' YEAR(2) TO MONTH, -2.770920e-001, 1506442671, NULL, DATE '4291-03-16',
118525960);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '60-2' YEAR(2) TO MONTH, 3.253531e-010, -185856546, 'F', DATE '2306-03-31',
384690799);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-7' YEAR(2) TO MONTH, 8.498935e+026, 1022755296, 'J1', DATE '1524-02-21',
571857522);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-5' YEAR(2) TO MONTH, -3.563480e-009, 98033596, 'PP', DATE '3385-12-29',
052317674);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-9' YEAR(2) TO MONTH, -3.851723e+022, -1293120714, NULL, DATE '4075-09-29',
703934613);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-8' YEAR(2) TO MONTH, 2.414542e+016, 1372762154, 'xsAvl', NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '93-11' YEAR(2) TO MONTH, -4.967948e-005, -1889709083, 'PISx', DATE '4289-11-10',
023962860);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-4' YEAR(2) TO MONTH, -2.155840e-021, -981332557, 'uXq', DATE '2121-08-16',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-9' YEAR(2) TO MONTH, -2.225228e+007, -2050601211, 'Z', DATE '3347-10-09',
135723672);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-8' YEAR(2) TO MONTH, -5.527781e+016, 400220692, 'sj', DATE '4398-11-06',
066028079);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-3' YEAR(2) TO MONTH, 1.631629e+016, -2141864220, 'T', DATE '2484-11-22',
124543358);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '48-7' YEAR(2) TO MONTH, 1.000000e+000, 481575321, 'ZVD', DATE '2659-09-29',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '81-8' YEAR(2) TO MONTH, -1.734885e-010, -1649491360, 'h', DATE '4282-05-01',
038794381);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-7' YEAR(2) TO MONTH, -1.483169e+021, NULL, '7VO7N', DATE '4005-02-27',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '18-4' YEAR(2) TO MONTH, 1.307891e+021, 869370012, 'DY', DATE '3004-02-08',
319499235);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '02-11' YEAR(2) TO MONTH, -4.250493e-008, 1111898589, 'F1', DATE '3939-09-02',
762660606);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-3' YEAR(2) TO MONTH, -1.946278e+024, 1060255774, 'nB', DATE '2878-11-13',
555062775);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-5' YEAR(2) TO MONTH, -5.803524e+011, 860129841, 'iY', DATE '3792-02-28',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-2' YEAR(2) TO MONTH, -6.023687e+002, 118815211, '2Zm', DATE '1542-10-24',
889762411);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-4' YEAR(2) TO MONTH, -6.229812e+028, -1589653919, 'ZJh', DATE '3115-11-13',
084759862);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '59-7' YEAR(2) TO MONTH, -1.415412e+016, 1902756366, NULL, DATE '3266-04-30',
324338286);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '47-1' YEAR(2) TO MONTH, NULL, -404986743, 'sxOm', DATE '3221-05-02', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '90-3' YEAR(2) TO MONTH, 2.094536e+005, NULL, 'sRLV', DATE '3763-09-14',
309982207);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '83-3' YEAR(2) TO MONTH, -4.029581e-012, -247651313, 'Y4zoE', DATE '1595-06-14',
285590935);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-4' YEAR(2) TO MONTH, 3.894080e-014, 1210992582, 'WP', DATE '2509-07-29',
712985602);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '24-8' YEAR(2) TO MONTH, -3.144453e+009, 1807935918, 'Vk94N', DATE '3447-01-13',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '73-6' YEAR(2) TO MONTH, 1.682230e+001, -1991089990, 'JhlW', DATE '3500-03-02',
094648909);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-10' YEAR(2) TO MONTH, 2.963540e-015, 2035204205, '5', DATE '3367-12-11',
170068222);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '52-1' YEAR(2) TO MONTH, 2.405999e-029, 1605902201, 'VBk', DATE '2867-12-01',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-5' YEAR(2) TO MONTH, -1.574944e-005, 869334300, '5X', DATE '3800-09-28',
877378627);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-9' YEAR(2) TO MONTH, -1.392076e-001, -1627620114, 'a1mNi', DATE '1559-06-12',
231502819);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '12-10' YEAR(2) TO MONTH, 4.668679e+036, 854640279, 'Stj8F', DATE '1645-10-03',
032755183);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-0' YEAR(2) TO MONTH, 4.777548e-030, -810865544, 'Jw1yu', DATE '2379-08-30',
343563644);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-11' YEAR(2) TO MONTH, -4.964000e+003, -694203027, '8', DATE '2000-09-14',
357394691);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '85-5' YEAR(2) TO MONTH, -6.099953e-005, -753542840, 'keQS4', DATE '3219-12-08',
950404542);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '80-1' YEAR(2) TO MONTH, NULL, -632582506, 'MUDV2', DATE '2874-07-20',
051774109);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-1' YEAR(2) TO MONTH, -1.854366e+025, -814612426, 'Q', NULL, 726021018
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '74-10' YEAR(2) TO MONTH, 1.328891e+017, -727777384, 'vgb', DATE '3814-11-06',
287424691);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-6' YEAR(2) TO MONTH, -2.284000e+003, 1607109300, '87Vso', DATE '3579-11-09',
963105090);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-9' YEAR(2) TO MONTH, 1.150727e+015, 902570259, 'dc2en', DATE '2436-12-31',
544709639);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-0' YEAR(2) TO MONTH, 2.176014e-001, -1821002090, 'jD0wp', DATE '4255-02-13',
430094229);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-7' YEAR(2) TO MONTH, 3.529381e-014, -224933714, '4', DATE '1815-09-08',
789847418);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '90-1' YEAR(2) TO MONTH, 4.833967e+006, -1604374486, 'A', DATE '2511-05-11',
444281796)
;"""
    output = _dci.cmdexec(stmt)
