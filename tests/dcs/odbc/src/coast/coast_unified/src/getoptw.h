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
