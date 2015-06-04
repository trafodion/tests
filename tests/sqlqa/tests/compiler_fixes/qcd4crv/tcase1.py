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
    
def test001(desc="""Checks for Invalid Statistics"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # fix for
    # made table name more complicated so test would perform as written (kk)
    # make definition schema name generic
    
    stmt = """control query default query_cache '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default cache_histograms 'off';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default pos_num_of_partns '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trash1234_qcd4crv (a int not null,
b char(10), c date, d timestamp, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table trash1234_qcd4crv2
(
sbin0_4             Integer                       default 3 not null,
time0_uniq          Time                          not null,
varchar0_uniq       VarChar(8)                    no default not null,
sdec0_n1000         Decimal(9)                    no default,
int0_dTOf6_4        Interval day to second(6)     not null,
ts1_n100            Timestamp     heading 'ts1_n100 allowing nulls',
ubin1_20            Numeric(9) unsigned           no default not null,
int1_yTOm_n100      Interval year(1) to month     no default,
double1_2           Double Precision              not null,
udec1_nuniq         Decimal(4) unsigned           ,
primary key ( time0_uniq  DESC)) attributes extent (16,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into trash1234_qcd4crv values (1,'b',current_date,current_timestamp),
(3,'c',current_date,current_timestamp),(5,'d',current_date,current_timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    # NCI #expect any *Import Completed Successfully*
    # NCI sh import $testcat.$testsch.trash1234_qcd4crv2 -I $popsdata/b2pns03.dat;
    # Not sure how to get around the date time data format problem NVT/import
    # script yet. Let's get the data from the global table for now.
    stmt = """insert into trash1234_qcd4crv2 (select * from """ + gvars.g_schema_sqldpop + """.b2pns03);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """update statistics for table trash1234_qcd4crv2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # HISTOGRAM INSERT of 4 rows.
    
    stmt = """insert into histograms
( select object_uid, 999638977, 0, 3, 1, 3, 10, 10,
timestamp'2006-04-14:17:55:19', _ucs2'(TIMESTAMP ''2006-04-10 10:00:00.000000'')',
_ucs2'(TIMESTAMP''2006-04-19 10:00:00.000000'')',
timestamp '0001-01-01 00:00:00',0,0,2,0,0.00000000000000000E+00,'M',0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histograms
( select object_uid, 999638982, 0, 2, 1, 3, 10, 10,
timestamp'2006-04-14:17:55:19', _ucs2'(DATE ''2006-04-10'')', _ucs2'(DATE ''2006-04-19'')',
timestamp '0001-01-01 00:00:00',0,0,2,0,0.00000000000000000E+00,'M',0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histograms
( select object_uid, 999638987, 0, 1, 1, 3, 10, 10,
timestamp'2006-04-14:17:55:19', _ucs2'(''0'')', _ucs2'(''9'')',
timestamp '0001-01-01 00:00:00',0,0,2,0,0.00000000000000000E+00,'M',0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histograms
( select object_uid, 999638992, 0, 0, 1, 3, 10, 10,
timestamp'2006-04-14:17:55:19', _ucs2'(0)', _ucs2'(9)',
timestamp '0001-01-01 00:00:00',0,0,2,0,0.00000000000000000E+00,'M',0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # HISTOGRAM_INTERVALS INSERT of 16 rows.
    stmt = """insert into histogram_intervals
(  select object_uid, 999638977, 0, 0, 0, _ucs2'(TIMESTAMP ''2006-04-10 10:00:00.000000'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638977, 1, 3, 3, _ucs2'(TIMESTAMP ''2006-04-12 10:00:00.000000'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638977, 2, 3, 3, _ucs2'(TIMESTAMP ''2006-04-15 10:00:00.000000'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638977, 3, 4, 4, _ucs2'(TIMESTAMP ''2006-04-19 10:00:00.000000'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638982, 0, 0, 0, _ucs2'(DATE ''2006-04-10'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638982, 1, 3, 3, _ucs2'(DATE ''2006-04-12'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638982, 2, 3, 3, _ucs2'(DATE ''2006-04-15'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638982, 3, 4, 4, _ucs2'(DATE ''2006-04-19'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638987, 0, 0, 0, _ucs2'(''0'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638987, 1, 3, 3, _ucs2'(''2'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638987, 2, 3, 3, _ucs2'(''5'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638987, 3, 4, 4, _ucs2'(''9'')',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638992, 0, 0, 0, _ucs2'(0)',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638992, 1, 3, 3, _ucs2'(2)',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638992, 2, 3, 3, _ucs2'(5)',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into histogram_intervals
(  select object_uid, 999638992, 3, 4, 4, _ucs2'(9)',.000,0,0,0,0,_ucs2' ',_ucs2' '
from """ + gvars.definition_schema + """.objects where object_name = 'trash1234_qcd4crv2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #---------------------------------
    # verify float columns have correct #intervals
    # no errors should be returned
    #---------------------------------
    stmt = """prepare xx from select double1_2 from trash1234_qcd4crv2 where time0_uniq = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select double1_2 from trash1234_qcd4crv2 where time0_uniq = time '00:24:53';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #----------------------------------
    # COLUMN A  histid = 999638992  ---
    #----------------------------------
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'()' where histogram_id = 999638992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'' where histogram_id = 999638992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0000' where histogram_id = 999638992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0000 0029' where histogram_id = 999638992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'()' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0000' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0000 0029' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638992 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    #----------------------------------
    # COLUMN B  histid = 999638987  ---
    #----------------------------------
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'()' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'('''')' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_warning_msg(output, '6003')
    #unexpect purge
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'''''' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0000' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0027 0000 0027' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0000 0029' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638987;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'()' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'('''')' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # NCI #unexpect any *WARNING[6003]*
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    # NCI #unexpect purge
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'''''' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0000' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0027 0000 0027' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0000 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638987 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    #----------------------------------
    # COLUMN C  histid = 999638982  ---
    #----------------------------------
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'()' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'('''')' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # NCI #expect any *WARNING[6004]*
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'(DATE '''')' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'''''' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'DATE ''''' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0000' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0044004100540045 0020 0027 0000 0027' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0000 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0044004100540045 0020 0027 0000 0027 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'()' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'('''')' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # NCI #unexpect any *WARNING[6003]*
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    # NCI #unexpect purge
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'(DATE '''')' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'''''' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'DATE ''''' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0000' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0027 0000 0027' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'00440041005400450020 0027 0000 0027' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0000 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0000 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638982 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    #----------------------------------
    # COLUMN D  histid = 999638977  ---
    #----------------------------------
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'()' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'('''')' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # NCI #expect any *WARNING[6004]*
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'(DATE '''')' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'(TIMESTAMP '''')' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'''''' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'DATE ''''' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2'TIMESTAMP ''''' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0000' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0044004100540045 0020 0027 0000 0027' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'00540049004D0045005300540041004D00500020 0027 0000 0027' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0000 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0044004100540045 0020 0027 0000 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 00540049004D0045005300540041004D00500020 0027 0000 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histograms set low_value = _ucs2 x'0028 00540049004D0045005300540041004D00500020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'()' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'('''')' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # NCI #unexpect any *WARNING[6003]*
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    # NCI #unexpect purge
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'(DATE '''')' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'(TIMESTAMP '''')' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'''''' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'DATE ''''' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2'TIMESTAMP ''''' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0000' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0027 0000 0027' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'00440041005400450020 0027 0000 0027' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'00540049004D0045005300540041004D00500020 0027 0000 0027' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0000 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0000 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0000 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00540049004D0045005300540041004D00500020 0027 0000 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00540049004D0045005300540041004D00500020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0032 0000 0033 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00440041005400450020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin;"""
    output = _dci.cmdexec(stmt)
    stmt = """update histogram_intervals set interval_boundary = _ucs2 x'0028 00540049004D0045005300540041004D00500020 0027 0032 0000 0033 0027 0029' where histogram_id = 999638977 and interval_number = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select a, b, c, d from trash1234_qcd4crv where a = 1 and b = '1' and c = date '2006-04-10' and d = TIMESTAMP '2006-04-10 10:00:00.000000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '6003')
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

