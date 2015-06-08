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
import setup

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dbrootdci = _testmgr.get_dbroot_dci_proc()


def test_autostats(desc="""auto update stats options"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist):
        return

    output = _dbrootdci.cmdexec("""set param ?t 'TBLZ';""")

    stmt = """prepare XX from select * from tblz
where colc between 600000 and 600500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLC)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLA)*""")
    _dci.unexpect_any_substr(output, """*(COLB)*""")
    _dci.unexpect_any_substr(output, """*(COLD)*""")
    _dci.expect_prepared_msg(output)

    stmt = """prepare XX from update tblz
set (colkey1, cola, colc) = (-colkey1, 50000, colkey1)
where colkey1 between 1000000 and 1999999
and mod(cola, 2) = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLB)*""")
    _dci.unexpect_any_substr(output, """*(COLC)*""")
    _dci.unexpect_any_substr(output, """*(COLD)*""")
    #_dci.expect_updated_msg(output, '20000')
    _dci.expect_prepared_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_selected_msg(output, '5')
    output = _dbrootdci.cmdexec("""execute reason_blank;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    # with on-nec-col, sample clause is applicable
    stmt = """update statistics for table tblz
on necessary columns sample random 20 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_selected_msg(output, '5')
    output = _dbrootdci.cmdexec("""execute reason_I;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    output = _dbrootdci.cmdexec("""execute show_sample;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 2000""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 2000""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 2000""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 2000""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 2000""")
    _dbrootdci.expect_selected_msg(output, '5')

    stmt = """showstats for table tblz on existing columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, "* 5000000 * 5000000 COLKEY1")
    _dci.expect_any_substr(output, "* 5000000 * 10000 COLKEY2")
    _dci.expect_any_substr(output, "* 5000000 * 5000000 COLA")
    _dci.expect_any_substr(output, "* 5000000 * 5000000 COLC")
    _dci.expect_any_substr(output, """* 5000000 * 13 \"_SALT_\"""")
    _dci.expect_complete_msg(output)

    stmt = """ update statistics for table tblz clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """prepare XX from insert into tblz
select -colkey1, cola, colb, -colkey2, colkey1, NULL
from tblz where colkey2 > 500000 and colkey2 < 709999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLA)*""")
    _dci.unexpect_any_substr(output, """*(COLB)*""")
    _dci.unexpect_any_substr(output, """*(COLC)*""")
    _dci.unexpect_any_substr(output, """*(COLD)*""")
    _dci.expect_prepared_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.unexpect_any_substr(output, """*COLA*""")
    _dbrootdci.unexpect_any_substr(output, """*COLB*""")
    _dbrootdci.unexpect_any_substr(output, """*COLC*""")
    _dbrootdci.unexpect_any_substr(output, """*COLD*""")
    _dbrootdci.expect_selected_msg(output, '3')
    output = _dbrootdci.cmdexec("""execute reason_blank;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """prepare XX from select cola, colb from tblz
where colkey2 = 700000 and colc is NULL
group by cola, colb order by cola;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLB)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLC)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6010]*(COLA, COLB)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLD)*""")
    _dci.expect_prepared_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLB * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.unexpect_any_substr(output, """*COLD*""")
    _dbrootdci.expect_selected_msg(output, '8')
    output = _dbrootdci.cmdexec("""execute reason_blank;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    # with on-nec-col, sample clause is applicable
    stmt = """update statistics for table tblz
on necessary columns sample 200000 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLB * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.unexpect_any_substr(output, """*COLD*""")
    _dbrootdci.expect_selected_msg(output, '8')
    output = _dbrootdci.cmdexec("""execute reason_I;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    output = _dbrootdci.cmdexec("""execute show_sample;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 400""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 400""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 400""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLA * 400""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLB * 400""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 400""")
    _dbrootdci.unexpect_any_substr(output, """*COLD*""")
    _dbrootdci.expect_selected_msg(output, '8')

    stmt = """showstats for table tblz on existing columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """* 5000000 * COLKEY1""")
    _dci.expect_any_substr(output, """* 5000000 * COLKEY2""")
    _dci.expect_any_substr(output, """* 5000000 * \"_SALT_\"""")
    _dci.expect_any_substr(output, """* 5000000 * COLA""")
    _dci.expect_any_substr(output, """* 5000000 * COLB""")
    _dci.expect_any_substr(output, """* 5000000 * COLC""")
    _dci.expect_any_substr(output, """* 5000000 * COLA, COLB""")
    _dci.unexpect_any_substr(output, """*COLD*""")

    stmt = """ update statistics for table tblz clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = ("""prepare XX from delete from tblz where mod(colc, 9) = 0 and"""
            + """ colkey1 between 2000 and 3000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLC)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLA)*""")
    _dci.unexpect_any_substr(output, """*(COLB)*""")
    _dci.unexpect_any_substr(output, """*(COLD)*""")
    _dci.expect_prepared_msg(output)

    stmt = """prepare XX from select colkey2, colc, cold from tblz
where colkey2 > 3000 and cold is NULL
group by colc, colkey2, cold order by colc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLC)*TBLZ""")
    _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLZ""")
    _dci.unexpect_any_substr(output, """*(COLA)*""")
    _dci.unexpect_any_substr(output, """*(COLB)*""")
    _dci.expect_prepared_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLD * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0""")
    _dbrootdci.unexpect_any_substr(output, "*COLA*")
    _dbrootdci.unexpect_any_substr(output, "*COLB*")
    _dbrootdci.expect_selected_msg(output, '8')
    output = _dbrootdci.cmdexec("""execute reason_blank;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    # with on-nec-col, sample clause is applicable
    stmt = """update statistics for table tblz
on necessary columns sample;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLD * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 0001-01-01 00:00:00 * 0 I""")
    _dbrootdci.unexpect_any_substr(output, "*COLA*")
    _dbrootdci.unexpect_any_substr(output, "*COLB*")
    _dbrootdci.expect_selected_msg(output, '8')
    output = _dbrootdci.cmdexec("""execute reason_I;""")
    _dbrootdci.expect_str_token(output, 'PASS')

    output = _dbrootdci.cmdexec("""execute show_sample;""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY1 * 99""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLKEY2 * 99""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLC * 99""")
    _dbrootdci.expect_any_substr(output, """TBLZ.COLD * 99""")
    _dbrootdci.expect_any_substr(output, """TBLZ._SALT_ * 99""")
    _dbrootdci.unexpect_any_substr(output, "*COLA*")
    _dbrootdci.unexpect_any_substr(output, "*COLB*")
    _dbrootdci.expect_selected_msg(output, '8')

    stmt = """showstats for table tblz on existing columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """* 5000000 * COLKEY1""")
    _dci.expect_any_substr(output, """* 5000000 * COLKEY2""")
    _dci.expect_any_substr(output, """* 5000000 * COLC""")
    _dci.expect_any_substr(output, """* 5000000 * COLD""")
    _dci.expect_any_substr(output, """* 5000000 * \"_SALT_\"""")
    _dci.expect_any_substr(output, """* 5000000 * COLKEY2, COLC, COLD""")
    _dci.unexpect_any_substr(output, "*COLA*")
    _dci.unexpect_any_substr(output, "*COLB*")
    _dci.expect_complete_msg(output)

    stmt = """ update statistics for table tblz clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
