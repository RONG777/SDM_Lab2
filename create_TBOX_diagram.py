from rdflib import Graph, RDF, RDFS
import graphviz

def generate_tbox_diagram(tbox_file):
    """Generate a Graphviz diagram from TBOX RDF file"""
    
    # Load TBOX
    g = Graph()
    g.parse(tbox_file, format="turtle")
    
    # Create Graphviz digraph
    dot = graphviz.Digraph('TBOX', comment='Research Publication Domain TBOX')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle', style='filled', width='1.5')
    
    # Color mapping for different types
    colors = {
        'Paper': '#87CEEB',      # Light blue
        'Author': '#FFD700',     # Gold
        'Reviewer': '#FFD700',   # Gold
        'Conference': '#FA8072', # Salmon
        'Workshop': '#FA8072',   # Salmon  
        'Journal': '#FA8072',    # Salmon
        'Edition': '#DDA0DD',    # Plum
        'Proceedings': '#90EE90', # Light green
        'Volume': '#90EE90',     # Light green
        'Review': '#DDA0DD',     # Plum
        'City': '#FFB6C1',       # Light pink
        'Keyword': '#E6E6FA',    # Lavender
        'University': '#FFB6C1', # Light pink
        'Company': '#FFB6C1'     # Light pink
    }
    
    # Extract classes
    classes = set()
    for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
        class_name = str(s).split('#')[-1]
        classes.add(class_name)
        color = colors.get(class_name, '#CCCCCC')
        dot.node(class_name, f"{class_name}\n○", fillcolor=color)
    
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        subclass = str(s).split('#')[-1]
        superclass = str(o).split('#')[-1]
        dot.edge(subclass, superclass, style='dashed', arrowhead='empty', label='rdfs:subClassOf')
    
    properties = {}
    subproperties = {}
    
    # First pass: collect all properties and subproperty relationships
    for s, p, o in g.triples((None, RDF.type, RDF.Property)):
        prop_name = str(s).split('#')[-1]
        properties[prop_name] = {'uri': s}
        
        # Check if it's a subproperty
        for _, _, superprop in g.triples((s, RDFS.subPropertyOf, None)):
            superprop_name = str(superprop).split('#')[-1]
            subproperties[prop_name] = superprop_name
    
    # Second pass: add properties with domain and range
    for prop_name, prop_info in properties.items():
        s = prop_info['uri']
        
        domain = None
        range_ = None
        for _, _, d in g.triples((s, RDFS.domain, None)):
            domain = str(d).split('#')[-1]
        for _, _, r in g.triples((s, RDFS.range, None)):
            range_ = str(r).split('#')[-1]
        
        if domain and range_ and domain in classes and range_ in classes:
            is_subprop = prop_name in subproperties
            
            if is_subprop and subproperties[prop_name] == 'writtenBy':
                dot.edge(domain, range_, label=f"{prop_name}\n○", style='bold', color='blue')
            elif is_subprop:
                dot.edge(domain, range_, label=f"{prop_name}\n○", style='bold')
            else:
                dot.edge(domain, range_, label=f"{prop_name}\n○")
    
    # Properties without specified domain (like hasEdition)
    for prop_name, prop_info in properties.items():
        s = prop_info['uri']
        domain = None
        range_ = None
        
        for _, _, r in g.triples((s, RDFS.range, None)):
            range_ = str(r).split('#')[-1]
                
    
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', style='dotted')
        legend.node('legend', 
                   '○ = Cardinality 0..*\\n'
                   '→ = Object Property\\n'
                   '⇢ = rdfs:subClassOf\\n'
                   '━ = rdfs:subPropertyOf\\n'
                   'Blue = subproperty of writtenBy\\n'
                   'Dotted = inferred relationship',
                   shape='plaintext', fillcolor='white')
    
    return dot

# Generate and save the diagram
if __name__ == "__main__":
    dot = generate_tbox_diagram("research_tbox.ttl")
    
    dot.render('tbox_diagram', format='png', cleanup=True)
    
    print("Diagram generated successfully!")
    print("Files created: tbox_diagram.png, tbox_diagram.dot")