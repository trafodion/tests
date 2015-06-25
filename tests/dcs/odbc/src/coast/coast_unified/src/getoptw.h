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


#ifndef __GETOPT_W_H
#define __GETOPT_W_H

#include "common.h"

#ifdef __cplusplus
#ifdef aCC_COMPILER
	int getopt_c(int argc, TCHAR* const *argv, const TCHAR *optstr);
	extern TCHAR *tcs_optarg;
	extern TCHAR *secondarg;
#else // else of aCC_COMPILER
	extern "C" {
		extern TCHAR *tcs_optarg;
		extern TCHAR *secondarg;
		extern int getopt_c(int argc, TCHAR** argv, const TCHAR *optstr);
		extern int optind;
		extern int opterr;
		extern int optopt;
	}
#endif
#endif

#endif /* GETOPT_H */
