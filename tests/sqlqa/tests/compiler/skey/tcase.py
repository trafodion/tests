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
    
def test001(desc="""Grouping on Store by table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select max(ws_coupon_amt),max( ws_net_paid), ws_warehouse_sk, ws_quantity from
web_sales_clone
group by (ws_quantity, ws_warehouse_sk);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    _dci.unexpect_any_substr(output, 'partial')
    #unexpect purge
    
    stmt = """prepare xx from
select max(ws_coupon_amt), ws_net_paid, ws_warehouse_sk, ws_quantity from
web_sales_clone
group by (ws_quantity, ws_warehouse_sk, ws_net_paid);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select max(ws_coupon_amt), ws_net_paid, ws_quantity from
web_sales_clone
group by (ws_net_paid,ws_quantity);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select max(ws_coupon_amt), ws_net_paid, ws_warehouse_sk, ws_quantity from
web_sales_clone
group by (ws_warehouse_sk, ws_quantity, ws_net_paid);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select max(ws_coupon_amt), ws_net_paid, ws_promo_sk, ws_quantity from
web_sales_clone
group by (ws_promo_sk, ws_quantity, ws_net_paid);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Grouping on PK table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare xx from
select ca_address_id, ca_city, ca_county, avg(ca_address_sk) from
sb_customer_address
group by (ca_address_id, ca_city, ca_county);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    #unexpect purge
    
    # expect partial sort with ca_address_sk in it
    # different plan on WM
    # didn't know how to fit into expect file, so used crude
    # case statement below.  When SORT node found, FAIL will not
    # be returned but when SORT node is found, it doesn't expect a FAIL
    
    stmt = """prepare xx from
select ca_address_id, ca_city, ca_county, avg(ca_address_sk) from
sb_customer_address
group by (ca_state, ca_address_id, ca_city, ca_county);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """select 'partial sort found ',
    # case locate('PartialSort',description)
    # when 0 then 'FAIL'
    # else 'PASS'
    # end
    # from table(explain(NULL,'XX'))
    # where operator = 'SORT';"""
    # output = _dci.cmdexec(stmt)
    # _dci.unexpect_any_substr(output, 'FAIL')
    #unexpect purge
    
    # don't expect partial sort here, key prefix not referenced
    stmt = """prepare xx from
select ca_city, max(ca_county), min(ca_street_type), count(*) from
sb_customer_address
group by (ca_city);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    _dci.unexpect_any_substr(output, 'partial')
    #unexpect purge
    
    # key prefix should create partial sort
    stmt = """prepare xx from
select ca_city, ca_county, ca_street_type, count(*) from
sb_customer_address
group by (ca_address_id, ca_city, ca_street_type, ca_county);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select max(ca_zip), ca_suite_number, count(*) from
sb_customer_address
group by (ca_address_id, ca_city,ca_suite_number);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Group by with join"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare xx from
select max(wsc.ws_coupon_amt),wsc.ws_net_paid, wsc.ws_warehouse_sk, wsc.ws_quantity from
web_sales_clone wsc, """ + gvars.g_schema_tpcds1x + """.web_sales ws
where wsc.ws_quantity = ws.ws_order_number
group by (wsc.ws_quantity, wsc.ws_warehouse_sk, wsc.ws_net_paid);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    stmt = """prepare xx from
select max(wsc.ws_coupon_amt),wsc.ws_net_paid,
wsc.ws_warehouse_sk, wsc.ws_quantity from
web_sales_clone wsc, """ + gvars.g_schema_tpcds1x + """.web_sales ws
where wsc.ws_quantity = ws.ws_order_number
group by (wsc.ws_warehouse_sk, wsc.ws_quantity, wsc.ws_net_paid);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Order by on store by key"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # don't expect partial sort here, not a prefix
    stmt = """prepare xx from
select ws_coupon_amt,ws_net_paid, ws_warehouse_sk, ws_quantity, ws_net_profit from
web_sales_clone
order by ws_net_profit, ws_quantity;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    _dci.unexpect_any_substr(output, 'partial')
    #unexpect purge
    
    stmt = """prepare xx from
select ws_coupon_amt,ws_net_paid, ws_warehouse_sk, ws_quantity, ws_net_profit from
web_sales_clone
order by ws_quantity, ws_net_profit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.expect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select ws_coupon_amt, ws_net_paid, ws_warehouse_sk, ws_quantity from
web_sales_clone
order by ws_quantity, ws_warehouse_sk, ws_net_paid;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.expect_any_substr(output, 'PartialSort_FromChild')
    
    #no partial key because descending?
    stmt = """prepare xx from
select ws_coupon_amt, ws_net_paid, ws_warehouse_sk, ws_quantity from
web_sales_clone
order by ws_quantity desc , ws_warehouse_sk desc, ws_net_paid;"""
    output = _dci.cmdexec(stmt)
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    _dci.unexpect_any_substr(output, 'partial')
    #unexpect purge
    
    _testmgr.testcase_end(desc)

def test005(desc="""Distinct clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # this query syntax is executed as an aggregate
    
    stmt = """prepare xx from
select distinct ca_address_id, ca_city, ca_country from
sb_customer_address;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select distinct ws_quantity, ws_coupon_amt, ws_net_paid, ws_warehouse_sk
from web_sales_clone
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    stmt = """prepare xx from
select distinct c_customer_sk, c_last_name, c_birth_day
from sb_customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # stmt = """select * from table(explain (null,'XX')) where description like '%Partial%';"""
    # output = _dci.cmdexec(stmt)
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Descending keys"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # run group by query against ascending key
    
    stmt = """prepare xa from
select sr_store_sk, sr_ticket_number, sr_reason_sk , avg(sr_return_amt)
from sb_store_returns_a
group by (sr_ticket_number, sr_reason_sk,sr_store_sk);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xa;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xa;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    # now try descending
    
    stmt = """prepare xd from
select sr_store_sk, sr_ticket_number, sr_reason_sk , avg(sr_return_amt)
from sb_store_returns_d
group by (sr_ticket_number, sr_reason_sk,sr_store_sk);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xd;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    #According to developer, we don't see PartialSort_FromChild in current SQ because of different cost models in NV and SQ. But when the feature gets added to SQ, we may need to change the expect file back to original one, the one being commented out.
    ##expect any *PartialSort_FromChild*
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.unexpect_any_substr(output, 'PartialSort_FromChild')
    
    # run order by query against ascending key
    
    stmt = """prepare xa from
select sr_store_sk, sr_ticket_number, sr_reason_sk , sr_return_amt - 20.00
from sb_store_returns_a
order  by sr_ticket_number, sr_reason_sk,sr_store_sk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xa;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xa;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.expect_any_substr(output, 'PartialSort_FromChild')
    
    # run order by query against descending key
    
    stmt = """prepare xd from
select sr_store_sk, sr_ticket_number, sr_reason_sk , sr_return_amt - 20.00
from sb_store_returns_d
order  by sr_ticket_number desc, sr_reason_sk desc,sr_store_sk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """log """ + defs.work_dir + """/exp1.log clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain xd;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    # output = _testmgr.shell_call("""grep -i 'partial' """ + defs.work_dir + """/exp1.log""")
    # _dci.expect_any_substr(output, 'PartialSort_FromChild')
    
    _testmgr.testcase_end(desc)

