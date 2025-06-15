from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import XSD

tbox_graph = Graph()

RESEARCH = Namespace("http://research.publications.com/ontology#")
tbox_graph.bind("research", RESEARCH)
tbox_graph.bind("rdfs", RDFS)
tbox_graph.bind("rdf", RDF)
tbox_graph.bind("xsd", XSD)

# Main classes
Paper = RESEARCH.Paper
Author = RESEARCH.Author
Event = RESEARCH.Event 
Conference = RESEARCH.Conference
Workshop = RESEARCH.Workshop
Journal = RESEARCH.Journal
Edition = RESEARCH.Edition
Proceedings = RESEARCH.Proceedings
Volume = RESEARCH.Volume
Review = RESEARCH.Review
Reviewer = RESEARCH.Reviewer
City = RESEARCH.City
Keyword = RESEARCH.Keyword
Organization = RESEARCH.Organization
University = RESEARCH.University
Company = RESEARCH.Company

# Add classes to the graph
tbox_graph.add((Paper, RDF.type, RDFS.Class))
tbox_graph.add((Paper, RDFS.label, Literal("Paper")))
tbox_graph.add((Paper, RDFS.comment, Literal("A research paper written by authors")))

tbox_graph.add((Author, RDF.type, RDFS.Class))
tbox_graph.add((Author, RDFS.label, Literal("Author")))
tbox_graph.add((Author, RDFS.comment, Literal("An author of research papers")))

# Event superclass
tbox_graph.add((Event, RDF.type, RDFS.Class))
tbox_graph.add((Event, RDFS.label, Literal("Event")))
tbox_graph.add((Event, RDFS.comment, Literal("An academic event (conference or workshop)")))

tbox_graph.add((Conference, RDF.type, RDFS.Class))
tbox_graph.add((Conference, RDFS.subClassOf, Event)) 
tbox_graph.add((Conference, RDFS.label, Literal("Conference")))
tbox_graph.add((Conference, RDFS.comment, Literal("A well-established research forum")))

tbox_graph.add((Workshop, RDF.type, RDFS.Class))
tbox_graph.add((Workshop, RDFS.subClassOf, Event))  
tbox_graph.add((Workshop, RDFS.label, Literal("Workshop")))
tbox_graph.add((Workshop, RDFS.comment, Literal("A forum for new research trends")))

tbox_graph.add((Journal, RDF.type, RDFS.Class))
tbox_graph.add((Journal, RDFS.label, Literal("Journal")))
tbox_graph.add((Journal, RDFS.comment, Literal("A periodical publication for research papers")))

tbox_graph.add((Edition, RDF.type, RDFS.Class))
tbox_graph.add((Edition, RDFS.label, Literal("Edition")))
tbox_graph.add((Edition, RDFS.comment, Literal("An edition of a conference or workshop")))

tbox_graph.add((Proceedings, RDF.type, RDFS.Class))
tbox_graph.add((Proceedings, RDFS.label, Literal("Proceedings")))
tbox_graph.add((Proceedings, RDFS.comment, Literal("Published records of papers from a conference/workshop edition")))

tbox_graph.add((Volume, RDF.type, RDFS.Class))
tbox_graph.add((Volume, RDFS.label, Literal("Volume")))
tbox_graph.add((Volume, RDFS.comment, Literal("A volume of a journal")))

tbox_graph.add((Review, RDF.type, RDFS.Class))
tbox_graph.add((Review, RDFS.label, Literal("Review")))
tbox_graph.add((Review, RDFS.comment, Literal("A review of a paper")))

tbox_graph.add((Reviewer, RDF.type, RDFS.Class))
tbox_graph.add((Reviewer, RDFS.subClassOf, Author))
tbox_graph.add((Reviewer, RDFS.label, Literal("Reviewer")))
tbox_graph.add((Reviewer, RDFS.comment, Literal("A scientist who reviews papers")))

tbox_graph.add((City, RDF.type, RDFS.Class))
tbox_graph.add((City, RDFS.label, Literal("City")))
tbox_graph.add((City, RDFS.comment, Literal("A city where a conference/workshop is held")))

tbox_graph.add((Keyword, RDF.type, RDFS.Class))
tbox_graph.add((Keyword, RDFS.label, Literal("Keyword")))
tbox_graph.add((Keyword, RDFS.comment, Literal("A keyword describing paper topics")))

tbox_graph.add((Organization, RDF.type, RDFS.Class))
tbox_graph.add((Organization, RDFS.label, Literal("Organization")))
tbox_graph.add((Organization, RDFS.comment, Literal("An organization that authors are affiliated with")))

tbox_graph.add((University, RDF.type, RDFS.Class))
tbox_graph.add((University, RDFS.subClassOf, Organization))
tbox_graph.add((University, RDFS.label, Literal("University")))
tbox_graph.add((University, RDFS.comment, Literal("A university that authors are affiliated with")))

tbox_graph.add((Company, RDF.type, RDFS.Class))
tbox_graph.add((Company, RDFS.subClassOf, Organization))
tbox_graph.add((Company, RDFS.label, Literal("Company")))
tbox_graph.add((Company, RDFS.comment, Literal("A company that authors are affiliated with")))

# Object Properties
writtenBy = RESEARCH.writtenBy
correspondingAuthor = RESEARCH.correspondingAuthor
publishedIn = RESEARCH.publishedIn
hasEdition = RESEARCH.hasEdition
heldIn = RESEARCH.heldIn
includesPaper = RESEARCH.includesPaper
hasVolume = RESEARCH.hasVolume
cites = RESEARCH.cites
hasKeyword = RESEARCH.hasKeyword
reviewOf = RESEARCH.reviewOf
writtenByReviewer = RESEARCH.writtenByReviewer
assignedTo = RESEARCH.assignedTo
publishedInProceedings = RESEARCH.publishedInProceedings
publishedInJournal = RESEARCH.publishedInJournal
affiliatedTo = RESEARCH.affiliatedTo
proceedingsOf = RESEARCH.proceedingsOf  

# Data Properties
hasAbstract = RESEARCH.hasAbstract
hasTitle = RESEARCH.hasTitle
hasYear = RESEARCH.hasYear
hasName = RESEARCH.hasName
hasStartDate = RESEARCH.hasStartDate
hasEndDate = RESEARCH.hasEndDate
reviewContent = RESEARCH.reviewContent
grade = RESEARCH.grade
volumeNumber = RESEARCH.volumeNumber  
volumeYear = RESEARCH.volumeYear     

# Add Object Properties
tbox_graph.add((writtenBy, RDF.type, RDF.Property))
tbox_graph.add((writtenBy, RDFS.domain, Paper))
tbox_graph.add((writtenBy, RDFS.range, Author))
tbox_graph.add((writtenBy, RDFS.label, Literal("written by")))

tbox_graph.add((correspondingAuthor, RDF.type, RDF.Property))
tbox_graph.add((correspondingAuthor, RDFS.subPropertyOf, writtenBy))
tbox_graph.add((correspondingAuthor, RDFS.domain, Paper))
tbox_graph.add((correspondingAuthor, RDFS.range, Author))
tbox_graph.add((correspondingAuthor, RDFS.label, Literal("corresponding author")))

tbox_graph.add((publishedIn, RDF.type, RDF.Property))
tbox_graph.add((publishedIn, RDFS.domain, Paper))
tbox_graph.add((publishedIn, RDFS.label, Literal("published in")))

tbox_graph.add((publishedInProceedings, RDF.type, RDF.Property))
tbox_graph.add((publishedInProceedings, RDFS.subPropertyOf, publishedIn))
tbox_graph.add((publishedInProceedings, RDFS.domain, Paper))
tbox_graph.add((publishedInProceedings, RDFS.range, Proceedings))
tbox_graph.add((publishedInProceedings, RDFS.label, Literal("published in proceedings")))

tbox_graph.add((publishedInJournal, RDF.type, RDF.Property))
tbox_graph.add((publishedInJournal, RDFS.subPropertyOf, publishedIn))
tbox_graph.add((publishedInJournal, RDFS.domain, Paper))
tbox_graph.add((publishedInJournal, RDFS.range, Volume))
tbox_graph.add((publishedInJournal, RDFS.label, Literal("published in journal")))

# Fixed hasEdition with proper domain
tbox_graph.add((hasEdition, RDF.type, RDF.Property))
tbox_graph.add((hasEdition, RDFS.domain, Event))  # Domain is Event (superclass of Conference and Workshop)
tbox_graph.add((hasEdition, RDFS.range, Edition))
tbox_graph.add((hasEdition, RDFS.label, Literal("has edition")))

tbox_graph.add((heldIn, RDF.type, RDF.Property))
tbox_graph.add((heldIn, RDFS.domain, Edition))
tbox_graph.add((heldIn, RDFS.range, City))
tbox_graph.add((heldIn, RDFS.label, Literal("held in")))

tbox_graph.add((includesPaper, RDF.type, RDF.Property))
tbox_graph.add((includesPaper, RDFS.domain, Proceedings))
tbox_graph.add((includesPaper, RDFS.range, Paper))
tbox_graph.add((includesPaper, RDFS.label, Literal("includes paper")))

tbox_graph.add((proceedingsOf, RDF.type, RDF.Property))
tbox_graph.add((proceedingsOf, RDFS.domain, Proceedings))
tbox_graph.add((proceedingsOf, RDFS.range, Edition))
tbox_graph.add((proceedingsOf, RDFS.label, Literal("proceedings of")))
tbox_graph.add((proceedingsOf, RDFS.comment, Literal("Links proceedings to the edition they document")))

tbox_graph.add((hasVolume, RDF.type, RDF.Property))
tbox_graph.add((hasVolume, RDFS.domain, Journal))
tbox_graph.add((hasVolume, RDFS.range, Volume))
tbox_graph.add((hasVolume, RDFS.label, Literal("has volume")))

tbox_graph.add((cites, RDF.type, RDF.Property))
tbox_graph.add((cites, RDFS.domain, Paper))
tbox_graph.add((cites, RDFS.range, Paper))
tbox_graph.add((cites, RDFS.label, Literal("cites")))

tbox_graph.add((hasKeyword, RDF.type, RDF.Property))
tbox_graph.add((hasKeyword, RDFS.domain, Paper))
tbox_graph.add((hasKeyword, RDFS.range, Keyword))
tbox_graph.add((hasKeyword, RDFS.label, Literal("has keyword")))

tbox_graph.add((reviewOf, RDF.type, RDF.Property))
tbox_graph.add((reviewOf, RDFS.domain, Review))
tbox_graph.add((reviewOf, RDFS.range, Paper))
tbox_graph.add((reviewOf, RDFS.label, Literal("review of")))

tbox_graph.add((writtenByReviewer, RDF.type, RDF.Property))
tbox_graph.add((writtenByReviewer, RDFS.domain, Review))
tbox_graph.add((writtenByReviewer, RDFS.range, Reviewer))
tbox_graph.add((writtenByReviewer, RDFS.label, Literal("written by reviewer")))

tbox_graph.add((assignedTo, RDF.type, RDF.Property))
tbox_graph.add((assignedTo, RDFS.domain, Paper))
tbox_graph.add((assignedTo, RDFS.range, Reviewer))
tbox_graph.add((assignedTo, RDFS.label, Literal("assigned to")))
tbox_graph.add((assignedTo, RDFS.comment, 
    Literal("Assigns reviewers to papers. Constraint: authors cannot review their own papers (enforced at application level)")))

tbox_graph.add((affiliatedTo, RDF.type, RDF.Property))
tbox_graph.add((affiliatedTo, RDFS.domain, Author))
tbox_graph.add((affiliatedTo, RDFS.range, Organization))
tbox_graph.add((affiliatedTo, RDFS.label, Literal("affiliated to")))
tbox_graph.add((affiliatedTo, RDFS.comment, Literal("Indicates author affiliation to university or company")))

# Add Data Properties
tbox_graph.add((hasAbstract, RDF.type, RDF.Property))
tbox_graph.add((hasAbstract, RDFS.domain, Paper))
tbox_graph.add((hasAbstract, RDFS.range, XSD.string))
tbox_graph.add((hasAbstract, RDFS.label, Literal("has abstract")))

tbox_graph.add((hasTitle, RDF.type, RDF.Property))
tbox_graph.add((hasTitle, RDFS.domain, Paper))
tbox_graph.add((hasTitle, RDFS.range, XSD.string))
tbox_graph.add((hasTitle, RDFS.label, Literal("has title")))

tbox_graph.add((hasYear, RDF.type, RDF.Property))
tbox_graph.add((hasYear, RDFS.domain, Edition))
tbox_graph.add((hasYear, RDFS.range, XSD.integer))
tbox_graph.add((hasYear, RDFS.label, Literal("has year")))

tbox_graph.add((hasName, RDF.type, RDF.Property))
tbox_graph.add((hasName, RDFS.range, XSD.string))
tbox_graph.add((hasName, RDFS.label, Literal("has name")))

tbox_graph.add((hasStartDate, RDF.type, RDF.Property))
tbox_graph.add((hasStartDate, RDFS.domain, Edition))
tbox_graph.add((hasStartDate, RDFS.range, XSD.date))
tbox_graph.add((hasStartDate, RDFS.label, Literal("has start date")))

tbox_graph.add((hasEndDate, RDF.type, RDF.Property))
tbox_graph.add((hasEndDate, RDFS.domain, Edition))
tbox_graph.add((hasEndDate, RDFS.range, XSD.date))
tbox_graph.add((hasEndDate, RDFS.label, Literal("has end date")))

tbox_graph.add((reviewContent, RDF.type, RDF.Property))
tbox_graph.add((reviewContent, RDFS.domain, Review))
tbox_graph.add((reviewContent, RDFS.range, XSD.string))
tbox_graph.add((reviewContent, RDFS.label, Literal("review content")))

tbox_graph.add((grade, RDF.type, RDF.Property))
tbox_graph.add((grade, RDFS.domain, Review))
tbox_graph.add((grade, RDFS.range, XSD.integer))
tbox_graph.add((grade, RDFS.label, Literal("grade")))


tbox_graph.add((volumeNumber, RDF.type, RDF.Property))
tbox_graph.add((volumeNumber, RDFS.domain, Volume))
tbox_graph.add((volumeNumber, RDFS.range, XSD.integer))
tbox_graph.add((volumeNumber, RDFS.label, Literal("volume number")))

tbox_graph.add((volumeYear, RDF.type, RDF.Property))
tbox_graph.add((volumeYear, RDFS.domain, Volume))
tbox_graph.add((volumeYear, RDFS.range, XSD.integer))
tbox_graph.add((volumeYear, RDFS.label, Literal("volume year")))

# Save the TBOX to a file
tbox_graph.serialize("research_tbox.ttl", format="turtle")
print("TBOX created and saved to research_tbox.ttl")

# Print some statistics
print(f"Number of classes: {len(list(tbox_graph.subjects(RDF.type, RDFS.Class)))}")
print(f"Number of properties: {len(list(tbox_graph.subjects(RDF.type, RDF.Property)))}")

# Print class hierarchy
print("\nClass Hierarchy:")
for subclass, _, superclass in tbox_graph.triples((None, RDFS.subClassOf, None)):
    sub_name = str(subclass).split('#')[-1]
    super_name = str(superclass).split('#')[-1]
    print(f"  {sub_name} ⊆ {super_name}")

# Print property hierarchy
print("\nProperty Hierarchy:")
for subprop, _, superprop in tbox_graph.triples((None, RDFS.subPropertyOf, None)):
    sub_name = str(subprop).split('#')[-1]
    super_name = str(superprop).split('#')[-1]
    print(f"  {sub_name} ⊆ {super_name}")