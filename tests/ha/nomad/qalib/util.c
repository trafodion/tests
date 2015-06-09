/*******************************************/
/* UTIL.C : library of C utility functions */
/*******************************************/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "util.h"

/***********************************************************************
** blank_pad()
**
** This function will append to the end of a string a certain number
** of blanks to make the string <size> bytes long.  It should be noted
** that no NULL terminator is put on the end of the blank padded string.
************************************************************************/
void blank_pad(char *buffer, size_t size)
   {
   size_t i;

   i=strlen(buffer);
   if (i<size) {
   	memset(&buffer[i],' ',size-i);
   	memset(&buffer[i+1],' ',size-i);
   }
   }

char *remove_char(char *buffer,unsigned int char_to_remove)
   {
   char *ptr;
   char *tptr;
   char tbuffer[255];

   tptr=tbuffer;
   ptr=buffer;
   while(*ptr!=NULL){
      if(*ptr!=char_to_remove){
         *tptr=*ptr;
         tptr++;
         }
      ptr++;
      }
   *tptr=NULL;
   strcpy(buffer,tbuffer);
   return(buffer);
   }

char *toupper_s(ptr)
char *ptr;
{
   char *saved_ptr;

   saved_ptr=ptr;

   /* scan string converting each character to upper case */
   while(*ptr!=NULL) {
      if(islower(*ptr)) *ptr=toupper(*ptr);
      ptr++;
      }

   return(saved_ptr);
   } /* end: toupper_s() */

/***********************************************************************
** atoh()
**
** This function converts a string of bytes into printable hex digits
** It returns a pointer to the string of hex digits.
************************************************************************/
char *atoh(char *InStrPtr,int InStrLen)
{
   char *HexStrPtr;
   int i;
   char *HexPtr;
   struct Byte{
      unsigned HighNibble  :4;
      unsigned LowNibble   :4;
      unsigned             :8; /* this is just here to remind you that */
                               /* bit fields are packed into an integer */
                               /* even if they only total 8 bits (1 byte) */
      };
   struct Byte *InPtr;

   HexStrPtr=(char *)malloc(2*InStrLen+1);
   HexPtr=HexStrPtr;
   for(i=0;i<InStrLen;i++){
      InPtr=(struct Byte *)InStrPtr;
      sprintf(HexPtr,"%X%X",InPtr->HighNibble,InPtr->LowNibble);
      HexPtr+=2;
      InStrPtr++;
      }
   *HexPtr=NULL;
   return(HexStrPtr);
   } /* end: atoh() */

/***********************************************************************
** HexStrToBytes()
**
** This function converts an ascii string of hex digits into its binary
** equivalent in bytes and returns a pointer to that buffer.
************************************************************************/
void *HexStrToBytes(char *StrPtr)
{
   char *ByteBufferPtr;
   char *HexStrPtr;
   char HexByte[3];
   void *BufferPtr;
   int BufferLength;
   int IntBuffer;
   int i;

   /* compute the length of the buffer needed to hold the bytes */
   BufferLength=((int)(strlen(StrPtr)+1)/2);
   BufferPtr=malloc(BufferLength);

   ByteBufferPtr=(char *)BufferPtr;
   HexStrPtr=StrPtr;

   for(i=0;i<BufferLength;i++){
      memcpy(HexByte,HexStrPtr,2);
      HexByte[2]=NULL;
      sscanf(HexByte,"%2X",&IntBuffer);
      *ByteBufferPtr=(char)IntBuffer;
      ByteBufferPtr++;
      HexStrPtr+=2;
      }

   return(BufferPtr);

   } /* end: HexStrToBytes() */



/************************************************************************
** LongRand()
**
** Returns a long random number from 0 to <range>-1
************************************************************************/
long LongRand(long range)
{
   union{
      struct{
         int HighInt;
         int LowInt;
         } LongIntStruct;
      long RandomNumber;
      } u1;

   u1.LongIntStruct.HighInt=rand();
   u1.LongIntStruct.LowInt=rand();
   return(u1.RandomNumber%range);
   } /* end: LongRand() */

/************************************************************************
** LongRandRange()
**
** Returns a long random number from min to max
************************************************************************/
long LongRandRange(long min,long max)
{
   union{
      struct{
         int HighInt;
         int LowInt;
         } LongIntStruct;
      long RandomNumber;
      } u1;
   long range;

   range=max-min;
   u1.LongIntStruct.HighInt=rand();
   u1.LongIntStruct.LowInt=rand();
   return((u1.RandomNumber%range)+min);
   } /* end: LongRand() */

/************************************************************************
** fget_s()
**
** This function works just like the standard 'fgets()' function except
** the newline and carriage return characters on the end of the input (if any)
** are replaced by a NULL which is what most programmers expect, anyway.
************************************************************************/
char *fget_s(char *buffer,int buf_size,FILE *fp)
{
   char *ptr;
   int i;

   ptr=fgets(buffer,buf_size,fp);
   if(ptr==NULL) return(ptr);

   i=(int)strlen(buffer);
   if((buffer[i-1]=='\n') || (buffer[i-1]=='\r')) buffer[i-1]=NULL;
   if((buffer[i-2]=='\r')) buffer[i-2]=NULL;
   return(ptr);
   } /* end: fget_s() */

/************************************************************************
** get_s()
**
** This function works just like the standard 'gets()' function except
** the newline and carriage return characters on the end of the input (if any)
** are replaced by a NULL which is what most programmers expect, anyway.
************************************************************************/
char *get_s(char *buffer)
{
   char *ptr;
   int i;

   ptr=gets(buffer);
   if(ptr==NULL) return(ptr);

   i=(int)strlen(buffer);
   if((buffer[i-1]=='\n') || (buffer[i-1]=='\r')) buffer[i-1]=NULL;
   if((buffer[i-2]=='\r')) buffer[i-2]=NULL;
   return(ptr);
   }

/************************************************************************
** sysnn()
**
** Returns the integer value of the current SYSnn or a negative number
** representing the error returned from PROCESS_GETINFOLIST_.
* >>> perhaps replace this with a java stored procedure someday if it is needed
************************************************************************/
/*
int sysnn(char *SystemNamePtr)
{
   #define PROGRAM_FILE     4

   int i;
   int error;
   int ErrorDetail;
   int RetAttrList[1];
   struct{
      int len;
      char OsimageFilename[80];
      } RetValuesList;
   int RetValuesLen;
   int SysnnNumber;
   char SystemName[80];
   int MyProcessHandle[10];
   int pin;
   int cpu;
   int SystemNumber;
   union{
      long status;
      struct{
         int CpuCount;
         int Cpus;
         }System;
      }u1;
   int BitMask;



   // if no remote system name was specified then get my local cpu...
   //...number since it is a cpu that is obviously up
   if(*SystemNamePtr==NULL){

      // get my cpu number since it is a cpu that is obviously up
      error=PROCESSHANDLE_NULLIT_(MyProcessHandle);
      if(error) return(-error);
      error=PROCESS_GETINFO_(MyProcessHandle);
      if(error) return(-error);
      error=PROCESSHANDLE_DECOMPOSE_(MyProcessHandle,&cpu);
      if(error) return(-error);
      }

   // otherwise, we need to find a valid cpu number on the remote system
   else {
      strcpy(SystemName,SystemNamePtr);
      blank_pad(SystemName,8);
      SystemName[8]=NULL;
      LOCATESYSTEM(&SystemNumber,(int *)SystemName);
      u1.status=REMOTEPROCESSORSTATUS(SystemNumber);
      i=15;
      BitMask=1;
      while(!(u1.System.Cpus & BitMask) && (i>=0)){
         i--;
         BitMask<<=1;
         }
      cpu=i;
      }

   // get the program filename for the cpu, pin 0 which will be the...
   //...current OSIMAGE filename
   RetAttrList[0]=PROGRAM_FILE;
   pin=0;
   error=PROCESS_GETINFOLIST_(cpu,&pin,
                              SystemNamePtr,(int)strlen(SystemNamePtr),
                              pin,
                              RetAttrList,1,
                              (int *)&RetValuesList,
                              (int)(sizeof(RetValuesList)+1)/2,
                              &RetValuesLen,&ErrorDetail);
   if(error) return(-error);

   RetValuesList.OsimageFilename[RetValuesList.len]=NULL;

   // scan for the system name (not used for now) and the SYSnn
   sscanf(RetValuesList.OsimageFilename,
          "\%[^.].$SYSTEM.SYS%d.OSIMAGE",SystemName,&SysnnNumber);

   return(SysnnNumber);

   } // end: sysnn()
*/
/***********************************************************************
** RandomString()
**
** This function returns a pointer to a NULL terminated ASCII string of
** characters randomly selected from 'A'-'Z' and 'a'-'z'.  The string
** will be <length> characters long.  This length does NOT include the
** NULL at the end of the string.
**
** NOTE: numeric characters ('1'-'9') are not used.
************************************************************************/
char *RandomString(int length)
{
   char *StringPtr;
   char *StringBeginningPtr;
   char Letters[53]={"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"};
   int i;

   /* allocate space for the string */
   StringPtr=(char *)malloc(length+1);
   StringBeginningPtr=StringPtr;

   /* loop, randomly filling the string */
   for(i=0;i<length;i++){
      *StringPtr=Letters[(rand()%52)];
      StringPtr++;
      }

   /* add NULL terminator */
   *StringPtr=NULL;

   return(StringBeginningPtr);
   }


//************************************************************
// FormatHexOutput()
// This function will format a buffer to be displayed as a hex
// string followed by its ascii representation, if possible.
//************************************************************
void FormatHexOutput( char *In
                    , char *Out
                    , long Length )
{
	long i;
	char *InBase = In;
	static char HexChars[] = "0123456789ABCDEF";

	if(Length <= 0 ){
		*Out='\0';
		return;
		}

	// convert the input bytes to hex
	for( i = 0; i < Length; i++ ){
      sprintf(Out," %02x", (unsigned char)*In);
		Out+=3;;
		In++;
		}

	*Out++ = ' ';

	// output the original data
	In = InBase;
	for( i = 0; i < Length; i++ ){
		if( isprint( *In ) )
			*Out++ = *In++;
		else{
			*Out++ = '.';
			++In;
			}
		}
	*Out = '\0';

	return;

	}  // end of FormatHexOutput
