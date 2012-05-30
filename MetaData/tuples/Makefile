# Makefile to create information about the publish PAT tuples

pat_jsons=$(patsubst %.txt,%.json,$(wildcard *.txt))
pat_tables=$(patsubst %.txt,%.rst,$(wildcard *.txt))

all: $(pat_jsons) $(pat_tables)

%.json: %.txt
	get_tuple_info.py $< $@ 

%.rst: %.json
	make_tuple_table.py $< $@
