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
                
    return data_lines

def process_table(data):
    downstream_map = defaultdict(list)
    
    for row in data:
        source = row[0]
        consumer_raw = row[1]
        
        consumers = re.split(r'<br>|,', consumer_raw)
        for consumer in consumers:
            c = consumer.strip()
            if c:
                downstream_map[c].append(source)
                
    return downstream_map

def generate_plan_markdown(downstream_map, out_file):
    # Normalize keys
    normalized_map = defaultdict(list)
    key_mapping = {}
    for k in downstream_map.keys():
        lower_k = k.lower()
        if lower_k not in key_mapping:
            key_mapping[lower_k] = k
        normalized_map[key_mapping[lower_k]].extend(downstream_map[k])

    # Sort consumers
    sorted_consumers = sorted(normalized_map.keys(), key=lambda x: x.lower())
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# CDR Demise Plan (v2 Detailed Draft)\n\n")
        f.write("## 1. Executive Summary\n")
        f.write("This document outlines the detailed execution plan for migrating from CDR to RCDP. It combines our internal delivery capabilities (estimation) with management's target milestones.\n\n")
        
        f.write("## 2. Detailed Execution Plan\n")
        f.write("This master plan is driven by Consumer (Downstream) requirements, detailing the necessary upstream dependencies and our estimated effort before mapping to the target Demise Batches.\n\n")
        
        f.write("| Consumer (Downstream) | Required Upstream Sources | Estimation (Man-Days) | Target Demise Batch | Target DV Ready Date | Target Demise Date |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        for consumer in sorted_consumers:
            # Deduplicate sources and join with comma
            sources = list(dict.fromkeys(normalized_map[consumer]))
            sources_str = ", ".join(sources)
            
            # Default placeholders for PM to fill
            est = "TBD"
            batch = "TBD"
            dv_date = "TBD"
            demise_date = "TBD"
            
            # Auto-assign Mona's constraints for RAPID2 and REGMAP to Batch 1
            if consumer.lower() in ['rapid2', 'regmap', 'rapid2 mi', 'regmap mi']:
                batch = "1"
                dv_date = "1-July-2026"
                demise_date = "30-July-2026"
                
            f.write(f"| {consumer} | {sources_str} | {est} | {batch} | {dv_date} | {demise_date} |\n")

if __name__ == '__main__':
    in_file = './cdr-demise-docs/mappings/pattern_mapping.md'
    out_file = './cdr-demise-docs/plans/CDR_Demise_Plan_v2.md'
    
    data = parse_markdown_table(in_file)
    downstream_map = process_table(data)
    generate_plan_markdown(downstream_map, out_file)
