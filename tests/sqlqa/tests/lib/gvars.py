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

DEFAULT_HPDCI_CLASSPATH = './hpdci.jar'
DEFAULT_JDBC_CLASSPATH = './hpt4jdbc.jar'

definition_schema = 'SET_IN_HPDCI_PY_AFTER_KNOWING_TARGET_TYPE'
current_schema_version = definition_schema
sys_definition_schema = definition_schema

system_defaults_cat = 'HP_SYSTEM_CATALOG'

repository_schema = 'MANAGEABILITY.INSTANCE_REPOSITORY'
query_stats_view = 'METRIC_QUERY_1'
security_schema = 'HP_SECURITY_SCHEMA'

test_catalog = 'trafodion'
test_definition_schema = test_catalog + '.' + definition_schema

histograms = 'SET_IN_HPDCI_PY_AFTER_KNOWING_TARGET_TYPE'
histogram_intervals = 'SET_IN_HPDCI_PY_AFTER_KNOWING_TARGET_TYPE'
inscmd = 'SET_IN_HPDCI_PY_AFTER_KNOWING_TARGET_TYPE'

tpch2x_schema = 'g_tpch2x'
wisc32_schema = 'g_wisc32'
sqldopt_schema = 'g_sqldopt'
sqldpop_schema = 'g_sqldpop'
tpcds1x_schema = 'g_tpcds1x'
hcubedb_schema = 'g_hcubedb'
arkcasedb_schema = 'g_arkcasedb'
skewbuster_schema = 'g_skewbuster'
cmureg_schema = 'g_cmureg'

g_schema_tpch2x = test_catalog + '.' + tpch2x_schema
g_schema_wisc32 = test_catalog + '.' + wisc32_schema
g_schema_sqldopt = test_catalog + '.' + sqldopt_schema
g_schema_sqldpop = test_catalog + '.' + sqldpop_schema
g_schema_tpcds1x = test_catalog + '.' + tpcds1x_schema
g_schema_hcubedb = test_catalog + '.' + hcubedb_schema
g_schema_arkcasedb = test_catalog + '.' + arkcasedb_schema
g_schema_skewbuster = test_catalog + '.' + skewbuster_schema
g_schema_cmureg = test_catalog + '.' + cmureg_schema

default_num_salt_partitions = '8'

# This is problematic.  We may have to create a small table and run
# 'showlable <table>, detail' to see what the partition names are.
# They may be '$FCxxx' or '$DBxxx'
# g_disc0 = '$FC0000'
# g_disc1 = '$FC0100'
# g_disc2 = '$FC0200'
# g_disc3 = '$FC0300'
# g_disc4 = '$FC0400'
# g_disc5 = '$FC0500'
# g_disc6 = '$FC0600'
# g_disc7 = '$FC0700'
# g_disc8 = '$FC0800'
# g_disc9 = '$FC0900'
# g_disc10 = '$FC1000'
# g_disc11 = '$FC1100'
# g_disc12 = '$FC1200'
# g_disc13 = '$FC1300'
# g_disc14 = '$FC1400'
# g_disc15 = '$FC1500'

g_disc0 = '$DB0001'
g_disc1 = '$DB0002'
g_disc2 = '$DB0003'
g_disc3 = '$DB0004'
g_disc4 = '$DB0005'
g_disc5 = '$DB0006'
g_disc6 = '$DB0007'
g_disc7 = '$DB0008'
g_disc8 = '$DB0009'
g_disc9 = '$DB0010'
g_disc10 = '$DB0011'
g_disc11 = '$DB0012'
g_disc12 = '$DB0013'
g_disc13 = '$DB0014'
g_disc14 = '$DB0015'
g_disc15 = '$DB0016'


