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

from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None

#             Update Statistics Testunit -- STAT100
#
#    This testunit contains functional tests for update statistics syntax.
#
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
    
def test001(desc="""Check HIST* objects"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return

    # check automatic creation of hist* objects
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """invoke """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """invoke """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table btpns13 on every column,(varchar1_2),
(sbin1_500,varchar0_20,char1_uniq),
(varchar1_2,char0_20,char1_uniq,sdec0_uniq,sdec1_100,sbin1_500,udec0_4,sbin0_uniq,
ubin0_20,varchar0_20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # look at histogram table information in objects table
    # #expectfile $test_dir/A001${release_str} A0S01
    # dfm has problem in matching. it emits mismatch eventhough the result is matching.
    # so modifying the exp result to expect only the number of rows.
    if hpdci.tgtSQ():
        stmt = """select object_name, object_name_space, object_type, object_security_class
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where object_name like '%HIST%'
order by object_name;"""
    elif hpdci.tgtTR():
        stmt = """select object_name, object_type
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where object_name like '%HIST%'
order by object_name;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # there should be 1 histogram record for every time the column is mentioned above, except
    # for the lone column
    
    stmt = """select object_name,  column_number, interval_count, rowcount, object_uid
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%'
order by object_name, column_number, object_uid;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 23)
    
    stmt = """select object_name, interval_number, interval_rowcount, interval_uec,
interval_boundary from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Update Statistics based on various column syntax"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    # update statistics for every other (single) column
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table btpwl10 on
(udec0_2000), ( sdec0_uniq ), ( char0_1000 ), ( sbin1_100), ( udec1_10 ), ( sdec1_2 ),
(ubin2_4), ( char2_2), ( sbin3_1000), ( char3_1000), ( ubin3_uniq), ( ubin4_4), ( sdec4_10), ( sbin5_4),
(udec5_20), ( sdec5_100), ( sdec6_2000), ( char6_20), ( sbin7_2), ( char7_uniq), ( ubin7_100),
(char8_500), ( sdec8_2000), ( ubin8_2), ( char9_uniq), ( sdec9_20), ( sbin10_uniq), ( char10_20),
(sdec10_500), ( sdec11_20), ( ubin11_2), ( sbin12_1000), ( char12_10), ( udec12_1000), ( sbin13_uniq),
(udec13_500), ( ubin14_2), ( udec14_10), ( sbin15_2), ( varchar15_uniq),
(sdec15_10), ( sdec16_100), ( udec16_1000), ( sbin17_uniq), ( ubin17_2000),
(udec17_100), ( char18_20), ( sdec18_4), ( sbin19_4), ( ubin19_10), ( sdec19_1000), ( udec20_uniq),
(char20_10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPWL10%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 53)
    
    # clear subset of columns
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpwl10 on
(udec0_2000), ( sdec0_uniq ), ( char0_1000 ), ( sbin1_100), ( udec1_10 ), ( sdec1_2 ),
(udec5_20), ( sdec5_100), ( sdec6_2000), ( char6_20), ( sbin7_2), ( char7_uniq), ( ubin7_100),
(sdec10_500), ( sdec11_20), ( ubin11_2), ( sbin12_1000), ( char12_10), ( udec12_1000), ( sbin13_uniq),
(udec17_100), ( char18_20), ( sdec18_4), ( sbin19_4), ( ubin19_10), ( sdec19_1000), ( udec20_uniq),
(char20_10) clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9202')
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPWL10%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 25)
    
    # clear all columns
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpwl10 on every column clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPWL10%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
    
    # update statistics for multiple column stats
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on
(char0_20, varchar1_2),
(sdec0_uniq, char1_uniq, varchar0_20),
(sdec1_100, ubin0_20, sbin1_500, sbin0_uniq, udec0_4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 20)
    
    # update statistics for duplicate columns
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21 on
(char1_20),
(sbin1_100, varchar1_4, char1_20),
(char1_20),
(char0_10, sdec0_10, varchar0_uniq, char1_20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, colcount, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNL21%'
order by column_number, colcount;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 13)
    
    # clear statistics on multi-column statistics only
    
    ##expect any *SQL operation complete.*
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21 on
(sbin1_100, varchar1_4, char1_20),
(char0_10, sdec0_10, varchar0_uniq, char1_20) clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9202')
    
    ##expect any *1 row(s) selected*
    stmt = """select object_name,  column_number, colcount, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNL21%'
order by column_number, colcount;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # use every column
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS01%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 10)
    
    # use "column to column" syntax
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pwl28 on
(int0_ytom_uniq) to (sdec2_500),
(udec3_n100)     to (time4_1000),
(dt16_m_n10)     to (char17_2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PWL28%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 32)
    
    # do backwards "to" range
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pwl28 on
(ts14_n100) to (udec14_100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9202')
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PWL28%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 36)
    
    # specify no column.  in mxobjects, it will update eof, indexlevels, nonempty blockcount
    # no rows are inserted in histogrm or histints
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9213')
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS03%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
   
    if hpdci.tgtSQ(): 
        stmt = """select non_empty_block_count, eof, index_level
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.partitions p, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects o
where p.object_uid = o.object_uid
and o.object_name like '%B2PNS03%';"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    # physical statistics shouldn't change when column done
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns03 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select non_empty_block_count, eof, index_level
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.partitions p, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects o
where p.object_uid = o.object_uid
and o.object_name like '%B2PNS03%';"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    # clear shouldn't affect physical statistics either
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns03 on every column clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select non_empty_block_count, eof, index_level
from """ + defs.w_catalog + """.""" + gvars.definition_schema + """.partitions p, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects o
where p.object_uid = o.object_uid
and o.object_name like '%B2PNS03%';"""
        output = _dci.cmdexec(stmt)
        _dci.unexpect_error_msg(output)
    
    # update statistics on empty table
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2empty on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2EMPTY%'
order by column_number desc, rowcount desc;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # clear statistics on empty table
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2empty on every column clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2EMPTY%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
    
    # update statistics on multi-column, specifying non-existent column
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table """ + defs.my_schema + """.b2pwl30 on
(char13_1000, varchar0_n1000), (int1_ytom_100, int99_ytom_100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9209')
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PWL30%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Update statistics based on interval specification"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    # generate 10 intervals
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on every column
generate 10 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select cast(object_name as char(20)), column_number, colcount, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%'
order by colcount, column_number;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # generate 1 interval
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on every column
generate 1 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # generate on empty table
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2empty on every column
generate 25 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select cast(object_name as char(20)), column_number, colcount, rowcount
from """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2EMPTY%'
order by column_number, colcount;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # use negative number for generate
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21
on (varchar1_4), (sdec0_10) generate -5 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')
    
    # use too big
    # 12/07/05: As of mx1128, max generate interval is 10000
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21
on (varchar1_4), (sdec0_10) generate 10001 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')
    
    # use too big float
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21
on (varchar1_4), (sdec0_10) generate 2.1E5 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Update statistics with sample option"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    # use default sampling (2%
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pwl34 on
(INT17_Y_N10),
(TS13_UNIQ)
sample;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select cast(object_name as char(20)),  column_number, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PWL34%'
order by column_number;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # use explicit sample 4E2
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns09 on
(dt1_mtoh_n20), (real1_uniq), (char0_100)
sample 4E2 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS09%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 3)
    
    # use int sample value
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample 456 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # use no sample value
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample  rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # use sample without column list
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
sample 10 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Update statistics with rowcount option"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns09 on
(dt1_mtoh_n20), (time0_nuniq), (char0_100), (int0_dtof6_n100), (udec1_2),
(int1_h_n10), (sbin0_100), (sdec0_nuniq)
sample 4E2 rows set rowcount 1.5E3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS09%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 8)
    
    # clear table
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns09 on every column clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS09%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
   
    stmt = """select count(*) from """ + defs.my_schema + """.b2pns09;"""
    output = _dci.cmdexec(stmt)
 
    # try with rowcount much greater than table
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns09 on
(dt1_mtoh_n20), (time0_nuniq), (char0_100), (int0_dtof6_n100), (udec1_2),
(int1_h_n10), (sbin0_100), (sdec0_nuniq)
sample 1.5E3 rows set rowcount 1.5E8;"""
    output = _dci.cmdexec(stmt)
    # On Trafodion, it sometimes returns 9207 when the SAMPLE option 
    # generates an empty sample set.
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
 
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2pns09 on
(dt1_mtoh_n20), (time0_nuniq), (char0_100), (int0_dtof6_n100), (udec1_2),
(int1_h_n10), (sbin0_100), (sdec0_nuniq);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS09%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 8)
    
    # try rowcount without sample
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column set rowcount 4E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # make sure no rows exist for failed command
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%B2PNS09%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 8)
    
    # try negative number
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample set rowcount -4E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')
    
    # try integer number
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample set rowcount 4000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #try sample size greater than rowcount
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample 4E3 rows set rowcount 1E3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')
    
    #try sample size equal to rowcount
    ##expect any *--- SQL operation complete.*
    stmt = """update statistics for table """ + defs.my_schema + """.b2uns01
on every column sample 1E3 rows set rowcount 1E3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Update statistics with clear option"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    # clear on table with no stats
    stmt = """update statistics for table """ + defs.my_schema + """.btpnl21 on every column clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(object_name as char(20)),  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNL21%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output, 0)
    
    # lots of columns cleared in testcase #A1, A4
    # subset of columns cleared in testcase #A1
    # statistics on empty table cleared in testcase #A1
    # statistics on multi-column cleared in testcase #A1
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Update statistic multiple times on same table"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(object_name as char(20)),  column_number, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # do it again, expect same results, use same result file
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select cast(object_name as char(20)),  column_number, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    # do it with fewer columns, expect different results
    
    stmt = """update statistics for table """ + defs.my_schema + """.btpns13 on
(varchar0_20),
(char1_uniq,varchar1_2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9202')
    
    stmt = """select cast(object_name as char(20)),  column_number, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%BTPNS13%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Try to update non-user objects or non-objects"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """update statistics for table """ + defs.w_catalog + """.""" + gvars.definition_schema + """.tbl_constraints on
(disabled),
(droppable),
(constraint_type);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output, '4082')
 
    # update statistics for edit file
    stmt = """update statistics for table """ + defs.my_schema + """.faketab on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # update statistics for non-existent file
    stmt = """update statistics for table """ + defs.my_schema + """.notab on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""Tests added in response to CRs"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table """ + defs.my_schema + """.t2 (c1 int, rowcount int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + defs.my_schema + """.t2 values (1,2),(2,3),(3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update statistics for table """ + defs.my_schema + """.t2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table """ + defs.my_schema + """.t2 on (rowcount);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '9202')
    
    stmt = """select object_name,  column_number, interval_count, rowcount
from  """ + defs.my_schema + """.""" + gvars.histograms + """, """ + defs.w_catalog + """.""" + gvars.definition_schema + """.objects
where table_uid = object_uid and
object_name like '%T2%';"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)
    stmt = """update statistics for table """ + defs.my_schema + """.t2 on (fakename);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9209')
    
    stmt = """update statistics for table """ + defs.my_schema + """.b2uwl16 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *row(s) deleted*
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    ##expect any *row(s) deleted*
    stmt = """delete from """ + defs.my_schema + """.""" + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""Tests for fixes"""):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table "test5" ("a" int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into "test5" values (1,2),(3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """update statistics for table "test5" on ("a"),(b), ("a",b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """drop table "test5";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

