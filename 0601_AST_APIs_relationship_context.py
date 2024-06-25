import os
import json
import csv

def add_api_call(apis, caller, call, relationship):
    # Check if the caller already exists to avoid duplicates
    if caller in apis:
        if not any(x == (call, relationship) for x in apis[caller]):
            apis[caller].append((call, relationship))
    else:
        apis[caller] = [(call, relationship)]

def dfs(node, call_chain=[], apis={}, called={}):
    if isinstance(node, dict):
        if node.get('type') == 'CallExpression' and isinstance(node.get('callee'), dict):
            callee = node['callee']
            if callee.get('type') == 'MemberExpression':
                obj = callee.get('object')
                if isinstance(obj, dict) and obj.get('type') == 'Identifier':
                    caller = obj.get('name')
                    # Safely get the method name
                    method = callee['property'].get('name')
                    if method:  # Ensure method is not None
                        full_call = f"{caller}.{method}"
                        # Record API call information
                        if call_chain:
                            prev_call = call_chain[-1]
                            add_api_call(apis, prev_call, full_call, 'sequential')
                            called.setdefault(full_call, True)
                        apis.setdefault(full_call, [])
                        call_chain.append(full_call)
        
        # Recursively process all child nodes
        for value in node.values():
            if isinstance(value, dict):
                dfs(value, call_chain, apis, called)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        dfs(item, call_chain, apis, called)

        # Record nested relationships
        if len(call_chain) > 1:
            add_api_call(apis, call_chain[-2], call_chain[-1], 'nested')

        # Record parallel relationships
        if len(call_chain) > 2:
            for i in range(len(call_chain) - 2):
                call1 = call_chain[i]
                call2 = call_chain[-1]
                add_api_call(apis, call1, call2, 'parallel')
        
        # Remove the current node from the call chain when returning
        if call_chain and node.get('type') == 'CallExpression':
            call_chain.pop()

    return apis, called

def process_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.txt', '.csv'))
            with open(input_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            apis, called = dfs(data)
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Caller', 'API', 'Relationship'])
                for caller, calls in apis.items():
                    if calls:
                        for call, relationship in calls:
                            csvwriter.writerow([caller, call, relationship])
                    elif caller not in called:
                        csvwriter.writerow([caller, '', ''])


# Example Usage
input_folder = '05_AST_json'  # Replace with actual input folder path
output_folder = '07_API_relationship'  # Replace with actual output folder path

process_files(input_folder, output_folder)
