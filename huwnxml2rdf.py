#!/usr/bin/env python3
# coding: utf8

"""
Convert Hungarian WordNet XML file to RDF semantic web/linked open data representation file (RDF/XML, ttl, n3, nt).
Author: Marton Mihaltz <mmihaltz@gmail.com>
"""

import os
import pprint
from rdflib import Namespace, Graph, Literal
from rdflib.namespace import RDF
import sys
import urllib
sys.path.append('/home/mm/NYTI/PyWNXML')
import WNQuery

# Namespaces used
huwn = Namespace("http://corpus.nytud.hu/huwn/")
lemon = Namespace("http://lemon-model.net/lemon#")
wnont = Namespace("http://wordnet-rdf.princeton.edu/ontology#")
cornetto = Namespace('http://purl.org/vocabularies/cornetto/cornetto-schema.ttl#')
w3cwn = Namespace('http://www.w3.org/2006/03/wn/wn20/instances/')
pwn20 = Namespace('http://wordnet-rdf.princeton.edu/wn20/')
pwn30 = Namespace('http://wordnet-rdf.princeton.edu/wn30/')
vuwn30 = Namespace('http://purl.org/vocabularies/princeton/wn30/')

# Some constants
POSTYPES = {"n": wnont.noun, "v": wnont.verb, "a": wnont.adjective, "b": wnont.adverb}

LINKTYPES = {'hypernym': wnont.hypernym, 'hyponym': wnont.hyponym, 
             'holo_member': wnont.member_holonym, 'mero_member': wnont.member_meronym, 
             'holo_part': wnont.part_holonym, 'mero_part': wnont.part_meronym,
             'holo_portion': wnont.substance_holonym, 'mero_portion': wnont.substance_meronym,
             'region_domain': wnont.domain_region, 'region_member': wnont.domain_member_region,
             'usage_domain': wnont.domain_usage, 'usage_member': wnont.domain_member_usage,
             'category_domain': wnont.domain_category, 'category_member': wnont.domain_member_category,
             'near_antonym': wnont.antonym, 'verb_group': wnont.verb_grop, 
             'similar_to': wnont.similar, 'also_see': wnont.also,
             'be_in_state': wnont.attribute, 'subevent': wnont.entail,
             'causes': wnont.cause
            } 
""" TODO: 'middle', 'is_consequent_state_of', 'has_consequent_state', 'is_preparatory_phase_of', 
'has_preparatory_phase', 'is_telos_of', 'has_telos', 'subevent_nec_of', 'near_synonym', 'partitions', 
"aktionsart", "converse", "has_consequence", "temporal_precondition"
"""

EXTLINKTYPES = {'eq_synonym': cornetto.eqSynonym, 'eq_near_synonym': cornetto.eqNearSynonym, 
                'eq_xpos_synonym': cornetto.xposNearSynonym, 'eq_has_hypernym': cornetto.eqHasHypernym}
"""Note: cornetto:xposNearSynonym is a cornetto:internalRelation !!! vs. others are externalRelation's"""
              
FORMATS = {'.rdf': 'pretty-xml', '.ttl': 'turtle', '.n3': 'n3', '.nt': 'nt'}

URIILLEGAL = '<>"{}|\`^ '
URIENCODE = dict([(c, urllib.parse.quote_plus(c)) for c in URIILLEGAL])

def word2id(word, pos):
  """Return a valid id from a word (synset literal) and its part-of-speech letter"""
  return ''.join([URIENCODE.get(c, c) for c in word]) + '-' + pos
  
def pos2uri(pos):
  """Return the URI representing part-of-speech pos (1 letter WNXML code)"""
  uri = POSTYPES.get(pos)
  if uri is None:
    sys.stderr.write('ERROR: invalid part-of-speech code "{}"\n'.format(pos))
  return uri

def add_synonym(g, syn, ss, s):
  """Add Synonym syn, whose containing Synset is ss (represented by Node s), to Graph g"""
  wid = word2id(syn.literal, ss.pos)
  wuri = huwn[wid]
  if (wuri, None, None) not in g: # add this LexicalEntry and its Form if they weren't already added
    g.add( (wuri, RDF.type, lemon.LexicalEntry) ) # a LexicalEntry
    g.add( (wuri, wnont.part_of_speech, pos2uri(ss.pos)) ) # pos
    wform = huwn[wid + '#CanonicalForm']
    g.add( (wuri, lemon.canonicalForm, wform) ) # canonicalForm(LexicalEntry, Form)
    g.add( (wform, RDF.type, lemon.Form) ) # a Form
    g.add( (wform, lemon.writtenRep, Literal(syn.literal, lang='hu')) ) # the literal itself, finally!
  g.add( (s, wnont.synset_member, wuri) ) # synset_member(Synset, LexicalEntry)
  sens = huwn[wid + '#' + str(syn.sense)]
  if (sens, None, None) in g: # sanity check
    sys.stderr.write('ERROR: duplicate lexical sense id "{}" ({})\n'.format(sens, s))
  g.add( (wuri, lemon.sense, sens) ) # sense(LexicalEntry, LexicalSense)
  g.add( (sens, RDF.type, lemon.LexicalSense) ) # a LexicalSense
  g.add( (sens, wnont.sense_number, Literal(syn.sense)) ) # sense_number
  g.add( (sens, lemon.reference, s) ) # reference(LexicalSense, Synset)
  # TODO: syn.lnote, syn.nucleus

def add_internal_link(g, targ, ptr, s):
  """Add internal relation to synset id targ with type ptr to Synset Node s in Graph g"""
  link = LINKTYPES.get(ptr)
  if link is None:
    sys.stderr.write('Warning: unknown link type "{}" ({})\n'.format(ptr, s))
    return
  t = huwn[targ] # target Synset URI
  g.add( (s, link, t) ) # link

def add_pwn20_link(g, targ, typ, s):
  """Add link to PWN2.0 synset id targ (in W3C WN20 resource + PWN20 resource) with type typ to Synset Node s in Graph g"""
  if not targ.startswith('ENG20-'):
    sys.stderr.write('Error: not PWN20 link target "{}" ({})\n'.format(targ, s))
    return
  link = EXTLINKTYPES.get(typ)
  if link is None:
    sys.stderr.write('Warning: unknown external link type "{}" ({})\n'.format(typ, s))
    return
  sid = targ[6:] # "offset-pos"
  t = pwn20[sid]
  g.add( (s, link, t) ) # link to PWN20
  #t = None # TODO: get wn20.synsetid based on PWN20 id -> look up 1st synonym+sensenumber+pos, eg. "synset-entity-noun-1.rdf"
  #g.add( (s, link, t) ) # link to W3C WN20
  # TODO: link to Lemon UBY ?

def add_pwn30_link(g, targ, typ, s):
  """Add link to PWN3.0 synset id targ (in PWN resource) with type typ to Synset Node s in Graph g"""
  if not targ.startswith('ENG30-'):
    sys.stderr.write('Error: not PWN30 link target "{}" ({})\n'.format(targ, s))
    return
  link = EXTLINKTYPES.get(typ)
  if link is None:
    sys.stderr.write('Warning: unknown external link type "{}" ({})\n'.format(typ, s))
    return
  sid = targ[6:] # "offset-pos"
  t = pwn30[sid]
  g.add( (s, link, t) ) # link to PWN30
  # TODO: link to VUA WN30: http://purl.org/vocabularies/princeton/wn30/synset-entity-noun-1
  # TODO: link to Lemon Uby WN30

def add_synset(g, ss):
  """Add subraph representing Synset ss to Graph g."""
  s = huwn[ss.wnid] # id
  g.add( (s, RDF.type, wnont.Synset) )
  g.add( (s, wnont.gloss, Literal(ss.definition, lang='hu')) ) # definition
  g.add( (s, wnont.part_of_speech, pos2uri(ss.pos)) ) # PoS
  # TODO: ss.bcs, ss.nl, ss.tnl, ss.snotes
  for usg in ss.usages: # usage samples
    g.add( (s, wnont.sample, Literal(usg, lang='hu')) )
  for syn in ss.synonyms: # synonym members
    add_synonym(g, syn, ss, s)
  for targ, typ in ss.ilrs: # internal relation links
    add_internal_link(g, targ, typ, s)
  if ss.wnid.startswith('ENG20-'): # ENG20 synset id -> PWN20 link
    add_pwn20_link(g, ss.wnid, 'eq_synonym', s)
  for targ, typ in ss.elrs: # external relation links (PWN2.0)
    add_pwn20_link(g, targ, typ, s)
  for targ, typ in ss.elrs3: # external relation links (PWN3.0)
    add_pwn30_link(g, targ, typ, s)
  if ss.wnid3 != '':
    add_pwn30_link(g, ss.wnid3, 'eq_synonym', s) # external relation link (PWN3.0)
  # TODO: ss.domain -> link to domains ontology?
  # TODO: ss.sumolinks -> link to sumo ?
  # TODO: ekszlinks
  # TODO: vframelinks

# - - - 

if len(sys.argv) != 3:
  sys.exit('Parameters: input output\n')

# Open output file
name, ext = os.path.splitext(sys.argv[2])
if ext not in FORMATS:
  sys.exit('Invalid output file extension.\nValid extensions: ' + ', '.join([x for x in FORMATS]) + '\n')
out = open(sys.argv[2], 'w')

# Load HuWN
sys.stderr.write('Reading XML...\n')
wn = WNQuery.WNQuery(sys.argv[1], open(os.devnull, "w"))
sys.stderr.write('Done\n')

# Create graph
g = Graph()
g.bind('huwn', huwn)
g.bind('wordnet-ontology', wnont)
g.bind("lemon", lemon)
g.bind("cornetto", cornetto)
g.bind("w3cwn", w3cwn)
g.bind("pwn20", pwn20)
g.bind("pwn30", pwn30)

# TODO: add HuWN metadata to graph

# Process each synset: nouns
sys.stderr.write('Generating RDF graph...\n')
cnt = 0
limit = 9999999999999999
for data in [wn.m_ndat, wn.m_vdat, wn.m_adat, wn.m_bdat]:
  for ssid in sorted(data.keys()):
    sset = data[ssid]
    add_synset(g, sset)
    cnt += 1
    if cnt == limit:
      break

# Dump graph to file
sys.stderr.write('Dumping to file...\n')
out.write(g.serialize(format=FORMATS[ext], encoding='utf8').decode('utf8'))
sys.stderr.write('Done.\n')
