# ---------------------------------------------------------------------------
# Makefile 
# Course:   BSy
# Date:	    M. Thaler, 1/2016
# File:     makefile 
# Version:  v.fs20
# ---------------------------------------------------------------------------
#macros

CC    	= gcc
CFLGS 	= -std=gnu99
LIBS	= -pthread
OFILES 	= main.o banking.o
HFILES  = banking.h

main:		$(OFILES) $(HFILES)
		$(CC) $(CFLGS) $(LIBS) $(OFILES) -o $@.e

.c.o:		
		$(CC) $(CFLGS) -c $<

.cc.o:
		$(CC) $(CFLGS) -c $<

clean:		
		rm -f *.o *.e
		@echo "directory cleaned"

all:
		@rm -f *.o
		make --no-print-directory main
#-----------------------------------------------------------------------------
