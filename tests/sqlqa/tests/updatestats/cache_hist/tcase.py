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
import setup

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
    
def test001(desc="""cache_histogram=on, hist_refresh_interval=3600"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # DESCRIPTION_BEGIN
    # MAP:{A001}
    # Histogram caching is enabled.
    # Cached histogram is not refreshed.
    # DESCRIPTION_END
    defs.testid = """A001"""
    defs.tblname = """T_""" + defs.testid
    # Create test table
    setup.cr8tbl()
    # default setting
    stmt = """control query default CACHE_HISTOGRAMS 'on';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default CACHE_HISTOGRAMS_REFRESH_INTERVAL '3600';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # sleep 1 sec b/n each query execution
    # Cache should not be refreshed since time b/n last read and current
    # is smaller than refresh_interval
    defs.SLEEP_TIME = 10
    setup.run_each_test()
    _testmgr.testcase_end(desc)

def test002(desc="""cache_histogram=on, hist_refresh_interval=1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # DESCRIPTION_BEGIN
    # MAP:{A002}
    # Histogram caching is enabled.
    # Cached histogram will be refreshed.
    # Verify that READ_TIME is updated when the cached histogram is refreshed.
    #
    # DESCRIPTION_END
    defs.testid = """A002"""
    defs.tblname = """T_""" + defs.testid
    # Create test table
    setup.cr8tbl()
    # default setting
    stmt = """control query default CACHE_HISTOGRAMS 'on';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default CACHE_HISTOGRAMS_REFRESH_INTERVAL '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # sleep 5 sec b/n each query execution
    # Cache should be refreshed since time b/n last read and current
    # is bigger than refresh_interval
    defs.SLEEP_TIME = 10
    setup.run_each_test()
    _testmgr.testcase_end(desc)

def test003(desc="""cache_histogram=off, hist_refresh_interval=3600"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # DESCRIPTION_BEGIN
    # MAP:{A003}
    # Histogram caching is disabled.
    # Cached histogram is not refreshed.
    # SHould READ_TIME affected by histogram cache refresh interval?
    # DESCRIPTION_END
    defs.testid = """A003"""
    defs.tblname = """T_""" + defs.testid
    # Create test table
    setup.cr8tbl()
    # default setting
    stmt = """control query default CACHE_HISTOGRAMS 'off';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default CACHE_HISTOGRAMS_REFRESH_INTERVAL '3600';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # repeate of scenario A001, but with caching of histogram disabled
    # since caching is off, it should read histogram for each access
    defs.SLEEP_TIME = 10
    setup.run_each_test()
    _testmgr.testcase_end(desc)

def test004(desc="""cache_histogram=off, hist_refresh_interval=1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # DESCRIPTION_BEGIN
    # MAP:{A004}
    # Histogram caching is disabled.
    # Cached histogram will not be refreshed.
    # SHould READ_TIME affected by histogram cache refresh interval?
    # DESCRIPTION_END
    defs.testid = """A004"""
    defs.tblname = """T_""" + defs.testid
    # Create test table
    setup.cr8tbl()
    # default setting
    stmt = """control query default CACHE_HISTOGRAMS 'off';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default CACHE_HISTOGRAMS_REFRESH_INTERVAL '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # repeate of scenario A004, but with caching of histogram disabled
    # since caching is off, it should read histogram for each access
    defs.SLEEP_TIME = 10
    setup.run_each_test()
    _testmgr.testcase_end(desc)

