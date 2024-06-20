# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc -std=gnu99 -pthread
CMPFLAGS=   -Wall 
LDFLAGS=
EXENAME1=   ProcA9.e
FNAM1=      ProcA9.o selectCPU.o
LIBNAME=    

$(EXENAME1):	$(FNAM1)
	$(CMP)  $(FNAM1) $(LDFLAGS) $(LIBNAME) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $< 

.cc.o:
	$(CMP) -c $(CMPFLAGS) $< 

clean:
	rm -f *.o $(EXENAME1)

all:
	@make clean
	@make

