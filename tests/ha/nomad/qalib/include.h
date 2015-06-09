/*************************************************************************
** INCLUDE.H
**
** Common include file which should be used by most ODBC QA C programs.
**************************************************************************/


/*************************************************************************
**
** Standard Includes - saves everyone from including all these in each
**                     program file
**
**************************************************************************/
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
//#include <direct.h>
#include <fcntl.h>
#include <ctype.h>
#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <sys/stat.h>
//#include <windows.h>
//#include <crtdbg.h>
#include <sqlext.h>		// needed for ODBC
#include <assert.h>
#include <errno.h>
#include <unistd.h>

/*********************************************
 * Additional includes for user libraries
 * *******************************************/
#include "util.h"
#include "log.h"
