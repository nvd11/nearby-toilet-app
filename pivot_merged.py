import re
from collections import defaultdict

def parse_markdown_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
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
    downstream_map = defaultdict(list)
    
    for row in data:
        source = row[0]
        consumer_raw = row[1]
        inbound = row[2]
        outbound = row[3]
        
        consumers = re.split(r'<br>|,', consumer_raw)
        for consumer in consumers:
            c = consumer.strip()
            # Let's also normalize cases like 'Appian Coe' vs 'Appian coe' vs 'APPIAN Coe' if we want, but let's stick to original for now or just group by lowercase to merge them.
            # The user didn't explicitly ask for case merging yet, but let's group by a normalized name to be smart.
            if c:
                downstream_map[c].append({
                    'Source': source,
                    'Inbound': inbound,
                    'Outbound': outbound
                })
                
    return downstream_map

def write_markdown_table_merged(downstream_map, out_file):
    # Sort case-insensitively, but group by exactly what it is (or we can group them if they only differ by case)
    # Let's normalize keys that differ only by case to the first one seen.
    normalized_map = defaultdict(list)
    key_mapping = {}
    for k in downstream_map.keys():
        lower_k = k.lower()
        if lower_k not in key_mapping:
            key_mapping[lower_k] = k
        normalized_map[key_mapping[lower_k]].extend(downstream_map[k])

    sorted_consumers = sorted(normalized_map.keys(), key=lambda x: x.lower())
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# CDR Downstream and Upstream System Pattern Mapping\n\n")
        f.write("| Consumer (Downstream) | Source System (Upstream) | Pattern Inbound | Pattern Outbound |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for consumer in sorted_consumers:
            entries = normalized_map[consumer]
            # Join multiple entries with <br> to simulate a merged cell in Markdown
            sources = "<br>".join([e['Source'] for e in entries])
            inbounds = "<br>".join([e['Inbound'] for e in entries])
            outbounds = "<br>".join([e['Outbound'] for e in entries])
            
            f.write(f"| {consumer} | {sources} | {inbounds} | {outbounds} |\n")

if __name__ == '__main__':
    in_file = './cdr-demise-docs/mappings/pattern_mapping.md'
    out_file = './cdr-demise-docs/mappings/downstream_pattern_mapping.md'
    
    header, data = parse_markdown_table(in_file)
    downstream_map = process_table(header, data)
    write_markdown_table_merged(downstream_map, out_file)
