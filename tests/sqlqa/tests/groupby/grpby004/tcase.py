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
    
    stmt = """Select cast(END_TIME AS  DATE) from emp group by
cast(END_TIME AS  DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    stmt = """Select cast(START_TIME AS  TIMESTAMP) from emp group by
cast(START_TIME AS  TIMESTAMP);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select experience + 3 from emp group by
experience + 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s1""")
    
    stmt = """select experience - 4 from emp group by
experience - 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s2""")
    
    stmt = """select experience + interval '2-7' year to month from emp  group by
experience + interval '2-7' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s3""")
    
    stmt = """select experience + interval '2' year from emp group by
experience + interval '2' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s4""")
    
    stmt = """select experience + interval '5' month from emp group by
experience + interval '5' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s5""")
    
    stmt = """select experience - interval '1-2' year to month from emp  group by
experience - interval '1-2' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s6""")
    
    stmt = """select experience - interval '4' year from emp group by
experience - interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s7""")
    
    stmt = """select experience - interval '3' month from emp group by
experience - interval '3' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s8""")
    
    stmt = """select experience + interval '2-7' year to month *2  from emp group by
experience + interval '2-7' year to month *2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a02s9""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Select hire_date from emp group by
hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s1""")
    
    stmt = """Select hire_date + 2 from emp group by
hire_date + 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s2""")
    
    stmt = """Select hire_date - 3 from emp group by
hire_date - 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s3""")
    
    stmt = """select hire_date + interval '1' day from emp group by
hire_date + interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s4""")
    
    stmt = """select hire_date + interval '2' month from emp group by
hire_date + interval '2' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s5""")
    
    stmt = """select hire_date + interval '4' year from emp group by
hire_date + interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s6""")
    
    stmt = """select hire_date + interval '4-2' year to month from emp group by
hire_date + interval '4-2' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s7""")
    
    stmt = """select hire_date - interval '20' day from emp group by
hire_date - interval '20' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s8""")
    
    stmt = """select hire_date - interval '9' month from emp group by
hire_date - interval '9' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s9""")
    
    stmt = """select hire_date - interval '7' year from emp group by
hire_date - interval '7' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s10""")
    
    stmt = """select hire_date - interval '3-5' year to month from emp group by
hire_date - interval '3-5' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a03s11""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Select start_time + 2 from emp group by
start_time + 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s1""")
    
    stmt = """Select start_time - 5 from emp group by
start_time - 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s2""")
    
    stmt = """select start_time + interval '1' hour from emp group by
start_time + interval '1' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s3""")
    
    stmt = """select start_time + interval '5' minute from emp group by
start_time + interval '5' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s4""")
    
    stmt = """select start_time + interval '9' second from emp group by
start_time + interval '9' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s5""")
    
    stmt = """select start_time + interval '4:20' hour to minute from emp group by
start_time + interval '4:20' hour to minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s6""")
    
    stmt = """select start_time + interval '4:20:30' hour to second from emp group by
start_time + interval '4:20:30' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s7""")
    
    stmt = """select start_time - interval '9' hour from emp group by
start_time - interval '9' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s8""")
    
    stmt = """select start_time - interval '40' minute from emp group by
start_time - interval '40' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s9""")
    
    stmt = """select start_time - interval '90' second from emp group by
start_time - interval '90' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s10""")
    
    stmt = """select start_time - interval '9:45' hour to minute from emp group by
start_time - interval '9:45' hour to minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s11""")
    
    stmt = """select start_time - interval '2:40:56' hour to second from emp group by
start_time - interval '2:40:56' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a04s12""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Select end_time + 1 from emp group by
end_time + 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s1""")
    
    stmt = """Select end_time - 10 from emp group by
end_time - 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s2""")
    
    stmt = """Select end_time + interval '1-01' year to month from emp group by
end_time + interval '1-01' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s3""")
    
    stmt = """Select end_time + interval '1:01:12' hour to second from emp group by
end_time + interval '1:01:12' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s4""")
    
    stmt = """Select end_time - interval '3-09' year to month from emp group by
end_time - interval '3-09' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s5""")
    
    stmt = """Select end_time - interval '7:49:19' hour to second from emp group by
end_time - interval '7:49:19' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a05s6""")
    
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Select hire_date + experience from emp group by
hire_date + experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s1""")
    
    stmt = """Select hire_date - experience from emp group by
hire_date - experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s2""")
    
    stmt = """Select hire_date + 2 - experience + 1  from emp group by
hire_date + 2 - experience + 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a06s3""")
    
    _testmgr.testcase_end(desc)

def test007(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Select experience*2 from emp group by
experience*2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s1""")
    
    stmt = """Select experience/2 from emp group by
experience/2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s2""")
    
    stmt = """Select hire_date + experience from emp group by
hire_date + experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s3""")
    
    stmt = """Select hire_date - experience from emp group by
hire_date - experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s4""")
    
    stmt = """Select experience + hire_date from emp group by
experience + hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s5""")
    
    stmt = """Select experience + end_time from emp group by
experience + end_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s6""")
    
    stmt = """Select end_time + experience from emp group by
end_time + experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s7""")
    
    stmt = """Select end_time - experience from emp group by
end_time - experience;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a07s8""")
    
    _testmgr.testcase_end(desc)

def test008(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Select hire_date - experience - 9 from emp group by
hire_date - experience - 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a08s1""")
    
    stmt = """Select experience + hire_date + (2 * 3)  from emp group by
experience + hire_date + (2 * 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a08s2""")
    
    stmt = """Select ( experience +  3) + ( end_time + 2 ) from emp group by
( experience +  3) + ( end_time + 2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a08s3""")
    
    stmt = """Select ( end_time - 1 ) + ( 2 + experience ) from emp group by
( end_time - 1 ) + ( 2 + experience );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a08s4""")
    _testmgr.testcase_end(desc)

