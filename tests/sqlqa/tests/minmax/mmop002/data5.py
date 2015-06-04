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
(INTERVAL '1-9' YEAR(2) TO MONTH, 1.891546e-004, 1570428985, 'KwJ', DATE '3021-11-23',
062061333);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-1' YEAR(2) TO MONTH, 3.194212e+013, -967276123, 'p9', DATE '1800-02-26',
975209191);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '69-10' YEAR(2) TO MONTH, 7.366061e+016, -1721376133, 'J', DATE '3590-12-18',
851469916);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-7' YEAR(2) TO MONTH, -1.599446e+012, -422914976, 'P2QK', NULL, 171329863
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '35-2' YEAR(2) TO MONTH, 3.539298e-025, -100710107, 'zp', DATE '3604-11-30',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-7' YEAR(2) TO MONTH, NULL, NULL, 'wjS', DATE '1888-06-08', 178202965
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-8' YEAR(2) TO MONTH, 1.234971e+006, -1541518895, NULL, DATE '3798-05-13',
195911132);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '83-1' YEAR(2) TO MONTH, 7.125644e+028, NULL, 'KQ', DATE '3895-08-21',
075041473);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '90-7' YEAR(2) TO MONTH, 4.796656e-005, -570321626, '4sH', DATE '1868-01-25',
784695631);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '92-5' YEAR(2) TO MONTH, 2.214580e-013, NULL, 'P', DATE '4457-09-13', 896567666
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-4' YEAR(2) TO MONTH, -9.991046e+032, NULL, NULL, DATE '1795-02-22',
547284324);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '27-0' YEAR(2) TO MONTH, 2.055770e+037, -1998769891, 'Pv5kE', DATE '3234-02-18',
054999338);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-6' YEAR(2) TO MONTH, -5.979631e-005, -82752821, NULL, NULL, 649468527
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-4' YEAR(2) TO MONTH, 4.875318e+000, 1223030, 'CI', DATE '4309-12-20',
464817979);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-9' YEAR(2) TO MONTH, -3.502069e+021, -414105420, 'pnysH', NULL, 529929322
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-1' YEAR(2) TO MONTH, -8.640644e+036, -439557607, '2', DATE '3995-02-23',
478929332);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-7' YEAR(2) TO MONTH, 9.839512e+025, -633157961, 'DR8n', DATE '3739-07-15',
292170188);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '73-1' YEAR(2) TO MONTH, -8.539525e-005, -1806546439, 'VAVuu', DATE '2379-07-28',
987324406);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '37-9' YEAR(2) TO MONTH, 3.413591e-013, -817996757, 'Z3', DATE '3393-06-27',
785580852);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, 1.162772e+025, 1842769208, 'eAhL', DATE '2064-03-05',
027164491);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-7' YEAR(2) TO MONTH, -1.232240e-012, -1981922752, 'F', DATE '2250-09-11',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-6' YEAR(2) TO MONTH, 1.004100e+004, 104143594, 'Z9I', DATE '1601-12-18',
842533016);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '90-4' YEAR(2) TO MONTH, -5.856064e-001, -733349322, 'GBF', DATE '3794-09-02',
767377247);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-5' YEAR(2) TO MONTH, -3.189986e-022, 1604665784, 'tElh', DATE '3422-02-07',
043227933);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '16-8' YEAR(2) TO MONTH, -6.448488e+000, -1888138089, NULL, DATE '3843-12-18',
227365159);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '79-10' YEAR(2) TO MONTH, 8.973000e+003, -2129988936, 'E82', DATE '1555-07-12',
584830216);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-10' YEAR(2) TO MONTH, 2.024914e-009, 1561623208, 'U', DATE '4255-04-22',
031964211);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '47-9' YEAR(2) TO MONTH, -2.658667e+022, -1574736349, 'le', DATE '3729-04-25',
202933940);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '75-0' YEAR(2) TO MONTH, -3.073317e-026, 1886552477, 'gN', DATE '2365-07-19',
976996822);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '97-2' YEAR(2) TO MONTH, -2.822816e+004, 1225216905, 'k0jjY', DATE '3122-03-25',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '84-9' YEAR(2) TO MONTH, 3.835970e+019, -1264186510, 'Z', DATE '1752-09-05',
987290540);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-11' YEAR(2) TO MONTH, -1.770771e+019, 365165460, 'Fitop', NULL, 078660678
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-10' YEAR(2) TO MONTH, -6.012365e-018, NULL, '8ET', DATE '3873-08-26',
712334675);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '11-6' YEAR(2) TO MONTH, 2.016296e+029, -1508810379, 'lWwu9', DATE '4177-10-09',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-3' YEAR(2) TO MONTH, 1.419844e-002, -1270219314, 'joF0', DATE '2106-06-06',
144694734);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-4' YEAR(2) TO MONTH, NULL, -1895013459, 'LFC', DATE '2120-06-09', 129543551
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-1' YEAR(2) TO MONTH, 1.070189e+016, 1724433211, NULL, DATE '1697-07-13',
649824676);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-7' YEAR(2) TO MONTH, 3.109692e+021, 616932493, 'IAKty', NULL, 908785371
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-3' YEAR(2) TO MONTH, NULL, NULL, 'fZ', DATE '2251-06-08', 512113449);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-5' YEAR(2) TO MONTH, 5.169055e-025, NULL, 'J', DATE '2478-06-18', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-9' YEAR(2) TO MONTH, 1.332350e+020, -366393314, NULL, DATE '4201-03-29',
428359644);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-3' YEAR(2) TO MONTH, 9.553617e-027, NULL, '3', DATE '4441-09-03', 552807461
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-8' YEAR(2) TO MONTH, -3.943973e+008, -1339564195, 'nNzU', DATE '2728-01-05',
532699812);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-10' YEAR(2) TO MONTH, 3.025446e-005, -1410176828, 'l', DATE '3139-01-14',
727921835);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '74-6' YEAR(2) TO MONTH, NULL, -149527189, NULL, DATE '3143-04-26', 340925680
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-6' YEAR(2) TO MONTH, 6.679659e+008, -1637113822, 'YIeZJ', DATE '4019-01-06',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, 6.212350e-009, 1186875613, 'rMhx', DATE '3089-03-31',
068373422);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-7' YEAR(2) TO MONTH, -2.682491e+011, -211527211, 'mV5', DATE '2773-01-11',
036379213);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-4' YEAR(2) TO MONTH, -3.548093e-022, 2094914184, 'XFH5', DATE '4251-08-13',
015289544);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-4' YEAR(2) TO MONTH, -2.307495e+008, -916267652, 'PY3Jm', DATE '3029-09-23',
164272856);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '87-0' YEAR(2) TO MONTH, -4.351249e-013, -10039031, 'V', DATE '1584-07-04',
631479161);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '66-9' YEAR(2) TO MONTH, 1.470848e-017, NULL, 'Z9', NULL, 234478031);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '18-4' YEAR(2) TO MONTH, 8.113537e-002, -834632001, 'a9W', DATE '3609-04-14',
339483106);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-2' YEAR(2) TO MONTH, 2.257277e-006, NULL, 'ja', DATE '1971-08-23', 391252191
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '57-11' YEAR(2) TO MONTH, 2.026439e+004, -1373499353, 'vdI', DATE '2125-02-06',
248893423);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '32-11' YEAR(2) TO MONTH, -1.759250e-002, -1054532409, 'xImH', NULL, 532570071
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '79-6' YEAR(2) TO MONTH, NULL, 1008357645, '1F', DATE '4145-10-21', 720433526
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '11-5' YEAR(2) TO MONTH, 1.376711e+004, -1916504896, 'g', DATE '2021-09-22',
688913123);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-0' YEAR(2) TO MONTH, 2.670512e-001, 1780765125, 'xux', DATE '2931-02-20',
101416618);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-5' YEAR(2) TO MONTH, -8.227997e-004, 1355389616, NULL, DATE '4344-08-22',
751114873);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-8' YEAR(2) TO MONTH, -4.162029e+017, -1778436215, 'B', DATE '3779-04-26',
539432276);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '51-11' YEAR(2) TO MONTH, -1.810606e+006, 636725291, 'u', DATE '4071-09-26',
794814711);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '57-7' YEAR(2) TO MONTH, NULL, -1042812088, 'UH', DATE '4272-06-19', 400975402
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '33-6' YEAR(2) TO MONTH, 3.657372e-018, -1693328549, 'lFJS', DATE '1892-03-02',
977260281);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '17-4' YEAR(2) TO MONTH, 1.810051e-021, -1332963529, 'bbG', DATE '2197-06-14',
577127106);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-9' YEAR(2) TO MONTH, 3.983456e-013, -1168470813, 'jS', DATE '2437-08-26',
591312378);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '85-4' YEAR(2) TO MONTH, 1.069826e-027, -201073382, 'Coo', DATE '4261-03-18',
429629901);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '97-6' YEAR(2) TO MONTH, -1.283185e-029, 39582577, 'S', DATE '3976-12-12',
841779190);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-3' YEAR(2) TO MONTH, 1.748351e-013, 962200070, 'yWDPt', DATE '1698-04-22',
220292081);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '22-4' YEAR(2) TO MONTH, 2.567670e-021, -1711264149, 't8', DATE '3257-06-06',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-4' YEAR(2) TO MONTH, -2.522778e-006, 1688635230, 'k', DATE '2380-09-05',
237106892);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-2' YEAR(2) TO MONTH, -1.381345e-015, 1172733603, '7Yq', DATE '3600-06-14',
656477688);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-5' YEAR(2) TO MONTH, 3.257237e-019, -1168008821, NULL, DATE '2063-12-16',
191932396);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-3' YEAR(2) TO MONTH, 8.185908e+002, NULL, '8WI', DATE '2647-02-15',
227239728);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '66-3' YEAR(2) TO MONTH, 1.000000e+000, 1235845734, '9cH1j', DATE '3801-07-31',
586685493);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '26-9' YEAR(2) TO MONTH, -1.476934e-014, -1536206954, 'U', DATE '1563-12-22',
843407395);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-1' YEAR(2) TO MONTH, -4.902872e+026, -1815868576, 'VCN', DATE '1548-01-25',
035632430);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-7' YEAR(2) TO MONTH, NULL, -159115610, '5', DATE '2859-04-02', 020972923
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, 3.985061e+018, -1226531500, 'MPy4x', DATE '3992-12-05',
543579987);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '88-10' YEAR(2) TO MONTH, NULL, NULL, '9', DATE '3266-08-21', NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '92-1' YEAR(2) TO MONTH, NULL, -1241367466, NULL, DATE '2627-01-13', 112187390
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-5' YEAR(2) TO MONTH, -3.034693e-025, 1856500013, 'H2', DATE '1780-12-31',
469352775);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-0' YEAR(2) TO MONTH, 1.989988e-011, 1548156763, 'DlLR', DATE '2402-03-14',
993393549);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-10' YEAR(2) TO MONTH, -5.952352e+002, -922914655, 'dG', DATE '4492-04-18',
615495635);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-6' YEAR(2) TO MONTH, 1.218111e-017, 1297937744, 'fdGd', DATE '2369-07-16',
514379799);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-9' YEAR(2) TO MONTH, 2.425191e+002, -49330956, 'uZE', DATE '2276-10-28',
930479418);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-9' YEAR(2) TO MONTH, 2.903858e-008, 114258377, 'yYni', DATE '2880-07-17',
661308460);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-8' YEAR(2) TO MONTH, NULL, 934540434, 'Xh', DATE '2892-12-14', 152171001
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-3' YEAR(2) TO MONTH, -1.677579e-007, -63258196, 's', DATE '2118-03-02',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-3' YEAR(2) TO MONTH, 4.173945e+033, -2101442317, 'B3bv', DATE '4132-12-16',
643066123);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '67-9' YEAR(2) TO MONTH, 1.603763e-009, -1684469296, 'lBxv', NULL, 690744339
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '08-6' YEAR(2) TO MONTH, -7.323550e+012, -910937969, 'xz2', DATE '3569-11-20',
497805150);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-11' YEAR(2) TO MONTH, NULL, -205494894, 'qOJxh', NULL, 239278024);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-4' YEAR(2) TO MONTH, 1.487623e-009, 33112339, 'M', DATE '3364-08-18',
313376433);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-9' YEAR(2) TO MONTH, -5.513478e+012, -2040069384, 'Vi', DATE '3092-01-20',
668378637);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '05-6' YEAR(2) TO MONTH, -1.057920e+022, 427268769, 'X66Bo', DATE '4134-02-08',
614026810);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-3' YEAR(2) TO MONTH, -8.551316e+019, 2041421302, 'mUO', NULL, 042772133
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-10' YEAR(2) TO MONTH, 1.766819e-001, 1218094892, 'uqrZW', DATE '2205-12-19',
609736285);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-1' YEAR(2) TO MONTH, -5.834617e+031, -712030944, NULL, DATE '1616-05-24',
252289442);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-10' YEAR(2) TO MONTH, 7.103577e+010, -1859908258, 'ts', DATE '2024-06-27',
931700768)
;"""
    output = _dci.cmdexec(stmt)
