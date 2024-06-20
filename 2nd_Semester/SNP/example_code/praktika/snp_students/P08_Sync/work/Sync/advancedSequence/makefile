# BSy M. Thaler
# Version v.fs20

CMP=		gcc -std=gnu99
CMPFLAGS=	-Wall -g
LIB=		-pthread	
EXENAME0=	startApp.e
EXENAME1=	coffeeTeller.e
EXENAME2=	customer.e

doit:
		@make --no-print-directory clean
		@make --no-print-directory startApp
		@make --no-print-directory coffeeTeller
		@make --no-print-directory customer

startApp:	startApp.o 
		$(CMP) $(CMPFLAGS) startApp.o $(LIB) -o $(EXENAME0)

coffeeTeller:	coffeeTeller.o 
		$(CMP) $(CMPFLAGS) coffeeTeller.o $(LIB) -o $(EXENAME1)

customer:	customer.o 
		$(CMP) $(CMPFLAGS) customer.o $(LIB) -o $(EXENAME2)

.c.o:		
		$(CMP) -c $(CMPFLAGS) $<

.cc.o:		
		$(CMP) -c $(CMPFLAGS) $<

all:
		@make clean
		make doit

clean:		
		@rm -f *.e *.o

purge:
		@make clean
