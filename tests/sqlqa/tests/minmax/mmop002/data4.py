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
(INTERVAL '2-2' YEAR(2) TO MONTH, NULL, -1938156720, 'rZ5iw', DATE '2161-08-15',
375064737);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-9' YEAR(2) TO MONTH, -5.457462e-005, 918614049, 'Re3', DATE '4090-06-15',
464773969);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '22-5' YEAR(2) TO MONTH, 8.591608e-008, 544547501, 'rr', DATE '2666-10-20',
017529775);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '41-6' YEAR(2) TO MONTH, 6.190461e+007, 2132442305, '68rE', DATE '3513-03-20',
795068201);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '45-7' YEAR(2) TO MONTH, -4.466111e+012, -147839235, 'pZZ5', DATE '3416-07-05',
344443965);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '17-8' YEAR(2) TO MONTH, 1.409612e-007, 890237957, 'e', NULL, 075505908
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '19-10' YEAR(2) TO MONTH, -5.420739e+008, 1409651026, 'Dvd8E', NULL, 104452822
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-6' YEAR(2) TO MONTH, 3.120938e+000, 358582181, 'pYV5', DATE '1745-05-29',
861977951);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '74-0' YEAR(2) TO MONTH, 3.593997e+025, 1604097310, NULL, DATE '3801-11-09',
821835573);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-3' YEAR(2) TO MONTH, -1.359550e-003, -1226992439, 'Ahw5', DATE '4004-09-28',
780528871);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-8' YEAR(2) TO MONTH, NULL, 329855009, 'J6EE', DATE '1618-12-28', 707708536
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-5' YEAR(2) TO MONTH, NULL, -1466732099, 'lOU', DATE '4456-05-17', 880819715
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-0' YEAR(2) TO MONTH, -6.364069e+015, -785069510, 'r9', DATE '3140-12-28',
688077690);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-10' YEAR(2) TO MONTH, 7.137314e+000, -834131533, 'JYEH', DATE '2007-04-07',
796267969);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '95-9' YEAR(2) TO MONTH, NULL, 1253932461, NULL, DATE '3747-06-29', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '21-1' YEAR(2) TO MONTH, -3.573103e+006, 284198526, 'GUIgM', DATE '4176-11-06',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-1' YEAR(2) TO MONTH, 3.177589e-021, NULL, '6', DATE '1563-06-03', 994586556
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '65-2' YEAR(2) TO MONTH, -8.782937e-038, NULL, '7756', DATE '2384-05-22',
635809676);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '64-9' YEAR(2) TO MONTH, -4.031420e+004, -1056597337, 'Lqijs', DATE '1663-02-05',
887267249);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-10' YEAR(2) TO MONTH, -1.207695e+021, -812027439, 'wDH', DATE '4460-12-17',
890555343);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '85-7' YEAR(2) TO MONTH, 4.067873e+002, -1422439427, 'AA', DATE '2726-03-10',
059296669);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-0' YEAR(2) TO MONTH, NULL, 1353249830, 'x', DATE '1799-10-26', 580095976
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-5' YEAR(2) TO MONTH, -6.109295e+015, 1887360316, '2', DATE '4108-08-15',
821099452);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '99-2' YEAR(2) TO MONTH, -1.851765e-015, NULL, NULL, DATE '4073-09-10',
138422512);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-4' YEAR(2) TO MONTH, -1.000000e+000, -1367851004, 'D', DATE '2794-12-01',
615215354);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-9' YEAR(2) TO MONTH, 3.372524e-009, -1240511970, 'hg530', DATE '2937-03-12',
890347814);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-9' YEAR(2) TO MONTH, -3.286926e+007, 11459181, '1j', DATE '2847-03-09',
040471066);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-0' YEAR(2) TO MONTH, 6.208298e-009, NULL, 'jHdj1', DATE '1597-10-21',
681839221);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-9' YEAR(2) TO MONTH, 1.638062e+017, -307846846, NULL, DATE '2511-02-04',
139615296);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-8' YEAR(2) TO MONTH, -1.361439e+021, -1240944146, 'bN', DATE '4107-01-24',
129257544);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-7' YEAR(2) TO MONTH, 1.000343e+002, 1158893090, '0fYP', DATE '3649-05-12',
456045947);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '35-6' YEAR(2) TO MONTH, -7.188082e+013, 1743016579, '6gT', DATE '2933-08-15',
944725246);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '30-2' YEAR(2) TO MONTH, -1.000000e+000, -508111400, 'X', DATE '2392-08-14',
276791733);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-7' YEAR(2) TO MONTH, 2.990185e+018, 1762385700, NULL, NULL, 126049964
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-11' YEAR(2) TO MONTH, NULL, 970147684, '7XkM', DATE '4159-04-22', 051898629
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '33-4' YEAR(2) TO MONTH, 8.196439e-004, -110510757, 'I', DATE '3709-10-03',
978762335);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '64-3' YEAR(2) TO MONTH, 3.320819e-026, 2022833759, 'Qmdf8', DATE '2538-03-04',
767261430);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '68-0' YEAR(2) TO MONTH, 1.042582e-004, -2068823893, 'uY3', DATE '3674-06-21',
903152027);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-5' YEAR(2) TO MONTH, 1.000000e+000, -658195324, 'lc', DATE '3605-09-03',
454775538);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, 7.733288e-011, -490472931, 'MiW2', DATE '2421-06-03',
449333841);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '85-2' YEAR(2) TO MONTH, NULL, 1320623344, 'ZHsI', DATE '4418-05-25', 208853703
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-8' YEAR(2) TO MONTH, -2.755360e+005, 325640123, 'sM', DATE '1546-01-24',
407502160);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-0' YEAR(2) TO MONTH, -3.769845e-009, 2074539582, '6u5q', DATE '2732-08-18',
974125625);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-0' YEAR(2) TO MONTH, 6.284922e+008, 167443349, 'pFO', NULL, 368214430
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-5' YEAR(2) TO MONTH, -3.559007e-030, NULL, 'c3q6', DATE '3551-05-27',
676957577);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-7' YEAR(2) TO MONTH, NULL, 1419148116, 'dNAHE', DATE '3367-09-10', 368140302
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '03-3' YEAR(2) TO MONTH, -1.181805e+007, 1886529422, 'CPZ', DATE '4321-04-04',
406513862);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-1' YEAR(2) TO MONTH, 1.905955e+019, -35518683, 'd7dg', DATE '3204-11-06',
598788111);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '12-6' YEAR(2) TO MONTH, 7.225865e+010, -1507198213, '5DGDU', DATE '3196-01-28',
249991530);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-5' YEAR(2) TO MONTH, 1.690083e+021, 281810781, 'nBHGO', DATE '2024-11-29',
882059344);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-11' YEAR(2) TO MONTH, 3.609544e+004, -620950723, 'bx6', DATE '1886-07-21',
063755441);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '41-5' YEAR(2) TO MONTH, 4.830417e-013, 181397476, 'VfB', DATE '4093-10-07',
629809000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '02-6' YEAR(2) TO MONTH, 1.959449e+017, -263102280, 'rFP', DATE '2538-10-12',
062314123);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-2' YEAR(2) TO MONTH, 2.258564e-012, -1057078071, NULL, DATE '1973-12-26',
899081006);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '07-10' YEAR(2) TO MONTH, -1.893478e+027, NULL, '3a', DATE '2208-03-26',
364815478);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-9' YEAR(2) TO MONTH, -7.619453e-013, -204932308, 'J0', DATE '3152-10-05',
163060806);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '63-5' YEAR(2) TO MONTH, NULL, -379618741, '0oh', DATE '1797-04-21', 621580608
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-10' YEAR(2) TO MONTH, 5.227694e+031, 475910775, 'W8bF', DATE '3788-04-21',
511360944);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-7' YEAR(2) TO MONTH, -6.119318e-004, -1852050312, '0e27y', DATE '1774-01-19',
579143602);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '46-3' YEAR(2) TO MONTH, 3.649045e-001, NULL, 'QhGt', DATE '3732-10-21',
019373532);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-6' YEAR(2) TO MONTH, -2.958007e+017, NULL, 'Cf', DATE '3741-01-18',
168938631);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-1' YEAR(2) TO MONTH, 3.777676e+003, 302650487, 'EOaF1', DATE '3848-02-07',
309827369);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-2' YEAR(2) TO MONTH, 3.043641e+007, -633771803, '8S5', DATE '1744-05-30',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-5' YEAR(2) TO MONTH, 5.794482e+019, -1779329072, 'MCsg', DATE '3817-06-28',
333345283);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '49-4' YEAR(2) TO MONTH, 1.172980e+024, -2026761066, '6sIWx', DATE '3357-08-16',
484767494);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-0' YEAR(2) TO MONTH, -4.754612e-014, 1436229310, 'e', DATE '3592-06-16',
162820930);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-7' YEAR(2) TO MONTH, -1.805343e-022, 116158450, 'IS', DATE '4494-08-02',
804459955);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '01-0' YEAR(2) TO MONTH, -7.472482e-014, 176088026, 'nlQbu', DATE '1929-10-25',
117904984);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-9' YEAR(2) TO MONTH, 5.949435e-010, 440019387, 'jcHZq', DATE '3815-12-01',
688593707);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-7' YEAR(2) TO MONTH, 3.040469e+029, 11196498, 'rE4y', NULL, 342219095
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-6' YEAR(2) TO MONTH, 1.529086e+000, 1128836905, 'VC', DATE '3983-07-27',
413966985);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '81-4' YEAR(2) TO MONTH, 3.197826e+011, -1979324052, '4', DATE '4267-03-23',
754839316);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '27-8' YEAR(2) TO MONTH, 1.305049e+000, NULL, '3', NULL, 643791755);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-7' YEAR(2) TO MONTH, NULL, -1334106584, 'HQF', DATE '3520-02-23', 917254584
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '69-9' YEAR(2) TO MONTH, -4.506499e-026, -1193970522, 'd4Cna', DATE '2125-11-20',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '16-9' YEAR(2) TO MONTH, 2.466156e+021, 1827121646, 'YC', DATE '3487-06-20',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-7' YEAR(2) TO MONTH, NULL, 398664961, 'xJ', NULL, 931028987);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-8' YEAR(2) TO MONTH, 1.859206e-003, -891566320, 'tsEaq', DATE '4451-02-08',
471664321);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, 1.466682e-038, 955129986, 'cz0', DATE '2496-04-30',
011838533);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-3' YEAR(2) TO MONTH, 1.796184e+016, -181468170, 'pW', DATE '2899-02-04',
532410464);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '66-2' YEAR(2) TO MONTH, NULL, -2068180035, 'lc', DATE '2013-09-05', 497500151
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-4' YEAR(2) TO MONTH, -5.921902e+025, -1641421752, 'PKtY', DATE '3054-01-03',
678927764);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-1' YEAR(2) TO MONTH, -7.999467e+015, NULL, 'BG', DATE '2457-04-25',
566145122);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '89-9' YEAR(2) TO MONTH, -2.741556e-003, 1542342086, '9orK', DATE '4192-08-08',
148031912);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '24-3' YEAR(2) TO MONTH, 2.571899e-005, -30332149, 'v', DATE '3394-09-22',
084150104);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-1' YEAR(2) TO MONTH, -4.989575e+027, -1509865049, 'Ka7L', DATE '4115-07-11',
280873643);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-6' YEAR(2) TO MONTH, 7.714989e+023, 926939767, 'byl2', DATE '4108-01-26',
562421913);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-3' YEAR(2) TO MONTH, 1.730267e+003, -1658426628, 'F', DATE '1914-03-23',
128454519);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-10' YEAR(2) TO MONTH, -4.847603e+027, 2130753980, NULL, DATE '1507-10-16',
418490645);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-1' YEAR(2) TO MONTH, -1.229140e+006, -1928604610, '2yiOI', DATE '3096-04-30',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-2' YEAR(2) TO MONTH, 4.506323e-023, -390803657, 'zXqk', DATE '2864-04-27',
447699426);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-0' YEAR(2) TO MONTH, -1.886152e+019, NULL, '7wyxd', DATE '2564-09-25',
822763049);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '65-10' YEAR(2) TO MONTH, 5.407558e+011, -1505213472, 'DnnQ', DATE '4387-09-24',
005436183);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-8' YEAR(2) TO MONTH, -2.208541e+007, -1636299474, 'G', DATE '4496-08-05',
906040098);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-8' YEAR(2) TO MONTH, 6.157871e+010, -1641668763, 'L', NULL, 042521993
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '69-9' YEAR(2) TO MONTH, 6.084978e+007, -2092807384, NULL, DATE '3366-08-17',
023817224);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '03-2' YEAR(2) TO MONTH, 2.007400e+004, -1570197541, 'iT', DATE '2055-06-25',
765279085);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-1' YEAR(2) TO MONTH, 3.534072e+013, -1890733533, 'Mc', DATE '2737-12-31',
879737148);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '24-7' YEAR(2) TO MONTH, -1.084944e+029, 201372082, 's25bv', DATE '4152-01-16',
110041202);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-9' YEAR(2) TO MONTH, -2.049745e-016, -1798560424, 'PM', DATE '2249-04-05',
508190546)
;"""
    output = _dci.cmdexec(stmt)
