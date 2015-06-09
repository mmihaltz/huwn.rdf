# Set the path and filename of huwn.xml to convert here:
HUWNFILE=../huwn/huwn.xml

all: huwn.ttl huwn.rdf huwn.nt huwn.n3

huwn.ttl: huwnxml2rdf.py $(HUWNFILE)
	python3 huwnxml2rdf.py $(HUWNFILE) huwn.ttl

huwn.rdf: huwnxml2rdf.py $(HUWNFILE)
	python3 huwnxml2rdf.py $(HUWNFILE) huwn.rdf

huwn.nt: huwnxml2rdf.py $(HUWNFILE)
	python3 huwnxml2rdf.py $(HUWNFILE) huwn.nt

huwn.n3: huwnxml2rdf.py $(HUWNFILE)
	python3 huwnxml2rdf.py $(HUWNFILE) huwn.n3