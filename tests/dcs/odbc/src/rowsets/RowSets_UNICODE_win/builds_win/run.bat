REM @@@ START COPYRIGHT @@@
REM
REM (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
REM
REM  Licensed under the Apache License, Version 2.0 (the "License");
REM  you may not use this file except in compliance with the License.
REM  You may obtain a copy of the License at
REM
REM      http://www.apache.org/licenses/LICENSE-2.0
REM
REM  Unless required by applicable law or agreed to in writing, software
REM  distributed under the License is distributed on an "AS IS" BASIS,
REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
REM  See the License for the specific language governing permissions and
REM  limitations under the License.
REM
REM @@@ END COPYRIGHT @@@


RowSets.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% 

REM date
echo ""
echo "Test Results for ROWSETS TESTS"
echo "----------------------------"

grep -ih 'TEST RESULT' *.log | tee summary.sum

echo "-------------------"
echo "END OF ROWSETS TESTS"

chmod -R 777 *
