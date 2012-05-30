# Makefile to create information about the publish PAT tuples

tuple_docs=$(fsa)/docs/source/tuples/

pat_jsons=$(patsubst %.txt,%.json,$(wildcard *.txt))
pat_tables=$(patsubst %.txt,$(tuple_docs)/%.rst,$(wildcard *.txt))

all: $(pat_jsons) $(pat_tables)

%.json: %.txt
	get_tuple_info.py $< $@ 

$(tuple_docs)/%.rst: %.json
	make_tuple_table.py $< $@
