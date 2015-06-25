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

#include "stdafx.h"

#ifdef WIN32

#define OPTERRCOLON (1)
#define OPTERRNF (2)
#define OPTERRARG (3)

TCHAR *optarg;
int optind = 1;
int opterr = 1;
int optopt;

static int
optiserr(int argc, TCHAR * const *argv, int oint, const TCHAR *optstr,
         int optchr, int err)
{
    if(opterr)
    {
        fprintf(stderr, "Error in argument %d, TCHAR %d: ", oint, optchr+1);
        switch(err)
        {
        case OPTERRCOLON:
            fprintf(stderr, ": in flags\n");
            break;
        case OPTERRNF:
            fprintf(stderr, "option not found %c\n", argv[oint][optchr]);
            break;
        case OPTERRARG:
            fprintf(stderr, "no argument for option %c\n", argv[oint][optchr]);
            break;
        default:
            fprintf(stderr, "unknown\n");
            break;
        }
    }
    optopt = argv[oint][optchr];
    return('?');
}
    
   

int
getopt(int argc, TCHAR* const *argv, const TCHAR *optstr)
{
    static int optchr = 0;
    static int dash = 0; /* have already seen the - */

    TCHAR *cp;

    if(optind >= argc)
        return(EOF);
    if(!dash && (argv[optind][0] !=  '-'))
        return(EOF);
    if(!dash && (argv[optind][0] ==  '-') && !argv[optind][1])
    {
        /*
         * use to specify stdin. Need to let pgm process this and
         * the following args
         */
        return(EOF);
    }
    if((argv[optind][0] == '-') && (argv[optind][1] == '-'))
    {
        /* -- indicates end of args */
        optind++;
        return(EOF);
    }
    if(!dash)
    {
        assert((argv[optind][0] == '-') && argv[optind][1]);
        dash = 1;
        optchr = 1;
    }

    /* Check if the guy tries to do a -: kind of flag */
    assert(dash);
    if(argv[optind][optchr] == ':')
    {
        dash = 0;
        optind++;
        return(optiserr(argc, argv, optind-1, optstr, optchr, OPTERRCOLON));
    }
    if(!(cp = (TCHAR*)_tcschr(optstr, argv[optind][optchr])))
    {
        int errind = optind;
        int errchr = optchr;

        if(!argv[optind][optchr+1])
        {
            dash = 0;
            optind++;
        }
        else
            optchr++;
        return(optiserr(argc, argv, errind, optstr, errchr, OPTERRNF));
    }
    if(cp[1] == ':')
    {
        dash = 0;
        optind++;
        if(optind == argc)
            return(optiserr(argc, argv, optind-1, optstr, optchr, OPTERRARG));
        optarg = argv[optind++];
        return(*cp);
    }
    else
    {
        if(!argv[optind][optchr+1])
        {
            dash = 0;
            optind++;
        }
        else
            optchr++;
        return(*cp);
    }
    assert(0);
    return(0);
}

#endif /* WIN32 */
