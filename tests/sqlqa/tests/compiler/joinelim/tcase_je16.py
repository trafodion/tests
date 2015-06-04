# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# =================  Begin Test Case Header  ==================
#
#  Description:        Constant folding and no-op situations.
#
#  Purpose:            Verify that boolean expressions are appropriately
#                      simplified when folded constants result in subexpressions
#                      that can be evaluated at compile time.
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""true and true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a from tconst where 2=2 and 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test002(desc="""true and false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a from tconst where 1=1 and 1=2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test003(desc="""true and unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a from tconst where 1=1 and a=2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (')
    
    _testmgr.testcase_end(desc)

def test004(desc="""false and true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 and 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test005(desc="""false and false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 and 2>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test006(desc="""false and unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 and a>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test007(desc="""unknown and true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 and 11>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (')
    
    _testmgr.testcase_end(desc)

def test008(desc="""unknown and false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 and 11>12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test009(desc="""unknown and unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 and a<12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (')
    
    _testmgr.testcase_end(desc)

def test010(desc="""true or true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=2 or 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test011(desc="""true or false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 1=1 or 1=2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test012(desc="""true or unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 1=1 or a=2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test013(desc="""false or true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 or 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test014(desc="""false or false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 or 2>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test015(desc="""false or unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where 2=3 or a>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (')
    
    _testmgr.testcase_end(desc)

def test016(desc="""unknown or true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 or 11>10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test017(desc="""unknown or false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 or 11>12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (')
    
    _testmgr.testcase_end(desc)

def test018(desc="""unknown or unknown"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from select a from tconst where a>3 or a<12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates ....')
    
    _testmgr.testcase_end(desc)

def test019(desc="""complex expr evaluates to true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # The Where clause for this query can be evaluated as TRUE without reference
    # to any column values, but is not handled by the current constant folding
    # algorithm. If the algorithm is extended to handle this case, the commented
    # #unexpect line for the "explain s" should be used instead of the one used now.
    stmt = """prepare s from
select a from tconst
where ((a=1 or 1=1) and (2=2 or a<10)) or (a>7 and a<20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #tabtype MODE_SPECIAL_1
    # EXPLAIN generates two line output
    #  executor_predicates .... (  16777216. or (A >=      ...8) and (A <=
    #                           19))
    # If it maches the following line, assume it is correct.
    #endtt
    
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test020(desc="""complex expression evaluates to false"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from
select a from tconst
where ((a=1 or 1=1) and (2=3 and a<10)) and (a>7 and a<20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test021(desc="""folded constant containing arithmetic expressions causes where clause to be true"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s
from select a from tconst
where a>3 or 2*25+10 > 100/2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'executor_predicates')
    
    _testmgr.testcase_end(desc)

def test022(desc="""folded constant containing arithmetic expressions evaluates to false and is dropped"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s
from select a from tconst
where a>3 or 2*25+10 < 100/2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (A > 3')
    
    _testmgr.testcase_end(desc)

def test023(desc="""partial evaluation"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from
select a from tconst
where ((a=1 or 1=1) and (sqrt(a)>3 and a<10)) or (a>7 and 20<20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... (sqrt(cast(A)) > cast(3)) and (A < 10')
    
    _testmgr.testcase_end(desc)

def test024(desc="""constant bool expression and nested query"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Constant folding is not applied in time to prevent a nested query from being
    # part of the plan, and there is currently no conditional evaluation of OR/AND.
    stmt = """prepare s from select * from tconst where 1=1 or a in (select b from tconst);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'nested_join')
    
    _testmgr.testcase_end(desc)

