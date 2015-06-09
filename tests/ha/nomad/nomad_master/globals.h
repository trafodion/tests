#ifndef __GLOBALSH      /* this prevents multiple copies of this... */
#define __GLOBALSH      /* ...include file from being #included... */

#define _MAX_PATH 300

#include "mstruct.h"
#include "commonglobals.h"

extern char g_CommandLine[16384];
extern char g_errstr[10];
extern char g_indent[10];
extern char g_token_string[80];
extern short g_current_token;
extern test_desc g_info;
extern char g_nomad_volume[_MAX_PATH];
extern char g_testid_file[_MAX_PATH];
extern char g_input_line[MAX_LINE];

extern HENV ghenv;
extern HDBC ghdbc;
extern HSTMT ghstmt;

#endif
