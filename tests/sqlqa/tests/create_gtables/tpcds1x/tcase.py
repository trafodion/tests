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

import call_center_ddl
import catalog_page_ddl
import catalog_returns_ddl
import catalog_sales_ddl
import customer_address_ddl
import customer_ddl
import customer_demographics_ddl
import date_dim_ddl
import household_demographics_ddl
import income_band_ddl
import inventory_ddl
import item_ddl
import promotion_ddl
import reason_ddl
import ship_mode_ddl
import store_ddl
import store_returns_ddl
import store_sales_ddl
import time_dim_ddl
import warehouse_ddl
import web_page_ddl
import web_returns_ddl
import web_sales_ddl
import web_site_ddl
from ...lib import hpdci
import defs
import table

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

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    # turn off stats warning, so that they don't interfere with expect file
    stmt = """control query default hist_missing_stats_warning_level '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default hist_rowcount_requiring_stats '1000000';"""
    output = _dci.cmdexec(stmt)

    tablelist = [['call_center', ['call_center.csv'], '6'], 
                 ['catalog_page', ['catalog_page.csv'], '11718'],
                 ['catalog_returns', ['catalog_returns.csv'], '144222'], 
                 ['catalog_sales', ['catalog_sales.csv'],'1440020'],
                 ['customer_address', ['customer_address.csv'], '50000'], 
                 ['customer', ['customer.csv'], '100000'],
                 ['customer_demographics', ['customer_demographics.csv'], '1920800'], 
                 ['date_dim', ['date_dim.csv'], '73049'],
                 ['household_demographics', ['household_demographics.csv'], '7200'], 
                 ['income_band', ['income_band.csv'], '20'],
                 ['inventory', ['inventory.csv'], '11745000'], 
                 ['item', ['item.csv'], '18000'],
                 ['promotion', ['promotion.csv'], '300'], 
                 ['reason', ['reason.csv'], '35'],
                 ['ship_mode', ['ship_mode.csv'], '20'], 
                 ['store', ['store.csv'], '12'],
                 ['store_returns', ['store_returns.csv'], '287607'], 
                 ['store_sales', ['store_sales.csv'], '2880143'],
                 ['time_dim', ['time_dim.csv'], '86400'], 
                 ['warehouse', ['warehouse.csv'], '5'],
                 ['web_page', ['web_page.csv'], '60'], 
                 ['web_returns', ['web_returns.csv'], '72176'],
                 ['web_sales', ['web_sales.csv'], '720068'], 
                 ['web_site', ['web_site.csv'], '30']]

    for items in tablelist:
        table.create_and_load(_testmgr, prop_file, items[0], items[1], items[2], '|')
    
    _testmgr.testcase_end(desc)

