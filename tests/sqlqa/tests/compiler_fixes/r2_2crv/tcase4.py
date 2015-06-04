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

#*********************************************
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Wrong cardinality estimate when comparing to a large in-list of values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #********************************************
    
    stmt = """set schema """ + gvars.g_schema_hcubedb + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select * from cube3 where a in
(3,8,11,20,22,23,24,26,27,33,35,38,51,52,54,57,61,62,63,69,70,72,167,207,
212,225,400,402,407,408,409,410,411,412,414,415,417,418,419,420,433,441,443,
444,503,505,507,509,510,512,514,515,516,519,524,528,530,532,534,535,537,545,
555,556,558,559,560,566,567,569,602,608,609,611,612,629,630,631,632,634,635,
640,642,643,644,646,648,654,655,656,657,660,661,664,667,668,669,671,673,674,
675,676,677,678,680,682,683,685,686,687,690,691,693,695,696,706,709,711,713,
714,718,725,727,732,735,738,739,740,742,744,748,749,751,752,756,757,758,763,
765,766,773,774,775,776,788,789,790,793,795,797,801,803,810,812,815,820,822,
824,825,826,832,847,849,851,853,854,859,867,873,878,882,885,886,887,890,892,
893,894,897,2000,2002,2004,2005,2007,2013,2014,2023,2024,2028,2031,2040,2046,
2048,2051,2054,2059,2061,2063,2067,2070,2071,2073,2077,2078,2079,2080,2081,2082,
2083,2088,2089,2093,2095,2101,2106,2109,2113,2114,2121,2122,2123,2128,2130,2131,
2132,2133,2134,2135,2173,2220,2244,2663,2716,2835,2848,2134,2135,2146,2173,2220,
2244,2663,2716,2835,2848);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expect any * row(s) selected*
    #execute xx;
    
    _testmgr.testcase_end(desc)

