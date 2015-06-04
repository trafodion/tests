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
(INTERVAL '89-9' YEAR(2) TO MONTH, 4.250394e-001, 1260082738, 'l', NULL, 272149860
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '34-3' YEAR(2) TO MONTH, -1.566383e-028, 798868238, 'g8Wti', DATE '2179-05-13',
689461495);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-4' YEAR(2) TO MONTH, NULL, -1878481830, 'BLu1i', DATE '2881-02-09',
069818270);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '85-7' YEAR(2) TO MONTH, 6.052972e-014, NULL, '3yH', DATE '2180-04-20',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-11' YEAR(2) TO MONTH, -5.025774e-013, -428231034, 'LTEd', DATE '3828-03-03',
587132855);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '07-10' YEAR(2) TO MONTH, -4.958337e-013, NULL, 'QX5', DATE '2335-09-08',
793227497);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-4' YEAR(2) TO MONTH, 3.457417e+008, -826205746, 'q', DATE '3895-10-13',
093208682);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-6' YEAR(2) TO MONTH, 1.697061e-036, -1904016038, 'Sb', DATE '1870-01-07',
200522699);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-0' YEAR(2) TO MONTH, 3.400638e+017, NULL, 'xz', DATE '3575-11-12', 950057739
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-0' YEAR(2) TO MONTH, 1.018223e+024, NULL, 'Svs6m', DATE '4010-04-14',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '22-2' YEAR(2) TO MONTH, 1.000000e+000, -423529857, NULL, DATE '3309-02-27',
192472987);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '26-1' YEAR(2) TO MONTH, 3.325651e-021, -1810594049, 'e', DATE '3486-08-19',
875814022);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-2' YEAR(2) TO MONTH, 8.410314e+024, -1188005035, 'p3pFf', DATE '2394-02-06',
322078041);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-7' YEAR(2) TO MONTH, 1.218348e+013, 183692419, 'A', DATE '2575-02-24',
228575021);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-5' YEAR(2) TO MONTH, 5.941318e+000, -1897994218, 'qB', DATE '3768-09-03',
095406349);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '94-3' YEAR(2) TO MONTH, -5.492252e-013, -384032447, 'E', NULL, 432890806
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-7' YEAR(2) TO MONTH, 8.985447e+003, 1384710706, 'pN', DATE '2511-03-14',
827746093);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-2' YEAR(2) TO MONTH, NULL, NULL, 'I', DATE '3639-02-10', 733837723);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '01-2' YEAR(2) TO MONTH, NULL, 1199191096, 'JUY', DATE '3373-12-20', 427076559
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '91-5' YEAR(2) TO MONTH, -8.574407e+022, 1375425534, 'Y', DATE '1646-06-11',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-2' YEAR(2) TO MONTH, -2.567172e-025, 259975675, NULL, DATE '1864-01-09',
742403010);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '70-8' YEAR(2) TO MONTH, 2.477361e-006, 1030854781, 'Ub', NULL, 443608221
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '19-2' YEAR(2) TO MONTH, -4.380492e-014, 642174470, NULL, DATE '4452-02-25',
058528985);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '95-10' YEAR(2) TO MONTH, -1.608537e-007, -550493648, NULL, DATE '3455-08-20',
385360923);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-0' YEAR(2) TO MONTH, 6.091423e-012, -552365013, 'brLgb', DATE '3036-09-04',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-5' YEAR(2) TO MONTH, 1.367432e-015, 521266746, 'Wt7o', DATE '3787-08-03',
113680324);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '27-3' YEAR(2) TO MONTH, -2.813809e-020, 1376812068, 'EKI8d', DATE '4438-02-09',
240431917);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-11' YEAR(2) TO MONTH, -1.004952e+004, 134403658, '931LS', NULL, 628591931
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-7' YEAR(2) TO MONTH, -4.823297e+023, -1522272605, '3', DATE '4038-04-27',
821953762);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '71-3' YEAR(2) TO MONTH, 2.592658e+006, -1439515551, 'fD', DATE '2182-04-14',
373662975);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-6' YEAR(2) TO MONTH, -1.761083e+033, -943397647, 'i', DATE '1981-02-22',
610565232);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-5' YEAR(2) TO MONTH, -3.308344e-012, -630026878, 'r', DATE '2322-11-04',
601450236);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '37-6' YEAR(2) TO MONTH, -5.366263e+013, -1871039470, 'AXabm', DATE '2014-03-11',
109450057);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-3' YEAR(2) TO MONTH, -7.212207e+018, -1924019391, 'WDGbi', DATE '3778-02-06',
976605568);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '0-11' YEAR(2) TO MONTH, 4.256418e-009, 643115782, 'RiFL', DATE '2490-11-07',
112898451);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '30-4' YEAR(2) TO MONTH, -1.025925e-004, 643580962, 'n6lu', DATE '1998-04-23',
320621092);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '57-7' YEAR(2) TO MONTH, -3.966506e-001, -824829606, 'bAFzj', DATE '1882-10-09',
746304486);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-9' YEAR(2) TO MONTH, -1.192329e-006, -238973920, 'yOOK', DATE '2782-05-14',
521220604);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-0' YEAR(2) TO MONTH, 1.389111e+017, 1133471796, NULL, DATE '4276-07-31',
381155498);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '6-0' YEAR(2) TO MONTH, -8.482862e-040, 1505001054, 'Sk', DATE '2802-07-18',
101012401);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '58-3' YEAR(2) TO MONTH, 3.747689e+010, 1139523804, NULL, NULL, 262960393
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '55-0' YEAR(2) TO MONTH, -2.585291e+007, 365524755, 'nww', DATE '4019-04-28',
944734763);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '91-3' YEAR(2) TO MONTH, -7.565194e+020, -48399269, NULL, DATE '1996-10-13',
840130180);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-8' YEAR(2) TO MONTH, 1.540285e-022, -332234696, 'Tri9b', DATE '2112-10-16',
033244879);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-2' YEAR(2) TO MONTH, -4.559539e-001, 436443616, 'r', DATE '3913-12-06',
253722289);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '81-9' YEAR(2) TO MONTH, -2.765155e+008, -1102365069, 'MfCH', DATE '1965-03-18',
324052031);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '01-11' YEAR(2) TO MONTH, -1.938972e-021, 1603002470, 'wxSbf', DATE '2842-10-26',
659727191);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '40-4' YEAR(2) TO MONTH, -4.357221e-015, 314346646, 'xbY7c', NULL, 302943244
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '31-0' YEAR(2) TO MONTH, -4.263678e-003, -1537562679, '6lsky', DATE '3097-09-13',
958179322);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '24-5' YEAR(2) TO MONTH, -2.692612e+025, 1009160221, 'jy', DATE '4266-02-10',
820156919);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '68-4' YEAR(2) TO MONTH, 1.017790e-015, 1358470168, 'vSN', NULL, 435525693
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-5' YEAR(2) TO MONTH, -1.649518e-008, -1965754031, 'f', DATE '2469-08-22',
230202134);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '20-11' YEAR(2) TO MONTH, -1.093727e+024, NULL, 'aAJuw', NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '5-3' YEAR(2) TO MONTH, 1.292616e+033, -834137896, 'J', DATE '2340-10-31',
471105490);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '32-6' YEAR(2) TO MONTH, -2.716483e+000, 198106114, 'yA', DATE '4362-06-21',
372830372);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-4' YEAR(2) TO MONTH, 2.757048e+008, 634451807, 'E', NULL, 434280808);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-6' YEAR(2) TO MONTH, 9.781961e+004, -339541467, 'b', DATE '2969-01-11',
035453871);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-2' YEAR(2) TO MONTH, 3.578233e+024, 1794124697, NULL, DATE '1700-07-23',
110559810);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '21-2' YEAR(2) TO MONTH, -8.344458e+013, NULL, '4H', DATE '1914-04-20',
281781239);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '28-2' YEAR(2) TO MONTH, -4.128895e+015, -742412677, 'lsQ', DATE '3877-09-02',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-5' YEAR(2) TO MONTH, 3.922224e-033, -1233327360, 'tj', DATE '3653-06-18',
108807030);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-3' YEAR(2) TO MONTH, 8.846496e+008, 141806557, NULL, DATE '4005-07-22',
471597821);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-5' YEAR(2) TO MONTH, 6.491312e-019, 1625206979, 'BV5', DATE '3201-06-28',
993424819);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-6' YEAR(2) TO MONTH, 3.212300e+004, -601650532, '4', NULL, 404508949
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-2' YEAR(2) TO MONTH, -1.091953e-008, -403158900, 'rGN3I', DATE '4097-12-18',
335158431);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '51-9' YEAR(2) TO MONTH, -1.290204e-025, 1090921581, 'wydg', NULL, 651209135
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '92-8' YEAR(2) TO MONTH, -1.364308e-009, 182602607, 'Vey6l', DATE '2896-01-04',
378742629);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '57-3' YEAR(2) TO MONTH, 7.283128e-018, NULL, 'v', DATE '1755-04-12', 115199138
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '87-9' YEAR(2) TO MONTH, 5.545333e+023, -1192670998, 'jU6qV', DATE '1694-07-14',
156179881);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '15-4' YEAR(2) TO MONTH, 2.860282e+017, -1709311356, 'j3MR', DATE '2953-04-15',
280587880);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '55-8' YEAR(2) TO MONTH, -3.274858e+020, -437129665, 'etUNy', DATE '1883-03-15',
067422533);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-1' YEAR(2) TO MONTH, 9.383560e-014, 102214366, '3jVB', DATE '1591-10-26',
996432154);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '1-6' YEAR(2) TO MONTH, -4.057405e+008, -568286144, 'RNsvL', DATE '2213-10-16',
811350724);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-9' YEAR(2) TO MONTH, 1.986875e-009, 1570427871, 'KAjMI', DATE '4031-04-12',
012110833);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-7' YEAR(2) TO MONTH, -6.350338e+008, -1225053481, 'vCe', NULL, 510959166
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-1' YEAR(2) TO MONTH, NULL, 679568366, 'RrfL', DATE '4443-07-18', 656580503
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '42-9' YEAR(2) TO MONTH, NULL, NULL, 'ZGw2', DATE '3372-02-26', 320551916
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-11' YEAR(2) TO MONTH, 6.911590e+005, 1309892078, 'C', DATE '2480-06-11',
418199563);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '59-0' YEAR(2) TO MONTH, 1.305267e-002, -1560742621, 'h', DATE '2267-02-09',
181380420);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '2-0' YEAR(2) TO MONTH, 1.647550e+023, -1659328726, NULL, DATE '3457-02-06',
864697163);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '57-2' YEAR(2) TO MONTH, -1.186139e+019, 673530062, 'kJ', DATE '2707-07-31',
669923152);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '4-8' YEAR(2) TO MONTH, -2.023472e+012, 821307792, 'Dv4', NULL, 490424572
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '03-11' YEAR(2) TO MONTH, -1.803144e-012, 571338753, 'fJ', DATE '3474-09-13',
955565698);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '01-6' YEAR(2) TO MONTH, -7.841831e+023, -83271255, 'i', DATE '4045-04-17',
602440869);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '43-5' YEAR(2) TO MONTH, 1.784875e+001, 1333471792, 'phTs', DATE '2046-09-08',
266851657);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-5' YEAR(2) TO MONTH, 8.058798e+028, -419522630, 'Pqku', DATE '3807-06-12',
544095558);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '70-6' YEAR(2) TO MONTH, 1.962400e-012, 1024054173, 'uM', DATE '3816-06-09',
690424155);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '07-8' YEAR(2) TO MONTH, -2.273003e+008, -1545250026, 'DZYuV', DATE '2155-04-08',
089483704);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '8-6' YEAR(2) TO MONTH, NULL, -365209879, 'Im', DATE '3860-10-02', 538394429
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-11' YEAR(2) TO MONTH, -1.118282e+013, -1785155468, 'V41Ng', DATE '1807-03-09',
365534169);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '66-1' YEAR(2) TO MONTH, 2.005959e+012, NULL, 'k', NULL, 694157581);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '44-10' YEAR(2) TO MONTH, -1.058343e+012, 1447149334, 'U1', DATE '3779-09-21',
676730331);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '3-7' YEAR(2) TO MONTH, 3.302901e+026, -1591077624, 'MG', DATE '3852-05-20',
742754706);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-0' YEAR(2) TO MONTH, -1.011932e+010, -2050877029, 'Wg', DATE '2030-04-01',
773489398);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '87-2' YEAR(2) TO MONTH, -3.473702e+025, -143433937, 'vjaCX', NULL, 472111522
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '72-9' YEAR(2) TO MONTH, NULL, -753354412, 'd5G', DATE '3008-08-01', 293786568
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '76-3' YEAR(2) TO MONTH, NULL, -289565503, 'CS', DATE '3306-09-28', 268528840
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '9-4' YEAR(2) TO MONTH, 3.134142e-017, -721851767, 'a7uw', DATE '2019-08-02',
NULL);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '7-6' YEAR(2) TO MONTH, 6.780797e-030, -607109455, 'pNMNb', DATE '1680-08-18',
386558557);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab1
values
(INTERVAL '39-1' YEAR(2) TO MONTH, 1.269857e+017, NULL, 'qPSZq', DATE '3530-11-09',
258886165)
;"""
    output = _dci.cmdexec(stmt)
