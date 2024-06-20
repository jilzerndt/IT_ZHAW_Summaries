# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=       gcc
CMPFLAGS=  -Wall
LDFLAGS=
EXENAM1=   ProcA1.e
FNAM1=     ProcA1
LIBNAME=

$(EXENAM1): $(FNAM1).o
	$(CMP)  $(FNAM1).o $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f *.o $(EXENAM1)

all:
	@make clean
	@make
