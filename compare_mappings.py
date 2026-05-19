import re

def parse_original(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
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
                source = cols[0]
                consumer_raw = cols[1]
                inbound = cols[2]
                outbound = cols[3]
                
                consumers = re.split(r'<br>|,', consumer_raw)
                for consumer in consumers:
                    c = consumer.strip()
                    if c:
                        # Normalize consumer name to lowercase for comparison, as we did in generation
                        records.append({
                            'consumer_norm': c.lower(),
                            'source': source,
                            'inbound': inbound,
                            'outbound': outbound,
                            'original_consumer': c
                        })
    return records

def parse_downstream(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    header_found = False
    current_consumer = None
    for line in lines:
        if line.strip().startswith('|'):
            if '---' in line:
                header_found = True
                continue
            if not header_found:
                continue
                
            cols = [col.strip() for col in line.strip().strip('|').split('|')]
            if len(cols) == 4:
                consumer = cols[0]
                source = cols[1]
                inbound = cols[2]
                outbound = cols[3]
                
                if consumer:
                    current_consumer = consumer
                
                if current_consumer and source: # skip empty lines if any
                    records.append({
                        'consumer_norm': current_consumer.lower(),
                        'source': source,
                        'inbound': inbound,
                        'outbound': outbound,
                        'original_consumer': current_consumer
                    })
    return records

def compare(orig_records, down_records):
    # Create sets of tuples for easy comparison
    orig_set = set((r['consumer_norm'], r['source'], r['inbound'], r['outbound']) for r in orig_records)
    down_set = set((r['consumer_norm'], r['source'], r['inbound'], r['outbound']) for r in down_records)
    
    missing_in_downstream = orig_set - down_set
    extra_in_downstream = down_set - orig_set
    
    print(f"Total original records (split): {len(orig_records)}")
    print(f"Total downstream records: {len(down_records)}")
    
    if not missing_in_downstream and not extra_in_downstream:
        print("\n✅ SUCCESS: Both files match perfectly! No data was lost or altered.")
    else:
        if missing_in_downstream:
            print(f"\n❌ ERROR: Found {len(missing_in_downstream)} records missing in downstream file:")
            for m in missing_in_downstream:
                print(f"  - {m}")
                
        if extra_in_downstream:
            print(f"\n❌ ERROR: Found {len(extra_in_downstream)} extra/altered records in downstream file:")
            for e in extra_in_downstream:
                print(f"  - {e}")

if __name__ == '__main__':
    orig_file = './cdr-demise-docs/mappings/pattern_mapping.md'
    down_file = './cdr-demise-docs/mappings/downstream_pattern_mapping.md'
    
    orig = parse_original(orig_file)
    down = parse_downstream(down_file)
    
    compare(orig, down)
