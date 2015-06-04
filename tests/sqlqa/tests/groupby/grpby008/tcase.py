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
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #Convertimestamp function
    stmt = """Select converttimestamp(JULIANTIMESTAMP (hire_date)) from emp group by  converttimestamp(JULIANTIMESTAMP (hire_date));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    #current function
    stmt = """Select CURRENT(5) from emp group by CURRENT(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #current_date function
    stmt = """select current_date from emp group by current_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #current_time function
    stmt = """select current_time from emp group by current_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #current_timestamp function
    stmt = """select current_timestamp(4) from emp group by current_timestamp(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #dateformat function
    stmt = """select dateformat(hire_date, USA) from emp group by dateformat(hire_date, USA);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    
    #day function
    stmt = """select day(hire_date) from emp group by  day(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s2""")
    
    #dayname function
    stmt = """select dayname(hire_date) from emp group by dayname(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    
    #dayofmonth function
    stmt = """select dayofmonth(hire_date) from emp group by dayofmonth(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    #dayofweek function
    stmt = """select dayofweek(hire_date) from emp group by  dayofweek(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s5""")
    
    #dayofyear function
    stmt = """select dayofyear(hire_date) from emp group by dayofyear(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s6""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #extract function
    stmt = """select extract(year from hire_date) from emp group by extract(year from hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    stmt = """select extract(month from hire_date) from emp group by extract(month from hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s2""")
    
    stmt = """select extract(day from hire_date) from emp group by extract(day from hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    
    #hour function
    stmt = """select hour(cast(hire_date as datetime year to second)) from emp group by hour(cast(hire_date as datetime year to second));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s4""")
    
    #juliantimestamp function
    stmt = """select Juliantimestamp(hire_date) from emp group by Juliantimestamp(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s5""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #minute function
    stmt = """select minute(cast(hire_date as datetime year to second)) from emp group by minute(cast(hire_date as datetime year to second));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s1""")
    
    #month function
    stmt = """select month(hire_date) from emp group by  month(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s2""")
    
    #monthname function
    stmt = """select monthname(hire_date) from emp group by monthname(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s3""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #quarter function
    stmt = """select quarter(hire_date) from emp group by  quarter(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s1""")
    
    #second function
    stmt = """select second(cast(hire_date as datetime year to second)) from emp group by second(cast(hire_date as datetime year to second));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s2""")
    
    #week function
    stmt = """select week(hire_date) from emp group by week(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s3""")
    
    #year function
    stmt = """select year(hire_date) from emp group by year(hire_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s4""")
    _testmgr.testcase_end(desc)

