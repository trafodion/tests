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
    
    stmt = """create table item
(
i_item_sk                 integer               not null,
i_item_id                 char(16)              not null,
i_rec_start_date          date                          ,
i_rec_end_date            date                          ,
i_item_desc               varchar(200)                  ,
i_current_price           decimal(7,2)                  ,
i_wholesale_cost          decimal(7,2)                  ,
i_brand_id                integer                       ,
i_brand                   char(50)                      ,
i_class_id                integer                       ,
i_class                   char(50)                      ,
i_category_id             integer                       ,
i_category                char(50)                      ,
i_manufact_id             integer                       ,
i_manufact                char(50)                      ,
i_size                    char(20)                      ,
i_formulation             char(20)                      ,
i_color                   char(20)                      ,
i_units                   char(10)                      ,
i_container               char(10)                      ,
i_manager_id              integer                       ,
i_product_name            char(50)                      ,
primary key (i_item_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ no partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    
