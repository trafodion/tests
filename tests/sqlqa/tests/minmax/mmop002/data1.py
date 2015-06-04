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
(INTERVAL '9-1' YEAR(2) TO MONTH, 3.910600e-014, -223872529, 'R0S', DATE '3641-11-19',
085013664);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '28-10' YEAR(2) TO MONTH, NULL, 1702546212, 'YE', DATE '3679-12-20', 331510685
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-1' YEAR(2) TO MONTH, -3.712822e-018, 90242722, '78cA', DATE '3739-02-09',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '93-9' YEAR(2) TO MONTH, 9.508272e+032, -932488105, 'Co', DATE '3278-03-30',
527726105);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-1' YEAR(2) TO MONTH, NULL, 1500323745, 'iou', DATE '4171-08-28', 828494130
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-0' YEAR(2) TO MONTH, NULL, 1632404064, 'IWH', DATE '3467-02-25', 514495184
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-10' YEAR(2) TO MONTH, 8.630287e-001, -125416659, NULL, DATE '2016-07-25',
185489571);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-2' YEAR(2) TO MONTH, 5.976787e-007, -976027341, '3S', DATE '4068-07-31',
277796318);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '86-2' YEAR(2) TO MONTH, -2.406485e-013, 991168607, 'xrmK', DATE '3703-05-31',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '49-11' YEAR(2) TO MONTH, 1.693702e-028, 524602324, 'u3H', DATE '2129-04-28',
822385265);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-5' YEAR(2) TO MONTH, -8.617068e+012, NULL, NULL, DATE '1663-12-20',
747457112);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-3' YEAR(2) TO MONTH, -5.582190e+003, 1989913107, '8', DATE '3163-05-29',
177096436);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-0' YEAR(2) TO MONTH, 3.196803e-028, 94232045, NULL, DATE '1564-09-18',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-11' YEAR(2) TO MONTH, 2.561963e-032, NULL, 'CN', DATE '2065-06-08',
350325041);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-10' YEAR(2) TO MONTH, -1.918843e-033, -1975244972, 'qid', DATE '4193-04-17',
051904326);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-1' YEAR(2) TO MONTH, 6.933829e+014, -852747677, 'ntX', DATE '2592-09-21',
182300552);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '90-2' YEAR(2) TO MONTH, -1.755036e-012, 1331114369, '6a', DATE '2477-12-09',
790999451);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-5' YEAR(2) TO MONTH, 5.332047e+009, -327339412, NULL, DATE '4433-04-07',
058480698);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-4' YEAR(2) TO MONTH, 6.073276e-022, 1722044599, 'y', DATE '3853-07-15',
400015518);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, NULL, 1838900764, 'ktFgh', DATE '1575-07-04', 815451480
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-3' YEAR(2) TO MONTH, 3.602650e-015, -274880413, 'B', DATE '2595-02-22',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '19-0' YEAR(2) TO MONTH, NULL, 1410758096, 'EN095', DATE '2755-06-05',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '18-4' YEAR(2) TO MONTH, -4.870839e-009, 1844687388, 'aY84u', DATE '2584-03-15',
922682932);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '59-4' YEAR(2) TO MONTH, 5.550954e-002, -1128081952, 'De', DATE '3022-06-05',
315928681);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-11' YEAR(2) TO MONTH, -2.996856e-001, -293721296, 'Mg', DATE '2778-11-03',
804280784);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-3' YEAR(2) TO MONTH, 1.122833e-001, 797924859, 'xv', DATE '3686-12-27',
271923327);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '48-3' YEAR(2) TO MONTH, 1.240559e-030, -1425329030, 'vn', DATE '4349-07-06',
653683308);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-4' YEAR(2) TO MONTH, -5.417135e+000, 1693775856, 'XZ', DATE '1965-08-28',
685824931);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '24-6' YEAR(2) TO MONTH, 4.956629e-005, NULL, '4', NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '76-11' YEAR(2) TO MONTH, -3.586414e-004, NULL, 'vZVh', DATE '2843-11-30',
542159031);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '09-10' YEAR(2) TO MONTH, -2.668627e+004, 1180434185, '4', DATE '2384-10-03',
070040538);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '63-4' YEAR(2) TO MONTH, -1.865103e+029, -856643510, '0TI', DATE '3878-08-01',
118878498);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-1' YEAR(2) TO MONTH, NULL, 1641440020, 'Zt3', DATE '3450-07-02', 728312222
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-0' YEAR(2) TO MONTH, 2.618619e-021, NULL, '0N', DATE '1514-09-16', 885954810
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-5' YEAR(2) TO MONTH, -2.351632e+006, 1532473479, 't', DATE '3013-05-04',
007086593);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-4' YEAR(2) TO MONTH, -1.822100e-004, 1832991165, NULL, DATE '2677-03-10',
204405049);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '56-3' YEAR(2) TO MONTH, 7.266624e-014, 4893519, 'XJV', DATE '2543-07-25',
583798165);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-7' YEAR(2) TO MONTH, 4.241716e-001, 797698366, 'qhWHR', DATE '4211-02-01',
625282185);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-10' YEAR(2) TO MONTH, -1.659919e-009, 1909717557, NULL, DATE '3032-10-16',
907529093);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-6' YEAR(2) TO MONTH, 7.612391e+023, -780123581, '7cFvx', DATE '2304-09-09',
754841395);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '87-5' YEAR(2) TO MONTH, NULL, 906666402, '1NP', DATE '4373-09-08', 038594238
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-3' YEAR(2) TO MONTH, -3.088410e+028, -2070106394, '0yn', DATE '3055-12-16',
561771233);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-8' YEAR(2) TO MONTH, NULL, 1884455825, 'F', DATE '2252-10-19', 133033300
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '38-3' YEAR(2) TO MONTH, 3.403825e+010, 1783980077, NULL, DATE '2727-08-01',
375727485);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '93-10' YEAR(2) TO MONTH, 4.771453e+007, -165271442, 'So', DATE '3833-05-15',
953751200);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '27-9' YEAR(2) TO MONTH, 1.369003e+021, 1083616929, 'kFz', DATE '3427-01-24',
246311723);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '18-7' YEAR(2) TO MONTH, -2.009053e+021, 1737092592, 'dC', DATE '2172-06-23',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-5' YEAR(2) TO MONTH, -1.487794e+030, 748594298, 'I9O', DATE '2889-10-13',
882485971);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-8' YEAR(2) TO MONTH, 2.321330e+023, -1808267722, NULL, DATE '2230-12-09',
275731238);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '09-5' YEAR(2) TO MONTH, NULL, 1807504698, 'wd', DATE '3846-01-25', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '62-2' YEAR(2) TO MONTH, 3.902322e+002, NULL, 'Tul', DATE '4298-01-24',
815531661);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '76-7' YEAR(2) TO MONTH, -3.094850e+002, 1652470118, 'I6e', DATE '2867-01-20',
408297175);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, 1.828901e+007, -2119503476, 'M', DATE '2772-08-30',
519183423);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-8' YEAR(2) TO MONTH, -5.756545e-033, 1790434741, 'RLG', DATE '1539-05-26',
510246019);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '69-5' YEAR(2) TO MONTH, -1.923142e+005, -1948815448, 'w', DATE '2771-10-08',
725540283);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-1' YEAR(2) TO MONTH, 5.563476e-024, -775890630, 'COXw', DATE '2216-02-18',
898198575);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-2' YEAR(2) TO MONTH, 3.605538e+021, -2075485388, '6Fn', NULL, 864969796
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '51-4' YEAR(2) TO MONTH, 1.991213e+011, -1507410141, 'IGV', DATE '4480-07-03',
469922804);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '38-2' YEAR(2) TO MONTH, NULL, NULL, 'JJ', DATE '3674-07-04', 285855557
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '51-3' YEAR(2) TO MONTH, 2.723701e+004, NULL, 'WX', DATE '4127-06-17',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-8' YEAR(2) TO MONTH, -2.657545e+031, -1544525273, 'cc', DATE '1679-09-25',
839546084);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '81-0' YEAR(2) TO MONTH, -1.068493e+014, -742104337, 'q3t4', DATE '2728-05-05',
414532720);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-3' YEAR(2) TO MONTH, -1.484442e+024, 1174311106, 'gBzwb', DATE '4114-06-26',
360729603);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-8' YEAR(2) TO MONTH, 2.712403e-001, 26726279, 'jFLxX', DATE '2691-02-08',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-5' YEAR(2) TO MONTH, -6.906004e+011, -867778823, 'Qgtpp', DATE '3518-06-02',
397183980);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-5' YEAR(2) TO MONTH, 1.080019e-013, -357764792, NULL, DATE '4305-06-22',
905545445);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-11' YEAR(2) TO MONTH, -5.888700e+014, NULL, 'Zfm1', DATE '3472-01-28',
834673041);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '69-0' YEAR(2) TO MONTH, -7.685829e-011, 1770281081, 'xCnvQ', DATE '1861-08-04',
025970002);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '26-9' YEAR(2) TO MONTH, -2.867874e+025, -1337690521, NULL, DATE '1927-01-03',
272200835);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '03-2' YEAR(2) TO MONTH, -4.788039e+012, 1320531962, NULL, DATE '1886-04-11',
116124714);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '56-10' YEAR(2) TO MONTH, 9.062911e-005, 2038608298, 'f', DATE '2519-09-30',
022608714);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '67-4' YEAR(2) TO MONTH, -1.369409e-002, -759480485, 'uwSe', DATE '3202-10-18',
215786063);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '68-11' YEAR(2) TO MONTH, -4.558859e+000, -1636190047, 'QRjK', DATE '4012-12-07',
660540222);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-9' YEAR(2) TO MONTH, -1.380375e+007, -689909182, 'uEDAn', DATE '3246-12-11',
905288015);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-2' YEAR(2) TO MONTH, 1.095488e+000, -1274959713, 'M', DATE '2784-03-10',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-10' YEAR(2) TO MONTH, -4.839032e-018, -423565998, 'aA', DATE '3890-01-21',
806482149);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '71-9' YEAR(2) TO MONTH, 7.241196e-018, NULL, 'XFqO', DATE '2696-12-11',
582109062);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '26-7' YEAR(2) TO MONTH, -4.456991e+007, 1290332699, 'ru', DATE '2611-08-10',
483328357);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-11' YEAR(2) TO MONTH, -4.522443e+006, -653021738, NULL, DATE '3489-04-26',
752355695);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '21-7' YEAR(2) TO MONTH, -1.835034e+005, -1840684966, 'L9f2', DATE '3729-04-04',
091178033);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-5' YEAR(2) TO MONTH, -2.245124e+006, -1078530750, 'DU', DATE '3884-11-08',
688378295);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '42-4' YEAR(2) TO MONTH, NULL, 729533134, 'wwfi0', DATE '4271-03-04', 902919986
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '12-11' YEAR(2) TO MONTH, -5.160808e+012, 107009615, 'tulvO', DATE '3166-03-09',
611673135);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '28-7' YEAR(2) TO MONTH, 1.982766e+000, NULL, 'hG1R', DATE '2342-12-28',
477351401);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '84-3' YEAR(2) TO MONTH, 2.547971e-010, -461459767, 'UaNgy', DATE '4297-10-02',
578517815);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-5' YEAR(2) TO MONTH, 2.919827e-009, -1884562529, 'Hm', DATE '3450-09-18',
876907146);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-11' YEAR(2) TO MONTH, 7.795151e-022, 1770614336, 'L', DATE '2404-07-10',
510613458);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-8' YEAR(2) TO MONTH, 5.336036e+021, -1319204103, '9Vleo', DATE '3036-11-23',
479351582);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-2' YEAR(2) TO MONTH, 2.416713e-021, NULL, 'GtyX5', NULL, 809722442);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '56-2' YEAR(2) TO MONTH, 4.698055e+024, -275790847, '7', DATE '4232-01-16',
523235113);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-2' YEAR(2) TO MONTH, 2.806122e+014, 270642185, 'RQhh2', DATE '3248-09-12',
020012392)
;"""
    output = _dci.cmdexec(stmt)
