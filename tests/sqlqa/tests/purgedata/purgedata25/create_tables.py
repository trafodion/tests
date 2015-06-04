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

import customer_ddl
import part_ddl
import lineitem_ddl
import partsupp_ddl
import orders_ddl
import region_ddl
import supplier_ddl
import nation_ddl
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

    customer_ddl._init(_testmgr)
    ##sh import ${my_schema}.customer -I ${test_dir}/customer.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.customer select * from """ + gvars.g_schema_cmureg + """.customer1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.customer -I ${test_dir}/customer.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.customer select * from """ + gvars.g_schema_cmureg + """.customer2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.customer -I ${test_dir}/customer.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.customer select * from """ + gvars.g_schema_cmureg + """.customer3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.customer -I ${test_dir}/customer.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.customer select * from """ + gvars.g_schema_cmureg + """.customer4;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.customer;"""
    output = _dci.cmdexec(stmt)   
    _dci.expect_str_token(output, '15000')

 
    orders_ddl._init(_testmgr)
    ##sh import ${my_schema}.orders -I ${test_dir}/orders.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.orders select * from """ + gvars.g_schema_cmureg + """.orders1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.orders -I ${test_dir}/orders.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.orders select * from """ + gvars.g_schema_cmureg + """.orders2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.orders -I ${test_dir}/orders.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.orders select * from """ + gvars.g_schema_cmureg + """.orders3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.orders -I ${test_dir}/orders.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.orders select * from """ + gvars.g_schema_cmureg + """.orders4;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '150000')


    part_ddl._init(_testmgr)
    ##sh import ${my_schema}.part -I ${test_dir}/part.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.part select * from """ + gvars.g_schema_cmureg + """.part1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.part -I ${test_dir}/part.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.part select * from """ + gvars.g_schema_cmureg + """.part2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.part -I ${test_dir}/part.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.part select * from """ + gvars.g_schema_cmureg + """.part3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.part -I ${test_dir}/part.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.part select * from """ + gvars.g_schema_cmureg + """.part4;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """select count(*) from """ + defs.my_schema + """.part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '20000')

 
    partsupp_ddl._init(_testmgr)
    ##sh import ${my_schema}.partsupp -I ${test_dir}/partsupp.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.partsupp select * from """ + gvars.g_schema_cmureg + """.partsupp1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.partsupp -I ${test_dir}/partsupp.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.partsupp select * from """ + gvars.g_schema_cmureg + """.partsupp2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.partsupp -I ${test_dir}/partsupp.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.partsupp select * from """ + gvars.g_schema_cmureg + """.partsupp3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.partsupp -I ${test_dir}/partsupp.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.partsupp select * from """ + gvars.g_schema_cmureg + """.partsupp4;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """select count(*) from """ + defs.my_schema + """.partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '80000')


    supplier_ddl._init(_testmgr)
    ##sh import ${my_schema}.supplier -I ${test_dir}/supplier.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.supplier select * from """ + gvars.g_schema_cmureg + """.supplier1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.supplier -I ${test_dir}/supplier.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.supplier select * from """ + gvars.g_schema_cmureg + """.supplier2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.supplier -I ${test_dir}/supplier.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.supplier select * from """ + gvars.g_schema_cmureg + """.supplier3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.supplier -I ${test_dir}/supplier.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.supplier select * from """ + gvars.g_schema_cmureg + """.supplier4;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """select count(*) from """ + defs.my_schema + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1000')


    lineitem_ddl._init(_testmgr)
    ##sh import ${my_schema}.lineitem -I ${test_dir}/lineitem.tbl.1
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.lineitem select * from """ + gvars.g_schema_cmureg + """.lineitem1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.lineitem -I ${test_dir}/lineitem.tbl.2
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.lineitem select * from """ + gvars.g_schema_cmureg + """.lineitem2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.lineitem -I ${test_dir}/lineitem.tbl.3
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.lineitem select * from """ + gvars.g_schema_cmureg + """.lineitem3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.lineitem -I ${test_dir}/lineitem.tbl.4
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.lineitem select * from """ + gvars.g_schema_cmureg + """.lineitem4;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """select count(*) from """ + defs.my_schema + """.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '600572')

 
    region_ddl._init(_testmgr)
    ##sh import ${my_schema}.region -I ${test_dir}/region.tbl
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.region select * from """ + gvars.g_schema_cmureg + """.region;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '5')

   
    nation_ddl._init(_testmgr)
    # loading nation table
    ##sh import ${my_schema}.nation -I ${test_dir}/nation.tbl
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.nation select * from """ + gvars.g_schema_cmureg + """.nation;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.nation;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '25')

