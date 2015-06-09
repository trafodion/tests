#ifndef __COMMONGLOBALSH      /* this prevents multiple copies of this... */
#define __COMMONGLOBALSH      /* ...include file from being #included... */


extern char gCommandFile[100];	// input command file name
extern SQLTypeInfo *gpSQLTypeInfoList;
extern char gDataSource[MAX_DATASOURCE_NAME];
extern char gUID[MAX_UID];
extern char gPWD[MAX_PWD];
extern long gMaxRowSize;
extern long gTrace;
extern long gDebug;
extern short gStopOnError;       // stop on errors if TRUE (1)

#endif
