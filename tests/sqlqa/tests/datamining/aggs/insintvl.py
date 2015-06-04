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
    
def test001(desc="""insintvl"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # insintvl.sql
    # jclear
    # 1997-05-01
    # Set up for the new aggregate tests.
    # Loads the data into the 'intrval' table.
    #
    stmt = """delete from intrval;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into intrval values
(interval '14' year, interval '76' month, interval '14' day,
interval '32' hour, interval '54' minute, interval '95' second, 1 ),
(interval '27' year, interval '96' month, interval '80' day,
interval '18' hour, interval '06' minute, interval '26' second, 2 ),
(interval '84' year, interval '64' month, interval '39' day,
interval '17' hour, interval '73' minute, interval '35' second, 3 ),
(interval '10' year, interval '81' month, interval '28' day,
interval '58' hour, interval '45' minute, interval '11' second, 4 ),
(interval '16' year, interval '44' month, interval '72' day,
interval '64' hour, interval '54' minute, interval '43' second, 5 ),
(interval '75' year, interval '10' month, interval '48' day,
interval '80' hour, interval '29' minute, interval '16' second, 6 ),
(null, interval '04' month, interval '42' day,
interval '75' hour, interval '69' minute, interval '20' second, 7 ),
(interval '99' year, null, interval '93' day,
interval '65' hour, interval '58' minute, interval '96' second, 8 ),
(interval '49' year, interval '10' month, null,
interval '66' hour, interval '57' minute, interval '14' second, 9 ),
(interval '96' year, interval '19' month, interval '50' day,
null, interval '68' minute, interval '43' second, 10 ),
(interval '82' year, interval '91' month, interval '7' day,
interval '59' hour, null, interval '03' second, 11 ),
(interval '03' year, interval '94' month, interval '92' day,
interval '32' hour, interval '54' minute, null, 12 ),
(interval '86' year, interval '89' month, interval '15' day,
interval '76' hour, interval '28' minute, interval '73' second, 13 ),
(interval '08' year, interval '04' month, interval '43' day,
interval '51' hour, interval '13' minute, interval '43' second, 14 ),
(interval '59' year, interval '39' month, interval '99' day,
interval '89' hour, interval '21' minute, interval - '09' second, 15 ),
(interval '23' year, interval '70' month, interval '10' day,
interval '35' hour, interval - '72' minute, interval '03' second, 16 ),
(interval '55' year, interval '54' month, interval '62' day,
interval - '35' hour, interval '56' minute, interval '03' second, 17 ),
(interval '36' year, interval '65' month, interval - '9' day,
interval '05' hour, interval '23' minute, interval '94' second, 18 ),
(interval '37' year, interval - '48' month, interval '90' day,
interval '59' hour, interval '02' minute, interval '71' second, 19 ),
(interval - '18' year, interval '88' month, interval '59' day,
interval '51' hour, interval '16' minute, interval '00' second, 20 ),
(interval '19' year, interval '32' month, interval '48' day,
interval '34' hour, interval '07' minute, interval '75' second, 21 ),
(interval '66' year, interval '58' month, interval '69' day,
interval '93' hour, interval '10' minute, interval '90' second, 22 ),
(interval '81' year, interval '60' month, interval '27' day,
interval '62' hour, interval '11' minute, interval '91' second, 23 ),
(interval '59' year, interval '28' month, interval '78' day,
interval '10' hour, interval '72' minute, interval '13' second, 24 ),
(interval '07' year, interval '52' month, interval '54' day,
interval '80' hour, interval '47' minute, interval '78' second, 25 ),
(interval '15' year, interval '91' month, interval '64' day,
interval '50' hour, interval '98' minute, interval '41' second, 26 ),
(null, interval '49' month, interval '22' day,
interval '37' hour, interval '72' minute, interval '82' second, 27 ),
(interval '37' year, null, interval '73' day,
interval '24' hour, interval '61' minute, interval '15' second, 28 ),
(interval '62' year, interval '38' month, null,
interval '46' hour, interval '99'minute, interval '61' second, 29 ),
(interval '75' year, interval '78' month, interval '11' day,
null, interval '39' minute, interval '09' second, 30 ),
(interval '70' year, interval '57' month, interval '23' day,
interval '27' hour, null, interval '53' second, 31 ),
(interval '69' year, interval '68' month, interval '70' day,
interval '58' hour, interval '61' minute, null, 32 ),
(interval '51' year, interval '22' month, interval '80' day,
interval '33' hour, interval '46' minute, interval '52' second, 33 ),
(interval '77' year, interval '33' month, interval '11' day,
interval '45' hour, interval '49' minute, interval '98' second, 34 ),
(interval '82' year, interval '32' month, interval '56' day,
interval '00' hour, interval '07' minute, interval - '65' second, 35 ),
(interval '85' year, interval '99' month, interval '93' day,
interval '37' hour, interval - '14' minute, interval '60' second, 36 ),
(interval '14' year, interval '78' month, interval '77' day,
interval - '12' hour, interval '37' minute, interval '99' second, 37 ),
(interval '86' year, interval '02' month, interval - '92' day,
interval '19' hour, interval '22' minute, interval '05' second, 38 ),
(interval '90' year, interval - '08' month, interval '73' day,
interval '52' hour, interval '56' minute, interval '53' second, 39 ),
(interval - '79' year, interval '34' month, interval '91' day,
interval '05' hour, interval '06' minute, interval '89' second, 40 ),
(interval '30' year, interval '37' month, interval '96' day,
interval '77' hour, interval '51' minute, interval '75' second, 41 ),
(interval '74' year, interval '70' month, interval '63' day,
interval '39' hour, interval '24' minute, interval '32' second, 42 ),
(interval '91' year, interval '30' month, interval '54' day,
interval '30' hour, interval '19' minute, interval '18' second, 43 ),
(interval '30' year, interval '67' month, interval '30' day,
interval '49' hour, interval '83' minute, interval '18' second, 44 ),
(interval '39' year, interval '53' month, interval '59' day,
interval '40' hour, interval '71' minute, interval '21' second, 45 ),
(interval '44' year, interval '72' month, interval '16' day,
interval '93' hour, interval '54' minute, interval '99' second, 46 ),
(null, interval '97' month, interval '69' day,
interval '07' hour, interval '52' minute, interval '35' second, 47 ),
(interval '17' year, null, interval '70' day,
interval '84' hour, interval '59' minute, interval '31' second, 48 ),
(interval '83' year, interval '99' month, null,
interval '35' hour, interval '17' minute, interval '62' second, 49 ),
(interval '45' year, interval '12' month, interval '79' day,
null, interval '1' minute, interval '18' second, 50 ),
(interval '51' year, interval '27' month, interval '91' day,
interval '50' hour, null, interval '89' second, 51 ),
(interval '68' year, interval '9' month, interval '54' day,
interval '31' hour, interval '66' minute, null, 52 ),
(interval '96' year, interval '65' month, interval '39' day,
interval '29' hour, interval '17' minute, interval '17' second, 53 ),
(interval '99' year, interval '09' month, interval '21' day,
interval '05' hour, interval '77' minute, interval '76' second, 54 ),
(interval '05' year, interval '99' month, interval '06' day,
interval '09' hour, interval '39' minute, interval - '95' second, 55 ),
(interval '68' year, interval '45' month, interval '78' day,
interval '02' hour, interval - '99' minute, interval '30' second, 56 ),
(interval '60' year, interval '74' month, interval '43' day,
interval - '63' hour, interval '52' minute, interval '86' second, 57 ),
(interval '73' year, interval '81' month, interval - '30' day,
interval '54' hour, interval '25' minute, interval '85' second, 58 ),
(interval '53' year, interval - '71' month, interval '04' day,
interval '12' hour, interval '17' minute, interval '13' second, 59 ),
(interval - '60' year, interval '20' month, interval '54' day,
interval '27' hour, interval '84' minute, interval '65' second, 60 ),
(interval '82' year, interval '76' month, interval '96' day,
interval '06' hour, interval '64' minute, interval '37' second, 61 ),
(interval '34' year, interval '51' month, interval '42' day,
interval '53' hour, interval '38' minute, interval '75' second, 62 ),
(interval '17' year, interval '99' month, interval '66' day,
interval '35' hour, interval '37' minute, interval '93' second, 63 ),
(interval '27' year, interval '53' month, interval '91' day,
interval '23' hour, interval '46' minute, interval '75' second, 64 ),
(interval '02' year, interval '82' month, interval '77' day,
interval '41' hour, interval '47' minute, interval '99' second, 65 ),
(interval '15' year, interval '07' month, interval '73' day,
interval '38' hour, interval '14' minute, interval '99' second, 66 ),
(null, interval '99' month, interval '30' day,
interval '92' hour, interval '32' minute, interval '35' second, 67 ),
(interval '90' year, null, interval '90' day,
interval '60' hour, interval '48' minute, interval '12' second, 68 ),
(interval '08' year, interval '59' month, null,
interval '05' hour, interval '00' minute, interval '36' second, 69 ),
(interval '50' year, interval '99' month, interval '54' day,
null, interval '45' minute, interval '85' second, 70 ),
(interval '30' year, interval '07' month, interval '14' day,
interval '14' hour, null, interval '54' second, 71 ),
(interval '47' year, interval '82' month, interval '66' day,
interval '54' hour, interval '75' minute, null, 72 ),
(interval '99' year, interval '61' month, interval '74' day,
interval '91' hour, interval '71' minute, interval '64' second, 73 ),
(interval '96' year, interval '76' month, interval '84' day,
interval '15' hour, interval '78' minute, interval '82' second, 74 ),
(interval '05' year, interval '36' month, interval '19' day,
interval '74' hour, interval '37' minute, interval - '44' second, 75 ),
(interval '19' year, interval '60' month, interval '50' day,
interval '04' hour, interval - '85' minute, interval '76' second, 76 ),
(interval '23' year, interval '05' month, interval '19' day,
interval - '85' hour, interval '88' minute, interval '78' second, 77 ),
(interval '18' year, interval '52' month, interval - '54' day,
interval '46' hour, interval '53' minute, interval '28' second, 78 ),
(interval '87' year, interval - '27' month, interval '44' day,
interval '63' hour, interval '46' minute, interval '40' second, 79 ),
(interval - '16' year, interval '51' month, interval '95' day,
interval '39' hour, interval '98' minute, interval '02' second, 80 ),
(interval '72' year, interval '71' month, interval '83' day,
interval '00' hour, interval '68' minute, interval '33' second, 81 ),
(interval '34' year, interval '93' month, interval '81' day,
interval '78' hour, interval '65' minute, interval '49' second, 82 ),
(interval '93' year, interval '10' month, interval '58' day,
interval '62' hour, interval '54' minute, interval '57' second, 83 ),
(interval '01' year, interval '51' month, interval '17' day,
interval '57' hour, interval '63' minute, interval '06' second, 84 ),
(interval '62' year, interval '84' month, interval '20' day,
interval '43' hour, interval '99' minute, interval '06' second, 85 ),
(interval '67' year, interval '53' month, interval '77' day,
interval '79' hour, interval '01' minute, interval '31' second, 86 ),
(null, interval '18' month, interval '86' day,
interval '03' hour, interval '79' minute, interval '24' second, 87 ),
(interval '44' year, null, interval '98' day,
interval '50' hour, interval '88' minute, interval '22' second, 88 ),
(interval '17' year, interval '45' month, null,
interval '37' hour, interval '44' minute, interval '96' second, 89 ),
(interval '60' year, interval '51' month, interval '58' day,
null, interval '15' minute, interval '6' second, 90 ),
(interval '15' year, interval '47' month, interval '61' day,
interval '13' hour, null, interval '16' second, 91 ),
(interval '48' year, interval '16' month, interval '05' day,
interval '65' hour, interval '67' minute, null, 92 ),
(interval '54' year, interval '35' month, interval '16' day,
interval '05' hour, interval '45' minute, interval - '90' second, 93 ),
(interval '08' year, interval '55' month, interval '04' day,
interval '55' hour, interval - '98' minute, interval '65' second, 94 ),
(interval '77' year, interval '50' month, interval '06' day,
interval - '11' hour, interval '66' minute, interval '17' second, 95 ),
(interval '18' year, interval '82' month, interval - '56' day,
interval '62' hour, interval '97' minute, interval '57' second, 96 ),
(interval '72' year, interval - '59' month, interval '24' day,
interval '87' hour, interval '82' minute, interval '39' second, 97 ),
(interval - '69' year, interval '55' month, interval '14' day,
interval '57' hour, interval '90' minute, interval '51' second, 98 ),
(interval '67' year, interval '53' month, interval '46' day,
interval '11' hour, interval '71' minute, interval '66' second, 99 ),
(interval '88' year, interval '69' month, interval '24' day,
interval '13' hour, interval '26' minute, interval '24' second, 100);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) as CountStar from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvla')
    # expect count = 100
    
    stmt = """select
sum (iyr) as SumYear,
avg (iyr) as AvgYear,
max (iyr) as MaxYear,
min (iyr) as MinYear
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvlb')
    # expect sum = 4334, avg = 45.62, max = 99, min = -79
    
    stmt = """select
sum (imon) as SumMon,
avg (imon) as AvgMon,
max (imon) as MaxMon,
min (imon) as MinMon
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvlc')
    # expect sum = 4655, avg = 49, max = 99, min = -71
    
    stmt = """select
sum (idy) as SumDat,
avg (idy) as AvgDat,
max (idy) as MaxDat,
min (idy) as MinDat
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvld')
    # expect sum = 4510, avg = 47.47, max = 99, min = -92
    
    stmt = """select
sum (imin) as SumMin,
avg (imin) as AvgMin,
max (imin) as MaxMin,
min (imin) as MinMin
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvle')
    # expect sum = 4003, avg = 42.13, max = 99, min = -99
    
    stmt = """select
sum (isec) as SumSec,
avg (isec) as AvgSec,
max (isec) as MaxSec,
min (isec) as MinSec
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insintvlexp""", 'insintvlf')
    # expect sum = 4055, avg = 42.68, max = 99, min = -95
    
    _testmgr.testcase_end(desc)

