# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc
CMPFLAGS=   -Wall
LDFLAGS=
EXENAME=    ProcA2.e
FNAME=      ProcA2
EXENAMC=    ChildProcA2.e
FNAMC=      ChildProcA2
LIBNAME=
LIBNAME=

compile:	$(EXENAME) $(EXENAMC)

$(EXENAME):	$(FNAME).o
	$(CMP)  $(FNAME).o $(LIBNAME) $(LDFLAGS) -o $@

$(EXENAMC):	$(FNAMC).o
	$(CMP)  $(FNAMC).o $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f *.o $(EXENAME) $(EXENAMC)

all:
	@make clean
	@make
