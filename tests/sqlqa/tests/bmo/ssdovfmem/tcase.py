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

import os
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
	
def test001(desc="""m01"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='m01'	

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			inner join D01 on D01.pk=F01.fk_d01
			inner join D02 on D02.pk=F01.fk_d02
			left join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test002(desc="""m05"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='m05'	

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 5] T01.val02, T02.val02
			from
			(
			Select F01.val02, D01.val01
			From F01
			right join D01 on D01.pk=F01.fk_d01
			where D01.val01>0
			) as T01(val01,val02)
			right join
			(
			Select F02.val01, F02.val02
			From F02
			where not exists
			(select val01
			 from D02
			 where D02.val02=F02.fk_d02
			)
			) as T02(val01,val02)
			on (T01.val02=T02.val01)
			where T02.val01>0
			order by 1,2
			;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, ' EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test003(desc="""b21"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b21'	

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			inner join D01 on D01.pk=F01.fk_d01
			left join D02 on D02.pk=F01.fk_d02
			inner join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test004(desc="""b23"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b23'

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			left join D01 on D01.pk=F01.fk_d01
			inner join D02 on D02.pk=F01.fk_d02
			left join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')


	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

#def test005(desc="""b24"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	id='b24'
#
#	stmt = """set schema """ + defs.w_catalog + """.g_tpch2x;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """prepare xx from 
#			select[first 50]* from customer, nation, lineitem, orders where c_nationkey = n_nationkey and c_custkey = o_custkey and l_orderkey = o_orderkey order by 1,2,4,5,6;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_prepared_msg(output)
#
#	stmt = """explain options 'f' xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """explain xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """execute xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output, '50')
#
#	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid current progress;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
#	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
#	
#	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid """ + qid + """ default;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """ accumulated;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	stmt = """select variable_info from
#			  table(statistics(NULL,'QID=""" + qid + """'));"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'Id TDB Name')
#	_dci.expect_any_substr(output, 'EX_SORT')
#	_dci.expect_any_substr(output, 'EX_ HASHJ')
#
#
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'MMAP')
#
#	_testmgr.testcase_end(desc)
#
#def test006(desc="""b25"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	id='b25'	
#
#	stmt = """prepare xx from 
#			select[first 20]* from customer, nation, lineitem, orders where c_nationkey = n_nationkey and c_custkey = o_custkey and l_orderkey = o_orderkey order by o_orderkey,c_custkey,o_custkey,c_name;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_prepared_msg(output)
#
#	stmt = """explain options 'f' xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """explain xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """execute xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output, '20')
#
#	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid current progress;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
#	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
#	
#	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid """ + qid + """ default;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """ accumulated;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	stmt = """select variable_info from
#			  table(statistics(NULL,'QID=""" + qid + """'));"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'Id TDB Name')
#	_dci.expect_any_substr(output, 'EX_SORT')
#	_dci.expect_any_substr(output, 'EX_ HASHJ')
#
#
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'MMAP')
#
#	_testmgr.testcase_end(desc)
#
#def test007(desc="""m03"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	id='m03'
#
#	stmt = """set schema """ + defs.w_catalog + """.g_tpch2x;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """prepare xx from 
#			select [last 1] * from lineitem order by l_orderkey,l_linenumber for read uncommitted access;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_prepared_msg(output)
#
#	stmt = """explain options 'f' xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """explain xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """execute xx;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output, '1')
#
#	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid current progress;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
#	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
#	
#	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """get statistics for qid """ + qid + """ default;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """get statistics for qid """ + qid + """ accumulated;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
#	output = _dci.cmdexec(stmt)
#	stmt = """select variable_info from
#			  table(statistics(NULL,'QID=""" + qid + """'));"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """log off;"""
#	output = _dci.cmdexec(stmt)
#	
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'Id TDB Name')
#	_dci.expect_any_substr(output, 'EX_SORT')
#
#	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
#	_dci.expect_any_substr(output, 'MMAP')
#
#	_testmgr.testcase_end(desc)
