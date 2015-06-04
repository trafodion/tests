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
import customer_ddl
import part_ddl
import partsupp_ddl
import orders_ddl
import region_ddl
import nation_ddl
import supplier_ddl
import lineitem_ddl
from ...lib import hpdci
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
    
def test001(desc='Create tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # stmt = """control query default POS 'LOCAL_NODE';"""
    # output = _dci.cmdexec(stmt)
    # dci.expect_complete_msg(output)
    # stmt = """control query default POS_NUM_OF_PARTNS '1';"""
    # output = _dci.cmdexec(stmt)
    # dci.expect_complete_msg(output)
    region_ddl._init(_testmgr)
    nation_ddl._init(_testmgr)
    
    # stmt = """control query default POS reset;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    # stmt = """control query default POS_NUM_OF_PARTNS 'SYSTEM';"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    supplier_ddl._init(_testmgr)
    customer_ddl._init(_testmgr)
    part_ddl._init(_testmgr)
    partsupp_ddl._init(_testmgr)
    orders_ddl._init(_testmgr)
    lineitem_ddl._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test002(desc='Import data into tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    table = defs.my_schema + """.region"""
    data_file = defs.data_dir + """/region.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.nation"""
    data_file = defs.data_dir + """/nation.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.supplier"""
    data_file = defs.data_dir + """/supplier.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.customer"""
    data_file = defs.data_dir + """/customer.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.part"""
    data_file = defs.data_dir + """/part.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.partsupp"""
    data_file = defs.data_dir + """/partsupp.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)
   
    table = defs.my_schema + """.orders"""
    data_file = defs.data_dir + """/orders.tbl"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.lineitem"""
    data_file = defs.data_dir + """/lineitem.tbl.1"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    table = defs.my_schema + """.lineitem"""
    data_file = defs.data_dir + """/lineitem.tbl.2"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, '|')
    _dci.expect_loaded_msg(output)

    # It seems to take forever for the transaction to go through.  Wait for
    # 30 seconds before select count(*)
    time.sleep(30)

    stmt = """select count(*) from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '5')
    stmt = """select count(*) from nation;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '25')
    stmt = """select count(*) from supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '20000')
    stmt = """select count(*) from customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '300000')
    stmt = """select count(*) from part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '400000')
    stmt = """select count(*) from partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1600000')
    stmt = """select count(*) from orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3000000')
    stmt = """select count(*) from lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '11997996')

    _testmgr.testcase_end(desc)

def test003(desc='Update statistics'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """update statistics for table region on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table nation on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table supplier on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table customer on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table part on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table partsupp on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table orders on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table lineitem on every column sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc='Grant privileges'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    tablelist = ['region', 'nation', 'supplier', 'customer', 'part', 'partsupp', 'orders', 'lineitem']

    for table in tablelist:
        # set privilege
        stmt = 'revoke all on table ' + table + ' from PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = 'grant select on table ' + table + ' to PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


