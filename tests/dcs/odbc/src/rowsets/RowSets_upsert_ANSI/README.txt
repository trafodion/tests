- @@@ START COPYRIGHT @@@
-
- (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
-
-  Licensed under the Apache License, Version 2.0 (the "License");
-  you may not use this file except in compliance with the License.
-  You may obtain a copy of the License at
-
-      http://www.apache.org/licenses/LICENSE-2.0
-
-  Unless required by applicable law or agreed to in writing, software
-  distributed under the License is distributed on an "AS IS" BASIS,
-  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-  See the License for the specific language governing permissions and
-  limitations under the License.
-
- @@@ END COPYRIGHT @@@


- The linux version of RowSets_ANSI is built and run from the linux build 
  structure.  See README.txt in the build strcuture for more details.

- To build the windows version
  (1) Go to RowSets_ANSI\builds_win, click on RowSets.vcproj, or any other
      vcproj file that is suitable for your machine.
  (2) on top of the window bar select:
      * 64-bit machine: Solution Configurations: Debug
                        Solution Platforms: x64
      * 32-bit machine: Solution Configurations: Debug
                        Solution Platforms: Win32
  (3) Build -> Rebuild Solution. 
      Rowsets.exe should be generated in
      * 64-bit machine: RowSets_ANSI\builds_win\Debug\x64
      * 32-bit machine: RowSets_ANSI\builds_win\Debug\Win32

- To run the windows version
  (1) Make sure that the data source that you want to use is registered:
      Control Panel -> Administrative Tools -> Data Sources (ODBC)
      If it is not there, you can either add it as "User DSN" for only
      this particular user, or "System DSN" for everyone to use.  It 
      does not matter since everyone log on to the PC using the same
      administrator account.
  (2) Open a DOS window, cd to where the program is (see to build it session
      about where the exe file is on each different type of machines).
  (3) If you are running from a 32-bit machine:
      * Modify ..\..\env_win32.bat to have your dsn/usrid/password/charset.
      * ..\..\env_win32.bat
      * ..\..\run.bat
      If you are running from a 64-bit machine:
      * Modify ..\..\env_win64.bat to have your dsn/usrid/password/charset.
      * ..\..\env_win64.bat
      * ..\..\run.bat
  (4) Once you are done, please move the log files to the linux location
      where all log files are saved.

