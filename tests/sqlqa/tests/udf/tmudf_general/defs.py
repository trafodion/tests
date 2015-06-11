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
test_dir = hpdci.my_test_dir(__name__)
work_dir = hpdci.my_work_dir(__name__)

# Set your own catalog and schema.  Change the variable names if necessary.
w_catalog = gvars.test_catalog
w_schema = hpdci.my_schema(__name__)
my_schema = w_catalog + '.' + w_schema

# Add additional variables here.
my_schema1 = my_schema + '1'
my_schema1_no_cat = w_schema + '1'

udf_dir = hpdci.get_test_env_setting('TEST_ENV_QALIB_UDF_DIR')
qa_tmudf_lib = """'""" + udf_dir + """/qaTmudfTest.so'"""

myShortTableEqualPreds = """where t1.c1 = t2.c1 and t1.c2 = t2.c2"""

myFullTableEqualPreds = """where
t1.c_char = t2.c_char and
t1.c_char_upshift = t2.c_char_upshift and
t1.c_char_not_casespecific = t2.c_char_not_casespecific and
t1.c_char_varying = t2.c_char_varying and
t1.c_char_varying_upshift = t2.c_char_varying_upshift and
t1.c_char_varying_not_casespecific = t2.c_char_varying_not_casespecific and
t1.c_varchar = t2.c_varchar and
t1.c_varchar_upshift = t2.c_varchar_upshift and
t1.c_varchar_not_casespecific = t2.c_varchar_not_casespecific and
t1.c_nchar = t2.c_nchar and
t1.c_nchar_upshift = t2.c_nchar_upshift and
t1.c_nchar_not_casespecific = t2.c_nchar_not_casespecific and
t1.c_nchar_varying = t2.c_nchar_varying and
t1.c_nchar_varying_upshift = t2.c_nchar_varying_upshift and
t1.c_nchar_varying_not_casespecific = t2.c_nchar_varying_not_casespecific and
t1.c_numeric = t2.c_numeric and
t1.c_numeric_unsigned = t2.c_numeric_unsigned and
t1.c_decimal = t2.c_decimal and
t1.c_decimal_unsigned = t2.c_decimal_unsigned and
t1.c_integer = t2.c_integer and
t1.c_integer_unsigned = t2.c_integer_unsigned and
t1.c_largeint = t2.c_largeint and
t1.c_smallint = t2.c_smallint and
t1.c_smallint_unsigned = t2.c_smallint_unsigned and
t1.c_float = t2.c_float and
t1.c_real = t2.c_real and
t1.c_double_precision = t2.c_double_precision and
t1.c_date = t2.c_date and
t1.c_time = t2.c_time and
t1.c_time5 = t2.c_time5 and
t1.c_timestamp = t2.c_timestamp and
t1.c_timestamp5 = t2.c_timestamp5 and
t1.c_interval = t2.c_interval and
t1.c_clob = t2.c_clob and
t1.c_blob = t2.c_blob
"""

myFullTableIsNullPreds = """where
t1.c_char is null and
t1.c_char_upshift is null and
t1.c_char_not_casespecific is null and
t1.c_char_varying is null and
t1.c_char_varying_upshift is null and
t1.c_char_varying_not_casespecific is null and
t1.c_varchar is null and
t1.c_varchar_upshift is null and
t1.c_varchar_not_casespecific is null and
t1.c_nchar is null and
t1.c_nchar_upshift is null and
t1.c_nchar_not_casespecific is null and
t1.c_nchar_varying is null and
t1.c_nchar_varying_upshift is null and
t1.c_nchar_varying_not_casespecific is null and
t1.c_numeric is null and
t1.c_numeric_unsigned is null and
t1.c_decimal is null and
t1.c_decimal_unsigned is null and
t1.c_integer is null and
t1.c_integer_unsigned is null and
t1.c_largeint is null and
t1.c_smallint is null and
t1.c_smallint_unsigned is null and
t1.c_float is null and
t1.c_real is null and
t1.c_double_precision is null and
t1.c_date is null and
t1.c_time is null and
t1.c_time5 is null and
t1.c_timestamp is null and
t1.c_timestamp5 is null and
t1.c_interval is null and
t1.c_clob is null and
t1.c_blob is null
"""

myFullPositionTableEqualPreds = """where
t1.C00_CHAR = t2.C00_CHAR and
t1.C01_CHAR = t2.C01_CHAR and
t1.C02_CHAR = t2.C02_CHAR and
t1.C03_VARCHAR = t2.C03_VARCHAR and
t1.C04_VARCHAR = t2.C04_VARCHAR and
t1.C05_VARCHAR = t2.C05_VARCHAR and
t1.C06_VARCHAR = t2.C06_VARCHAR and
t1.C07_VARCHAR = t2.C07_VARCHAR and
t1.C08_VARCHAR = t2.C08_VARCHAR and
t1.C09_CHAR = t2.C09_CHAR  and
t1.C10_CHAR = t2.C10_CHAR and
t1.C11_CHAR = t2.C11_CHAR and
t1.C12_VARCHAR = t2.C12_VARCHAR and
t1.C13_VARCHAR = t2.C13_VARCHAR and
t1.C14_VARCHAR = t2.C14_VARCHAR and
t1.C15_NUMERIC = t2.C15_NUMERIC and
t1.C16_NUMERIC_UNSIGNED = t2.C16_NUMERIC_UNSIGNED and
t1.C17_DECIMAL_LSE = t2.C17_DECIMAL_LSE and
t1.C18_DECIMAL_UNSIGNED = t2.C18_DECIMAL_UNSIGNED and
t1.C19_INT = t2.C19_INT and
t1.C20_INT_UNSIGNED = t2.C20_INT_UNSIGNED  and
t1.C21_LARGEINT = t2.C21_LARGEINT and
t1.C22_SMALLINT = t2.C22_SMALLINT and
t1.C23_SMALLINT_UNSIGNED = t2.C23_SMALLINT_UNSIGNED and
t1.C24_DOUBLE_PRECISION = t2.C24_DOUBLE_PRECISION and
t1.C25_REAL = t2.C25_REAL and
t1.C26_DOUBLE_PRECISION = t2.C26_DOUBLE_PRECISION and
t1.C27_DATE = t2.C27_DATE and
t1.C28_TIME = t2.C28_TIME and
t1.C29_TIME = t2.C29_TIME and
t1.C30_TIMESTAMP = t2.C30_TIMESTAMP and
t1.C31_TIMESTAMP = t2.C31_TIMESTAMP and
t1.C32_INTERVAL = t2.C32_INTERVAL and
t1.C33_VARCHAR = t2.C33_VARCHAR and
t1.C34_VARCHAR = t2.C34_VARCHAR
"""
