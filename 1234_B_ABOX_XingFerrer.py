from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import XSD
import pandas as pd
import datetime
import ast

abox_graph = Graph()

RESEARCH = Namespace("http://research.publications.com/ontology#")
INSTANCE = Namespace("http://research.publications.com/instance#")
abox_graph.bind("research", RESEARCH)
abox_graph.bind("instance", INSTANCE)
abox_graph.bind("rdfs", RDFS)
abox_graph.bind("rdf", RDF)
abox_graph.bind("xsd", XSD)

tbox_graph = Graph()
tbox_graph.parse("research_tbox.ttl", format="turtle")

# Merge TBOX into ABOX
abox_graph = abox_graph + tbox_graph

try:
    papers = pd.read_csv("data/semantic_scholar/sc_data_csv/papers-processed.csv")
    authors = pd.read_csv("data/semantic_scholar/sc_data_csv/authors-sample.csv").fillna('')
    keywords = pd.read_csv("data/semantic_scholar/sc_data_csv/keywords.csv")
    journals = pd.read_csv("data/semantic_scholar/sc_data_csv/journals.csv")
    conferences = pd.read_csv("data/semantic_scholar/sc_data_csv/conferences.csv")
    volumes = pd.read_csv("data/semantic_scholar/sc_data_csv/volume.csv")
    editions = pd.read_csv("data/semantic_scholar/sc_data_csv/editions.csv")
    universities = pd.read_csv("data/semantic_scholar/sc_data_csv/universities.csv")
    companies = pd.read_csv("data/semantic_scholar/sc_data_csv/companies.csv")
    
    # Relationships
    related_to = pd.read_csv('data/semantic_scholar/sc_data_csv/related-to.csv')
    written_by = pd.read_csv('data/semantic_scholar/sc_data_csv/written-by.csv')
    reviewed_by = pd.read_csv('data/semantic_scholar/sc_data_csv/reviewed-by.csv')
    cited_by = pd.read_csv('data/semantic_scholar/sc_data_csv/cited-by.csv')
    published_in = pd.read_csv('data/semantic_scholar/sc_data_csv/published-in.csv')
    is_from = pd.read_csv("data/semantic_scholar/sc_data_csv/is_from.csv")
    volume_from = pd.read_csv("data/semantic_scholar/sc_data_csv/volume_from.csv")
    affiliations = pd.read_csv("data/semantic_scholar/sc_data_csv/affiliated-to.csv")
        
except FileNotFoundError as e:
    print(f"Error: Could not find file - {e}")
    raise

def create_uri(namespace, id_value):
    # Replace spaces and special characters with underscores
    safe_id = str(id_value).replace(' ', '_').replace(',', '_').replace(':', '_')
    return namespace[safe_id]

for _, row in authors.iterrows():
    author_uri = create_uri(INSTANCE, f"Author_{row['authorid']}")
    abox_graph.add((author_uri, RDF.type, RESEARCH.Author))
    abox_graph.add((author_uri, RESEARCH.hasName, Literal(row['name'])))
    
    if row.get('homepage'):
        abox_graph.add((author_uri, RESEARCH.homepage, Literal(row['homepage'])))
    if row.get('hindex'):
        abox_graph.add((author_uri, RESEARCH.hindex, Literal(int(row['hindex']), datatype=XSD.integer)))

reviewer_ids = reviewed_by['reviewerID'].unique()
for reviewer_id in reviewer_ids:
    reviewer_uri = create_uri(INSTANCE, f"Reviewer_{reviewer_id}")
    # Get author name
    author_data = authors[authors['authorid'] == str(reviewer_id)]
    if not author_data.empty:
        abox_graph.add((reviewer_uri, RDF.type, RESEARCH.Reviewer))
        abox_graph.add((reviewer_uri, RESEARCH.hasName, Literal(author_data.iloc[0]['name'])))

for _, row in papers.iterrows():
    paper_uri = create_uri(INSTANCE, f"Paper_{row['corpusid']}")
    abox_graph.add((paper_uri, RDF.type, RESEARCH.Paper))
    abox_graph.add((paper_uri, RESEARCH.hasTitle, Literal(row['title'])))
    
    abstract = f"Abstract for paper: {row['title']}"  
    abox_graph.add((paper_uri, RESEARCH.hasAbstract, Literal(abstract)))
    
    if row.get('year') and not pd.isna(row['year']):
        abox_graph.add((paper_uri, RESEARCH.hasYear, Literal(int(row['year']), datatype=XSD.integer)))
    if row.get('DOI'):
        abox_graph.add((paper_uri, RESEARCH.doi, Literal(row['DOI'])))

for _, row in keywords.iterrows():
    keyword_uri = create_uri(INSTANCE, f"Keyword_{row['keyword']}")
    abox_graph.add((keyword_uri, RDF.type, RESEARCH.Keyword))
    abox_graph.add((keyword_uri, RESEARCH.hasName, Literal(row['keyword'])))

for _, row in conferences.iterrows():
    conf_uri = create_uri(INSTANCE, f"Conference_{row['conferenceID']}")
    abox_graph.add((conf_uri, RDF.type, RESEARCH.Conference))
    abox_graph.add((conf_uri, RESEARCH.hasName, Literal(row['conferenceName'])))
    if row.get('url'):
        abox_graph.add((conf_uri, RESEARCH.url, Literal(row['url'])))

for _, row in journals.iterrows():
    journal_uri = create_uri(INSTANCE, f"Journal_{row['venueID']}")
    abox_graph.add((journal_uri, RDF.type, RESEARCH.Journal))
    abox_graph.add((journal_uri, RESEARCH.hasName, Literal(row['journalName'])))
    if row.get('issn'):
        abox_graph.add((journal_uri, RESEARCH.issn, Literal(row['issn'])))
    if row.get('url'):
        abox_graph.add((journal_uri, RESEARCH.url, Literal(row['url'])))

cities_created = set()
for _, row in editions.iterrows():
    edition_uri = create_uri(INSTANCE, f"Edition_{row['editionID']}")
    abox_graph.add((edition_uri, RDF.type, RESEARCH.Edition))
    abox_graph.add((edition_uri, RESEARCH.hasName, Literal(row['edition'])))
    
    try:
        year = int(row['edition'].split()[-1])
        abox_graph.add((edition_uri, RESEARCH.hasYear, Literal(year, datatype=XSD.integer)))
    except:
        pass
    
    if row.get('startDate'):
        abox_graph.add((edition_uri, RESEARCH.hasStartDate, Literal(row['startDate'], datatype=XSD.date)))
    if row.get('endDate'):
        abox_graph.add((edition_uri, RESEARCH.hasEndDate, Literal(row['endDate'], datatype=XSD.date)))
    
    city_name = f"City_for_{row['edition']}"
    city_uri = create_uri(INSTANCE, city_name)
    if city_name not in cities_created:
        abox_graph.add((city_uri, RDF.type, RESEARCH.City))
        abox_graph.add((city_uri, RESEARCH.hasName, Literal(city_name)))
        cities_created.add(city_name)
    abox_graph.add((edition_uri, RESEARCH.heldIn, city_uri))

for _, row in volumes.iterrows():
    volume_uri = create_uri(INSTANCE, f"Volume_{row['volumeID']}")
    abox_graph.add((volume_uri, RDF.type, RESEARCH.Volume))
    abox_graph.add((volume_uri, RESEARCH.hasName, Literal(f"Volume {row['volume']}")))
    if row.get('year'):
        abox_graph.add((volume_uri, RESEARCH.hasYear, Literal(int(row['year']), datatype=XSD.integer)))

proceedings_created = {}
for _, row in is_from.iterrows():
    edition_id = row['editionID']
    conf_id = row['conferenceID']
    
    proceedings_uri = create_uri(INSTANCE, f"Proceedings_Edition_{edition_id}")
    if edition_id not in proceedings_created:
        abox_graph.add((proceedings_uri, RDF.type, RESEARCH.Proceedings))
        # Get edition name
        edition_data = editions[editions['editionID'] == edition_id]
        if not edition_data.empty:
            proceedings_name = f"Proceedings of {edition_data.iloc[0]['edition']}"
            abox_graph.add((proceedings_uri, RESEARCH.hasName, Literal(proceedings_name)))
        proceedings_created[edition_id] = proceedings_uri


for _, row in written_by.iterrows():
    paper_uri = create_uri(INSTANCE, f"Paper_{row['paperID']}")
    author_uri = create_uri(INSTANCE, f"Author_{row['authorID']}")
    
    abox_graph.add((paper_uri, RESEARCH.writtenBy, author_uri))
    
    if row.get('is_corresponding', False):
        abox_graph.add((paper_uri, RESEARCH.correspondingAuthor, author_uri))

for _, row in related_to.iterrows():
    paper_uri = create_uri(INSTANCE, f"Paper_{row['paperID']}")
    keyword_uri = create_uri(INSTANCE, f"Keyword_{row['keyword']}")
    abox_graph.add((paper_uri, RESEARCH.hasKeyword, keyword_uri))

for _, row in cited_by.iterrows():
    citing_paper = create_uri(INSTANCE, f"Paper_{row['paperID_citing']}")
    cited_paper = create_uri(INSTANCE, f"Paper_{row['paperID_cited']}")
    abox_graph.add((citing_paper, RESEARCH.cites, cited_paper))

for _, row in is_from.iterrows():
    conf_uri = create_uri(INSTANCE, f"Conference_{row['conferenceID']}")
    edition_uri = create_uri(INSTANCE, f"Edition_{row['editionID']}")
    abox_graph.add((conf_uri, RESEARCH.hasEdition, edition_uri))

for _, row in volume_from.iterrows():
    journal_id = row.get('journalID', row.get('venueID'))
    if journal_id:
        journal_uri = create_uri(INSTANCE, f"Journal_{journal_id}")
        volume_uri = create_uri(INSTANCE, f"Volume_{row['volumeID']}")
        abox_graph.add((journal_uri, RESEARCH.hasVolume, volume_uri))

for _, row in published_in.iterrows():
    paper_uri = create_uri(INSTANCE, f"Paper_{row['paperID']}")
    venue_id = row['venueID']
    
    if venue_id in journals['venueID'].values:
        journal_volumes = volume_from[volume_from.get('journalID', volume_from.get('venueID')) == venue_id]
        if not journal_volumes.empty:
            volume_uri = create_uri(INSTANCE, f"Volume_{journal_volumes.iloc[0]['volumeID']}")
            abox_graph.add((paper_uri, RESEARCH.publishedInJournal, volume_uri))
    else:
        for edition_id, proceedings_uri in proceedings_created.items():
            abox_graph.add((paper_uri, RESEARCH.publishedInProceedings, proceedings_uri))
            abox_graph.add((proceedings_uri, RESEARCH.includesPaper, paper_uri))
            break 

for _, row in reviewed_by.iterrows():
    review_uri = create_uri(INSTANCE, f"Review_{row['paperID']}_{row['reviewerID']}")
    paper_uri = create_uri(INSTANCE, f"Paper_{row['paperID']}")
    reviewer_uri = create_uri(INSTANCE, f"Reviewer_{row['reviewerID']}")
    
    abox_graph.add((review_uri, RDF.type, RESEARCH.Review))
    abox_graph.add((review_uri, RESEARCH.reviewOf, paper_uri))
    abox_graph.add((review_uri, RESEARCH.writtenByReviewer, reviewer_uri))
    
    if row.get('review'):
        abox_graph.add((review_uri, RESEARCH.reviewContent, Literal(row['review'])))
    if row.get('grade'):
        abox_graph.add((review_uri, RESEARCH.grade, Literal(int(row['grade']), datatype=XSD.integer)))
    
    abox_graph.add((paper_uri, RESEARCH.assignedTo, reviewer_uri))

# Affiliations 
for _, row in affiliations.iterrows():
    author_uri = create_uri(INSTANCE, f"Author_{row['authorID']}")
    affiliation_id = row['affiliationID']
    
    # Check if it's a university
    if affiliation_id in universities['affiliationID'].values:
        uni_data = universities[universities['affiliationID'] == affiliation_id].iloc[0]
        uni_uri = create_uri(INSTANCE, f"University_{affiliation_id}")
        abox_graph.add((uni_uri, RDF.type, RESEARCH.University))
        abox_graph.add((uni_uri, RESEARCH.hasName, Literal(uni_data['affiliation'])))
        abox_graph.add((author_uri, RESEARCH.affiliatedTo, uni_uri))
    
    # Check if it's a company
    elif affiliation_id in companies['affiliationID'].values:
        comp_data = companies[companies['affiliationID'] == affiliation_id].iloc[0]
        comp_uri = create_uri(INSTANCE, f"Company_{affiliation_id}")
        abox_graph.add((comp_uri, RDF.type, RESEARCH.Company))
        abox_graph.add((comp_uri, RESEARCH.hasName, Literal(comp_data['affiliation'])))
        abox_graph.add((author_uri, RESEARCH.affiliatedTo, comp_uri))

abox_graph.serialize("research_ontology.ttl", format="turtle")
print("Complete ontology created and saved to research_ontology.ttl")

print("\n=== Ontology Statistics ===")
print(f"Total triples: {len(abox_graph)}")

# Count instances by class
classes_to_count = [
    (RESEARCH.Paper, "Papers"),
    (RESEARCH.Author, "Authors"),
    (RESEARCH.Reviewer, "Reviewers"),
    (RESEARCH.Conference, "Conferences"),
    (RESEARCH.Workshop, "Workshops"),
    (RESEARCH.Journal, "Journals"),
    (RESEARCH.Edition, "Editions"),
    (RESEARCH.Proceedings, "Proceedings"),
    (RESEARCH.Volume, "Volumes"),
    (RESEARCH.Review, "Reviews"),
    (RESEARCH.City, "Cities"),
    (RESEARCH.Keyword, "Keywords"),
    (RESEARCH.University, "Universities"),
    (RESEARCH.Company, "Companies")
]

print("\nInstance counts:")
for class_uri, class_name in classes_to_count:
    count = len(list(abox_graph.subjects(RDF.type, class_uri)))
    print(f"  {class_name}: {count}")

# Count property usage
properties_to_count = [
    (RESEARCH.writtenBy, "writtenBy"),
    (RESEARCH.hasKeyword, "hasKeyword"),
    (RESEARCH.cites, "cites"),
    (RESEARCH.publishedInProceedings, "publishedInProceedings"),
    (RESEARCH.publishedInJournal, "publishedInJournal"),
    (RESEARCH.reviewOf, "reviewOf"),
    (RESEARCH.affiliatedTo, "affiliatedTo")
]

print("\nProperty usage:")
for prop_uri, prop_name in properties_to_count:
    count = len(list(abox_graph.subject_objects(prop_uri)))
    print(f"  {prop_name}: {count} triples")
