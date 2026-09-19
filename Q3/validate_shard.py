import json
import os
import re
import sys
import pandas as pd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid(name, email):
    if name == None or name == "":
        return False
    if email == None or not EMAIL_RE.match(str(email).strip()):
        return False
    return True

def main():
    index = int(os.environ.get("JOB_COMPLETION_INDEX"))
    pod_name = os.environ.get("POD_NAME", "unknown_pod")
    node_name = os.environ.get("NODE_NAME", "unknown_node")
    shard_path = f"/data/shard_{index}.csv"
    df = pd.read_csv(shard_path)
    invalid_rows = sum([0 if is_valid(row["Name"], row["Email"]) else 1 for _, row in df.iterrows()])
    results = {"shard_idx" : index, "shard_file" : f"shard_{index}.csv", "pod_name": pod_name, "node_name":node_name, "total_rows": len(df), "invalid_rows": invalid_rows}

if ___name__ == "__main__":
    main()
