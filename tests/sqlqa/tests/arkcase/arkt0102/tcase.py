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
    
def test001(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        This test verifies the SQL Update
    #                      Statistics command.
    #                      On empty unpartitioned and partitioned
    #                      tables of all organizations
    #
    # Purpose:             Does UPDATE STATISTICS work on empty tables?
    #                      It should generate the histogram rows as follows:
    #                      In histograms table:
    #                      rowcount = 0
    #                      total_uec = 0
    #                      high_value=low_value = ()
    #                      HISINTS has one row with that histogram_id, where
    #                      interval_boundary = ()
    #                      interval_row_count = interval_uec = 0
    #                       Table organizations:
    #                         K, explicit key.
    #                         K, syskey; with index (can't be
    #                            partitioned)
    #                         E, syskey.
    #                       Single and multiple partitions.
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """CREATE TABLE p0tk01 
( col_1 pic x(3) not null
, col_2 pic x(7) not null
, col_3 pic 9(3) not null
, PRIMARY KEY (col_1, col_3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE TABLE p0tk02 
( col_1 pic x(3) not null
, col_2 pic x(7) not null
, col_3 pic 9(3) not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX p0tk02i 
ON p0tk02 (col_2 DESC);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    #  Check stored statistics for each table before and after
    #  Update Statistics. Update Statistics on an empty table.
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from p0tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from p0tk02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """UPDATE STATISTICS FOR TABLE p0tk02 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')

    stmt = """CREATE TABLE p0te01 
( col_bin_16 smallint
, col_bin_32 integer
, col_bin_64 largeint
, varchar_254 varchar (254)
, col_varchar_3 varchar (3)
, col_varchar_4 varchar (4)
, col_varchar_5 varchar (5)
) no partition
--      CATALOG $subvol_for_temporary_data_1_A
--      ORGANIZATION E
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Check statistics for each table before and after updating
    #  statistics; look for 0 rows versus rows with default stats
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """UPDATE STATISTICS FOR TABLE p0te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    # Repeat tests for partioned tables
    #-------------
    # KEY SEQUENCED:
    #-------------
    stmt = """CREATE TABLE p0tk03 
( col_1 pic x(3) not null
, col_2 pic x(7)
, col_3 pic 9(3) not null
, PRIMARY KEY (col_1, col_3)
) number of partitions 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create identical KS table to be indexed:
    stmt = """CREATE TABLE p0tk04 
( col_1 pic x(3) not null
, col_2 pic x(7)
, col_3 pic 9(3) not null
, PRIMARY KEY (col_1, col_3)
) number of partitions 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create partitioned index
    stmt = """CREATE INDEX p0tk04i 
ON p0tk04 
(col_2 DESC)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Check that default stats exist for all partitions of each table,
    #  update histogram statistics for one partition of indexed table,
    #  then check that default stats still exist for all partitions
    #  and that StatisticsTime column is updated for that table
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    stmt = """UPDATE STATISTICS FOR TABLE p0tk04 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    
    stmt = """UPDATE STATISTICS FOR TABLE p0tk03 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s15')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s16')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s17')
    
    stmt = """UPDATE STATISTICS FOR TABLE p0tk04 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s18')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s19')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s20')
    
    # Repeat tests for an partitioned ES table
    stmt = """CREATE TABLE p0te02 
( col_bin_16 smallint
, col_bin_32 integer
, col_bin_64 largeint
, varchar_254 varchar (254)
, col_varchar_3 varchar (3)
, col_varchar_4 varchar (4)
, col_varchar_5 varchar (5)
) no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s21')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s22')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s23')
    
    stmt = """UPDATE  STATISTICS FOR TABLE p0te02 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s24')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s25')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s26')
    
    stmt = """DROP TABLE p0tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE p0tk02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE p0tk03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE p0tk04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE p0te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE p0te02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE p0tk01;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE p0tk02;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE p0tk03;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE p0tk04;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE p0te01;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE p0te02;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        This test verifies the SQL Update Statistics
    #                      command.
    #                      Small KS and ES tables are first populated
    #                      and are then rows are deleted. UPDATE STATISTICS
    #                      for some and then ALL fields
    #
    #    Purpose:  Does UPDATE STATISTICS reflect values
    #              for tables with few records?
    #
    #              Tables have 20 columns of all data types
    #              except date-time, double precision,
    #              float, and real.
    #
    #              Data distibution:
    #              some columns with identical values,
    #              some with 1 in 2, 1 in 4,
    #              1 in 10, 1 in 20, 2 with all
    #              unique values
    #
    #              Update Statistics for all catalog tables
    #              (few records normally).
    #
    # =================== End Test Case Header  ===================
    #-------------
    #  KEY SEQUENCED:
    #-------------
    #  Organization K, explicit key, copied from global database table
    #  btsel01, with addition of one col (char_245)
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE p1tk01 (
char_1                 CHAR(1)                not null
, pic_x_long             PICTURE X(200) DISPLAY not null
, var_char_1             VARCHAR(1)             not null
, var_char_245           VARCHAR(245)           not null
, binary_signed          numeric (4) signed     not null
, binary_32_u            numeric (9,2) UNSIGNED not null
, binary_64_s            numeric (18,3) SIGNED  not null
, pic_comp_1             PIC S9(10) COMP        not null
, pic_comp_2             PIC SV9(2) COMP        not null
, pic_comp_3             PIC S9(3)V9(5) COMP    not null
, small_int              SMALLINT               not null
, medium_int             INTEGER UNSIGNED       not null
, large_int              LARGEINT SIGNED        not null
, decimal_1              DECIMAL (1)            not null
, decimal_2_signed       DECIMAL (2,2) SIGNED   not null
, decimal_3_unsigned     DECIMAL (3,0) UNSIGNED not null
, pic_decimal_1          PIC S9(1)V9(1)         not null
--SIGN IS LEADING
, pic_decimal_2          PICTURE V999 DISPLAY   not null
, pic_decimal_3          PIC S9 DISPLAY         not null
--SIGN IS LEADING
, char_245               char(245)              not null
) no partition
--    CATALOG $arkt0102
attribute
--     AUDIT
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Index the table with simple, one-column indexes:
    stmt = """CREATE INDEX p1tk01a 
ON p1tk01 
( char_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01b 
ON p1tk01 
( pic_x_long )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01c 
ON p1tk01 
( var_char_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01d 
ON p1tk01 
( var_char_245 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01e 
ON p1tk01 
( binary_signed )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01f 
ON p1tk01 
( binary_32_u   )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01g 
ON p1tk01 
( binary_64_s   )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01h 
ON p1tk01 
( pic_comp_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01i 
ON p1tk01 
( pic_comp_2 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # CREATE UNIQUE INDEX should succeed here because it's on a
    #  column which does not allow nulls
    stmt = """CREATE UNIQUE INDEX p1tk01j 
ON p1tk01 
( pic_comp_3 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01k 
ON p1tk01 
( small_int  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01l 
ON p1tk01 
( medium_int )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01m 
ON p1tk01 
( large_int  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01n 
ON p1tk01 
( decimal_1  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01o 
ON p1tk01 
( decimal_2_signed )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01p 
ON p1tk01 
( decimal_3_unsigned )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01q 
ON p1tk01 
( pic_decimal_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01r 
ON p1tk01 
( pic_decimal_2 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01s 
ON p1tk01 
( pic_decimal_3 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1tk01t 
ON p1tk01 
( binary_signed DESC )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    stmt = """INSERT INTO p1tk01 
VALUES (
'A'
, 'bobby01'
--    , constant (Every 1 the same)
, 'C'
--    , 1 in 10 the same
, 'a long line of text for the LONG varchar field'
--    , constant (Every 1 the same)
, 99
--    , 1 in 25 the same (1 to 25)
, 1
--    , 1 in 5 the same (-2 to +2)
, -2
--    , 1 in 10 the same (-1 to -10)
, -1
--    , 1 in 2 the same (0 and -.01)
, 0
--    , all different values
, 1
, 10
, 10000
, 1000000000
, 9
, .9
, 900
, 9.9
, 0.999
, 9
, 'a long line of text for the LONG char field'
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby02' , 'C'
, 'a long line of text for the LONG varchar field - 2'
, 99 , 1 , -2 , -1 , 0 , 2
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    #  After 2 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby03' , 'C'
, 'a long line of text for the LONG varchar field - 3'
, 99 , 2 , -2 , -1 , 0 , 3
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 3 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby04' , 'C'
, 'a long line of text for the LONG varchar field - 4'
, 99 , 2 , -2 , -1 , 0 , 4
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 4 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby05' , 'C'
, 'a long line of text for the LONG varchar field - 5'
, 99 , 3 , -2 , -1 , 0 , 5
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 5 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby06' , 'C'
, 'a long line of text for the LONG varchar field - 6'
, 99 , 3 , -2 , -2 , 0 , 6
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -6');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 6 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby07' , 'C'
, 'a long line of text for the LONG varchar field - 7'
, 99 , 4 , -2 , -2 , 0 , 7
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 7 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby08' , 'C'
, 'a long line of text for the LONG varchar field - 8'
, 99 , 4 , -2 , -2 , 0 , 8
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 8 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby09' , 'C'
, 'a long line of text for the LONG varchar field - 9'
, 99 , 4 , -2 , -2 , 0 , 9
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -9');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 9 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby10' , 'C'
, 'a long line of text for the LONG varchar field - 10'
, 99 , 5 , -2 , -2 , 0 , 10
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 10 inserts
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby11' , 'C'
, 'a long line of text for the LONG varchar field - 11'
, 99 , 6 , -1 , -3 , 0 , 11
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby12' , 'C'
, 'a long line of text for the LONG varchar field - 12'
, 99 , 6 , -1 , -3 , 0 , 12
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby13' , 'C'
, 'a long line of text for the LONG varchar field - 13'
, 99 , 7 , -1 , -3 , 0 , 13
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -13');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby14' , 'C'
, 'a long line of text for the LONG varchar field - 14'
, 99 , 7 , -1 , -3 , 0 , 14
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby15' , 'C'
, 'a long line of text for the LONG varchar field - 15'
, 99 , 8 , -1 , -3 , 0 , 15
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby16' , 'C'
, 'a long line of text for the LONG varchar field - 16'
, 99 , 8 , -1 , -4 , 0 , 16
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -16');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby17' , 'C'
, 'a long line of text for the LONG varchar field - 17'
, 99 , 9 , -1 , -4 , 0 , 17
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field - 17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby18' , 'C'
, 'a long line of text for the LONG varchar field - 18'
, 99 , 9 , -1 , -4 , 0 , 18
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -18');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby19' , 'C'
, 'a long line of text for the LONG varchar field - 19'
, 99 , 10 , -1 , -4 , 0 , 19
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -19');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby20' , 'C'
, 'a long line of text for the LONG varchar field - 20'
, 99 , 10 , -1 , -4 , 0 , 20
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 20 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s11')
    
    stmt = """insert into p1tk01 
values ('A' , 'bobby21' , 'C'
, 'a long line of text for the LONG varchar field 21'
, 99 , 11 , 0 , -5 , 0 , 21
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby22' , 'C'
, 'a long line of text for the LONG varchar field - 22'
, 99 , 11 , 0 , -5 , 0 , 22
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby23' , 'C'
, 'a long line of text for the LONG varchar field - 23'
, 99 , 12 , 0 , -5 , 0 , 23
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby24' , 'C'
, 'a long line of text for the LONG varchar field - 24'
, 99 , 12 , 0 , -5 , 0 , 24
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby25' , 'C'
, 'a long line of text for the LONG varchar field - 25'
, 99 , 13 , 0 , -5 , 0 , 25
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -25');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby26' , 'C'
, 'a long line of text for the LONG varchar field - 26'
, 99 , 13 , 0 , -6 , -0.01, 26
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -26');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby27' , 'C'
, 'a long line of text for the LONG varchar field - 27'
, 99 , 14 , 0 , -6 , -0.01, 27
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -27');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby28' , 'C'
, 'a long line of text for the LONG varchar field - 28'
, 99 , 14 , 0 , -6 , -0.01, 28
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby29' , 'C'
, 'a long line of text for the LONG varchar field - 29'
, 99 , 15 , 0 , -6 , -0.01, 29
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1tk01 
values ('A' , 'bobby30' , 'C'
, 'a long line of text for the LONG varchar field - 30'
, 99 , 15 , 0 , -6 , -0.01, 30
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
, 'a long line of text for the LONG char field -30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 30 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s12')
    
    #  Delete all but 10 records,
    #  then check that stats are updated
    stmt = """DELETE FROM p1tk01 
WHERE binary_32_u < 11 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 20)
    
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT pic_comp_3 FROM p1tk01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s13')
    stmt = """SELECT binary_32_u FROM p1tk01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s14')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s15')
    
    #  Delete all records, then check that 0 records remain and that
    #  stats are updated
    stmt = """DELETE FROM p1tk01 
WHERE char_1 <> 'Z' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10)
    
    stmt = """UPDATE STATISTICS FOR TABLE p1tk01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT pic_comp_3 FROM p1tk01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s16')
    
    #  Do same INSERT tests for ES table
    # -----------------------
    #  ENTRY SEQUENCED table
    # -----------------------
    
    stmt = """CREATE TABLE p1te01 (
char_1                 CHAR(1)                not null
, pic_x_long             PICTURE X(200) DISPLAY not null
, var_char_1             VARCHAR(1)             not null
, var_char_245           VARCHAR(245)           not null
, binary_signed          numeric (4) signed     not null
, binary_32_u            numeric (9,2) UNSIGNED not null
, binary_64_s            numeric (18,3) SIGNED  not null
, pic_comp_1             PIC S9(10) COMP        not null
, pic_comp_2             PIC SV9(2) COMP        not null
, pic_comp_3             PIC S9(3)V9(5) COMP    not null
, small_int              SMALLINT               not null
, medium_int             INTEGER UNSIGNED       not null
, large_int              LARGEINT SIGNED        not null
, decimal_1              DECIMAL (1)            not null
, decimal_2_signed       DECIMAL (2,2) SIGNED   not null
, decimal_3_unsigned     DECIMAL (3,0) UNSIGNED not null
, pic_decimal_1          PIC S9(1)V9(1)         not null
--SIGN IS LEADING
, pic_decimal_2          PICTURE V999 DISPLAY   not null
, pic_decimal_3          PIC S9                 not null
--SIGN IS LEADING
) no partition
--    CATALOG $arkt0102
--    ORGANIZATION E
attribute
--     AUDIT
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Index the table with simple, one-column indexes:
    stmt = """CREATE INDEX p1te01a 
ON p1te01 
( char_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01b 
ON p1te01 
( pic_x_long )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01c 
ON p1te01 
( var_char_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01d 
ON p1te01 
( var_char_245 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01e 
ON p1te01 
( binary_signed )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01f 
ON p1te01 
( binary_32_u   )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01g 
ON p1te01 
( binary_64_s   )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
--    BLOCKSIZE 512 ;
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01h 
ON p1te01 
( pic_comp_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01i 
ON p1te01 
( pic_comp_2 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  CREATE UNIQUE INDEX :should succeed because it's on a
    #  column which does not allow nulls
    stmt = """CREATE UNIQUE INDEX p1te01j 
ON p1te01 
( pic_comp_3 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01k 
ON p1te01 
( small_int  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01l 
ON p1te01 
( medium_int )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01m 
ON p1te01 
( large_int  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01n 
ON p1te01 
( decimal_1  )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01o 
ON p1te01 
( decimal_2_signed )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01p 
ON p1te01 
( decimal_3_unsigned )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01q 
ON p1te01 
( pic_decimal_1 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01r 
ON p1te01 
( pic_decimal_2 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01s 
ON p1te01 
( pic_decimal_3 )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX p1te01t 
ON p1te01 
( binary_signed DESC )
--    CATALOG $arkt0102
attribute
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """INSERT INTO p1te01 
VALUES (
'A'
, 'bobby01'
--    , constant (Every 1 the same)
, 'C'
--    , 1 in 10 the same
, 'a long line of text for the LONG varchar field'
--    , constant (Every 1 the same)
, 99
--    , 1 in 25 the same (1 to 25)
, 1
--    , 1 in 5 the same (-2 to +2)
, -2
--    , 1 in 10 the same (-1 to -10)
, -1
--    , 1 in 2 the same (0 and -.01)
, 0
--    , all different values
, 1
, 10
, 10000
, 1000000000
, 9
, .9
, 900
, 9.9
, 0.999
, 9
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 1 insert:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s17')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby02' , 'C'
, 'a long line of text for the LONG varchar field - 2'
, 99 , 1 , -2 , -1 , 0 , 2
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 2 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s18')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby03' , 'C'
, 'a long line of text for the LONG varchar field - 3'
, 99 , 2 , -2 , -1 , 0 , 3
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 3 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s19')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby04' , 'C'
, 'a long line of text for the LONG varchar field - 4'
, 99 , 2 , -2 , -1 , 0 , 4
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 4 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s20')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby05' , 'C'
, 'a long line of text for the LONG varchar field - 5'
, 99 , 3 , -2 , -1 , 0 , 5
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  After 5 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s21')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby06' , 'C'
, 'a long line of text for the LONG varchar field - 6'
, 99 , 3 , -2 , -2 , 0 , 6
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 6 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s22')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby07' , 'C'
, 'a long line of text for the LONG varchar field - 7'
, 99 , 4 , -2 , -2 , 0 , 7
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 7 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s23')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby08' , 'C'
, 'a long line of text for the LONG varchar field - 8'
, 99 , 4 , -2 , -2 , 0 , 8
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 8 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s24')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby09' , 'C'
, 'a long line of text for the LONG varchar field - 9'
, 99 , 4 , -2 , -2 , 0 , 9
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # After 9 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s25')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby10' , 'C'
, 'a long line of text for the LONG varchar field - 10'
, 99 , 5 , -2 , -2 , 0 , 10
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 10 inserts
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s26')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby11' , 'C'
, 'a long line of text for the LONG varchar field -11'
, 99 , 6 , -1 , -3 , 0 , 11
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby12' , 'C'
, 'a long line of text for the LONG varchar field - 12'
, 99 , 6 , -1 , -3 , 0 , 12
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby13' , 'C'
, 'a long line of text for the LONG varchar field - 13'
, 99 , 7 , -1 , -3 , 0 , 13
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby14' , 'C'
, 'a long line of text for the LONG varchar field - 14'
, 99 , 7 , -1 , -3 , 0 , 14
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby15' , 'C'
, 'a long line of text for the LONG varchar field - 15'
, 99 , 8 , -1 , -3 , 0 , 15
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby16' , 'C'
, 'a long line of text for the LONG varchar field - 16'
, 99 , 8 , -1 , -4 , 0 , 16
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby17' , 'C'
, 'a long line of text for the LONG varchar field - 17'
, 99 , 9 , -1 , -4 , 0 , 17
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby18' , 'C'
, 'a long line of text for the LONG varchar field - 18'
, 99 , 9 , -1 , -4 , 0 , 18
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby19' , 'C'
, 'a long line of text for the LONG varchar field - 19'
, 99 , 10 , -1 , -4 , 0 , 19
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby20' , 'C'
, 'a long line of text for the LONG varchar field - 20'
, 99 , 10 , -1 , -4 , 0 , 20
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 20 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s27')
    
    stmt = """insert into p1te01 
values ('A' , 'bobby21' , 'C'
, 'a long line of text for the LONG varchar field - 21'
, 99 , 11 , 0 , -5 , 0 , 21
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby22' , 'C'
, 'a long line of text for the LONG varchar field - 22'
, 99 , 11 , 0 , -5 , 0 , 22
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby23' , 'C'
, 'a long line of text for the LONG varchar field - 23'
, 99 , 12 , 0 , -5 , 0 , 23
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby24' , 'C'
, 'a long line of text for the LONG varchar field - 24'
, 99 , 12 , 0 , -5 , 0 , 24
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby25' , 'C'
, 'a long line of text for the LONG varchar field - 25'
, 99 , 13 , 0 , -5 , 0 , 25
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby26' , 'C'
, 'a long line of text for the LONG varchar field - 26'
, 99 , 13 , 0 , -6 , -0.01, 26
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby27' , 'C'
, 'a long line of text for the LONG varchar field - 27'
, 99 , 14 , 0 , -6 , -0.01, 27
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby28' , 'C'
, 'a long line of text for the LONG varchar field - 28'
, 99 , 14 , 0 , -6 , -0.01, 28
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby29' , 'C'
, 'a long line of text for the LONG varchar field - 29'
, 99 , 15 , 0 , -6 , -0.01, 29
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p1te01 
values ('A' , 'bobby30' , 'C'
, 'a long line of text for the LONG varchar field - 30'
, 99 , 15 , 0 , -6 , -0.01, 30
, 10 , 10000 , 1000000000
, 9 , .9 , 900 , 9.9 , 0.999 , 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  After 30 inserts:
    stmt = """UPDATE STATISTICS FOR TABLE p1te01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s28')
    
    if hpdci.tgtSQ():
        stmt = """update statistics for table """ + gvars.test_definition_schema + """.cols;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
        stmt = """update statistics for table """ + gvars.test_definition_schema + """.objects;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    stmt = """drop table p1tk01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table p1te01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A10
    #  Description:        This test verifies the SQL Update
    #                      statistics commnad on columns of datatypes
    #                      DOUBLE PRECISION, FLOAT, & REAL
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # ---------------------------------
    # Open a Log file
    # ---------------------------------
    # ---------------------------------
    
    stmt = """create table p9tab (
c1  float
, c2  float(22)
, c3  float(23)
, c4  real
, c5  double precision not null
, primary key (c5)
) no partition
-- catalog $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index p9indx 
on p9tab 
(c1)
-- catalog $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view p9pv 
(c1,c2,c4,c5) as
select c1,c2,c4,c5 from
 p9tab 
where c2 > 1.0e2 and
c5 < 1.0e2
--   for protection
--   catalog $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create sv comparing real to double precision
    stmt = """create view p9sv 
(c2,c3) as
select c2,c3 from
 p9tab 
where c3 >= c4
-- catalog $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into p9tab 
--   values (1.0e1,1.0e2,1.0e3,1.0e4,1.0e5,1.0e6);
values (1.0e1,1.0e2,1.0e3,1.0e4,1.0e5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
--   values (2.1e1,2.1e2,2.1e3,2.1e4,2.1e5,1.0e6);
values (2.1e1,2.1e2,2.1e3,2.1e4,2.1e5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
--   values (5.5e1,5.5e2,5.5e3,5.5e4,5.5e5,1.0e6);
values (5.5e1,5.5e2,5.5e3,5.5e4,5.5e5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
--   values (8.0e1,8.0e2,8.0e3,8.0e4,8.0e5,1.0e6);
values (8.0e1,8.0e2,8.0e3,8.0e4,8.0e5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
--   (c1,c2,c3,c4,c5,c6)
--  values (2,333.333,0.4E5,400E-3,100,1.06E77);
(c1,c2,c3,c4,c5)
values (2,333.333,0.4E5,400E-3,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
(c1,c2,c3,c4,c5)
values (101.0,1.02E2,103,1.4E1,1.5E1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
--    (c1,c2,c3,c4,c5,c6)
--  values (61,52,43,4.1234567,5.12345678901,0E1);
(c1,c2,c3,c4,c5)
values (61,52,43,4.1234567,5.12345678901);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into p9tab 
(c5)
values (0E0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from p9tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    stmt = """select * from p9pv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    stmt = """select * from p9sv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    stmt = """select * from p9tab 
where c1 > 1.0E1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    
    stmt = """update statistics for table p9tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from p9tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    
    stmt = """drop view  p9pv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view  p9sv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table p9tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A11
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  UPDATE STATISTICS on columns with DATETIME, DATE, TIME,
    #  TIMESTAMP, and INTERVAL datatypes
    #
    #  |                                                     |
    #  |  Test Case Name:  PA                                |
    #  |                                                     |
    #  |  Purpose: UPDATE STATISTICS on columns with         |
    #  |           DATETIME, DATE, TIME, and TIMESTAMP       |
    #  |           datatypes                                 |
    #  |                                                     |
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    #  Create local table with examples of all date-time
    #  datatypes incl. all formats for DATETIME
    stmt = """CREATE TABLE PATAB1 
(
col_1    TIMESTAMP
not null
HEADING 'TIMESTAMP DEFAULT FORMAT'
, col_2    TIMESTAMP
not null
HEADING 'TIMESTAMP USA FORMAT'
, col_3    TIMESTAMP
not null
HEADING 'TIMESTAMP EUROPEAN FORMAT'
, col_4    DATE
default date '06/15/1998' not null
HEADING 'DATE DEFAULT CURRENT TIMESTAMP'
, col_5    TIME
default time '11:43:00' not null
HEADING 'TIME DEFAULT CURRENT TIMESTAMP'
, col_6    TIMESTAMP
default timestamp '06/15/1998 11:46:00.0000' not null
HEADING 'TIMESTAMP DEFAULT CURRENT TIMESTAMP'
, PRIMARY KEY (col_1)
)
--      CATALOG $subvol_for_temporary_data_1_A
--    ORGANIZATION K
attribute
--      AUDIT
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create index on date-time column
    stmt = """CREATE INDEX paindx 
ON PATAB1 
(col_6)
--     CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create views using date-time literals
    stmt = """CREATE VIEW papv (c1,c2) as
select col_1, col_2 from PATAB1 
where col_1 <
timestamp '1993-10-09:17:44:39.123456'
--       for protection
--    CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE VIEW pasv (c1,c2) as
select col_5, col_6 from PATAB1 
where col_6 <
timestamp '1993-10-09:17:44:39.123456'
--     CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Be careful not to mix am/pm qualifier w/ military time
    stmt = """INSERT INTO PATAB1 
VALUES (
timestamp '1989-10-09 17:44:39.123456' ,
timestamp '10/09/1989 07:44:39.123456 pm' ,
timestamp '09.10.1989 17.44.39.123456' ,
date '1989-10-09',
time '17:44:39',
timestamp '1989-10-09 17:44:39.123456'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO PATAB1 
VALUES (
timestamp '1990-10-09 17:44:39.123456',
timestamp '10/09/1990 07:44:39.123456 pm',
timestamp '09.10.1990 17.44.39.123456',
date '1990-10-09',
time '18:44:39',
timestamp '1990-10-09 17:44:39.123456'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO PATAB1 
VALUES (
timestamp '1991-10-09 17:44:39.123456' ,
timestamp '10/09/1991 07:44:39.123456 pm' ,
timestamp '09.10.1991 17.44.39.123456' ,
date '1991-10-09',
time '19:44:39',
timestamp '1991-10-09 17:44:39.123456'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * from PATAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    
    stmt = """SELECT * from papv ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    
    stmt = """SELECT * from pasv ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    
    stmt = """UPDATE STATISTICS FOR TABLE PATAB1 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Check column stats
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from PATAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    
    # Add a column with date-time datatype, insert a row
    stmt = """INSERT INTO PATAB1 
VALUES (
timestamp '1993-01-01 01:01:01.123456' ,
timestamp '01/01/1993 01:01:01.123456 am' ,
timestamp '01.01.1993 01.01.01.123456' ,
date '1993-01-01',
time '01:01:01',
timestamp '1993-01-01 01:01:01.123456'
--     timestamp '1993-01-01:01:01:01.123456'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Update and check statistics for all columns
    stmt = """UPDATE STATISTICS FOR TABLE PATAB1 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from PATAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    
    # Create table with col with DATETIME datatype
    # where display size of col > 20 chars
    
    stmt = """CREATE TABLE PATAB2 
(
col_1    TIMESTAMP  NO DEFAULT NOT NULL
HEADING 'EVENT TIME'
, col_2    PIC X(3) NO DEFAULT NOT NULL
HEADING 'EVENT TYPE'
, col_3    NUMERIC (10,1) DEFAULT NULL
HEADING 'EVENT SEQUENCE'
, PRIMARY KEY (col_1)
)
--     CATALOG $subvol_for_temporary_data_1_A
--     ORGANIZATION K
attribute
--      AUDIT
-- 1/25/99 For now the only blocksize supported is 4096
BLOCKSIZE 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX paindx2 
ON PATAB2 
(col_3)
--     CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO PATAB2 
VALUES (timestamp '1989-10-09 17:44:39.123456' ,
'AAA',1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO PATAB2 
VALUES (timestamp '1990-11-09 17:45:40.123456' ,
'BBB',2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO PATAB2 
VALUES (timestamp '1991-05-09 17:45:40.123456' ,
'CCC',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM PATAB2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    
    # Update and check statistics
    stmt = """UPDATE STATISTICS FOR TABLE PATAB2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from PATAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    
    stmt = """drop view papv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pasv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table PATAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table PATAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE  511 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE  512 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE  513 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 1024 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 2048 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 4094 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 4095 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 4097 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 4098 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 14096 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1) 		)
attribute BLOCKSIZE 40980 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    # expected error
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1)          )
--   attribute BLOCKSIZE 4095, BLOCKSIZE 4096 ;
attribute BLOCKSIZE """ + defs.blksize1 + """, BLOCKSIZE """ + defs.blksize2 + """ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1)          )
--   attribute BLOCKSIZE 4096, BLOCKSIZE 4095 ;
attribute BLOCKSIZE """ + defs.blksize2 + """, BLOCKSIZE """ + defs.blksize1 + """ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3058')
    
    stmt = """CREATE TABLE testblocksize01 (
char_1 CHAR(1)          )
--   attribute BLOCKSIZE 4096, BLOCKSIZE 4096 ;
attribute BLOCKSIZE """ + defs.blksize2 + """, BLOCKSIZE """ + defs.blksize2 + """ ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3092')
    
    # TRAFODION: This test uses to create a different schema and use the same table
    # name or the schema that this table did not exist.  It is changed to
    # a none-existent table in the same schema.
    # But for some reason, this does not even return the 1004 object not
    # exist error on SQ.  Perhaps the block size errors earlier screwed
    # things up?  Need to debug.
    stmt = """drop table ABCDEFGtestblocksize01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
   
    stmt = """drop table \"module\";"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table \"module\" ("ARE"   integer,
"ADD"   integer,
"AFTER" integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """insert into \"module\" values(1,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from \"module\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """update statistics for table module on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
   
    stmt = """drop table \"module\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test005(desc="""n24"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N24
    #  Description:        This test verifies the SQL Error handling
    #                      for UPDATE STATISTICS.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from """ + gvars.histogram_intervals + """;"""
    output = _dci.cmdexec(stmt)
    
    #   Non-existent table
    stmt = """UPDATE ALL STATISTICS FOR TABLE
n0notab on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Create table on which to create needed objects:
    stmt = """CREATE TABLE n0table 
( col_1 pic x(3) not null
, col_2 pic x(7)
, col_3 pic 9(3) not null
, PRIMARY KEY (col_1, col_3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO n0table 
VALUES ( 'ABC' , 'steven' , 123 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO n0table 
VALUES ( 'DEF' , 'doreen' , 456 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO n0table 
VALUES ( 'GHI' , 'rick'   , 789 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table on every column ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create protection view:
    stmt = """CREATE VIEW n0pv 
AS SELECT col_1, col_2, col_3
FROM n0table 
WHERE col_1 = 'TU' AND col_3 < 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table on every column ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from n0pv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n24exp""", 'n24s1')
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0pv on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9205')
    
    #  Create shorthand view:
    stmt = """CREATE VIEW n0sv 
( column1, column2 )
AS SELECT x.col_1, n0table.col_1
FROM n0table 
, n0table x
WHERE x.col_1 > n0table.col_1
--      CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE
 n0sv on every column ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9205')
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from n0sv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n24exp""", 'n24s4')
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX n0index 
ON n0table 
( col_1
)
--  CATALOG $subvol_for_temporary_data_1_A
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select histogram_id, rowcount, total_uec, high_value, low_value
from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select """ + gvars.histogram_intervals + """.histogram_id, interval_boundary,
interval_rowcount, interval_uec
from """ + gvars.histogram_intervals + """, """ + gvars.histograms + """
where """ + gvars.histogram_intervals + """.histogram_id = """ + gvars.histograms + """.histogram_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select count(*) from n0index;"""
    output = _dci.cmdexec(stmt)
    # Trafodion allows you to select from index
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    
    stmt = """select * from n0index;"""
    output = _dci.cmdexec(stmt)
    # Trafodion allows you to select from index
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    
    #  attempt to update histogram statistics for index; should get SQL [-4030]
    stmt = """UPDATE STATISTICS FOR TABLE
 n0index  on every column;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER TABLE n0table 
ADD CONSTRAINT n0assert CHECK (col_1 in ('ABC', 'DEF', 'GHI'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE STATISTICS FOR TABLE
n0assert on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   Bad syntax; 
    stmt = """UPDATE STATISTICS junk on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Bad syntax;
    stmt = """UPDATE STATISTICS FOR TABLE
 n0table, junk  on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Bad syntax;
    stmt = """UPDATE SOME STATISTICS FOR TABLE
 n0table on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   Too-long name for table name; 
    stmt = """UPDATE STATISTICS FOR TABLE
garbageofalongname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """UPDATE STATISTICS FOR TABLE \$sillyvol_A.n0table;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE STATISTICS FOR TABLE * ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE STATISTICS FOR TABLE *.*;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE STATISTICS FOR TABLE \$*.*.*;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE STATISTICS FOR TABLE
*;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """UPDATE STATISTICS FOR TABLE #badcharacter;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """UPDATE STATISTICS FOR TABLE subvol.*badchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """UPDATE STATISTICS FOR TABLE \$*.subvol.n0table;"""
    output = _dci.cmdexec(stmt)
    
    #  Invalid table name
    stmt = """UPDATE STATISTICS FOR TABLE
@badchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """drop view n0pv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view n0sv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE n0table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view n0pv;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view n0sv;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table n0table cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

