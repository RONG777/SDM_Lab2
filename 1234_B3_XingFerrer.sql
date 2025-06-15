-- Query 1: Find the Research Collaboration Network and Identify Key Influencers
-- This query leverages inference, graph patterns, and aggregation to find influential researchers

PREFIX research: <http://research.publications.com/ontology#>
PREFIX instance: <http://research.publications.com/instance#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?author ?authorName 
       (COUNT(DISTINCT ?paper) as ?paperCount)
       (COUNT(DISTINCT ?coAuthor) as ?collaboratorCount)
       (COUNT(DISTINCT ?citingPaper) as ?citationCount)
       (COUNT(DISTINCT ?reviewedPaper) as ?reviewCount)
       (COUNT(DISTINCT ?keyword) as ?topicDiversity)
       (?paperCount + ?collaboratorCount * 2 + ?citationCount * 3 + ?reviewCount * 2 + ?topicDiversity as ?influenceScore)
WHERE {
    -- Find authors and their names
    ?author a research:Author ;
            research:hasName ?authorName .
    
    -- Papers written by the author
    ?paper research:writtenBy ?author .
    
    -- Find co-authors (excluding self)
    ?paper research:writtenBy ?coAuthor .
    FILTER(?coAuthor != ?author)
    
    -- Papers that cite this author's work
    OPTIONAL {
        ?citingPaper research:cites ?paper .
    }
    
    -- Keywords associated with author's papers (topic diversity)
    OPTIONAL {
        ?paper research:hasKeyword ?keyword .
    }
    
    -- Papers reviewed by this author (if they are also a reviewer)
    -- This leverages RDFS inference: Reviewer rdfs:subClassOf Author
    OPTIONAL {
        ?reviewer rdfs:subClassOf research:Reviewer .
        ?reviewer research:hasName ?authorName .
        ?review research:writtenByReviewer ?reviewer ;
                research:reviewOf ?reviewedPaper .
    }
}
GROUP BY ?author ?authorName
HAVING (?paperCount > 2)  # Focus on active researchers
ORDER BY DESC(?influenceScore)
LIMIT 20


-- Query 2: Discover Cross-Domain Research Trends and Venue Quality Metrics
-- This query uses inference, property paths, and complex aggregations

PREFIX research: <http://research.publications.com/ontology#>
PREFIX instance: <http://research.publications.com/instance#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?venue ?venueName ?venueType
       (COUNT(DISTINCT ?paper) as ?totalPapers)
       (COUNT(DISTINCT ?citedPaper) as ?citedPapers)
       (AVG(?citationPerPaper) as ?avgCitations)
       (COUNT(DISTINCT ?keyword) as ?topicCoverage)
       (GROUP_CONCAT(DISTINCT ?topKeyword; SEPARATOR=", ") as ?topKeywords)
       (?citedPapers / ?totalPapers * 100 as ?citationRate)
WHERE {
    -- Venues can be Conferences, Workshops, or Journals (using UNION for flexibility)
    {
        ?venue a research:Conference ;
               research:hasName ?venueName .
        BIND("Conference" as ?venueType)
        
        -- Get papers from conference proceedings
        ?venue research:hasEdition ?edition .
        ?proceedings research:includesPaper ?paper .
    } UNION {
        ?venue a research:Workshop ;
               research:hasName ?venueName .
        BIND("Workshop" as ?venueType)
        
        -- Get papers from workshop proceedings
        ?venue research:hasEdition ?edition .
        ?proceedings research:includesPaper ?paper .
    } UNION {
        ?venue a research:Journal ;
               research:hasName ?venueName .
        BIND("Journal" as ?venueType)
        
        -- Get papers from journal volumes
        ?venue research:hasVolume ?volume .
        ?paper research:publishedInJournal ?volume .
    }
    
    -- Count citations for each paper
    OPTIONAL {
        SELECT ?paper (COUNT(?citingPaper) as ?citationPerPaper)
        WHERE {
            ?citingPaper research:cites ?paper .
        }
        GROUP BY ?paper
    }
    
    -- Check if paper is cited at all
    OPTIONAL {
        ?anyCitingPaper research:cites ?paper .
        BIND(?paper as ?citedPaper)
    }
    
    -- Get keywords for topic analysis
    OPTIONAL {
        ?paper research:hasKeyword ?keyword .
        ?keyword research:hasName ?keywordName .
        
        -- Identify top keywords (those appearing in multiple papers)
        {
            SELECT ?keyword (COUNT(?p) as ?keywordFreq)
            WHERE {
                ?p research:hasKeyword ?keyword .
            }
            GROUP BY ?keyword
            HAVING (?keywordFreq > 3)
        }
        BIND(?keywordName as ?topKeyword)
    }
    
}
GROUP BY ?venue ?venueName ?venueType
HAVING (?totalPapers > 5)  -- Only venues with sufficient papers
ORDER BY DESC(?citationRate) DESC(?avgCitations)