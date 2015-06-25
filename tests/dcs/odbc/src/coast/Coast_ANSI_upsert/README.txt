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



- The unix version of Coast_ANSI is built and run from the unix build 
  structure.  See README.txt in the build strcuture for more details.

- To build the windows version
  (1) Go to Coast_ANSI\builds_win, click on COAST.vcproj, or any other vcproj
      file that is suitable for your machine.
  (2) on top of the window bar select:
      * 64-bit machine: Solution Configurations: Debug
                        Solution Platforms: x64
  (3) Build -> Rebuild Solution. 
      Coast.exe should be generated in
      * 64-bit machine: Coast_ANSI\builds_win\Debug\x64

- To run the windows version
(A) On the target side:
   The coast tests need setup on the target machine,  see README.txt
   <test_root>/src/odbctest_spjs for more details.  This only needs to
   be done once per machine.

(B) On the client side:
  (1) Make sure that the data source that you want to use is registered:
      Control Panel -> Administrative Tools -> Data Sources (ODBC)
      If it is not there, you can either add it as "User DSN" for only
      this particular user, or "System DSN" for everyone to use.  It 
      does not matter since everyone log on to the PC using the same
      administrator account.
  (2) Open a DOS window, cd to where the program is (see to build it session
      about where the exe file is on each different type of machines).
  (3) Running from a 64-bit machine:
      * Modify ..\..\env_win64.bat to have your dsn/usrid/password/charset.
      * ..\..\env_win64.bat
      * ..\..\run.bat

