# huwn.rdf
Hungarian WordNet in RDF format for the Linked Open Data cloud.

Maintainer: Márton Miháltz <mmihaltz@gmail.com>

##Changes:
* 2015-06-10:
  * Generated from HuWN Release 2015-06-09
* 2015-06-08:
  * Generated from HuWN Release 2015-06-03
* 2015-05-04:
  * Generated from HuWN Release 2015-04-29
  * Changed lincense to META-SHARE Commons BY NC ND License v1.0
* 2015-02-18
  * First release, generated from HuWN Release 2015-02-18

##About

Hungarian WordNet in RDF (Turtle) format for Linked Open Data / semantic web applications.

The data model uses Princeton WordNet RDF's model (http://wordnet-rdf.princeton.edu/ontology#), which relies on
the Lemon model (http://lemon-model.net/lemon#). 

This resource links Hungarian synsets to Princeton WordNet 2.0 and 3.0 synet
URIs (http://wordnet-rdf.princeton.edu/wn20/, http://wordnet-rdf.princeton.edu/wn30/) using Cornetto external
equivalence relations (http://purl.org/vocabularies/cornetto/cornetto-schema.ttl).

Contains 42K synsets, of which 27K are linked to Princeton (English) WN synsets. 855K RDF triples, 54K external resource links.

##Files
- huwn.ttl.gz: Hungarian WordNet RDF in Turtle notation.
- huwnxml2rdf.py: python3 script used to generate huwn.ttl from huwn.xml. Uses [pywnxml](https://github.com/ppke-nlpg/pywnxml) and [rdflib](http://rdflib.readthedocs.org).
- Makefile: make targets for the conversion. Use if you want different file formats (RDF/XML, N3, NT).
- LICENSE.pdf: license information.

##See also
- Hungarian WordNet [in XML format](https://github.com/dlt-rilmta/huwn)
- HuWN [home](http://corpus.nytud.hu/huwn/)
- Metadata record at [datahub.io](http://datahub.io/dataset/hungarian-wordnet-rdf), [opendata.hu](http://opendata.hu/dataset/magyar-wordnet-rdf)

##License
META-SHARE Commons BY NC ND License v1.0 (see LICENSE.pdf, or [META-SHARE licenses](http://www.meta-net.eu/meta-share/licenses))
