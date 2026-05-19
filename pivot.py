import re
from collections import defaultdict

def parse_markdown_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Extract headers
    header_line = None
    data_lines = []
    for line in lines:
        if line.strip().startswith('|'):
            if '---' in line:
                continue
            if not header_line:
                header_line = [col.strip() for col in line.strip().strip('|').split('|')]
            else:
                data_lines.append([col.strip() for col in line.strip().strip('|').split('|')])
                
    return header_line, data_lines

def process_table(header, data):
    # original headers: ['Source system name', 'Consumer', 'Pattern Inbound', 'Pattern Outbound']
    
    downstream_map = defaultdict(list)
    
    for row in data:
        source = row[0]
        consumer_raw = row[1]
        inbound = row[2]
        outbound = row[3]
        
        # Split consumers by <br>, comma, or newline.
        # Be careful with things like "MI Risk and Compliance Assurance Services,MI", "RC- Rapid2, RCRI, CIMT, Engage2"
        # Let's split by <br> and comma. But note "MI Risk and Compliance..." might be one thing? 
        # Actually splitting by <br> and `,` is safe.
        
        consumers = re.split(r'<br>|,', consumer_raw)
        for consumer in consumers:
            c = consumer.strip()
            if c:
                downstream_map[c].append({
                    'Source': source,
                    'Inbound': inbound,
                    'Outbound': outbound
                })
                
    return downstream_map

def write_markdown_table(downstream_map, out_file):
    # Sort by Consumer
    sorted_consumers = sorted(downstream_map.keys(), key=lambda x: x.lower())
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# CDR Downstream and Upstream System Pattern Mapping\n\n")
        f.write("| Consumer (Downstream) | Source System (Upstream) | Pattern Inbound | Pattern Outbound |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for consumer in sorted_consumers:
            entries = downstream_map[consumer]
            # To make it look clean, we can either span rows or just repeat the consumer
            # Let's group by consumer, and join multiple sources with <br> if we want, OR just flat rows.
            # Flat rows are usually better for filtering/sorting.
            for entry in entries:
                f.write(f"| {consumer} | {entry['Source']} | {entry['Inbound']} | {entry['Outbound']} |\n")

if __name__ == '__main__':
    in_file = './cdr-demise-docs/mappings/pattern_mapping.md'
    out_file = './cdr-demise-docs/mappings/downstream_pattern_mapping.md'
    
    header, data = parse_markdown_table(in_file)
    downstream_map = process_table(header, data)
    write_markdown_table(downstream_map, out_file)
    print(f"Successfully pivoted table and saved to {out_file}")
