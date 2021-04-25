from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import SKOS
from slugify import slugify


def add_related_words(graph, word, related_words):
    related_words_obj_list = []
    for related_word in related_words:
        related_word_obj = URIRef(f"http://example.org/thesaurus/{slugify(related_word)}")
        graph.add((related_word_obj, RDF.type, SKOS.Concept))
        graph.add((related_word_obj, SKOS.prefLabel, Literal(f"{related_word}", lang="tr")))
        graph.add((related_word_obj, SKOS.inScheme, thesaurus))
        related_words_obj_list.append(related_word_obj)

    word_obj = URIRef(f"http://example.org/thesaurus/{slugify(word)}")
    graph.add((word_obj, RDF.type, SKOS.Concept))
    graph.add((word_obj, SKOS.prefLabel, Literal(f"{word}", lang="tr")))
    graph.add((word_obj, SKOS.inScheme, thesaurus))
    for related_word_obj in related_words_obj_list:
        graph.add((word_obj, SKOS.related, related_word_obj))


g = Graph()
thesaurus = URIRef("http://example.org/thesaurus")
g.add((thesaurus, RDF.type, SKOS.ConceptScheme))

add_related_words(g, "rammstein", ["metal", "alman", "endüstriyel"])
add_related_words(g, "linux", ["işletim sistemi", "çekirdek", "linus torvalds", "sunucu"])
add_related_words(g, "papağan", ["kuş"])
add_related_words(g, "metal", ["alaşım", "kimya", "endüstriyel"])
g.bind("skos", SKOS)

out = g.serialize(format='nt').decode("utf-8")
print(out)


qres = g.query("""
SELECT ?rrwordt
WHERE {
?word skos:prefLabel "rammstein"@tr.
?word skos:related ?rword.
?rword skos:related ?rrword.
?rrword skos:prefLabel ?rrwordt.
}
""")


for row in qres:
    print("rammstein has second degree relation with %s" % row)
