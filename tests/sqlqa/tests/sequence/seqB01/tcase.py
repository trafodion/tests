# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import time
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


# ---------------------------------------------------------
#testcase test001 CREATE SEQUENCE default success
# ---------------------------------------------------------
def test001(desc="""CREATE SEQUENCE default success"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop sequence b_seq;"""
    output = _dci.cmdexec(stmt)

    # create sequence default 
    stmt = """create sequence b_seq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence b_seq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQB01.B_SEQ""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    stmt = """alter sequence b_seq increment by 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence b_seq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQB01.B_SEQ""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 10""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""") 
    _dci.expect_any_substr(output, """;""")
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'SEQUENCE_SEQB01.B_SEQ')

    stmt = """get sequences in schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'B_SEQ')

    stmt = """select seqnum(b_seq, current) from (values(1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s5')

    stmt = """select seqnum(b_seq, next) from (values(1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s6')

    stmt = """drop sequence b_seq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
 # ------------------------------------------------------------------------
