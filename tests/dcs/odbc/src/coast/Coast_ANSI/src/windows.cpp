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

//#include <fs\feerrors.h>
#include <stdio.h>
#include <windows.h>
//#include <odbcCommon.h>
//#include <odbcsrvrcommon.h>
#ifndef unixcli
//#include <cextdecs.h>
#else
#include <unistd.h>
#endif

/*
char * _strupr(char *);
char * _itoa(int, char *, int);
char * _ltoa(long, char *, int);
*/

char * _strupr(char * str) 
{

	char *s;
    for (s=str ; *s != '\0'; s++)  if (*s <= 'z' && *s >= 'a')  *s &= 0xdf;
  
	return str;
}


char * _itoa(int n, char *buff, int base) {

   char t[100], *c=t, *f=buff;
   int d;
   int bit;

   if (base == 10) {
     if (n < 0) {
        *(f++) = '-';
        n = -n;
     }

   while ( n > 0) {
      d = n % base;
      *(c++) = d + '0';
      n = n / base;
   }
   
   }
   
   else {
	  if (base == 2) bit = 1;
      else if (base == 8) bit = 3;
      else if (base == 16) bit = 4;
      else printf("Base value unknown!\n");

	  while (n != 0) {
		 d = (n  & (base-1));
		 *(c++) = d < 10 ? d + '0' : d - 10 + 'A';
		 n = (unsigned int) n >> bit;
	  }

   }

   c--;

   while (c >= t) *(f++) = *(c--);
     
   *f = '\0';
   return buff;

}

#ifndef aCC_COMPILER
char * _ltoa(long n, char *buff, int base) 
{

   char t[100], *c=t, *f=buff;
   long d;
   int bit;

   if (base == 10) {
     if (n < 0) {
        *(f++) = '-';
        n = -n;
	 }

     while (n > 0) {
        d = n % base;
        *(c++) = d + '0';
        n = n / base;
	 }
   }
   
   else {

     if (base == 2) bit = 1;
     else if (base == 8) bit = 3;
     else if (base == 16) bit = 4;
     else ; // printf("Base value unknown!\n");

     while (n != 0) {
        d = (n  & (base-1));
        *(c++) = d < 10 ? d + '0' : d - 10 + 'A';
        n = (unsigned int) n >> bit;
	 }

   }

   c--;

   while (c >= t) *(f++) = *(c--);
     
   *f = '\0';
   return buff;
}
#endif

char *_strdup( const char *strSource )
{
	char* tp = NULL;
	if ((tp = (char*)malloc(strlen(strSource)+1))!=NULL)
		strcpy(tp,strSource);
	return tp;
}


char* _ultoa(unsigned long n, char *buff, int base)
{

   char t[100], *c=t, *f=buff;
   unsigned long d;
   int bit;

   if (base == 10) {

     while (n > 0) {
        d = n % base;
        *(c++) = d + '0';
        n = n / base;
	 }
   }
   
   else {

     if (base == 2) bit = 1;
     else if (base == 8) bit = 3;
     else if (base == 16) bit = 4;
     else ; // printf("Base value unknown!\n");

     while (n != 0) {
        d = (n  & (base-1));
        *(c++) = d < 10 ? d + '0' : d - 10 + 'A';
        n = (unsigned long) n >> bit;
	 }

   }

   c--;

   while (c >= t) *(f++) = *(c--);
     
   *f = '\0';
   return buff;
}

char *_i64toa( __int64 n, char *buff, int base )
{
   char t[100], *c=t, *f=buff;
   long d;
    int bit;

   if (base == 10) {
     if (n < 0) {
        *(f++) = '-';
        n = -n;
	 }

     while (n != 0) {
        d = n % base;
		if (d < 0) d = -d;
        *(c++) = d + '0';
        n = n / base;
	 }
   }
   
   else {
	 short bitlen = 64;

     if (base == 2) bit = 1;
     else if (base == 8) bit = 3;
     else if (base == 16) bit = 4;
     else ; // printf("Base value unknown!\n");

     while (bitlen != 0) {
        d = (n  & (base-1));
        *(c++) = d < 10 ? d + '0' : d - 10 + 'A';
        n =  n >> bit;
		bitlen -= bit;
	 }

   }

   c--;

   while (c >= t) *(f++) = *(c--);
     
   *f = '\0';
   return buff;
}

__int64 _atoi64( const char *s )
{
	__int64 n = 0;
	char* t = (char*)s;
	char c;

	while(*t != 0)
	{
		c = *t++;
		if (c < '0' || c > '9') continue;
		n = n * 10 +c - '0';
	}
	if (*s == '-') n = -n;
	return n;
}


char* trim(char *string)
{
	char sep[] = " ";
	char *token;
	char *assembledStr;

	assembledStr = (char*)malloc( strlen(string) + 1);
	if (assembledStr == NULL ) return string;
	assembledStr[0]=0;

	token = strtok( string, sep );   
	while( token != NULL )   {
	  strcat(assembledStr, token); 
	  token = strtok( NULL, sep );
	  if(token != NULL)
		strcat(assembledStr, sep);
	  }
	strcpy( string, assembledStr);
	free( assembledStr);
	return string;
}

BOOL GetComputerName (LPSTR lpBuffer, LPDWORD nSize)
{
	int actualSize;
#ifndef unixcli
	NODENUMBER_TO_NODENAME_(	-1L,// Node number (if not present or -1 is the current node)
		lpBuffer,	// buffer that contains the name
		*nSize,		// buffer size
		&actualSize);// actual size returned
#else
	gethostname(lpBuffer, actualSize);
#endif
	lpBuffer[actualSize] = '\0';
	*nSize = actualSize;

	return TRUE;
}
/*
int GetWindowText(HWND hWnd, LPTSTR lpString, int nMaxCount )
{
	PROCESS_HANDLE pHandle;
	short retlen = 0;
	lpString[0]=0;

	if (PROCESSHANDLE_GETMINE_(pHandle) == 0)
	{
		PROCESSHANDLE_DECOMPOSE_ (
					pHandle
					,OMITREF			//[ short *cpu ]
					,OMITREF			//[ short *pin ]
					,OMITREF			//[ long *nodenumber ]
					,OMITREF			//[ char *nodename ]
					,OMITSHORT			//[ short maxlen ]
					,OMITREF			//[ short *nodename-length ]
					,lpString			//[ char *procname ]
					,nMaxCount			//[ short maxlen ]
					,&retlen			//[ short *procname-length ]
					,OMITREF			//[ long long *sequence-number ] 
					);
		lpString[retlen]=0;
	}
	return retlen;
}
void ODBCNLS_GetCodePage(unsigned long *dwACP)
{
	*dwACP = 0;
}


// thread functions
struct myThreadDef {
	int ThreadId;
	int ThreadType;
    LPTHREAD_START_ROUTINE lpStartAddress;
    LPVOID lpParameter;
    DWORD dwCreationFlags;
    DWORD ExitCode;
} myThreadDef;

BOOL CloseHandle(HANDLE hObject)
{
	struct myThreadDef * myThread;
	myThread = 	(struct myThreadDef *)hObject;
	if (myThread != NULL)
	{
		delete myThread;
		return TRUE;
	}
	return FALSE;
}
BOOL
GetExitCodeThread(
    HANDLE hThread,
    LPDWORD lpExitCode
    )
{
	struct myThreadDef * myThread;
	myThread = (struct myThreadDef *) hThread;
	if (myThread != NULL)
	{
		*lpExitCode = myThread->ExitCode;
		return TRUE;
	}
	return FALSE;
}

HANDLE
CreateThread(
    LPSECURITY_ATTRIBUTES lpThreadAttributes,
    DWORD dwStackSize,
    LPTHREAD_START_ROUTINE lpStartAddress,
    LPVOID lpParameter,
    DWORD dwCreationFlags,
    LPDWORD lpThreadId
    )
{
	struct myThreadDef *myThread;

	myThread = (struct myThreadDef *) new (struct myThreadDef);
	myThread->lpStartAddress = lpStartAddress;
	myThread->lpParameter = lpParameter;
	myThread->dwCreationFlags = dwCreationFlags;

	if (dwCreationFlags != CREATE_SUSPENDED)
	{
		// call the thread function right away
		myThread->ExitCode = (*lpStartAddress)(lpParameter);
	}
	return (HANDLE) myThread;
}


DWORD
SuspendThread(
    HANDLE hThread
    )
{
	// we can't suspend it, return error
	return 0xFFFFFFFF;
}

DWORD
ResumeThread(
    HANDLE hThread
    )
{
	struct myThreadDef *myThread;

	myThread = (struct myThreadDef *) hThread;
	if (myThread != NULL)
	{
		// call the stored function
		myThread->ExitCode = (*myThread->lpStartAddress)(myThread->lpParameter);
	}
	return 1; // (the thread was suspended and successfully restarted)
}

DWORD
WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
    )
{
	// I don't think there is a need to wait ??
	return WAIT_OBJECT_0;
}


DWORD	GetCurrentProcessId()
{
	short error;
	short processId;
	short cpuNumber;
	short errorDetail;
	PROCESS_HANDLE pHandle;

	if ((error = PROCESSHANDLE_NULLIT_ (pHandle)) != 0)
		return -1;

	if ((error = PROCESSHANDLE_GETMINE_(pHandle)) != 0)
		return -1;

	if ((error = PROCESSHANDLE_DECOMPOSE_ (pHandle
						, &cpuNumber
						, &processId)) != 0)
		return -1;

	if ((error = PROCESS_GETINFO_(pHandle,
			OMITREF, OMITSHORT,OMITREF,		// proc string,max buf len,act len
			OMITREF,						// priority
			OMITREF,						// Mom's proc handle 
			OMITREF, OMITSHORT,OMITREF,		// home term,max buf len,act len  
			OMITREF,						// Process execution time 
			OMITREF,						// Creator Access Id 
			OMITREF,						// Process Access Id 
			OMITREF,						// Grand Mom's proc handle 
			OMITREF,						// Job Id 
			OMITREF, OMITSHORT,OMITREF,		// Program file,max buf len,act len  
			OMITREF, OMITSHORT,OMITREF,		// Swap file,max buf len,act len 
			&errorDetail,
			OMITREF,						// Process type 
			&processId) ) != 0)

	{
		return -1;
	}

	return processId;
}
*/

//========================= Driver Conversion ====================
/*
char *fcvt(double value,int count,int *dec,int *sign ) throw ()
{
	static char buffer[100];
	char inbuffer[100];
	char format[10];
	int lcount;
	char* f=inbuffer;
	char* of=buffer;
	char c;
	bool bdec = false;

	*dec = 0;
	*sign = 0;
	lcount = (count > 40)? 40: count;

	strcpy(format,"%40.");
	strcat(format,_itoa(count,inbuffer,10));
	strcat(format,"f");

	sprintf(inbuffer,format,value);
	
	while(*f++ == ' ');
	f--;

	if(*f=='-') *sign=1;

	while(*f != 0)
	{
		c = *f++;
		if (c=='.') bdec = true;
		if (c < '0' || c > '9') continue;
		*of++ = c;
		if (!bdec) (*dec)++;
		if (bdec && --lcount==0) break;
	}
	while (lcount > 0)
	{
		*of++ = '0';
		lcount--;
	}
	*of = 0;
	return buffer;
}
*/
int _vsnprintf( char *buffer, size_t count, const char *format, va_list argptr )
{ 
	return 0;
}

HANDLE CreateEvent(LPSECURITY_ATTRIBUTES lpEventAttributes, BOOL bManualReset,BOOL bInitialState,LPTSTR lpName ) 
{
	return 0;
}
 
BOOL SetEvent(HANDLE hEvent )
{ 
	return TRUE;
}

DWORD WaitForMultipleObjects(DWORD nCount, const HANDLE *lpHandles, BOOL fWaitAll,DWORD dwMilliseconds )
{
	return WAIT_OBJECT_0;
}

DWORD FormatMessage (DWORD dwFlags, LPCVOID lpSource,DWORD dwMessageId,DWORD dwLanguageId,LPTSTR lpBuffer,DWORD nSize, va_list *Arguments)
{
	if ((lpBuffer = (char*)malloc(10))==NULL)
		return 0;
	itoa(*(int*)lpSource,lpBuffer,10);
	return strlen(lpBuffer);
}

int GetDateFormat(LCID Locale, DWORD dwFlags, CONST SYSTEMTIME *lpDate, LPCTSTR lpFormat, LPTSTR lpDateStr,int cchDate )
{
	return 0;
}

int GetTimeFormat(LCID Locale, DWORD dwFlags, const SYSTEMTIME *lpTime, LPCTSTR lpFormat, LPTSTR lpTimeStr, int cchTime )
{
	return 0;
}

int GetNumberFormat(LCID Locale, DWORD dwFlags, LPCTSTR lpValue, const NUMBERFMT *lpFormat, LPTSTR lpNumberStr, int cchNumber )
{
	return 0;
}

BOOL FreeLibrary( HMODULE hLibModule)
{
	return TRUE;
}

HMODULE GetModuleHandle(LPCTSTR lpModuleName )
{ 
	return 0;
}

int GetLastError()
{
	return 999;
}

HLOCAL LocalFree(HLOCAL hMem )
{
	if (hMem != NULL) free (hMem);
	return NULL;
}

FARPROC GetProcAddress(HMODULE hModule, LPCWSTR lpProcName)
{
	return NULL;
}

void ODBCNLS_ValidateLanguage (unsigned long *dwLanguageId)
{
}




