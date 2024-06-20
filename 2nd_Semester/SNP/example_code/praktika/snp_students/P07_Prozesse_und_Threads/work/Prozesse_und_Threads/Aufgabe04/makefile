# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc
CMPFLAGS=   -Wall 
LDFLAGS=    
EXENAM1=    ProcA4.e
FNAM1=      ProcA4.o workerUtils.o selectCPU.o
LIBNAME=

$(EXENAM1):	$(FNAM1)
	$(CMP)  $(FNAM1) $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f *.o $(EXENAM1)

all:
	@make clean
	@make

