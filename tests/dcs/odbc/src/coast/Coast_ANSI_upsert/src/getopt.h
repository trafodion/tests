/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

#ifndef __GETOPT
#define __GETOPT

#ifdef __cplusplus
    #ifdef aCC_COMPILER
	 int getopt_c(int argc, char* const *argv, const char *optstr);
	 extern char *secondarg;
    #else
        extern "C" {
		extern char *optarg;
		extern char *secondarg;
		extern int optind;
		extern int opterr;
		extern int optopt;
		extern int getopt_c(int argc, char* const *argv, const char *optstr);
        }
     #endif
#endif

#endif /* GETOPT_H */
