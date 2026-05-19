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
    in_md = 37.0 
    in_lower = inbound.lower()
    if 'file' in in_lower: in_md = 37.0
    elif 'db' in in_lower or 'table' in in_lower: in_md = 37.0 
    elif 'api' in in_lower: in_md = 33.0
    elif 'event' in in_lower or 'pubsub' in in_lower: in_md = 32.5
        
    out_md = 20.5 
    out_lower = outbound.lower()
    if 'file' in out_lower: out_md = 22.5
    elif 'api' in out_lower: out_md = 23.5
    elif 'table' in out_lower or 'view' in out_lower: out_md = 20.5
        
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
                
    if 'REGMAP MI' in consumer_map:
        found = any(src.lower() == 'regmap' for src in consumer_map['REGMAP MI']['sources'].keys())
        if not found:
            consumer_map['REGMAP MI']['sources']['REGMAP'] = 37.0 
            
    return consumer_map

def get_consumer_cost(consumer, sources_dict, outbound_md, seen_sources):
    inbound_total = 0
    for src, base_md in sources_dict.items():
        if consumer.lower() == 'regmap mi' and src.lower() == 'helios':
            inbound_total += 10.0
        elif consumer.lower() == 'regmap' and src.lower() == 'rdh and helios(rdm)':
            inbound_total += 10.0
        elif consumer.lower() == 'rapid2 mi' and src.lower() == 'rapid2':
            inbound_total += 20.0
        elif consumer.lower() == 'askc business' and src.lower() == 'askc':
            inbound_total += 20.0
        elif src in seen_sources:
            inbound_total += 5.0
        else:
            inbound_total += base_md
    return inbound_total + outbound_md

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

    unprocessed = list(normalized_map.keys())
    seen_sources = {}
    ordered_consumers = []
    
    # Calculate overall total MD
    overall_total_md = 0.0
    temp_seen_sources = {}
    
    while unprocessed:
        best_consumer = None
        best_cost = float('inf')
        
        for consumer in unprocessed:
            sources_dict = normalized_map[consumer]['sources']
            outbound_md = normalized_map[consumer]['outbound_md']
            cost = get_consumer_cost(consumer, sources_dict, outbound_md, temp_seen_sources)
            
            if cost < best_cost or (cost == best_cost and (best_consumer is None or consumer < best_consumer)):
                best_cost = cost
                best_consumer = consumer
                
        ordered_consumers.append(best_consumer)
        unprocessed.remove(best_consumer)
        overall_total_md += best_cost
        
        sources_dict = normalized_map[best_consumer]['sources']
        for src in sources_dict.keys():
            if src not in temp_seen_sources:
                temp_seen_sources[src] = best_consumer

    seen_sources_for_writing = {}
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# CDR Demise Master Plan (v3 Comprehensive)\n\n")
        f.write("## 1. Executive Summary\n")
        f.write("This master plan aligns management's target dates with our engineering team's Pattern-Based Estimation Methodology. By applying standardized Man-Day (MD) baselines to each integration, we provide a transparent and data-driven schedule. **The execution roadmap is intelligently sorted by migration difficulty (Quick Wins first), maximizing upstream reusability to reduce overall delivery time.**\n\n")
        
        f.write(f"**📊 Project Effort Overview:**\n")
        f.write(f"Based on the detailed roadmap below, the total estimated effort for the entire CDR Demise project is **{overall_total_md} Man-Days (MD)**.\n")
        
        man_months = overall_total_md / 20.0
        engineers_needed_12m = man_months / 12.0
        
        f.write(f"* **Man-Months equivalent:** ~{round(man_months, 1)} Man-Months (assuming 20 working days/month).\n")
        f.write(f"* **Resource Projection:** To deliver this project within a **12-month timeframe**, a dedicated team of at least **{round(engineers_needed_12m, 1)} full-time engineers** is required.\n\n")
        
        f.write("***External Dependency Note: For upstream systems outside of the Risk and Compliance (RC) department, our ingestion strategy heavily depends on the API Proxy Service currently being built by the CDR team. Any delays in their API proxy delivery will directly impact our RCDP integration timeline.***\n\n")
        
        f.write("## 2. Estimation Methodology (Baselines)\n")
        f.write("Calculations are based on the following finalized baselines. *(Note: Direct upstream DB connections are strictly prohibited; any legacy DB patterns are estimated based on a forced migration to File/API/Event).* \n\n")
        f.write("*   **Upstream File (NAS/SFTP):** 37.0 MD\n")
        f.write("*   **Upstream API Pull:** 33.0 MD\n")
        f.write("*   **Upstream Event Driven (Pub/Sub):** 32.5 MD\n")
        f.write("*   **Downstream Auth Views:** 20.5 MD\n")
        f.write("*   **Downstream File Export:** 22.5 MD\n")
        f.write("*   **Downstream API Provision:** 23.5 MD\n")
        f.write("*   **💡 Upstream Reusability Discount:** If an upstream source is already ingested for a previous consumer, subsequent consumers only require **5.0 MD** to develop additional data points/fields from that same source.\n\n")
        
        f.write("## 3. Execution Roadmap & Effort Calculation\n")
        f.write("The Total MD for each consumer is calculated as: `(Sum of Upstream Source MDs) + Downstream Pattern MD`.\n\n")
        
        f.write("| Consumer (Downstream) | Required Upstream Sources | Effort Formula (Upstream + Downstream) | Calculated Effort | Target Demise Batch | Target DV Ready | Target Demise Date | Remark |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        for consumer in ordered_consumers:
            sources_dict = normalized_map[consumer]['sources']
            sources_list = sorted(list(sources_dict.keys()))
            
            outbound_md = normalized_map[consumer]['outbound_md']
            
            inbound_parts = []
            inbound_total = 0
            row_remarks = {}
            
            for src in sources_list:
                base_md = sources_dict[src]
                
                if consumer.lower() == 'regmap mi' and src.lower() == 'helios':
                    md = 10.0
                    inbound_parts.append("10")
                    seen_sources_for_writing[src] = consumer
                    row_remarks[src] = "RCDP already has Helios connection; 10 MD for pipeline extension."
                elif consumer.lower() == 'regmap mi' and src.lower() == 'regmap':
                    md = 37.0
                    inbound_parts.append("37")
                    seen_sources_for_writing[src] = consumer
                    row_remarks[src] = "Missing source added per Jason's correction; applying full integration baseline (37.0 MD) as no prior connection exists."
                elif consumer.lower() == 'regmap' and src.lower() == 'rdh and helios(rdm)':
                    md = 10.0
                    inbound_parts.append("10")
                    seen_sources_for_writing[src] = consumer
                    row_remarks[src] = "RCDP already has RDH connection; 10 MD for pipeline extension."
                elif consumer.lower() == 'rapid2 mi' and src.lower() == 'rapid2':
                    md = 20.0
                    inbound_parts.append("20")
                    seen_sources_for_writing[src] = consumer
                    row_remarks[src] = "RCDP already has RAPID2 connection; 20 MD for heavy table creation & history data migration."
                elif consumer.lower() == 'askc business' and src.lower() == 'askc':
                    md = 20.0
                    inbound_parts.append("20")
                    seen_sources_for_writing[src] = consumer
                    row_remarks[src] = "RCDP already has ASKC connection; 20 MD for heavy table creation & history data migration."
                elif src in seen_sources_for_writing:
                    md = 5.0
                    inbound_parts.append("5")
                    covered_by = seen_sources_for_writing[src]
                    row_remarks[src] = f"Source '{src}' already covered by **{covered_by}**; 5 MD for additional data points."
                else:
                    md = base_md
                    val_str = str(md) if md % 1 != 0 else str(int(md))
                    inbound_parts.append(val_str)
                    seen_sources_for_writing[src] = consumer 
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
