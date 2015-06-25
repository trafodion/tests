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


#include "wcharsplmt.h"
#include "common.h"

#define MAX_PATH_LEN 1024
#define MAX_MODE_LEN 20
#define MAX_MSG_LEN 2000

UFILE* u_fopen_u(const UChar* ucsFileName, const UChar* mode)
{
	int32_t srcFileLen = u_strlen(ucsFileName) + 1;
	int32_t srcModeLen = u_strlen(mode) + 1;

	// Calculate the max capacity of the output buffer size
	int32_t destFileLen = UCNV_GET_MAX_BYTES_FOR_STRING(srcFileLen, ucnv_getMaxCharSize(icu_conv->converter));
	int32_t destModeLen = UCNV_GET_MAX_BYTES_FOR_STRING(srcModeLen, ucnv_getMaxCharSize(icu_conv->converter));

	char *filename = (char*)malloc(sizeof(char)*destFileLen);
	char *cmode = (char*)malloc(sizeof(char)*destModeLen);

	UFILE *ufile;

	ucnv_fromUChars(icu_conv->converter, filename, destFileLen, ucsFileName, -1, &icu_conv->err);
	ucnv_fromUChars(icu_conv->converter, cmode, destModeLen, mode , -1, &icu_conv->err);

	ufile = u_fopen(filename, cmode, icu_conv->locale, icu_conv->codepage);

	free(filename);
	free(cmode);
	return ufile;
}

void u_perror(const UChar* uerr)
{
	int32_t ulen = u_strlen(uerr) + 1; 
	int32_t clen = UCNV_GET_MAX_BYTES_FOR_STRING(ulen, ucnv_getMaxCharSize(icu_conv->converter));
	
	char* cerr = (char*)malloc(sizeof(char)*clen);
	
	ucnv_fromUChars(icu_conv->converter, cerr, clen, uerr, ulen , &icu_conv->err);
	perror(cerr);

	free(cerr);
	cerr = NULL;
}

// printf for UChar strings.
/*
int32_t u_printf_u(const UChar *format, ...)
{
	int32_t pnum;
	va_list arglist;
	
	int len = u_strlen(format) + 1;
	char buff[len];
//	UChar* TempArg;

	va_start(arglist, format);
//	TempArg = va_arg(arglist, UChar*);

//	while(1)
//	{
//		temp = va_arg(arglist, short);
//		if(temp == 0)
//			break;
//	}

	ucnv_fromUChars(icu_conv->converter, buff, len, format, u_strlen(format) , &icu_conv->err);
	buff[len] = '\0';

	pnum = vprintf(buff, arglist);

	va_end(arglist);

	return pnum;
}
* */

int32_t u_printf_conv(const UChar* format, ...)
{
	va_list argList;
	va_start(argList, format);

	UChar *u_OutputString = (UChar*)malloc(sizeof(UChar)*10000);
	char *OutputString = (char*)malloc(sizeof(char)*20000);

	u_vsprintf_u(u_OutputString, format, argList);
	va_end(argList);
	
	ucnv_fromUChars(icu_conv->converter, OutputString, 20000, u_OutputString, -1, &icu_conv->err);
	int pnum = printf("%s\n", OutputString);

	free(u_OutputString);
	free(OutputString);

	//u_OutputString = NULL;
	//OutputString = NULL;
	return pnum;
}

// Unicode version of strtok (implement for icu)
UChar* u_strtok(UChar *wcs, const UChar *delim)
{
	UChar* savePtr = NULL;
	return u_strtok_r(wcs, delim, &savePtr);
}

// Convert date and time to a unicode string
size_t u_strftime(UChar* ucs, size_t maxsize,
		const UChar* format, const struct tm* timeptr)
{
	size_t rt;
	int32_t fLen = u_strlen(format) + 1;
	int32_t outFormatLen = UCNV_GET_MAX_BYTES_FOR_STRING(fLen, ucnv_getMaxCharSize(icu_conv->converter));
	int32_t tLen = outFormatLen 
		+ 4		// Year
		+ 2		// Month
		+ 2		// Day
		+ 2		// Hour
		+ 2		// Minute
		+ 2		// Second
		+ 4;	// For null-terminated
	
	int p_maxSize = maxsize/4;
	if( p_maxSize < tLen)
	{
		printf("The given buffer length formating time string is not sufficient. Exit......\n");
		exit(1);
	}

	// Convert the format string from UChar* to char*, thus strftime can accept it as its arg.
	char *tempFormatBuffer = (char*)malloc(sizeof(char)*outFormatLen);
	ucnv_fromUChars(icu_conv->converter, tempFormatBuffer, outFormatLen, format, -1, &icu_conv->err);

	// Call the ANSI version of strftime() function to convert the date and time into a char string
	char *tempTimeBuffer = (char*)malloc(sizeof(char)*p_maxSize);
	rt = strftime(tempTimeBuffer, p_maxSize, tempFormatBuffer, timeptr);

	// Convert the char string of date time to a UChar string. ucs has mem space already.
	ucnv_toUChars(icu_conv->converter, ucs, maxsize, tempTimeBuffer, -1, &icu_conv->err);

	free(tempTimeBuffer);
	free(tempFormatBuffer);
	return rt;
}

UChar* u_ctime(const time_t *timep)
{
	char *tempstr = ctime(timep);
	int len = 4 * (strlen(tempstr) + 1);
	UChar *retucs = (UChar*)malloc(len);

	ucnv_toUChars(icu_conv->converter, retucs, len, tempstr, -1, &icu_conv->err);

	return retucs;
}

/*
 * Duplicate a unicode string with a new pointer
 */
UChar* u_strdup(const UChar* ucs)
{
	uint32_t len = u_strlen(ucs) + 1;
	UChar* dupucs = (UChar*)malloc(sizeof(UChar)*len);

	return u_strcpy(dupucs,ucs);
}

/*
 * Convert the string ucs to upper case
 * returns the pointer of the new string
 * */
UChar* u_strupr(UChar* ucs)
{
	int32_t destlen = u_strlen(ucs)+1;
	UChar* dest = (UChar*)malloc(sizeof(UChar)*destlen);
	UErrorCode errorCode = U_ZERO_ERROR;

	int32_t resLen = u_strToUpper(dest, destlen, ucs, -1, NULL, &errorCode);

	if(resLen > 0)
		return dest;
	else
		return NULL;
}

/*
 * Compare two strings, case insensitive. Returns a negative,
 * zero, or positive integer, respectively indicating that 
 * ucs1 is less than, match, or greater than ucs2.
 * */
int32_t u_stricmp(const UChar* ucs1,const UChar* ucs2)
{
	return u_strcasecmp(ucs1, ucs2, U_FOLD_CASE_DEFAULT);
}

/*
 * Compare two strings within specified n characters,
 * case insensitive. Returns a negative, zero, or positive
 * integer, respectively indicating that ucs1 is less than,
 * match, or greater than ucs2.
 * */
int32_t u_strnicmp(const UChar* ucs1, const UChar* ucs2, int32_t n)
{
	return u_strncasecmp(ucs1, ucs2, n, U_FOLD_CASE_DEFAULT);
}

// Convert a unicode string to double numbers
double ucnv_tof(const UChar *nptr)
{
	if(nptr == NULL)
	{
		return 0;
	}

	int32_t len = u_strlen(nptr) + 1;
	int32_t destLen = UCNV_GET_MAX_BYTES_FOR_STRING(len, ucnv_getMaxCharSize(icu_conv->converter));
	
	char *buff= (char*)malloc(sizeof(char)*destLen);

	ucnv_fromUChars(icu_conv->converter, buff, destLen, nptr, -1, &icu_conv->err);

	double ret = atof(buff);
	free(buff);

	return  ret;
}

// Convert a integer value to a unicode string(UChar*)
UChar* ucnv_fromi(int value, UChar* ucs, int radix)
{
	int32_t rt = 0;
	if(ucs == NULL)
	{
		return NULL;
	}

	if(radix <= 0 || radix > 36)
	{
		return NULL;
	}

	rt = u_snprintf(ucs, radix, "%d", value);
	if(rt > radix)
	{
		return NULL;
	}
	ucs[rt] = '\0';

	return ucs;
}

// Convert a long int value to a unicode string(UChar*)
UChar* ucnv_froml(long value, UChar* ucs, int radix)
{
	int32_t rt = 0;
	if(ucs == NULL)
	{
		return NULL;
	}

	if(radix <= 0 || radix > 36)
	{
		return NULL;
	}

	rt = u_snprintf(ucs, radix, "%ld", value);
	if(rt > radix)
	{
		return NULL;
	}
	ucs[rt] = '\0';

	return ucs;
}

// Convert a UChar string which represent a number to an integer value
int ucnv_toi(const UChar *nptr)
{
	if(nptr == NULL)
	{
		return 0;
	}

	int32_t len = u_strlen(nptr) + 1;
	int32_t destLen = UCNV_GET_MAX_BYTES_FOR_STRING(len, ucnv_getMaxCharSize(icu_conv->converter));
	
	char *buff= (char*)malloc(sizeof(char)*destLen);
	ucnv_fromUChars(icu_conv->converter, buff, destLen, nptr, len, &icu_conv->err);

	int ret = atoi(buff);

	free(buff);
	return ret;
}

// Convert mbs to UChar string.
size_t u_mbstoucs(UChar* dest, const char* src, size_t n)
{
	int slen = strlen(src) + 1;
	int32_t destLen = slen * 2;

	size_t rt = ucnv_toUChars(icu_conv->converter, dest, destLen, src, -1, &icu_conv->err);
	dest[destLen] = (UChar)L'\0';
}

// Convert UChar string to mbs string.
size_t u_ucstombs(char* dest, const UChar* uSrc, size_t n)
{
	int ulen = u_strlen(uSrc) + 1;
	int destLen = n;
//	int32_t destLen = UCNV_GET_MAX_BYTES_FOR_STRING(ulen, ucnv_getMaxCharSize(icu_conv->converter));

//	char *buff = (char*)malloc(sizeof(char) * destLen);
	size_t rt = ucnv_fromUChars(icu_conv->converter, dest, destLen, uSrc, -1, &icu_conv->err);

	return rt;
}

// UChar version of _stprintf, with %s conversion modifier
// instead of %S for Unicode conversion, for complying 
// with Windows call of _stprintf.
#if defined(unixcli)&&defined(UNICODE)
int32_t u_sprintf_conv(UChar* ucs, const UChar* format, ...)
{
	va_list argList;
	int32_t retvalue = 0;

	va_start(argList, format);

	if(u_strstr(format, (UChar*)L"s") != NULL)
	{
		UChar *ucsFormat = replace_sToS(format);
		retvalue = u_vsprintf_u(ucs, ucsFormat, argList);
		
		free(ucsFormat);
		ucsFormat = NULL;
	}
	else
		u_vsprintf_u(ucs, format, argList);
	
	va_end(argList);

	return retvalue;
}

int32_t u_vfprintf_conv(UFILE* ufile, const UChar* format, va_list ap)
{
	int32_t retvalue = 0;
	if(u_strstr(format, (UChar*)L"s") != NULL)
	{
		UChar* ucsFormat = replace_sToS(format);
		retvalue = u_vfprintf_u(ufile, ucsFormat, ap);
		free(ucsFormat);
		ucsFormat = NULL;
	}
	else
		retvalue = u_vfprintf_u(ufile, format, ap);

	return retvalue;
}

int32_t u_fprintf_conv(UFILE* ufile, const UChar* format, ...)
{
	va_list argList;
	va_start(argList, format);

	int32_t retvalue = 0;
	if(u_strstr(format, (UChar*)L"s") != NULL)
	{
		UChar *ucsFormat = replace_sToS(format);
		retvalue = u_vfprintf_u(ufile, ucsFormat, argList);
		free(ucsFormat);
		ucsFormat = NULL;
	}
	else
		retvalue = u_vfprintf_u(ufile, format, argList);

	va_end(argList);

	return retvalue;
}


// Replace %s with %S on POSIX for /printf/sprintf/...
// Returns the number of 's' has been replaced
UChar* replace_sToS(const UChar* format)
{
	int len = u_strlen(format)+1;
	int32_t iCount = 0;

	UChar *savePtr = NULL;

	UChar buff[len];
	UChar subStr[len];
	UChar *dest = (UChar*)malloc(len * sizeof(UChar));

	u_strcpy(dest, (UChar*)L"");
	u_strcpy(buff, format);
	buff[len] = '\0';

	UChar* temp = u_strtok_r(buff, (UChar*)L"s", &savePtr);

	bool bSetFirst_s = false;
	while(temp)
	{
		// if the source string begins with the delim, strtok_r returns the sub
		// strings between the frist delim and second delim, thus we need to add
		// the first 's' here to the begining of the destination string.
		if(!bSetFirst_s && (buff[0] == L's')) {
			u_strcpy(subStr, (UChar*)L"s");
			u_strcat(subStr, (const UChar*)temp);
			bSetFirst_s = true;
		} else {
			u_strcpy(subStr, (const UChar*)temp);
			bSetFirst_s = true;
		}

		UChar leadChr = subStr[u_strlen(subStr)-1];
		if(leadChr == PERCENT_SIGN)	// if the leading character of current 's' is '%'
		{
			u_strcat(subStr, (UChar*)L"S");	// replace the s with upper 'S'
			iCount++;
		}
		else
		{
			if(savePtr)		//If savePtr is NULL, means no token is found, do nothing
			{
				if(u_strcmp(savePtr, (UChar*)L""))	// else remain with lower 's' if it is not the end of the string
				{
					u_strcat(subStr, (UChar*)L"s");
					iCount++;
				}
			}
		}
		u_strcat(dest, (const UChar*)subStr);	// concatenate to the new format string with upper '%S'

		temp = u_strtok_r(NULL, (UChar*)L"s", &savePtr);
	}

	return dest;
}
#endif //end of if defined unixcli and UNICODE
