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
import time
import setup

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

    # notes: cqd index_elimination_level 'maximum'; --disables feature


def verifyIndex(stmt, qryid, expidx):
    global _testmgr
    global _testlist
    global _dci

    checkPlan4Index(stmt, qryid, expidx, 'AGGRESSIVE')
    checkPlan4Index(stmt, qryid, expidx, 'MAXIMUM')
    output = _dci.cmdexec("""set param ?qid """ + qryid + """;""")
    #stmt = ("""select case when cmptime_cqdon < cmptime_cqdoff""" +
    #        """ then 'PASS' else 'FAIL' end""" +
    #        """ from cmptimes where qryid = '""" + qryid + """';""")
    stmt = """execute check_cmptime;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'PASS')


def checkPlan4Index(stmt, qryid, expidx, cqdval=None):
    global _testmgr
    global _testlist
    global _dci

    if cqdval == 'AGGRESSIVE':
        output = _dci.cmdexec("cqd INDEX_ELIMINATION_LEVEL reset;")
    else:
        output = _dci.cmdexec("cqd INDEX_ELIMINATION_LEVEL '" + cqdval + "';")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    if cqdval == 'AGGRESSIVE':
        output = _dci.cmdexec("""explain options 'f' XX;""")
        #_dci.expect_any_substr(output, """trafodion_index_scan%""" + expidx)
        output = _dci.cmdexec("""execute check_idx_scan;""")
        _dci.expect_any_substr(output, expidx)
        #output = _dci.cmdexec("""explain XX;""")

    output = _dci.cmdexec("""get statistics;""")
    _dci.expect_complete_msg(output)
    found = False
    for line in output.splitlines():
        if line.startswith('Compile Time'):
            found = True
            token = line.split(':')
            try:
		if int(token[1]) != 0:
                    raise ValueError("Excessive Compile Time")
            except ValueError as e:
                _testmgr.mismatch_record(e)

            CompileTime = token[2]
            if cqdval == 'AGGRESSIVE':
                mystmt = ("""insert into""" +
                          """ cmptimes(qryid, cmptime_cqdon)""" +
                          """ values ('""" + qryid + """', """ +
                          CompileTime + """);""")
                myoutput = _dci.cmdexec(mystmt)
                _dci.expect_inserted_msg(myoutput, '1')
            else:
                mystmt = ("""update cmptimes""" +
                          """ set cmptime_cqdoff = """ +
                          CompileTime + """ where qryid = '""" +
                          qryid + """';""")
                myoutput = _dci.cmdexec(mystmt)
                _dci.expect_updated_msg(myoutput, '1')
    if not found:
        _testmgr.mismatch_record("Compile Time not found")


def test_1heuristics(desc="""use idx that provides max coverage of pred"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_1heuristics"""

    # use index that provides the maximum coverage of the predicate.
    # do this only when the output from one index is the super-set of
    # the other.
    setup.drop_idxs()

    stmt = """create index idx1
on lineitem(l_partkey, l_suppkey, l_quantity)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx2
on lineitem(l_partkey, l_suppkey)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx3
on lineitem(l_partkey, l_quantity)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx4
on lineitem(l_partkey)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx5
on lineitem(l_suppkey)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx6
on lineitem(l_quantity)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx7
on lineitem(l_receiptdate, l_extendedprice)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx8
on lineitem(l_receiptdate)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx9
on lineitem(l_extendedprice)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234 and l_partkey = 21284;"""
    verifyIndex(stmt, '1a', 'IDX4')

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234 and l_quantity = 7;"""
    verifyIndex(stmt, '1b', 'IDX5')

    stmt = """prepare XX from select * from lineitem
where l_partkey = 21284 and l_suppkey = 1234
and l_linenumber = 4;"""
    verifyIndex(stmt, '1c', 'IDX4')

    stmt = """prepare XX from select * from lineitem
where l_partkey = 21284;"""
    verifyIndex(stmt, '1d', 'IDX4')

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234;"""
    verifyIndex(stmt, '1e', 'IDX5')

    output = _dci.cmdexec("""drop index idx4;""")
    _dci.expect_complete_msg(output)

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234 and l_partkey = 21284;"""
    verifyIndex(stmt, '1f', 'IDX3')

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234 and l_quantity = 7;"""
    verifyIndex(stmt, '1g', 'IDX5')

    stmt = """prepare XX from select * from lineitem
where l_partkey = 21284 and l_suppkey = 1234
and l_linenumber = 4;"""
    verifyIndex(stmt, '1h', 'IDX5')

    stmt = """prepare XX from select * from lineitem
where l_suppkey = 1234;"""
    verifyIndex(stmt, '1i', 'IDX5')

    stmt = """prepare XX from select * from lineitem
where l_extendedprice = 5966.73;"""
    verifyIndex(stmt, '1j', 'IDX9')

    stmt = """prepare XX from select * from lineitem
where l_receiptdate = date'1992-01-23';"""
    verifyIndex(stmt, '1k', 'IDX8')

    stmt = """prepare XX from select * from lineitem
where l_receiptdate = date'1992-05-30'
and l_extendedprice = 22661.60;"""
    verifyIndex(stmt, '1l', 'IDX9')

    _testmgr.testcase_end(desc)


def test_2heuristics(desc="""choose index with higher selectivity"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """test_2heuristics"""

    # if no index is a prefix of the other and the two do not produce
    # same output, pick one with higher selectivity.
    setup.drop_idxs()

    stmt = """create index idx1 on lineitem(l_orderkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx2 on lineitem(l_partkey) salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx3 on lineitem(l_suppkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx4 on lineitem(l_linenumber) salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx5 on lineitem(l_quantity);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx6 on lineitem(l_extendedprice)
salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx7 on lineitem(l_discount);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx8 on lineitem(l_commitdate) salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx9 on lineitem(l_shipmode);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idx10 on lineitem(l_comment) salt like table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # l_commitdate UEC = 2466
    # l_partkey UEC = 400000
    stmt = """prepare XX from select * from lineitem
where l_commitdate = date'1996-01-31' and l_partkey = 4556973;"""
    verifyIndex(stmt, '2a', 'IDX2')

    # l_commitdate UEC = 2466
    # l_discount UEC = 11
    stmt = """prepare XX from select * from lineitem
where l_commitdate = date'1998-12-31' and l_discount = .06;"""
    verifyIndex(stmt, '2b', 'IDX8')

    # l_suppkey UEC = 20000
    # l_extendedprice UEC = 984297
    stmt = """prepare XX from select * from lineitem
where l_suppkey = 9473 and l_extendedprice = 58473.45;"""
    verifyIndex(stmt, '2c', 'IDX6')

    # l_comment UEC = 5136812
    # l_extendedprice UEC = 984297
    stmt = """prepare XX from select * from lineitem
where l_comment = 'unusual accounts a' and l_extendedprice = 58473.45;"""
    verifyIndex(stmt, '2d', 'IDX10')

    output = _dci.cmdexec("""select * from cmptimes order by qryid;""")
    _testmgr.testcase_end(desc)
