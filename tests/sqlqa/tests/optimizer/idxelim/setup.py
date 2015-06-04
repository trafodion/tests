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


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)

    output = _dci.cmdexec("""drop table lineitem cascade;""")

    stmt = """create table lineitem
like """ + gvars.g_schema_tpch2x + """.lineitem
with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into lineitem
select * from """ + gvars.g_schema_tpch2x + """.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '11997996')

    stmt = ("""update statistics for table lineitem """ +
            """on every column sample random 10 percent;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table lineitem on existing column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""drop table cmptimes;""")
    stmt = """create table cmptimes(
        qryid varchar(4) not null primary key,
        cmptime_cqdon numeric(8,6),
        cmptime_cqdoff numeric(8,6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """prepare check_idx_scan from
select substr(description, strt, 150)
from (select description, locate('scan_type', description) as strt
from table(explain(NULL,'XX'))
where operator = 'TRAFODION_INDEX_SCAN') t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    output = _dci.cmdexec("""set param ?qid 'zz';""")
    stmt = """prepare check_cmptime from
select case when cmptime_cqdon < cmptime_cqdoff
then 'PASS' else 'FAIL' end from cmptimes
where qryid = ?qid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """cqd QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # workaround for lp bug 1409937
    stmt = """cqd CACHE_HISTOGRAMS 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """cqd CACHE_HISTOGRAMS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

def drop_idxs():
    global _testmgr
    global _testlist
    global _dci

    output = _dci.cmdexec("""drop index idx1;""")
    output = _dci.cmdexec("""drop index idx2;""")
    output = _dci.cmdexec("""drop index idx3;""")
    output = _dci.cmdexec("""drop index idx4;""")
    output = _dci.cmdexec("""drop index idx5;""")
    output = _dci.cmdexec("""drop index idx6;""")
    output = _dci.cmdexec("""drop index idx7;""")
    output = _dci.cmdexec("""drop index idx8;""")
    output = _dci.cmdexec("""drop index idx9;""")
    output = _dci.cmdexec("""drop index idx10;""")
