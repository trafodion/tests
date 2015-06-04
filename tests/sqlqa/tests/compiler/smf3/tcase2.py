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

    stmt = """set param ?curr_model 'T2';"""
    output = _dci.cmdexec(stmt)
    
def test001(desc="""TPCDS Query 7"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 7;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 7
    # rowcount = 5194
    stmt = """prepare xx from
select [first 100] i_item_id,
avg(ss_quantity) agg1,
avg(ss_list_price) agg2,
avg(ss_coupon_amt) agg3,
avg(ss_sales_price) agg4
from store_sales, customer_demographics, date_dim, item, promotion
where ss_sold_date_sk = d_date_sk and
ss_item_sk = i_item_sk and
ss_cdemo_sk = cd_demo_sk and
ss_promo_sk = p_promo_sk and
cd_gender = 'F' and
cd_marital_status = 'D' and
cd_education_status = 'Advanced Degree' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 2000
group by i_item_id
order by i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 100)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""TPCDS Query 9"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #set showshape on;
    stmt = """set param ?q 9;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # tpcds query 9
    # rowcount = 709
    stmt = """prepare xx from
select  [first 100]
i_item_id ,sum(total_sales) total_sales
from
(select * from
(select
i_item_id,sum(ss_ext_sales_price) total_sales
from
store_sales,
date_dim,
customer_address,
item
where
i_item_id in (select
i_item_id
from
item
where
i_color in ('purple','peru','dark'))
and     ss_item_sk              = i_item_sk
and     ss_sold_date_sk         = d_date_sk
and     d_year                  = 2000
and     d_moy                   = 5
and     ss_addr_sk              = ca_address_sk
and     ca_gmt_offset           = -5
group by
i_item_id) as ss
union all
select
*
from (select
i_item_id,sum(cs_ext_sales_price) total_sales
from
catalog_sales,
date_dim,
customer_address,
item
where
i_item_id in (select
i_item_id
from
item
where
i_color in ('purple','peru','dark'))
and     cs_item_sk              = i_item_sk
and     cs_sold_date_sk         = d_date_sk
and     d_year                  = 2000
and     d_moy                   = 5
and     cs_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by
i_item_id) as cs
union all
select
*
from (select
i_item_id,sum(ws_ext_sales_price) total_sales
from
web_sales,
date_dim,
customer_address,
item
where
i_item_id in (select
i_item_id
from
item
where
i_color in ('purple','peru','dark'))
and     ws_item_sk              = i_item_sk
and     ws_sold_date_sk         = d_date_sk
and     d_year                  = 2000
and     d_moy                   = 5
and     ws_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by
i_item_id) as ws
) tmp1
group by
i_item_id
order by
total_sales,i_item_id
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds9')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""TPCDS Query 18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 18;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 18
    # rowcount = 5182
    stmt = """prepare xx from
select  [first 200]
i_item_id,
ca_country,
ca_state,
ca_county,
agg1,
agg2,
agg3,
agg4,
agg5,
agg6,
agg7
from
(
select i_item_id,
ca_country,
ca_state,
ca_county,
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4,
avg(cs_net_profit) agg5,
avg(c_birth_year) agg6,
avg(cd1.cd_dep_count) agg7
from catalog_sales, customer_demographics cd1,
customer_demographics cd2, customer,
customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd1.cd_demo_sk and
cs_bill_customer_sk = c_customer_sk and
cd1.cd_gender = 'F' and
cd1.cd_education_status = 'Primary' and
c_current_cdemo_sk = cd2.cd_demo_sk and
c_current_addr_sk = ca_address_sk and
c_birth_month in (9,4,3,11,1,12) and
d_year = 1999 and
ca_state in ('VA','NE','MI','WV','WV','CO','IN')
group by 1,2,3,4
union all
select i_item_id,
cast(null as char),
ca_state,
ca_county,
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4,
avg(cs_net_profit) agg5,
avg(c_birth_year) agg6,
avg(cd1.cd_dep_count) agg7
from catalog_sales, customer_demographics cd1,
customer_demographics cd2, customer,
customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd1.cd_demo_sk and
cs_bill_customer_sk = c_customer_sk and
cd1.cd_gender = 'F' and
cd1.cd_education_status = 'Primary' and
c_current_cdemo_sk = cd2.cd_demo_sk and
c_current_addr_sk = ca_address_sk and
c_birth_month in (9,4,3,11,1,12) and
d_year = 1999 and
ca_state in ('VA','NE','MI','WV','WV','CO','IN')
group by 1,2,3,4
union all
select i_item_id,
cast(null as char),
cast(null as char),
ca_county,
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4,
avg(cs_net_profit) agg5,
avg(c_birth_year) agg6,
avg(cd1.cd_dep_count) agg7
from catalog_sales, customer_demographics cd1,
customer_demographics cd2, customer,
customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd1.cd_demo_sk and
cs_bill_customer_sk = c_customer_sk and
cd1.cd_gender = 'F' and
cd1.cd_education_status = 'Primary' and
c_current_cdemo_sk = cd2.cd_demo_sk and
c_current_addr_sk = ca_address_sk and
c_birth_month in (9,4,3,11,1,12) and
d_year = 1999 and
ca_state in ('VA','NE','MI','WV','WV','CO','IN')
group by 1,2,3,4
union all
select i_item_id,
cast(null as char),
cast(null as char),
cast(null as char),
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4,
avg(cs_net_profit) agg5,
avg(c_birth_year) agg6,
avg(cd1.cd_dep_count) agg7
from catalog_sales, customer_demographics cd1,
customer_demographics cd2, customer,
customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd1.cd_demo_sk and
cs_bill_customer_sk = c_customer_sk and
cd1.cd_gender = 'F' and
cd1.cd_education_status = 'Primary' and
c_current_cdemo_sk = cd2.cd_demo_sk and
c_current_addr_sk = ca_address_sk and
c_birth_month in (9,4,3,11,1,12) and
d_year = 1999 and
ca_state in ('VA','NE','MI','WV','WV','CO','IN')
group by 1,2,3,4
union all
select cast(null as char),
cast(null as char),
cast(null as char),
cast(null as char),
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4,
avg(cs_net_profit) agg5,
avg(c_birth_year) agg6,
avg(cd1.cd_dep_count) agg7
from catalog_sales, customer_demographics cd1,
customer_demographics cd2, customer,
customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd1.cd_demo_sk and
cs_bill_customer_sk = c_customer_sk and
cd1.cd_gender = 'F' and
cd1.cd_education_status = 'Primary' and
c_current_cdemo_sk = cd2.cd_demo_sk and
c_current_addr_sk = ca_address_sk and
c_birth_month in (9,4,3,11,1,12) and
d_year = 1999 and
ca_state in ('VA','NE','MI','WV','WV','CO','IN')
group by 1,2,3,4
) v1
order by 2,3,4,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds18')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""TPCDS Query 21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #set showshape on;
    stmt = """set param ?q 21;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 21
    # rowcount = 1849
    stmt = """prepare xx from
select [first 100]
*
from
(
select
w_warehouse_name
,i_item_id
,sum(case when (cast(d_date as date) < cast ('1999-06-25' as date))
then inv_quantity_on_hand
else 0
end) as inv_before
,sum(case when (cast(d_date as date) >= cast ('1999-06-25' as date))
then inv_quantity_on_hand
else 0
end) as inv_after
from
inventory
,warehouse
,item
,date_dim
where
i_current_price between 0.99 and 1.49
and i_item_sk          = inv_item_sk
and inv_warehouse_sk   = w_warehouse_sk
and inv_date_sk    = d_date_sk
and d_date between (cast ('1999-06-25' as date) - 30 )
and (cast ('1999-06-25' as date) + 30 )
group by
w_warehouse_name, i_item_id) x
where (case when inv_before > 0
then inv_after / inv_before
else null
end) between 2/3 and 3/2
order by w_warehouse_name, i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds21')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""TPCDS query 26"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set param ?q 26;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 26
    # rowcount = 3525
    stmt = """prepare xx from
select [first 100] i_item_id,
avg(cs_quantity) agg1,
avg(cs_list_price) agg2,
avg(cs_coupon_amt) agg3,
avg(cs_sales_price) agg4
from catalog_sales, customer_demographics, date_dim, item, promotion
where cs_sold_date_sk = d_date_sk and
cs_item_sk = i_item_sk and
cs_bill_cdemo_sk = cd_demo_sk and
cs_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'S' and
cd_education_status = 'Unknown' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id
order by i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds26')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc="""TPCDS Query 33"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #set showshape on;
    stmt = """set param ?q 33;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 33
    # rowcount = 714
    stmt = """prepare xx from
select [first 100]
i_manufact_id ,sum(total_sales) total_sales
from  (select * from (
select
i_manufact_id,sum(ss_ext_sales_price) total_sales
from
store_sales,
date_dim,
customer_address,
item
where
i_manufact_id in (select
i_manufact_id
from
item
where i_category in ('Electronics'))
and     ss_item_sk              = i_item_sk
and     ss_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     ss_addr_sk              = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id) as ss
union all
select * from (
select
i_manufact_id,sum(cs_ext_sales_price) total_sales
from
catalog_sales,
date_dim,
customer_address,
item
where
i_manufact_id               in (select
i_manufact_id
from
item
where i_category in ('Electronics'))
and     cs_item_sk              = i_item_sk
and     cs_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     cs_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id) as cs
union all
select * from (
select
i_manufact_id,sum(ws_ext_sales_price) total_sales
from
web_sales,
date_dim,
customer_address,
item
where
i_manufact_id               in (select
i_manufact_id
from
item
where i_category in ('Electronics'))
and     ws_item_sk              = i_item_sk
and     ws_sold_date_sk         = d_date_sk
and     d_year                  = 1998
and     d_moy                   = 2
and     ws_bill_addr_sk         = ca_address_sk
and     ca_gmt_offset           = -5
group by i_manufact_id) as ws) tmp1
group by i_manufact_id
order by total_sales
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds33')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc="""TPCDS query 71"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 71;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 71
    stmt = """prepare xx from
select [last 0] i_brand_id brand_id, i_brand brand,t_hour,t_minute,
sum(ext_price) ext_price
from item, (select ws_ext_sales_price as ext_price,
ws_sold_date_sk as sold_date_sk,
ws_item_sk as sold_item_sk,
ws_sold_time_sk as time_sk
from web_sales,date_dim
where d_date_sk = ws_sold_date_sk
and d_moy=11
and d_year=1998
union all
select cs_ext_sales_price as ext_price,
cs_sold_date_sk as sold_date_sk,
cs_item_sk as sold_item_sk,
cs_sold_time_sk as time_sk
from catalog_sales,date_dim
where d_date_sk = cs_sold_date_sk
and d_moy=11
and d_year=1998
union all
select ss_ext_sales_price as ext_price,
ss_sold_date_sk as sold_date_sk,
ss_item_sk as sold_item_sk,
ss_sold_time_sk as time_sk
from store_sales,date_dim
where d_date_sk = ss_sold_date_sk
and d_moy=11
and d_year=1998
) as tmp,time_dim
where
sold_item_sk = i_item_sk
and i_manager_id=1
and time_sk = t_time_sk
and (t_meal_time = 'breakfast' or t_meal_time = 'dinner')
group by i_brand, i_brand_id,t_hour,t_minute
order by ext_price desc, i_brand_id
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc="""TPCDS Query 76"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 76;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 76
    # rowcount = 1708
    stmt = """prepare xx from
select  [first 100 ]i_item_id,
avg(ws_quantity) agg1,
avg(ws_list_price) agg2,
avg(ws_coupon_amt) agg3,
avg(ws_sales_price) agg4
from web_sales, customer_demographics, date_dim, item, promotion
where ws_sold_date_sk = d_date_sk and
ws_item_sk = i_item_sk and
ws_bill_cdemo_sk = cd_demo_sk and
ws_promo_sk = p_promo_sk and
cd_gender = 'M' and
cd_marital_status = 'D' and
cd_education_status = '2 yr Degree' and
(p_channel_email = 'N' or p_channel_event = 'N') and
d_year = 1999
group by i_item_id
order by i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds76')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc="""TPCDS Query 82"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 82;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 82
    # rowcount = 0
    stmt = """prepare xx from
select  i_item_id
,i_item_desc
,i_current_price
from item, inventory, date_dim, store_sales
where i_current_price between 85 and 85+30
and inv_item_sk = i_item_sk
and d_date_sk=inv_date_sk
and d_date between cast('2001-02-23' as date) and (cast('2001-02-23' as date) +  60)
and i_manufact_id in (73,780,911,221)
and inv_quantity_on_hand between 100 and 500
and ss_item_sk = i_item_sk
group by i_item_id,i_item_desc,i_current_price
order by i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""TPCDS Query 91"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 91;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # Stream 0, Query 91
    stmt = """prepare xx from
select  [last 0]
cc_call_center_id Call_Center,
cc_name Call_Center_Name,
cc_manager Manager,
sum(cr_net_loss) Returns_Loss
from
call_center,
catalog_returns,
date_dim,
customer,
customer_address,
customer_demographics,
household_demographics
where
cr_call_center_sk       = cc_call_center_sk
and     cr_returned_date_sk     = d_date_sk
and     cr_returning_customer_sk= c_customer_sk
and     cd_demo_sk              = c_current_cdemo_sk
and     hd_demo_sk              = c_current_hdemo_sk
and     ca_address_sk           = c_current_addr_sk
and     d_year                  = 1999
and     d_moy                   = 12
and     ( (cd_marital_status       = 'M'
and cd_education_status     = 'Unknown')
or(cd_marital_status       = 'W'
and cd_education_status     = 'Advanced Degree'))
and     hd_buy_potential like '501-1000%'
and     ca_gmt_offset           = -7
group by cc_call_center_id,cc_name,cc_manager,
cd_marital_status,cd_education_status
order by 4 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cmp_time = time '""" + defs.et + """' where query = ?q
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_cost =
(select total_cost from table(explain(NULL,'XX'))
where operator = 'ROOT')
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T2_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute compare_T1_and_T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute get_low_values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """execute comp_plan_and_cost;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, 'PASS')
    
    stmt = """select * from """ + defs.my_schema + """.timetable
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

