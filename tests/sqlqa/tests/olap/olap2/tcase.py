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

#Notes:test685 will take around 120 minutes.
#OLAP tests with 'partition by' clause
# move following cqds to setup file
#cqd QUERY_STRATEGIZER 'ON';
#cqd EXPLAIN_STRATEGIZER_PARAMETERS 'ON';
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and unbounded following  ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and unbounded following  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and 4 following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 12 preceding and 4 preceding ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and unbounded following  ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and 3 following  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 12 preceding and 8 preceding ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 20 preceding and current row ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and 4 following  ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 25 preceding and 15 preceding  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 22 preceding and 5 preceding ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 3 preceding and unbounded following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 2 preceding and current row ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 18 preceding and 7 preceding  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 200 preceding and unbounded following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 34 preceding and 4 following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 8 preceding and 4 preceding ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 6 preceding and unbounded following  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 8 preceding and 5 following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 3 following and 8 following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 2 preceding and 3 following ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 2 preceding and unbounded following  ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 2 following and 5 following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 3 following and unbounded following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #schema tpcds1x
    _testmgr.testcase_end(desc)

def test007(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between unbounded preceding and 3 preceding ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between unbounded preceding and current row ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between unbounded preceding and unbounded following) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between unbounded preceding and 10 following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between current row and current row ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between current row and unbounded following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between current row and 10 following) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 20 preceding and 12 preceding ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 100 preceding and current row ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 10 preceding and 2 following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test017(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 4 preceding and unbounded following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test018(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 4 following and 5 following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]  dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand,
sum(ss_ext_sales_price) over (partition by i_brand_id order by i_brand_id
rows between 4 following and unbounded following ) as ext_price
from   """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt,
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand, """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id,ss_ext_sales_price
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test020(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and 10 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select  avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and 10 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test021(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and 5 preceding) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test022(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select  avg(ctr_total_return)*1.2
from (select wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test023(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and 3 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test024(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and 4 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between current row and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 111)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test025(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test026(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and 3 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 108)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test027(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and 5 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 4 preceding and 3 preceding) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 372)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test028(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 13 preceding and 6 preceding) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 4 preceding and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test029(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and current row) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 5 preceding and 4 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test030(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and 15 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 4 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test031(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 6 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 4 following and 8 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 370)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test032(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 3 following and 6 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 4 following and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test033(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between unbounded preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 4 following and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 370)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test034(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 10 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 110)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test035(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and 6 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 108)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test036(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between current row and 3 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 24 preceding and 6 preceding) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 360)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test037(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 15 preceding and 12 preceding) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 4 preceding and 6 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test038(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 3 preceding and 4 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 107)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test039(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 3 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt,ca_state
rows between 6 following and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 370)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test040(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 3 following and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 following and 12 following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test041(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between unbounded preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between current row and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test042(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 3 following and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr1
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select  wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) over (partition by  wr_return_amt order by wr_return_amt
rows between 6 preceding and unbounded following) as ctr_total_return
from """ + gvars.g_schema_tpcds1x + """.WEB_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS 
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk,wr_return_amt
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test043(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
avg(ss_quantity) over (partition by  ss_quantity order by ss_quantity
rows between unbounded preceding and unbounded following ) as SalesQuantity ,
avg(ss_ext_sales_price) over (partition by  ss_quantity order by ss_quantity
rows between unbounded preceding and unbounded following ) as SalesPrice ,
avg(ss_ext_wholesale_cost) over (partition by  ss_quantity order by ss_quantity
rows between unbounded preceding and unbounded following ) as SalesCost ,
sum(ss_ext_wholesale_cost) over (partition by  ss_quantity order by ss_quantity
rows between unbounded preceding and unbounded following ) as WholeSale
from """ + gvars.g_schema_tpcds1x + """.STORE_SALES,
 """ + gvars.g_schema_tpcds1x + """.STORE, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS,
 """ + gvars.g_schema_tpcds1x + """.HOUSEHOLD_DEMOGRAPHICS,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM 
where s_store_sk = ss_store_sk
and  ss_sold_date_sk = d_date_sk and d_year = 2001
and
(
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'S'
and
cd_education_status = '2 yr Degree'
and
ss_sales_price between 100.00 and 150.00
and
hd_dep_count = 3
)
or
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'W'
and
cd_education_status = 'College'
and
ss_sales_price between 50.00 and 100.00
and
hd_dep_count = 1
)
or
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'D'
and
cd_education_status = 'Advanced Degree'
and
ss_sales_price between 150.00 and 200.00
and
hd_dep_count = 1
)
)
and
(
(
ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('WV', 'VT', 'IA')
and ss_net_profit between 100 and 200
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('NC', 'IA', 'OK')
and ss_net_profit between 150 and 300
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('SD', 'ND', 'OK')
and ss_net_profit between 50 and 250
)    

) group by ss_quantity,ss_ext_sales_price,ss_ext_wholesale_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    # LP1425745
    _dci.expect_selected_msg(output, 5)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test044(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
i_manufact_id ,
sum(total_sales) total_sales
from  (select * from (
select
i_manufact_id,
sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price
rows between 6 preceding and 10 following)as total_sales
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES,
 """ + gvars.g_schema_tpcds1x + """.DATE_DIM,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS,
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where
i_manufact_id in (select
i_manufact_id
from
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where i_category in ('Electronics'))
and     ss_item_sk              = i_item_sk
and     ss_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     ss_addr_sk              = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id,ss_ext_sales_price) as ss
union all
select * from (
select
i_manufact_id,
sum(cs_ext_sales_price) over (partition by cs_ext_sales_price order by cs_ext_sales_price
rows between 6 preceding and 10 following)as total_sales
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES,
 """ + gvars.g_schema_tpcds1x + """.DATE_DIM,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS,
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where
i_manufact_id               in (select
i_manufact_id
from
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where i_category in ('Electronics'))
and     cs_item_sk              = i_item_sk
and     cs_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     cs_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id, cs_ext_sales_price) as cs
union all
select * from (
select
i_manufact_id,
sum(ws_ext_sales_price) over (partition by ws_ext_sales_price order by ws_ext_sales_price
rows between 6 preceding and 10 following)as total_sales
from
 """ + gvars.g_schema_tpcds1x + """.WEB_SALES,
 """ + gvars.g_schema_tpcds1x + """.DATE_DIM,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS,
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where
i_manufact_id               in (select
i_manufact_id
from
 """ + gvars.g_schema_tpcds1x + """.ITEM 
where i_category in ('Electronics'))
and     ws_item_sk              = i_item_sk
and     ws_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     ws_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id, ws_ext_sales_price) as ws) tmp1
group by i_manufact_id
order by total_sales;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #with count:
    _testmgr.testcase_end(desc)

def test045(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and 4 preceding ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 4 following and 6 following) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test046(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and current row ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 2 following and unbounded following ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test047(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 2 preceding and 4 following ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test048(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and 4 following ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 2 preceding and unbounded following ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test049(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and current row ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 12 preceding and 4 preceding ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test050(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between current row and current row ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 2 preceding and current row ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test051(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between current row and unbounded following ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between current row and 4 following ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test052(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
w_state
,i_item_id
,count(case when (cast(d_date as date) < cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following ) as sales_before
,count(case when (cast(d_date as date) >= cast ('2002-04-27' as date))
then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end)  over (partition by  i_item_id order by i_item_id
rows between 4 preceding and unbounded following ) as sales_after
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES left outer join """ + gvars.g_schema_tpcds1x + """.CATALOG_RETURNS on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between (cast ('2002-04-27' as date) - 30 )
and (cast ('2002-04-27' as date) + 30 )
group by
w_state,i_item_id,
d_date,
cs_sales_price,
cr_refunded_cash
order by
w_state,
i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test053(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] s_store_name, s_store_id,
sum(case when (d_day_name='Sunday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as sun_sales,
sum(case when (d_day_name='Monday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as mon_sales,
sum(case when (d_day_name='Tuesday') then ss_sales_price else  null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as tue_sales,
sum(case when (d_day_name='Wednesday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as wed_sales,
sum(case when (d_day_name='Thursday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as thu_sales,
sum(case when (d_day_name='Friday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as fri_sales,
sum(case when (d_day_name='Saturday') then ss_sales_price else null end) over (partition by s_store_id order by s_store_id
rows between current row and unbounded following ) as sat_sales
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.STORE 
where d_date_sk = ss_sold_date_sk and
s_store_sk = ss_store_sk and
s_gmt_offset = -5 and
d_year = 2001
group by
s_store_name,
s_store_id,
d_day_name,
ss_sales_price;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test054(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
ss_item_sk,
ss_sold_date_sk,
ss_customer_sk,
ss_sales_price,
sum (ss_quantity) over (partition by  ss_quantity order by ss_quantity,ss_sales_price,ss_item_sk
rows between unbounded preceding and unbounded following ) as Store_sales_Qty
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES,
 """ + gvars.g_schema_tpcds1x + """.STORE,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS,
 """ + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS,
 """ + gvars.g_schema_tpcds1x + """.DATE_DIM 
where s_store_sk = ss_store_sk
and  ss_sold_date_sk = d_date_sk and d_year = 1999
and
(
(
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'M'
and
cd_education_status = '2 yr Degree'
and
ss_sales_price between 100.00 and 150.00
)
or
(
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'M'
and
cd_education_status = '2 yr Degree'
and
ss_sales_price between 50.00 and 100.00
)
or
(
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'M'
and
cd_education_status = '2 yr Degree'
and
ss_sales_price between 150.00 and 200.00
)
)
and
(
(
ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('MT', 'FL', 'NC')
and ss_net_profit between 0 and 2000
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('IL', 'GA', 'NY')
and ss_net_profit between 150 and 3000
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('MA', 'TN', 'CO')
and ss_net_profit between 50 and 25000
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    # LP1425745
    _dci.expect_selected_msg(output, 409)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test055(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between unbounded preceding and 10 preceding ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test056(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between unbounded preceding and current row ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test057(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between unbounded preceding and unbounded following) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test058(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between unbounded preceding and 10 following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test059(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between current row and current row ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test060(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between current row and 12 following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test061(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between current row and unbounded following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test062(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 12 preceding and 6 preceding ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test063(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 8 preceding and unbounded following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test064(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 4 preceding and 4 following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test065(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 4 following and 6 following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test066(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,sum(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 6 following and unbounded following) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1657)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test067(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]  dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,variance(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price,dt.d_year,
 """ + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id ,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
rows between 6 following and unbounded following) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #ERROR[8810] Executor ran into an internal failure
    
    _testmgr.testcase_end(desc)

def test068(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]   dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id brand_id
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand brand
,variance(ss_ext_sales_price) over (partition by  ss_ext_sales_price order by ss_ext_sales_price
rows between 3 preceding and unbounded following) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM dt
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where dt.d_date_sk = """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_item_sk = """ + gvars.g_schema_tpcds1x + """.ITEM.i_item_sk
and """ + gvars.g_schema_tpcds1x + """.ITEM.i_manager_id = 1
and dt.d_moy=11
and dt.d_year=2002
group by dt.d_year
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand
,""" + gvars.g_schema_tpcds1x + """.ITEM.i_brand_id
,ss_ext_sales_price
order by dt.d_year
,ext_price desc
,brand_id ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test069(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
substr(w_warehouse_name,1,20)
,sm_type
,web_name
,sum(case when (ws_ship_date_sk - ws_sold_date_sk <= 30 ) then 1 else 0 end)  over (partition by ws_ship_date_sk order by ws_ship_date_sk
rows between 10 preceding and unbounded following ) as "30 days"
,avg(case when (ws_ship_date_sk - ws_sold_date_sk > 30) and
(ws_ship_date_sk - ws_sold_date_sk <= 60) then 1 else 0 end )  over (partition by ws_ship_date_sk order by ws_ship_date_sk
rows between 10 preceding and unbounded following ) as "31-60 days"
,min(case when (ws_ship_date_sk - ws_sold_date_sk > 60) and
(ws_ship_date_sk - ws_sold_date_sk <= 90) then 1 else 0 end)  over (partition by ws_ship_date_sk order by ws_ship_date_sk
rows between 10 preceding and unbounded following ) as "61-90 days"
,max(case when (ws_ship_date_sk - ws_sold_date_sk > 90) and
(ws_ship_date_sk - ws_sold_date_sk <= 120) then 1 else 0 end) over (partition by ws_ship_date_sk order by ws_ship_date_sk
rows between 10 preceding and unbounded following )  as "91-120 days"
,stddev(case when (ws_ship_date_sk - ws_sold_date_sk  > 120) then 1 else 0 end)  over (partition by ws_ship_date_sk order by ws_ship_date_sk
rows between 10 preceding and unbounded following ) as ">120 days"
from
 """ + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.SHIP_MODE 
,""" + gvars.g_schema_tpcds1x + """.WEB_SITE 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
extract(year from d_date) = 1999
and ws_ship_date_sk   = d_date_sk
and ws_warehouse_sk   = w_warehouse_sk
and ws_ship_mode_sk   = sm_ship_mode_sk
and ws_web_site_sk    = web_site_sk
group by
1
,sm_type
,web_name
,ws_ship_date_sk
,ws_sold_date_sk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test070(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(ss_quantity)  over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following ) as agg1,
avg(ss_list_price) over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following )as agg2,
avg(ss_coupon_amt) over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following )as agg3,
avg(ss_sales_price) over (partition by  i_item_id order by i_item_id
rows between unbounded preceding and unbounded following )as agg4
from """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where ss_sold_date_sk = d_date_sk and
ss_item_sk = i_item_sk and
ss_cdemo_sk = cd_demo_sk and
ss_promo_sk = p_promo_sk and
cd_gender = 'F' and
cd_marital_status = 'D' and
cd_education_status = 'Advanced Degree' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 2000
group by
i_item_id,
ss_quantity,
ss_list_price,
ss_coupon_amt,
ss_sales_price;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test071(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,ship_carriers
,"year"
,sum(jan_sales) as jan_sales
,sum(feb_sales) as feb_sales
,sum(mar_sales) as mar_sales
,sum(apr_sales) as apr_sales
,sum(may_sales) as may_sales
,sum(jun_sales) as jun_sales
,sum(jul_sales) as jul_sales
,sum(aug_sales) as aug_sales
,sum(sep_sales) as sep_sales
,sum(oct_sales) as oct_sales
,sum(nov_sales) as nov_sales
,sum(dec_sales) as dec_sales
,sum(jan_sales/w_warehouse_sq_ft) as jan_sales_per_sq_foot
,sum(feb_sales/w_warehouse_sq_ft) as feb_sales_per_sq_foot
,sum(mar_sales/w_warehouse_sq_ft) as mar_sales_per_sq_foot
,sum(apr_sales/w_warehouse_sq_ft) as apr_sales_per_sq_foot
,sum(may_sales/w_warehouse_sq_ft) as may_sales_per_sq_foot
,sum(jun_sales/w_warehouse_sq_ft) as jun_sales_per_sq_foot
,sum(jul_sales/w_warehouse_sq_ft) as jul_sales_per_sq_foot
,sum(aug_sales/w_warehouse_sq_ft) as aug_sales_per_sq_foot
,sum(sep_sales/w_warehouse_sq_ft) as sep_sales_per_sq_foot
,sum(oct_sales/w_warehouse_sq_ft) as oct_sales_per_sq_foot
,sum(nov_sales/w_warehouse_sq_ft) as nov_sales_per_sq_foot
,sum(dec_sales/w_warehouse_sq_ft) as dec_sales_per_sq_foot
,sum(jan_net) as jan_net
,sum(feb_net) as feb_net
,sum(mar_net) as mar_net
,sum(apr_net) as apr_net
,sum(may_net) as may_net
,sum(jun_net) as jun_net
,sum(jul_net) as jul_net
,sum(aug_net) as aug_net
,sum(sep_net) as sep_net
,sum(oct_net) as oct_net
,sum(nov_net) as nov_net
,sum(dec_net) as dec_net    

from (
(select
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,'ZOUROS' || ',' || 'UPS' as ship_carriers
,d_year as "year"
,sum(case when d_month_seq = 1
then ws_sales_price* ws_quantity else 0 end)  over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jan_sales
,sum(case when d_month_seq = 2
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as feb_sales
,sum(case when d_month_seq = 3
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as mar_sales
,sum(case when d_month_seq = 4
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as apr_sales
,sum(case when d_month_seq = 5
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as may_sales
,sum(case when d_month_seq = 6
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jun_sales
,sum(case when d_month_seq = 7
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jul_sales
,sum(case when d_month_seq = 8
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as aug_sales
,sum(case when d_month_seq = 9
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as sep_sales
,sum(case when d_month_seq = 10
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as oct_sales
,sum(case when d_month_seq = 11
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as nov_sales
,sum(case when d_month_seq = 12
then ws_sales_price* ws_quantity else 0 end) over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as dec_sales
,sum(case when d_month_seq = 1
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jan_net
,sum(case when d_month_seq = 2
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as feb_net
,sum(case when d_month_seq = 3
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as mar_net
,sum(case when d_month_seq = 4
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as apr_net
,sum(case when d_month_seq = 5
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as may_net
,sum(case when d_month_seq = 6
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jun_net
,sum(case when d_month_seq = 7
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as jul_net
,sum(case when d_month_seq = 8
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as aug_net
,sum(case when d_month_seq = 9
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as sep_net
,sum(case when d_month_seq = 10
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as oct_net
,sum(case when d_month_seq = 11
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as nov_net
,sum(case when d_month_seq = 12
then ws_net_paid_inc_ship * ws_quantity else 0 end)over (partition by  ws_sales_price order by ws_sales_price
rows between unbounded preceding and unbounded following ) as dec_net
from
 """ + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.TIME_DIM 
,""" + gvars.g_schema_tpcds1x + """.SHIP_MODE 
where
ws_warehouse_sk =  w_warehouse_sk
and ws_sold_date_sk = d_date_sk
and ws_sold_time_sk = t_time_sk
and ws_ship_mode_sk = sm_ship_mode_sk
and d_year = 2001
and t_time between 5722 and 5722+28800
and sm_carrier in ('ZOUROS','UPS')
group by
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,d_year
,ws_sales_price
,d_month_seq
,ws_quantity
,ws_net_paid_inc_ship
)
union all
(select
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,'ZOUROS' || ',' || 'UPS' as ship_carriers
,d_year as "year"
,sum(case when d_month_seq = 1
then cs_ext_sales_price* cs_quantity else 0 end) as jan_sales
,sum(case when d_month_seq = 2
then cs_ext_sales_price* cs_quantity else 0 end) as feb_sales
,sum(case when d_month_seq = 3
then cs_ext_sales_price* cs_quantity else 0 end) as mar_sales
,sum(case when d_month_seq = 4
then cs_ext_sales_price* cs_quantity else 0 end) as apr_sales
,sum(case when d_month_seq = 5
then cs_ext_sales_price* cs_quantity else 0 end) as may_sales
,sum(case when d_month_seq = 6
then cs_ext_sales_price* cs_quantity else 0 end) as jun_sales
,sum(case when d_month_seq = 7
then cs_ext_sales_price* cs_quantity else 0 end) as jul_sales
,sum(case when d_month_seq = 8
then cs_ext_sales_price* cs_quantity else 0 end) as aug_sales
,sum(case when d_month_seq = 9
then cs_ext_sales_price* cs_quantity else 0 end) as sep_sales
,sum(case when d_month_seq = 10
then cs_ext_sales_price* cs_quantity else 0 end) as oct_sales
,sum(case when d_month_seq = 11
then cs_ext_sales_price* cs_quantity else 0 end) as nov_sales
,sum(case when d_month_seq = 12
then cs_ext_sales_price* cs_quantity else 0 end) as dec_sales
,sum(case when d_month_seq = 1
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as jan_net
,sum(case when d_month_seq = 2
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as feb_net
,sum(case when d_month_seq = 3
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as mar_net
,sum(case when d_month_seq = 4
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as apr_net
,sum(case when d_month_seq = 5
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as may_net
,sum(case when d_month_seq = 6
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as jun_net
,sum(case when d_month_seq = 7
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as jul_net
,sum(case when d_month_seq = 8
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as aug_net
,sum(case when d_month_seq = 9
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as sep_net
,sum(case when d_month_seq = 10
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as oct_net
,sum(case when d_month_seq = 11
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as nov_net
,sum(case when d_month_seq = 12
then cs_net_paid_inc_ship_tax * cs_quantity else 0 end) as dec_net
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
,""" + gvars.g_schema_tpcds1x + """.TIME_DIM 
,""" + gvars.g_schema_tpcds1x + """.SHIP_MODE 
where
cs_warehouse_sk =  w_warehouse_sk
and cs_sold_date_sk = d_date_sk
and cs_sold_time_sk = t_time_sk
and cs_ship_mode_sk = sm_ship_mode_sk
and d_year = 2001
and t_time between 5722 and 5722+28800
and sm_carrier in ('ZOUROS','UPS')
group by
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,d_year
)
) x
group by
w_warehouse_name
,w_warehouse_sq_ft
,w_city
,w_county
,w_state
,w_country
,ship_carriers
,"year"
order by w_warehouse_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test085(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows 49001 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test086(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test087(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test088(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows unbounded preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test089(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows 5000 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test090(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test091(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey   order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test092(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test093(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test094(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test095(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey  order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test096(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test097(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test098(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test099(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test100(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #testsfor function sum:
    _testmgr.testcase_end(desc)

def test101(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test102(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test103(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows unbounded preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test104(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test105(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test106(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test107(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test108(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test109(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test110(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test111(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test112(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test113(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test114(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test115(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test116(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #for max:
    _testmgr.testcase_end(desc)

def test117(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test118(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test119(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test120(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test121(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test122(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test123(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test124(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test125(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test126(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test127(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test128(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test129(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test130(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test131(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test132(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #For min:
    _testmgr.testcase_end(desc)

def test133(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test134(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test135(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test136(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test137(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test138(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test139(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test140(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test141(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test142(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test143(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test144(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test145(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test146(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test147(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #tests for count:
    _testmgr.testcase_end(desc)

def test148(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test149(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test150(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test151(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test152(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test153(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test154(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test155(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test156(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test157(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test158(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test159(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test160(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test161(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test162(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #for variance:
    _testmgr.testcase_end(desc)

def test163(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test164(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test165(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test166(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test167(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test168(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test169(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  current row and  4 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test170(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test171(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  6 preceding and  current row) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test172(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  10 preceding    and unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test173(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  5 preceding    and  21 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test174(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  21 following    and  unbounded following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test175(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  8598745 following and 9876584 following) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test176(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  28598745 preceding and 19876584 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 59450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test177(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]  """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  4 preceding and 4 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 543948;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test178(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 preceding and 4 preceding) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 preceding and 3 preceding) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #TestS324
    _testmgr.testcase_end(desc)

def test179(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and 4 preceding) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 preceding and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    
    _testmgr.testcase_end(desc)

def test180(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and current row) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 preceding and 3 following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test181(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and unbounded following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test182(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and 4 following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and 3 following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test183(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between current row and current row) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 following  and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test184(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between current row and unbounded following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 5 following and 6 following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test185(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between current row and 4 following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 following and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test186(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 preceding and current row) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and 3 following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #Q2:
    _testmgr.testcase_end(desc)

def test187(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 preceding and unbounded following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test188(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 preceding and 4 following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and 3 following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test189(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and unbounded following)  as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 4 preceding and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test190(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and 6 following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and current row) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test191(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and 6 following) as ActBal,    

sum(p_partkey) over (partition by p_partkey order by p_partkey desc
rows current row) as PartKey,
s_name,
n_name,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test192(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
max(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and 6 following) as ActBal,    

count(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test193(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
max(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and 6 following) as ActBal,    

count(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test194(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
count(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 following and unbounded following) as ActBal,    

min(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between current row and 5 following) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    _testmgr.testcase_end(desc)

def test195(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
min(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between current row and unbounded following) as ActBal,    

max(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between 5 following and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q2:
    
    _testmgr.testcase_end(desc)

def test196(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
max(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows between 5 preceding and unbounded following) as ActBal,    

avg(p_partkey) over (partition by p_partkey order by p_partkey desc
rows between unbounded preceding and unbounded following) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test197(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
max(s_acctbal) over (partition by p_partkey order by p_partkey desc
rows 5 preceding) as ActBal,    

avg(p_partkey) over (partition by p_partkey order by p_partkey desc
rows unbounded preceding) as PartKey,
s_name,
n_name,
p_mfgr
s_phone
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost)
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test199(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and 5 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3a
    _testmgr.testcase_end(desc)

def test200(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3b:
    _testmgr.testcase_end(desc)

def test202(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3c:
    _testmgr.testcase_end(desc)

def test203(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and 5 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3d:
    _testmgr.testcase_end(desc)

def test204(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between current row and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test205(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3e:
    _testmgr.testcase_end(desc)

def test206(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between current row and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3f:
    _testmgr.testcase_end(desc)

def test207(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between current row and 25 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3g:
    _testmgr.testcase_end(desc)

def test208(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 250 preceding and 150 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3h:
    _testmgr.testcase_end(desc)

def test209(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 50 preceding and 25 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test210(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 50 preceding and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test211(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 50 preceding and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test212(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 50 preceding and 25 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test213(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 50 following and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q3:
    _testmgr.testcase_end(desc)

def test214(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 25 following and 500 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Q6:
    _testmgr.testcase_end(desc)

def test215(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test216(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test217(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test218(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test219(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test220(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test221(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and 10 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test223(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 5 preceding and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test224(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 5 preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test225(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 5 preceding and 4 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test226(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 5 following and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test227(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 500 following and 800 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test228(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    
    _testmgr.testcase_end(desc)

def test229(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and current row) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    
    _testmgr.testcase_end(desc)

def test230(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
min(l_extendedprice * (1 - l_discount)) as sum_disc_price,
max(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
stddev(l_quantity) as avg_qty,
count(l_extendedprice) as avg_price,
variance(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test231(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 5 following ) as sum_qty ,
min(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    
    _testmgr.testcase_end(desc)

def test232(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and current row) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test233(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and unbounded following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    
    _testmgr.testcase_end(desc)

def test234(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and 5 following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test235(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 5 preceding and 4 preceding)  as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    
    _testmgr.testcase_end(desc)

def test236(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 5 preceding and current row) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test237(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 5 preceding and unbounded following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test238(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 5 following and unbounded following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1
    _testmgr.testcase_end(desc)

def test239(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select  [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 5 following and 6 following) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified
    _testmgr.testcase_end(desc)

def test240(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
min(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
max(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
count(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
stddev(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding )as avg_price,
variance(l_discount) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified--only preceding
    _testmgr.testcase_end(desc)

def test241(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and current row ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between current row and current row ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between 8 preceding and 5 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 10 preceding and current row ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 10 preceding and 5 preceding )as avg_price,
avg(l_discount) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified-Mixed
    #Found a save abend from MXCI
    _testmgr.testcase_end(desc)

def test242(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and current row) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between current row and current row ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and unbounded following ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between current row and 5 following)as avg_price,
avg(l_discount) over (partition by  l_quantity order by l_quantity
rows between 6 preceding and 4 preceding ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified-Only mixed  'following'
    _testmgr.testcase_end(desc)

def test243(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 5 following and unbounded following) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between current row and unbounded following ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between current row and 10 following ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 10 preceding and unbounded following ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 6 preceding and 10 following)as avg_price,
avg(l_discount) over (partition by  l_quantity order by l_quantity
rows between 4 following and 6 following ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified-Only mixed 'unbounded following'
    _testmgr.testcase_end(desc)

def test244(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 5 following and unbounded following) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between current row and unbounded following ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between 5 following and unbounded following ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 10 preceding and unbounded following ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 6 preceding and unbounded following)as avg_price,
avg(l_discount) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q1-- Modified
    _testmgr.testcase_end(desc)

def test245(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between 10 following  and 15 following ) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity)
over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and current row ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between 15 preceding and 10 following )as avg_price,
avg(l_discount) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_discount,
l_extendedprice
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3
    _testmgr.testcase_end(desc)

def test246(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and 150000 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3
    _testmgr.testcase_end(desc)

def test247(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test248(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test249(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test250(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test251(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test252(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test253(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test254(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 1000 preceding and 750 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test255(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 preceding and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test256(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 preceding and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test257(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between  10 preceding and 15 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test258(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 following and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test259(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 following and 12 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3
    _testmgr.testcase_end(desc)

def test260(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and 12 following ) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3a
    _testmgr.testcase_end(desc)

def test261(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3b
    _testmgr.testcase_end(desc)

def test262(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3c
    _testmgr.testcase_end(desc)

def test263(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3d
    _testmgr.testcase_end(desc)

def test264(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q3e
    _testmgr.testcase_end(desc)

def test265(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test266(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test267(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_price,
avg(l_discount)  over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test268(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and current row ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and unbounded following ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 following ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between current row and 10 following ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between current row and unbounded following ) as avg_price,
avg(l_discount)  over (partition by  l_quantity order by l_quantity
rows between 5 following and 6 following ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q4
    
    _testmgr.testcase_end(desc)

def test269(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
count(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and 10 preceding ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test270(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
stddev(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and current row ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test271(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
avg(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and unbounded following ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test272(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and 10 following ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test273(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
max(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and current row ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test274(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
sum(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between current row and current row ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q5
    _testmgr.testcase_end(desc)

def test275(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test276(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 12 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test277(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test278(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 5 preceding and 10 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test279(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test280(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 100 following and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test281(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
n_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 200 following and 300 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and o_orderdate >= date '1996-01-01'
and o_orderdate < date '1996-01-01' + interval '1' year
group by
n_name,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q6
    _testmgr.testcase_end(desc)

def test282(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test283(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test284(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test285(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test286(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test287(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test288(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 10 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test289(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 25 preceding and 10 preceding) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test290(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test291(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test292(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 5 preceding and 4 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test293(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 5 following and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test294(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice * l_discount) over (partition by l_extendedprice order by l_extendedprice
rows between 5 following and 10 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q7
    _testmgr.testcase_end(desc)

def test295(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test296(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test297(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test298(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test299(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test300(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test301(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 100 following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test302(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 5 preceding )
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test303(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test304(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test305(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test306(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and unbounded following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test307(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
supp_nation,
cust_nation,
l_year,
sum(volume) as REVENUE 
from
(
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract (year from l_shipdate) as l_year,
stddev(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and 10 following)
as volume
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = 'ARGENTINA' and n2.n_name = 'ROMANIA')
or (n1.n_name = 'ROMANIA' and n2.n_name = 'ARGENTINA')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation, l_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q8
    _testmgr.testcase_end(desc)

def test308(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test309(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test310(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test311(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test312(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test313(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test314(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 10 following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test315(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 250 preceding and 100 preceding) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test316(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test317(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test318(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 5 following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test319(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and unbounded following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test320(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_year,
sum(case when nation='ROMANIA' then volume else 0 end )/ sum(volume) as mkt_share
from
(
select
n2.n_name as NATION,
extract( year from o_orderdate ) as o_year,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 8 following and 10 following) as volume
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.NATION n1,
 """ + gvars.g_schema_tpch2x + """.NATION n2,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'EUROPE'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = 'LARGE POLISHED BRASS'
) all_nations
group by
o_year
order by
o_year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q9
    _testmgr.testcase_end(desc)

def test321(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test322(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test323(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test324(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test325(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test326(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test327(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and 10 following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test328(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 100 preceding and 75 preceding)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test329(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test330(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test331(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 12 following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test332(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and unbounded following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test333(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
NATION,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as NATION,
extract (year from o_orderdate) as o_year,
stddev(l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)
over (partition by l_extendedprice order by l_extendedprice
rows between 3 following and 5 following)  as amount    

from
 """ + gvars.g_schema_tpch2x + """.PART, """ + gvars.g_schema_tpch2x + """.SUPPLIER, """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.PARTSUPP, """ + gvars.g_schema_tpch2x + """.ORDERS, """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%navy%'
) profit
group by
NATION,
o_year
order by
NATION,
o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q10
    
    _testmgr.testcase_end(desc)

def test334(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test335(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test336(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test337(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test338(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test339(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test340(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 10 following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test341(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 5 preceding) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test342(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test343(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test344(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 12 following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test345(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and unbounded following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test346(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and 12 following) as REVENUE,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '1994-08-01'
and o_orderdate < date '1994-08-01' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment,
l_extendedprice,
l_discount
order by
 REVENUE desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q11
    _testmgr.testcase_end(desc)

def test347(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and 4 preceding ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test348(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and current row ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test349(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and unbounded following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test350(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and 10 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test351(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and current row ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test352(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and unbounded following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test353(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and 10 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test354(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 10 preceding and 5 preceding ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test355(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 12 preceding and current row ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test356(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 10 preceding and unbounded following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test357(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 10 preceding and 5 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test358(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 10 following and unbounded following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test359(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 10 preceding and 5 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12
    _testmgr.testcase_end(desc)

def test360(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 preceding )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12a
    _testmgr.testcase_end(desc)

def test361(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and current row)  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12b
    _testmgr.testcase_end(desc)

def test362(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
stddev((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following )  as high_line_count,
stddev(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 21 following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12c
    _testmgr.testcase_end(desc)

def test363(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
count((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 15 following )  as high_line_count,
count(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row  and current row) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12d
    _testmgr.testcase_end(desc)

def test364(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,    

avg((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row  and current row )  as high_line_count,
avg(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row  and unbounded following) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12e
    _testmgr.testcase_end(desc)

def test365(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
min((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row  and unbounded following )  as high_line_count,
min(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row  and 15 following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12f
    _testmgr.testcase_end(desc)

def test366(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
max((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row  and 15 following )  as high_line_count,
max(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q12g
    _testmgr.testcase_end(desc)

def test367(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,    

stddev((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as std_high_line_count,    

stddev(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and current row) as  std_low_line_count,    
    
count((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as cnt_high_line_count,    

count(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as cnt_low_line_count,    
    
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as sum_high_line_count,    

sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as sum_low_line_count,    
    
avg((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as avg_high_line_count,    

avg(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as avg_low_line_count,    
    
min((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as min_high_line_count,    

min(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as min_low_line_count,    

max((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding )  as max_high_line_count,    

max(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)    

over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 preceding ) as max_low_line_count    
    
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #x13
    _testmgr.testcase_end(desc)

def test368(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between unbounded preceding and 4 preceding)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test369(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between unbounded preceding and current row)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test370(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between unbounded preceding and unbounded following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test371(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between unbounded preceding and 10 following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test372(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between current row and current row)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test373(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between current row and unbounded following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test374(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between current row and 15 following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test375(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 8 preceding and 4 preceding)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test376(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 10 preceding and current row)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test377(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 10 preceding and unbounded following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test378(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 10 preceding and 8 following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test379(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 10 following and unbounded following)
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test380(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
c_count,
count(*) as custdist
from
(
select
count(o_orderkey) over (partition by o_orderkey order by o_orderkey
rows between 10 following and 12 following )
as  c_count
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER, """ + gvars.g_schema_tpch2x + """.ORDERS where
c_custkey = o_custkey
and o_comment not like '%unusual%accounts%'
group by
c_custkey,
o_orderkey
) c_orders
group by
c_count
order by
custdist desc,
c_count desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q14
    _testmgr.testcase_end(desc)

def test381(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test382(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test383(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test384(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test385(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test386(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test387(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between current row and 10 following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test388(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 50 preceding and 40 preceding)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test389(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and current row)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test390(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and unbounded following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test391(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 preceding and 4 following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test392(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and unbounded following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test393(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare  xx  from
select [last 0]
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between 10 following and 15 following)as promo_revenue    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
l_partkey = p_partkey
and l_shipdate >= date '1995-08-01'
and l_shipdate < date '1995-08-01' + interval '1' month
group by
l_extendedprice,
l_discount
order by
promo_revenue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q15
    _testmgr.testcase_end(desc)

def test394(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between unbounded preceding and 4 preceding) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
max(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test395(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between unbounded preceding and 4 preceding) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
avg(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test396(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between unbounded preceding and current row) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
count(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test397(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between unbounded preceding and unbounded following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
avg(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test398(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between unbounded preceding and 4 following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
stddev(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test399(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between current row and current row) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
min(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test400(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between current row and unbounded following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
avg(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test401(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between current row and 100 following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
count (total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test402(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between 12 preceding and current row) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
max(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test403(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between 20 preceding and 50 following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
min(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test404(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between 5 preceding and unbounded following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
count(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test405(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_suppkey,
s_name,
s_address,
s_phone,
avg(total_revenue)  over (partition by total_revenue order by total_revenue desc
rows between 4 following and 6 following) as totalrevenue
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 REVENUE 
where
s_suppkey = supplier_no
and total_revenue = (
select
max(total_revenue)
from
 REVENUE  )
order by
s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test406(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
p_brand,
p_type,
p_size,
count(ps_suppkey) over (partition by ps_suppkey order by ps_suppkey
rows between unbounded preceding and 4 preceding)
as supplier_cnt
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = ps_partkey
and p_brand <> 'Brand#22'
and p_type not like 'SMALL ANODIZED%'
and p_size in (14, 20, 17, 11, 5, 7, 6, 43)
and ps_suppkey not in (
select
s_suppkey
from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER 
where
s_comment like '%Customer%Complaints%'
)
group by
p_brand,
p_type,
p_size,
ps_suppkey
order by
supplier_cnt desc,
p_brand,
p_type,
p_size;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q17
    _testmgr.testcase_end(desc)

def test407(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test408(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and current row) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test409(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and unbounded following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test410(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 10 following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test411(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and current row) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test412(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and unbounded following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test413(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between current row and 12 following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test414(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and 4 preceding) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test415(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and current row) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test416(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and unbounded following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test417(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and 10 following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test418(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 2 following and 6 following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test419(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice / 7.0)
over (partition by l_extendedprice order by l_extendedprice
rows between 12 preceding and unbounded following) as avg_yearly    

from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_partkey = l_partkey
and p_brand = 'Brand#21'
and p_container = 'SM CASE'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = p_partkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18
    _testmgr.testcase_end(desc)

def test420(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
stddev(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 preceding ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18a
    _testmgr.testcase_end(desc)

def test421(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and current row ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18b
    _testmgr.testcase_end(desc)

def test422(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
count(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18c
    _testmgr.testcase_end(desc)

def test423(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
avg(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18d
    _testmgr.testcase_end(desc)

def test424(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
max(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and current row ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18e
    _testmgr.testcase_end(desc)

def test425(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
min(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and unbounded following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q18f
    _testmgr.testcase_end(desc)

def test426(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
stddev(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 preceding ) as std_lquantity,    

count(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following ) as cnt_lquantity,    

sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 5 preceding and 4 following ) as sum_lquantity,    

avg(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 5 following and 40 following ) as avg_lquantity,    

min(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and 4 following ) as min_lquantity,    

max(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 following and unbounded following ) as max_lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 116)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #q19
    
    _testmgr.testcase_end(desc)

def test427(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
sum(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19a
    
    _testmgr.testcase_end(desc)

def test428(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

avg(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19b
    
    _testmgr.testcase_end(desc)

def test429(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

max(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19c
    
    _testmgr.testcase_end(desc)

def test430(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

min(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19d
    
    _testmgr.testcase_end(desc)

def test431(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

stddev(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19e
    
    _testmgr.testcase_end(desc)

def test432(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

count(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q19f
    _testmgr.testcase_end(desc)

def test433(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]    

count(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as cnt_revenue,
stddev(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as std_revenue,    

max(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as max_revenue,    

min(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as min_revenue,    

avg(l_extendedprice* (1 - l_discount))
over (partition by l_extendedprice order by l_extendedprice
rows between 2 preceding and 1 preceding)
as avg_revenue
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM,
 """ + gvars.g_schema_tpch2x + """.PART 
where
(
p_partkey = l_partkey
and p_brand = 'Brand#13'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 2 and l_quantity <= 2 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#45'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 20 and l_quantity <= 20 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#12'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 25 and l_quantity <= 25 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
and
l_extendedprice > 112335;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q20
    _testmgr.testcase_end(desc)

def test434(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_name,
s_address,
sum(s_acctbal) over (partition by s_acctbal  order by s_acctbal desc
rows between unbounded preceding and 4 preceding) as ActBal    

from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey in (
select
ps_suppkey
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP 
where
ps_partkey in (
select
p_partkey
from
 """ + gvars.g_schema_tpch2x + """.PART 
where
p_name like 'midnight%'
)
and ps_availqty > (
select
0.5 * sum(l_quantity)
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_partkey = ps_partkey
and l_suppkey = ps_suppkey
and l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
)
)
and s_nationkey = n_nationkey
and n_name = 'VIETNAM'
order by
s_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q21
    
    _testmgr.testcase_end(desc)

def test435(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_name,
count(*)  numwait,
sum(l_extendedprice* (1 - l_discount)) over (partition by l_extendedprice order by l_extendedprice
rows between unbounded preceding and 4 preceding) as REVENUE     

from
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.LINEITEM l1,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM l2
where
l2.l_orderkey = l1.l_orderkey
and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM l3
where
l3.l_orderkey = l1.l_orderkey
and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = 'MOROCCO'
group by
s_name,
l_extendedprice,
l_discount
order by
numwait desc,
s_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q22
    _testmgr.testcase_end(desc)

def test436(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
cntrycode,
count(*) as numcust,
sum(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as totacctbal
from
(
select
substr(c_phone, 1, 2) as cntrycode,
c_acctbal
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER 
where
substr(c_phone,1, 2) in
('20', '15', '13', '24', '33', '34', '11')
and c_acctbal > (
select
avg(c_acctbal)
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER 
where
c_acctbal > 9990.00
and substr(c_phone, 1, 2) in
('20', '15', '13', '24', '33', '34', '11')
)
and not exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_custkey = c_custkey
)
) custsale
group by
cntrycode,
c_acctbal
order by
cntrycode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #q22a (Count,stddev,sum,avg,min and max with windows)
    _testmgr.testcase_end(desc)

def test437(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
cntrycode,
count(*) as numcust,
sum(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding)  as sum_totacctbal,    

avg(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as avg_totacctbal,    

max(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as max_totacctbal,    

min(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as min_totacctbal,    

stddev(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as std_totacctbal,    

count(c_acctbal)
over (partition by c_acctbal  order by c_acctbal
rows between 2 preceding and 1 preceding) as count_totacctbal    

from
(
select
substr(c_phone, 1, 2) as cntrycode,
c_acctbal
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER 
where
substr(c_phone,1, 2) in
('20', '15', '13', '24', '33', '34', '11')
and c_acctbal > (
select
avg(c_acctbal)
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER 
where
c_acctbal > 9999.00
and substr(c_phone, 1, 2) in
('20', '15', '13', '24', '33', '34', '11')
)
and not exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_custkey = c_custkey
)
) custsale
group by
cntrycode,
c_acctbal
order by
cntrycode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Mix
    #max 590000
    _testmgr.testcase_end(desc)

def test438(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and 2 preceding) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and 2 following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test439(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and 2 following) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and unbounded following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 4 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test440(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 5 following) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test441(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and current row) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 5 following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 40 preceding and 20 preceding) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test442(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 3 following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 40 preceding and 25 preceding) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 24 preceding and 16 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test443(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 4 following) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 10 preceding and 5 preceding) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 40 preceding and 12 following) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 24 preceding and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test444(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 preceding) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and 4 following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and unbounded following) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test445(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 6 preceding and 3 preceding) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and 6 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test446(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 6 preceding and 3 preceding) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and 6 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test447(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and 5 following) as stddev,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and unbounded following) as AvgPrice,
Min(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and current row) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 following and 4 following) as MaxPrice,
sum(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #count and variance
    _testmgr.testcase_end(desc)

def test448(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and 2 preceding) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and 2 following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test449(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and 2 following) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and unbounded following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 4 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test450(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and unbounded following) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between unbounded preceding and current row) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 5 following) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test451(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between  unbounded preceding and current row) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 5 following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 40 preceding and 26 preceding) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test452(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and current row) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 3 following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 42 preceding and 15 preceding) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 400 preceding and 106 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test453(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and 4 following) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 30 preceding and 15 preceding) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 40 preceding and 10 following) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 400 preceding and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test454(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between current row and unbounded following) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 preceding) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and 4 following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and unbounded following) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test455(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 6 preceding and 3 preceding) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and 6 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test456(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 6 preceding and 3 preceding) as stddev,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and 2 following) as AvgPrice,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and unbounded following) as MinPrice,
Max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and current row) as MaxPrice,
avg(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and 6 following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test457(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and 5 following) as stddev,
max(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 preceding and unbounded following) as AvgPrice,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 preceding and current row) as MinPrice,
variance(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 3 following and 4 following) as MaxPrice,
count(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,o_totalprice rows between 4 following and unbounded following) as SumPrice,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test458(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0] """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey, """ + gvars.g_schema_tpch2x + """.LINEITEM.l_quantity, o_totalprice, o_orderstatus,
stddev(o_totalprice) over (partition by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey order by """ + gvars.g_schema_tpch2x + """.LINEITEM.l_partkey,
o_totalprice rows between  unbounded preceding and 5 preceding) as stddev,
o_orderdate
from """ + gvars.g_schema_tpch2x + """.LINEITEM, """ + gvars.g_schema_tpch2x + """.ORDERS 
where """ + gvars.g_schema_tpch2x + """.LINEITEM.l_orderkey =""" + gvars.g_schema_tpch2x + """.ORDERS.o_orderkey
and o_totalprice > 343000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Tests with wisc32 queries: (for dense_rank)
    _testmgr.testcase_end(desc)

def test459(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and 5 preceding) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test460(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test461(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test462(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and 5 following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test463(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test464(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test465(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and 5 following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test466(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and 4 preceding) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test467(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test468(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test469(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 following and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test470(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 following and 8 following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test471(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and 5 preceding) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test472(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test473(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test474(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between unbounded preceding and 5 following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test475(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test476(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and unbounded following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test477(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between current row and 5 following) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test478(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and 4 preceding) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test479(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and current row) as unique_1,
dense_rank() over (partition by unique1 order by sum(unique1)) as DenseRank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test480(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and unbounded following) as unique_1,
rank() over (partition by unique1 order by sum(unique1)) as Rank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test481(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 preceding and 4 following) as unique_1,
rank() over (partition by unique1 order by sum(unique1)) as Rank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test482(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 following and unbounded following) as unique_1,
rank() over (partition by unique1 order by sum(unique1)) as Rank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test483(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from select [last 0] ten, count(unique1)
over (partition by unique1 order by sum(unique1)
rows between 5 following and 8 following) as unique_1,
rank() over (partition by unique1 order by sum(unique1)) as Rank
from """ + gvars.g_schema_wisc32 + """.ABASE 
where fiftypercent = 1 group  by ten,unique1 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test484(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*sum(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between unbounded preceding and 5 preceding) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test485(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between unbounded preceding and current row) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test486(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between unbounded preceding and unbounded following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test487(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between unbounded preceding and 4 following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test488(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between current row and current row) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test489(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between current row and 4 following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test490(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between current row and unbounded following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test491(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 5 preceding and 4 preceding) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test492(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 4 preceding and current row) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test493(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 4 preceding and 5 following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test494(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 6 preceding and unbounded following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test495(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 4 following and unbounded following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test496(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*avg(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between 4 following and 6 following) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test497(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from select [last 0] b.ten,
1e0*variance(b.two * b.evenonepercent
+ b.four / b.oddonepercent
+ b.ten + (b.evenonepercent + 2)
+ b.twenty * (b.oddonepercent * 3)
+ b.onepercent / (b.evenonepercent + 500)
+ b.tenpercent + (b.oddonepercent * 600)
+ b.twentypercent * (b.evenonepercent + 7000)
+ b.fiftypercent / (b.oddonepercent * 8000)
+ b.evenonepercent + (b.evenonepercent + 90000)
+ b.oddonepercent * (b.oddonepercent * 10000))
over (partition by b.two,b.onepercent  order by b.two,b.onepercent rows between unbounded preceding and 5 preceding) as nsolap
from """ + gvars.g_schema_wisc32 + """.BBASE b
where b.fiftypercent = 1
group by b.ten,
b.two,
b.onepercent,
b.evenonepercent,
b.four,
b.oddonepercent,
b.twenty,
b.tenpercent,
b.twentypercent,
b.fiftypercent
order by
b.ten for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test498(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between unbounded preceding and 2500 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test499(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  o_orderdate,
o_shippriority
l_orderkey, sum(l_extendedprice * (1 - l_discount))
over (partition by o_shippriority,o_orderdate order by o_shippriority, o_orderdate
rows between 400000 following and 350000 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
c_mktsegment = 'MACHINERY'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '1995-03-05'
and l_shipdate > date '1995-03-05'
and o_totalprice < 450000
group by
l_orderkey,
o_orderdate,
o_shippriority,
l_extendedprice,
l_discount
order by
 REVENUE desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #Mix
    _testmgr.testcase_end(desc)

def test500(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test501(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and current row ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test502(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test503(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between unbounded preceding and 10 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test504(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test505(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and unbounded following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test506(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between current row and 5 following) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test507(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 15 preceding and 10 preceding ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test508(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 preceding and current row) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test509(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 15 preceding and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test510(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 15 preceding and 10 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test511(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 15 following and unbounded following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test512(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]  l_partkey, l_quantity,
sum(l_extendedprice * l_discount)
over (partition by  l_partkey, l_quantity order by l_partkey, l_quantity
rows between 10 following  and 15 following ) as REVENUE 
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate >= date '1996-01-01'
and l_shipdate < date '1996-01-01' + interval '1' year
and l_discount between 0.02 - 0.01 and 0.02 + 0.01
and l_quantity < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test513(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test514(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test515(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test516(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #Mix
    _testmgr.testcase_end(desc)

def test517(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #Mix
    _testmgr.testcase_end(desc)

def test518(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test519(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_returnflag,
l_linestatus,
sum(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_qty ,
sum(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_base_price ,
sum(l_extendedprice * (1 - l_discount)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as sum_charge,
avg(l_quantity) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_qty,
avg(l_extendedprice) over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_price,
avg(l_discount)  over (partition by  l_quantity order by l_quantity
rows between unbounded preceding and 10 preceding ) as avg_disc,
count(*) as count_order
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
l_shipdate <= date '1998-12-01' - interval '72' day(2)
group by
l_returnflag,
l_linestatus,
l_quantity,
l_extendedprice,
l_discount,
l_tax
order by
l_returnflag,
l_linestatus;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Mix
    
    _testmgr.testcase_end(desc)

def test520(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and 10 preceding ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test521(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and current row) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test522(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and unbounded following) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test523(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between unbounded preceding and 5 following)  as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test524(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between current row and current row) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test525(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between current row and unbounded following) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test526(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between current row and 5 following) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test527(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 10 preceding and 8 preceding) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test528(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 5 preceding and current row) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test529(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 5 preceding and unbounded following) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test530(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 10 preceding and 5 following ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test531(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 5 following and unbounded following    ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test532(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 5 following and 10 following    ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test533(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
o_orderkey,
o_orderpriority,
min(o_totalprice) over (partition by  o_custkey, o_orderkey  order by o_custkey, o_orderkey
rows between 500 preceding and current row    ) as ordercount
from
 """ + gvars.g_schema_tpch2x + """.ORDERS 
where
o_orderdate >= date '1993-10-01'
and o_orderdate < date '1993-10-01' + interval '3' month
and exists (
select
*
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority,
o_orderkey,
o_custkey,
o_totalprice
order by
o_orderpriority;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test534(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and 4 preceding ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum(ps_supplycost * ps_availqty) * 0.0000001000    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test535(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and current row) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test536(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and unbounded following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test537(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between unbounded preceding and 100 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test538(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and current row ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test539(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and unbounded following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test540(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between current row and 100 following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test541(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 preceding and 50 preceding) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test542(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 preceding and current row) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test543(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 preceding and unbounded following ) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test544(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 preceding and 200 following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test545(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 following and unbounded following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test546(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
ps_partkey,
sum(ps_supplycost * ps_availqty) over (partition by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey order by """ + gvars.g_schema_tpch2x + """.PARTSUPP.ps_suppkey
rows between 100 following and 200 following) as value0
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
group by
ps_suppkey,
ps_supplycost,
PS_AVAILQTY,
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum((ps_supplycost * ps_availqty) * 0.0000001000)    

from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION 
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'BRAZIL'
)
order by value0 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #x12
    _testmgr.testcase_end(desc)

def test547(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 preceding )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and current row) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test548(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test549(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row and current row )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test550(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row and 10 following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 40 preceding and 20 preceding ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test551(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 100 preceding and current row)  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test552(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and 20 following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 10 following and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test553(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 100 following and 200 following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 200 following and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #here boss
    _testmgr.testcase_end(desc)

def test554(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and current row )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between  unbounded preceding and 4 preceding ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test555(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between  unbounded preceding and 4 following  )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test556(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between current row and unbounded following  )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row and current row  ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test557(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 30 preceding and 20 preceding  )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between current row and 10 following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test558(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and unbounded following  )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 100 preceding and current row ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test559(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between 10 following and unbounded following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and 20 following  ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test560(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
l_shipmode,
sum((case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end))    

over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following )  as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end)
over (partition by  l_orderkey  order by l_orderkey
rows between 20 following and unbounded following ) as low_line_count
from
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey = l_orderkey
and l_shipmode in ('MAIL', 'TRUCK')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '1993-01-01'
and l_receiptdate < date '1993-01-01' + interval '12' month
group by
l_shipmode,
l_orderkey,
o_orderpriority
order by
l_shipmode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #x18
    _testmgr.testcase_end(desc)

def test561(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 4 preceding ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test562(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and current row) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test563(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and unbounded following) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test564(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between unbounded preceding and 20 following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test565(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and current row ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test566(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and unbounded following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test567(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between current row and 12 following) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test568(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and 8 preceding) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #partition by clause
    _testmgr.testcase_end(desc)

def test569(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over ( partition by c_custkey order by l_orderkey
rows between 10 preceding and 8 preceding ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test570(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and current row) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test571(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and unbounded following) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test572(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 preceding and 14 following) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test573(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 following and unbounded following ) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test574(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity) over (partition by  l_orderkey  order by l_orderkey
rows between 10 following and 18 following) as lquantity    

from
 """ + gvars.g_schema_tpch2x + """.CUSTOMER,
 """ + gvars.g_schema_tpch2x + """.ORDERS,
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
where
o_orderkey in (
select
l_orderkey
from
 """ + gvars.g_schema_tpch2x + """.LINEITEM 
group by
l_orderkey having
sum(l_quantity) > 312
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
l_orderkey,
l_quantity
order by
o_totalprice desc,
o_orderdate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test575(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select [last 0]
s_acctbal,
s_name,
n_name,
p_partkey,
p_mfgr,
s_address,
s_phone,
s_comment
from
 """ + gvars.g_schema_tpch2x + """.PART,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = 5
and p_type like '%COPPER'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
and ps_supplycost = (
select
min(ps_supplycost) over (partition by  """ + gvars.g_schema_tpch2x + """.PART.p_partkey, """ + gvars.g_schema_tpch2x + """.PART.p_mfgr  order by """ + gvars.g_schema_tpch2x + """.PART.p_partkey, """ + gvars.g_schema_tpch2x + """.PART.p_mfgr
rows between unbounded preceding and 10 preceding ) as partsuppcost
from
 """ + gvars.g_schema_tpch2x + """.PARTSUPP,
 """ + gvars.g_schema_tpch2x + """.SUPPLIER,
 """ + gvars.g_schema_tpch2x + """.NATION,
 """ + gvars.g_schema_tpch2x + """.REGION 
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'AFRICA'
)
order by
s_acctbal desc,
n_name,
s_name,
p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4391')
    
    _testmgr.testcase_end(desc)

def test576(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select  [last 0]
substr(w_warehouse_name,1,20)
,sm_type
,cc_name
,sum(case when (cs_ship_date_sk - cs_sold_date_sk <= 30 ) then 1 else 0 end) over (partition by cs_ship_date_sk order by cs_ship_date_sk
rows between unbounded preceding and unbounded following ) as "30 days"
,avg(case when (cs_ship_date_sk - cs_sold_date_sk > 30) and
(cs_ship_date_sk - cs_sold_date_sk <= 60) then 1 else 0 end ) over (partition by cs_ship_date_sk order by cs_ship_date_sk
rows between unbounded preceding and unbounded following ) as "31-60 days"
,count(case when (cs_ship_date_sk - cs_sold_date_sk > 60) and
(cs_ship_date_sk - cs_sold_date_sk <= 90) then 1 else 0 end)  over (partition by cs_ship_date_sk order by cs_ship_date_sk
rows between unbounded preceding and unbounded following ) as "61-90 days"
,max(case when (cs_ship_date_sk - cs_sold_date_sk > 90) and
(cs_ship_date_sk - cs_sold_date_sk <= 120) then 1 else 0 end) over (partition by cs_ship_date_sk order by cs_ship_date_sk
rows between unbounded preceding and unbounded following ) as "91-120 days"
,min(case when (cs_ship_date_sk - cs_sold_date_sk  > 120) then 1 else 0 end) over (partition by cs_ship_date_sk order by cs_ship_date_sk
rows between unbounded preceding and unbounded following ) as ">120 days"
from
 """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.SHIP_MODE 
,""" + gvars.g_schema_tpcds1x + """.CALL_CENTER 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
extract (year from d_date) = 2002
and cs_ship_date_sk   = d_date_sk
and cs_warehouse_sk   = w_warehouse_sk
and cs_ship_mode_sk   = sm_ship_mode_sk
and cs_call_center_sk = cc_call_center_sk
group by
1
,sm_type
,cc_name,
cs_ship_date_sk,
cs_sold_date_sk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test577(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_brand_id brand_id, i_brand brand, i_manufact_id, i_manufact,
sum(ss_ext_sales_price)  over (partition by i_manufact_id order by i_manufact_id
rows between 10 preceding and unbounded following ) as ext_price
from """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.STORE_SALES, """ + gvars.g_schema_tpcds1x + """.ITEM,""" + gvars.g_schema_tpcds1x + """.CUSTOMER,""" + gvars.g_schema_tpcds1x + """.CUSTOMER_ADDRESS,""" + gvars.g_schema_tpcds1x + """.STORE 
where d_date_sk = ss_sold_date_sk
and ss_item_sk = i_item_sk
and i_manager_id=36
and d_moy=11
and d_year=2001
and ss_customer_sk = c_customer_sk
and c_current_addr_sk = ca_address_sk
and substr(ca_zip,1,5) <> substr(s_zip,1,5)
and ss_store_sk = s_store_sk
group by i_brand, i_brand_id,i_manufact_id, i_manufact,SS_EXT_SALES_PRICE
order by ext_price desc, i_brand, i_brand_id,i_manufact_id, i_manufact ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test578(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
t_s_secyear.customer_id,
t_s_secyear.customer_first_name,
t_s_secyear.customer_last_name,
t_s_secyear.c_preferred_cust_flag,
t_s_secyear.c_birth_country,
t_s_secyear.c_login
from (
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price - ss_ext_discount_amt) over (partition by ss_ext_list_price order by ss_ext_list_price
rows between unbounded preceding and unbounded following ) as year_total
,'s' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year,
SS_EXT_LIST_PRICE,
ss_ext_discount_amt
union all
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price - ws_ext_discount_amt) over (partition by d_year order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'w' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,WS_EXT_LIST_PRICE
,WS_EXT_DISCOUNT_AMT
) as t_s_firstyear
,(
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price - ss_ext_discount_amt) over (partition by d_year  order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'s' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,SS_EXT_LIST_PRICE
,SS_EXT_DISCOUNT_AMT    

union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price - ws_ext_discount_amt) over (partition by d_year  order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'w' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,WS_EXT_LIST_PRICE
,WS_EXT_DISCOUNT_AMT
) as t_s_secyear
,(
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price - ss_ext_discount_amt) over (partition by d_year order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'s' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,SS_EXT_LIST_PRICE
,SS_EXT_DISCOUNT_AMT
union all
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price - ws_ext_discount_amt) over (partition by d_year order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'w' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,WS_EXT_LIST_PRICE
,WS_EXT_DISCOUNT_AMT
) as t_w_firstyear
,(
select  c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price - ss_ext_discount_amt) over (partition by d_year order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'s' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,SS_EXT_LIST_PRICE
,SS_EXT_DISCOUNT_AMT
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price - ws_ext_discount_amt) over (partition by d_year order by d_year
rows between unbounded preceding and unbounded following ) as year_total
,'w' sale_type
from """ + gvars.g_schema_tpcds1x + """.CUSTOMER 
,""" + gvars.g_schema_tpcds1x + """.WEB_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
,WS_EXT_LIST_PRICE
,WS_EXT_DISCOUNT_AMT    

) as t_w_secyear
where t_s_secyear.customer_id = t_s_firstyear.customer_id
and t_s_firstyear.customer_id = t_w_secyear.customer_id
and t_s_firstyear.customer_id = t_w_firstyear.customer_id
and t_s_firstyear.sale_type = 's'
and t_w_firstyear.sale_type = 'w'
and t_s_secyear.sale_type = 's'
and t_w_secyear.sale_type = 'w'
and t_s_firstyear.dyear = 1999
and t_s_secyear.dyear = 1999+1
and t_w_firstyear.dyear = 1999
and t_w_secyear.dyear = 1999+1
and t_s_firstyear.year_total > 0
and t_w_firstyear.year_total > 0
and case when t_w_firstyear.year_total > 0
then t_w_secyear.year_total / t_w_firstyear.year_total else null end
> case
when t_s_firstyear.year_total > 0
then t_s_secyear.year_total / t_s_firstyear.year_total else null end
order by t_s_secyear.customer_id,
t_s_secyear.customer_first_name,
t_s_secyear.customer_last_name,
t_s_secyear.c_preferred_cust_flag,
t_s_secyear.c_birth_country,
t_s_secyear.c_login;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test579(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
*
from
(
select
w_warehouse_name
,i_item_id
,sum(case when (cast(d_date as date) < cast ('1999-06-25' as date))
then inv_quantity_on_hand
else 0
end)  over (partition by i_item_id order by i_item_id
rows between current row and unbounded following ) as inv_before
,sum(case when (cast(d_date as date) >= cast ('1999-06-25' as date))
then inv_quantity_on_hand
else 0
end)  over (partition by i_item_id order by i_item_id
rows between current row and unbounded following )as inv_after
from
 """ + gvars.g_schema_tpcds1x + """.INVENTORY 
,""" + gvars.g_schema_tpcds1x + """.WAREHOUSE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM 
where
i_current_price between 0.99 and 1.49
and i_item_sk          = inv_item_sk
and inv_warehouse_sk   = w_warehouse_sk
and inv_date_sk    = d_date_sk
and d_date between (cast ('1999-06-25' as date) - 30 )
and (cast ('1999-06-25' as date) + 30 )
group by
w_warehouse_name,d_date,INV_QUANTITY_ON_Hand, i_item_id) x
where (case when inv_before > 0
then inv_after / inv_before
else null
end) between 2/3 and 3/2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test580(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0]
c_last_name,c_first_name,ss_ticket_number,cnt,
sum(C_CUSTOMER_SK) over (partition by c_customer_id  order by C_CUSTOMER_ID
rows between 5 following and unbounded following) as total_sales
from
(select ss_ticket_number
,ss_customer_sk
,count(*) cnt
from """ + gvars.g_schema_tpcds1x + """.STORE_SALES,""" + gvars.g_schema_tpcds1x + """.DATE_DIM,""" + gvars.g_schema_tpcds1x + """.STORE,""" + gvars.g_schema_tpcds1x + """.HOUSEHOLD_DEMOGRAPHICS 
where """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_sold_date_sk = """ + gvars.g_schema_tpcds1x + """.DATE_DIM.d_date_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_store_sk = """ + gvars.g_schema_tpcds1x + """.STORE.s_store_sk
and """ + gvars.g_schema_tpcds1x + """.STORE_SALES.ss_hdemo_sk = """ + gvars.g_schema_tpcds1x + """.HOUSEHOLD_DEMOGRAPHICS.hd_demo_sk
and """ + gvars.g_schema_tpcds1x + """.DATE_DIM.d_dom between 1 and 5
and """ + gvars.g_schema_tpcds1x + """.DATE_DIM.d_year in (1999,1999+1,1999+2)
and """ + gvars.g_schema_tpcds1x + """.STORE.s_city in ('Fairview','Midway','Midway',
'Fairview','Fairview','Fairview')
and (""" + gvars.g_schema_tpcds1x + """.HOUSEHOLD_DEMOGRAPHICS.hd_buy_potential like '1001-5000%' or
 """ + gvars.g_schema_tpcds1x + """.HOUSEHOLD_DEMOGRAPHICS.hd_buy_potential like '5001-10000%')
group by ss_ticket_number,ss_customer_sk) mp,""" + gvars.g_schema_tpcds1x + """.CUSTOMER 
where ss_customer_sk = c_customer_sk
and cnt between 1 and 5
order by cnt desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test581(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and 5 preceding)  as store_sales_profit
,max(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and current row) as store_returns_loss
,min(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and unbounded following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test582(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and current row)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and unbounded following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and 4 following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test583(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and unbounded following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and 6 following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and current row) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test584(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between unbounded preceding and 6 following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and current row) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and unbounded following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test585(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and current row)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and unbounded following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and 4 following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test586(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and unbounded following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and 4 following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 18 preceding and 12 preceding) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test587(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between current row and 4 following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 12 preceding and 6 preceding) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and current row) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test588(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 8 preceding and 6 preceding)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and current row) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and unbounded following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test589(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and current row)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and unbounded following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and 6 following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test590(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and unbounded following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and 6 following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 2 following and 4 following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test591(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 4 preceding and 6 following)  as store_sales_profit
,sum(sr_net_loss) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 2 following and 12 following) as store_returns_loss
,sum(cs_net_profit) over (partition by i_item_id ,s_store_id  order by  i_item_id ,s_store_id
rows between 3 following and unbounded following) as catalog_sales_profit
from
 """ + gvars.g_schema_tpcds1x + """.STORE_SALES 
,""" + gvars.g_schema_tpcds1x + """.STORE_RETURNS 
,""" + gvars.g_schema_tpcds1x + """.CATALOG_SALES 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d1
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d2 
,""" + gvars.g_schema_tpcds1x + """.DATE_DIM d3
,""" + gvars.g_schema_tpcds1x + """.STORE 
,""" + gvars.g_schema_tpcds1x + """.ITEM 
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,ss_net_profit
,sr_net_loss
,cs_net_profit
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test592(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 10 preceding and unbounded following ) as agg1,
avg(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 10 preceding and unbounded following ) as agg2,
avg(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 10 preceding and unbounded following ) as agg3,
avg(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between 10 preceding and unbounded following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test593(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and 4 preceding ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and current row ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and unbounded following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and 2 following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test594(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and current row ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and unbounded following ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and 4 following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and current row ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test595(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and 3 following ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and current row ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and unbounded following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and unbounded following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)

def test596(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Prepare xx  from
select [last 0] i_item_id,
avg(cs_quantity) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and current row ) as agg1,
sum(cs_list_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between unbounded preceding and unbounded following ) as agg2,
count(cs_coupon_amt) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and unbounded following ) as agg3,
min(cs_sales_price) over (partition by cs_quantity,cs_item_sk order by cs_quantity,cs_item_sk
rows between current row and 3 following ) as agg4
from """ + gvars.g_schema_tpcds1x + """.CATALOG_SALES, """ + gvars.g_schema_tpcds1x + """.CUSTOMER_DEMOGRAPHICS, """ + gvars.g_schema_tpcds1x + """.DATE_DIM, """ + gvars.g_schema_tpcds1x + """.ITEM, """ + gvars.g_schema_tpcds1x + """.PROMOTION 
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id,cs_quantity,cs_list_price,cs_item_sk,cs_sales_price,cs_coupon_amt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics for qid current;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

