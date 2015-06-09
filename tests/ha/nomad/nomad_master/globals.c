//******************************************************************
//** GLOBALS.C - Declarations for global variables
//*******************************************************************
#include "commonglobals.c"
char g_CommandLine[16384];

char g_errstr[10] = "***ERROR:";
char g_indent[10] = "         ";
char g_token_string[80];
short g_current_token;
test_desc g_info;
char g_nomad_volume[_MAX_PATH];
char g_testid_file[_MAX_PATH];
char g_input_line[MAX_LINE];
HENV ghenv;
HDBC ghdbc;
HSTMT ghstmt;
