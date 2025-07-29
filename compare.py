#!/usr/bin/env python3
import sys
from regressionTests import parseFile, color, colors

def compare_rules(file1, file2):
    parsed1 = parseFile(file1)
    parsed2 = parseFile(file2)
    
    if isinstance(parsed1, str) or isinstance(parsed2, str):
        print(f"Error parsing files: {parsed1 if isinstance(parsed1, str) else parsed2}")
        return
    
    rules1 = parsed1[8]  # Rules are at index 8 in the returned tuple
    rules2 = parsed2[8]
    
    if rules1 != rules2:
        print(f"Rules differ between {file1} and {file2}")
        if len(rules1) != len(rules2):
            print(f"Number of rules: {len(rules1)} vs {len(rules2)}")
        else:
            for i in range(len(rules1)):
                if rules1[i] != rules2[i]:
                    print(f"Rule {i+1} differs:")
                    print(f"--- {file1}")
                    print(f"+++ {file2}")
                    print(f"{rules1[i]}")
                    print(f"{rules2[i]}")
                    print("-------------------")
    else:
       print("no souce")

def compare_all(file1, file2):
    parsed1 = parseFile(file1)
    print("Parsing file 2... \n \n")
    parsed2 = parseFile(file2)

    if isinstance(parsed1, str) or isinstance(parsed2, str):
        print(f"Error parsing files: {parsed1 if isinstance(parsed1, str) else parsed2}")
        return

    sections = [
        ("lemmas", 0),
        ("results", 1),
        ("steps", 2),
        ("time", 3),
        ("proof", 4),
        ("equations", 5),
        ("functions", 6),
        ("warnings", 7),
        ("rules", 8),
        ("builtins", 9),
        ("configblock", 10),
        ("macros", 11)
    ]

    for name, idx in sections:
        val1 = parsed1[idx]
        val2 = parsed2[idx]
        if name == "rules":
            # print("\nRules comparison:")
            if len(val1) != len(val2):
                print(f"  Number of rules: {len(val1)} vs {len(val2)}")
                for i in range(min(len(val1), len(val2))):
                    print(f"  Rule {i+1} in {file1}: {val1[i]['name']}")
                    print(f"  Rule {i+1} in {file2}: {val2[i]['name']}")
                if len(val1) > len(val2):
                    for i in range(len(val2), len(val1)):
                        print(f"  Extra rule in {file1}: {val1[i]['name']}")
                elif len(val2) > len(val1):
                    for i in range(len(val1), len(val2)):
                        print(f"  Extra rule in {file2}: {val2[i]['name']}")
            else:
                identical = True
                for i in range(len(val1)):
                    ruleA = val1[i]
                    ruleB = val2[i]
                    # print(f"  Rule {i+1}:")
                    # print(f"    {file1}: {ruleA['name']}, attributes: {ruleA['attributes']}")
                    # print(f"    {file2}: {ruleB['name']}, attributes: {ruleB['attributes']}")
                    if ruleA['name'] != ruleB['name']:
                        print(f"    Rule name changed from '{ruleA['name']}' to '{ruleB['name']}'")
                        identical = False
                    if ruleA['attributes'] != ruleB['attributes']:
                        print(f"    Attributes for rule '{ruleA['name']}' changed from {ruleA['attributes']} to {ruleB['attributes']}")
                        identical = False
                    if ruleA['body'] != ruleB['body']:
                        print(f"    Body for rule '{ruleA['name']}' changed:\n---{file1}---\n{ruleA['body']}\n---{file2}---\n{ruleB['body']}")
                        identical = False
                if identical:
                    print("All rules are identical.")
            continue  # Skip the generic comparison for rules
        if val1 != val2:
            print(f"\n{name.capitalize()} differ between {file1} and {file2}:")
            if isinstance(val1, list) and isinstance(val2, list):
                if len(val1) != len(val2):
                    print(f"  Number of items: {len(val1)} vs {len(val2)}")
                for i in range(min(len(val1), len(val2))):
                    if val1[i] != val2[i]:
                        print(f"  Item {i+1} differs:\n    {file1}: {val1[i]}\n    {file2}: {val2[i]}")
                if len(val1) > len(val2):
                    for i in range(len(val2), len(val1)):
                        print(f"  Extra in {file1}: {val1[i]}")
                elif len(val2) > len(val1):
                    for i in range(len(val1), len(val2)):
                        print(f"  Extra in {file2}: {val2[i]}")
            else:
                print(f"  {file1}: {val1}")
                print(f"  {file2}: {val2}")
        else:
            print(f"{name.capitalize()} are identical.")
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compare_rules.py file1.spthy file2.spthy")
        sys.exit(1)
    compare_all(sys.argv[1], sys.argv[2])