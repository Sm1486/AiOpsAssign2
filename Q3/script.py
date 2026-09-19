
import json
import os
import random
import pandas as pd

random.seed(42)

VALID_DOMAINS = ["gmail.com", "yahoo.com", "edu.in"]
INCORRECT_EMAILS = ["cat@apple.com", "dog@banana.com"]
NAME = ["SAM", "TAM", "CAT", "PAT"]

NUM_SHARDS = 8
ROWS_PER_SHARD = 10

def make_valid_email(user_id):
    return f"user{user_id}@{random.choice(VALID_DOMAINS)}"

os.makedirs("shards", exist_ok=True)

ground_truth = {}

for shard_idx in range(NUM_SHARDS):
    n_invalid = random.randint(1, 4)
    invalid_positions = set(random.sample(range(ROWS_PER_SHARD), n_invalid))
    names, emails = [], []
    for row_idx in range(ROWS_PER_SHARD):
        user_id = shard_idx * ROWS_PER_SHARD + row_idx
        if row_idx in invalid_positions:
            if random.random() < 0.5:
                names.append(random.choice(NAME))
                emails.append(random.choice(INCORRECT_EMAILS))
            else:
                names.append("")
                emails.append(make_valid_email(user_id))
        else:
            names.append(random.choice(NAME))
            emails.append(make_valid_email(user_id))

    df = pd.DataFrame({"Name": names, "Email": emails})
    df.to_csv(f"shards/shard_{shard_idx}.csv", index = False)
    ground_truth[f"shard_{shard_idx}"] = n_invalid

    with open("shards/ground_truth.json", "w") as f:
        json.dump(ground_truth, f)
