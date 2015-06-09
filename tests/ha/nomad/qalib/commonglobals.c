//******************************************************************
//** commonglobals.C - Declarations for global variables
//*******************************************************************

#include "defines.h"

char gCommandFile[100];	// input command file name
SQLTypeInfo *gpSQLTypeInfoList;
char gDataSource[MAX_DATASOURCE_NAME];
char gUID[MAX_UID];
char gPWD[MAX_PWD];
long gMaxRowSize;
long gTrace=0;
long gDebug=0;
short gStopOnError = 0;             // flag to denote stopping on consistency errors
