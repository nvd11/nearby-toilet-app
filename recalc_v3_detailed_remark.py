import re
from collections import defaultdict

def parse_markdown_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data_lines = []
    header_found = False
    for line in lines:
        if line.strip().startswith('|'):
            if '---' in line:
                header_found = True
                continue
            if not header_found:
                continue
            cols = [col.strip() for col in line.strip().strip('|').split('|')]
            if len(cols) == 4:
                data_lines.append(cols)
    return data_lines

def calculate_effort(inbound, outbound):
    in_md = 34
    in_lower = inbound.lower()
    if 'file' in in_lower: in_md = 34
    elif 'db' in in_lower or 'table' in in_lower: in_md = 34 
    elif 'api' in in_lower: in_md = 30
    elif 'event' in in_lower or 'pubsub' in in_lower: in_md = 29.5
        
    out_md = 17.5
    out_lower = outbound.lower()
    if 'file' in out_lower: out_md = 19.5
    elif 'api' in out_lower: out_md = 20.5
    elif 'table' in out_lower or 'view' in out_lower: out_md = 17.5
        
    return in_md, out_md

def process_data(data):
    consumer_map = defaultdict(lambda: {'sources': {}, 'outbound_md': 0})
    for row in data:
        source = row[0]
        consumer_raw = row[1]
        inbound = row[2]
        outbound = row[3]
        in_md, out_md = calculate_effort(inbound, outbound)
        consumers = re.split(r'<br>|,', consumer_raw)
        for consumer in consumers:
            c = consumer.strip()
            if c:
                consumer_map[c]['sources'][source] = in_md
                consumer_map[c]['outbound_md'] = out_md 
    return consumer_map

def generate_v3_plan(consumer_map, out_file):
    normalized_map = defaultdict(lambda: {'sources': {}, 'outbound_md': 0})
    key_mapping = {}
    for k, v in consumer_map.items():
        lower_k = k.lower()
        if lower_k not in key_mapping:
            key_mapping[lower_k] = k
        for src, md in v['sources'].items():
            normalized_map[key_mapping[lower_k]]['sources'][src] = md
        normalized_map[key_mapping[lower_k]]['outbound_md'] = v['outbound_md']

    batch1_names = ['rapid2', 'regmap', 'rapid2 mi', 'regmap mi']
    
    def sort_key(x):
        lower_x = x.lower()
        is_batch1 = 0 if lower_x in batch1_names else 1
        return (is_batch1, lower_x)
        
    sorted_consumers = sorted(normalized_map.keys(), key=sort_key)
    
    # Store which downstream consumer first "covered" the upstream source
    seen_sources = {}
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# CDR Demise Master Plan (v3 Comprehensive)\n\n")
        f.write("## 1. Executive Summary\n")
        f.write("This master plan aligns management's 4-batch target dates with our engineering team's Pattern-Based Estimation Methodology. By applying standardized Man-Day (MD) baselines to each integration, we provide a transparent and data-driven schedule.\n\n")
        
        f.write("## 2. Estimation Methodology (Baselines)\n")
        f.write("Calculations are based on the following finalized baselines. *(Note: Direct upstream DB connections are strictly prohibited; any legacy DB patterns are estimated based on a forced migration to File/API/Event).* \n\n")
        f.write("*   **Upstream File (NAS/SFTP):** 34.0 MD\n")
        f.write("*   **Upstream API Pull:** 30.0 MD\n")
        f.write("*   **Upstream Event Driven (Pub/Sub):** 29.5 MD\n")
        f.write("*   **Downstream Auth Views:** 17.5 MD\n")
        f.write("*   **Downstream File Export:** 19.5 MD\n")
        f.write("*   **Downstream API Provision:** 20.5 MD\n")
        f.write("*   **💡 Upstream Reusability Discount:** If an upstream source is already ingested for a previous consumer (e.g., in Batch 1), subsequent consumers only require **5.0 MD** to develop additional data points/fields from that same source.\n\n")
        
        f.write("## 3. Execution Roadmap & Effort Calculation\n")
        f.write("The Total MD for each consumer is calculated as: `(Sum of Upstream Source MDs) + Downstream Pattern MD`.\n\n")
        
        f.write("| Consumer (Downstream) | Required Upstream Sources | Effort Formula (Upstream + Downstream) | Calculated Effort | Target Demise Batch | Target DV Ready | Target Demise Date | Remark |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        for consumer in sorted_consumers:
            sources_dict = normalized_map[consumer]['sources']
            sources_list = sorted(list(sources_dict.keys()))
            
            outbound_md = normalized_map[consumer]['outbound_md']
            
            inbound_parts = []
            inbound_total = 0
            row_remarks = {}
            
            for src in sources_list:
                base_md = sources_dict[src]
                if src in seen_sources:
                    md = 5.0
                    inbound_parts.append("5")
                    covered_by = seen_sources[src]
                    row_remarks[src] = f"Source '{src}' already covered by **{covered_by}**; 5 MD for additional data points."
                else:
                    md = base_md
                    val_str = str(md) if md % 1 != 0 else str(int(md))
                    inbound_parts.append(val_str)
                    seen_sources[src] = consumer # Mark this consumer as the one who paid the full price
                    row_remarks[src] = ""
                inbound_total += md
            
            total_md = inbound_total + outbound_md
            
            inbound_str = " + ".join(inbound_parts)
            outbound_str = str(outbound_md) if outbound_md % 1 != 0 else str(int(outbound_md))
            
            if len(inbound_parts) > 1:
                formula = f"({inbound_str}) + {outbound_str}"
            elif len(inbound_parts) == 1:
                formula = f"{inbound_str} + {outbound_str}"
            else:
                formula = f"0 + {outbound_str}"
            
            batch = "TBD"
            dv_date = "TBD"
            demise_date = "TBD"
            
            if consumer.lower() in batch1_names:
                batch = "1"
                dv_date = "1-July-2026"
                demise_date = "30-July-2026"
                
            for i, source in enumerate(sources_list):
                remark = row_remarks[source]
                if i == 0:
                    f.write(f"| **{consumer}** | {source} | {formula} | **{total_md} MD** | {batch} | {dv_date} | {demise_date} | {remark} |\n")
                else:
                    f.write(f"| | {source} | | | | | | {remark} |\n")

if __name__ == '__main__':
    in_file = './cdr-demise-docs/mappings/pattern_mapping.md'
    out_file = './cdr-demise-docs/plans/CDR_Demise_Plan_v3.md'
    data = parse_markdown_table(in_file)
    cmap = process_data(data)
    generate_v3_plan(cmap, out_file)
