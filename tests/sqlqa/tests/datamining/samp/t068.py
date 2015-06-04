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
    
def test001(desc="""test068"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test068
    # DDunn
    # 1999-01-19
    # Testing sampling with all different join types
    # depends on tables samptb066a, b & c created in test066
    #
    # 1. natural left join
    # check the straight data first
    stmt = """select empid, salary, datehired
from samptb066a  NATURAL LEFT JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's1')
    # expect 12 rows with these values sorted on the first column:
    #         123     25000.00  1999-01-01
    #        1234     20000.00  1979-12-12
    #        2345     36000.00  1987-07-29
    #        3455     45000.00  1991-01-01
    #        4900     45000.00  1997-03-06
    #        5678     50000.00  1983-12-01
    #        6234     20000.00  1976-04-04
    #        6789     55000.00  1990-09-07
    #        6798     60000.00  1986-03-04
    #        8901     40000.00  1993-04-05
    #        9012     40000.00  1940-10-04
    #        9123     20050.00  1995-01-15
    
    stmt = """select empid, salary, datehired
from samptb066a  NATURAL LEFT JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
sample first 9 rows
sort by empid
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's2')
    # expect the first 9 rows of the data above
    
    # the same query as a view
    stmt = """create view vwsamp068a as
select empid, salary, datehired
from samptb066a  NATURAL LEFT JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
sample first 9 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwsamp068a 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's4')
    # expect the same 9 rows as above
    
    # 2. natural inner join
    # check the straight data first
    stmt = """select empid, salary, datehired
from samptb066a  NATURAL INNER JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's5')
    # expect 12 rows with the same values as above
    
    stmt = """create view vwsamp068b as
select empid, salary, datehired
from samptb066a  NATURAL INNER JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
sample first 9 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select empid, datehired
from vwsamp068b 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's7')
    # expect the same 9 rows as above
    
    # 3. natural right join
    # check the straight data first
    stmt = """select empid, salary, datehired
from samptb066a  NATURAL RIGHT JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's8')
    # expect 12 rows with the same values as above
    
    stmt = """create view vwsamp068c as
select empid, salary, datehired
from samptb066a  NATURAL RIGHT JOIN samptb066b 
where empid = empid and datehired < date '2000-01-01'
sample first 9 rows
sort by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select empid, datehired, salary
from vwsamp068c 
order by empid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's10')
    # expect the same 9 rows as above
    
    # 4. cross join
    # check the straight data first
    stmt = """select samptb066a.empid, samptb066a.salary, datehired
from samptb066a cross join samptb066b 
where samptb066a.empid = 123
order by datehired;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's11')
    # expect 13 rows with the following values sorted on the date:
    #        123     25000.00  1940-10-04
    #        123     25000.00  1976-04-04
    #        123     25000.00  1979-12-12
    #        123     25000.00  1983-12-01
    #        123     25000.00  1986-03-04
    #        123     25000.00  1987-07-29
    #        123     25000.00  1990-09-07
    #        123     25000.00  1991-01-01
    #        123     25000.00  1993-04-05
    #        123     25000.00  1995-01-15
    #        123     25000.00  1997-03-06
    #        123     25000.00  1999-01-01
    #        123     25000.00  2000-09-08
    
    stmt = """create view vwsamp068d as
select samptb066a.empid, samptb066a.salary, datehired
from samptb066a cross join samptb066b 
where samptb066a.empid = 123
sample first 9 rows
sort by datehired;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwsamp068d 
order by datehired;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test068.exp""", 's13')
    # expect the first 9 rows of the data above
    
    # cleanup
    stmt = """drop view vwsamp068a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vwsamp068b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vwsamp068c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vwsamp068d;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

