#SNP_SHARED_MAKEFILE := $(if $(SNP_SHARED_MAKEFILE),$(SNP_SHARED_MAKEFILE),"~/snp/shared.mk")

SERVER_SOURCES    := src/person_server.c src/tcp_server.c src/snp_error_handler.c src/person.c src/list.c
SERVER_HEADERS    := $(SERVER_SOURCES):%h,%c)
SERVER_OBJECTS    := $(SERVER_SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files

CLIENT_SOURCES    := src/person_client.c src/tcp_client.c src/snp_error_handler.c src/person.c
CLIENT_HEADERS    := $(CLIENT_SOURCES):%h,%c)
CLIENT_OBJECTS    := $(CLIENT_SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files

TCP_CLIENT_SOURCES    := src/test_tcp_client.c src/tcp_client.c src/snp_error_handler.c src/person.c
TCP_CLIENT_HEADERS    := $(TCP_CLIENT_SOURCES):%h,%c)
TCP_CLIENT_OBJECTS    := $(TCP_CLIENT_SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files

TCP_SERVER_SOURCES    := src/test_tcp_server.c src/tcp_server.c src/snp_error_handler.c src/person.c
TCP_SERVER_HEADERS    := $(TCP_SERVER_SOURCES):%h,%c)
TCP_SERVER_OBJECTS    := $(TCP_SERVER_SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files

DEPS              := $(SERVER_SOURCES:%.c=%.d) $(CLIENT_SOURCES:%.c=%.d)    # list of gcc -MD ... produced *.d files

CREATEDIRS    := bin doc

TSTSOURCES        := tests/tests.c

default: all
	@echo "#### $@ is $< ####"

PHONY.: default all clean mkdir

# directories to create (and remove upon cleanup)

all: mkdir bin/person_client bin/person_server bin/tcp_server bin/tcp_client
	@echo "#### $@ built ####"
  
bin/person_server: $(SERVER_OBJECTS)
	gcc -o $@ $^ 

bin/person_client: $(CLIENT_OBJECTS)
	gcc -o $@ $^ 

bin/tcp_server: $(TCP_SERVER_OBJECTS)
	gcc -o $@ $^ 

bin/tcp_client: $(TCP_CLIENT_OBJECTS)
	gcc -o $@ $^ 

%.o: .%c .%h
	gcc -o $@ $^

# create needed directories (ignoring any error)
mkdir:
	mkdir -p $(CREATEDIRS)

clean:
	$(RM) $(SERVER_OBJECTS) $(CLIENT_OBJECTS) $(TCP_SERVER_OBJECTS) $(TCP_CLIENT_OBJECTS) $(DEPS)
	$(RM) -r $(CREATEDIRS)
	@echo "#### $@ done ####"






