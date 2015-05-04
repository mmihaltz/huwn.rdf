# huwn.rdf
Hungarian WordNet in RDF format for the Linked Open Data cloud.

Maintainer: Márton Miháltz <mmihaltz@gmail.com>

Hungarian WordNet (Release 2015-02-18) in RDF (Turtle) format for Linked Open Data / semantic web applications.

The data model uses Princeton WordNet RDF's model (http://wordnet-rdf.princeton.edu/ontology#), which relies on
the Lemon model (http://lemon-model.net/lemon#). 

This resource links Hungarian synsets to Princeton WordNet 2.0 and 3.0 synet
URIs (http://wordnet-rdf.princeton.edu/wn20/, http://wordnet-rdf.princeton.edu/wn30/) using Cornetto external
equivalence relations (http://purl.org/vocabularies/cornetto/cornetto-schema.ttl).

Files:
- huwn.ttl.gz: Hungarian WordNet RDF in Turtle notation.
- huwnxml2rdf.py: python3 script used to generate huwn.ttl from huwn.xml.
- Makefile: make targets for the conversion. Use if you want different file formats (RDF/XML, N3, NT).

See also:
- Hungarian WordNet [in XML format](https://github.com/dlt-rilmta/huwn)

License:
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
