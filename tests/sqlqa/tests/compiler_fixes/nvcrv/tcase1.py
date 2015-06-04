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

# Description: This test verifies
#  Subquery select from view gets error 4018
#  Test case inputs:  .
#  Test case outputs:
#  History:  Created on 07/12/2006
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Subquery select from view gets error 4018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table a1(i  int not null not droppable,c char(5),d varchar(5), primary key(i)) attributes extent (16,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view av1(v1,v2) as select i,c from a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare xx from select (select v1 from av1 group by v1) from a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """prepare xx from select(select * from av1 group by v1) from a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4012')
    
    stmt = """prepare xx from select (select V2 from av1 group by v2 ) from a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select (select V2 from av1 group by v2 ) from a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select count(select i from a1 group by i) from av1 group by v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select (select i from a1 group by i),(select v1 from av1 group by v1) from av1 group by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select (select i from a1 group by i),(select c from a1 group by c),(select d from a1 group by d) from av1 group by v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select (select i from a1 group by i),(select c from a1 group by c),(select d from a1 group by d) from av1 group by v1
union select (select i from a1 group by i),(select c from a1 group by c),(select d from a1 group by d) from av1 group by v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select (select i from a1 group by i),(select v1 from av1 group by v1) from av1 group by v2 union all
select (select i from a1 group by i),(select v1 from av1 group by v1) from av1 group by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select (select i from a1 group by i),(select v1 from av1 group by v1) from av1 group by v2 union all
select (select i from a1 group by i),(select v1 from av1 group by v1) from av1 order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select (select i from a1 group by i),(select v1 from av1 group by v1) from a1 group by i union
select (select i from a1 group by i),(select v1 from av1 group by v1) from a1 FOR READ UNCOMMITTED ACCESS order by 2 ascending ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '3192')
    
    _testmgr.testcase_end(desc)

