import os
import glob

for path in glob.glob("data/data_v2/**/**.json"):
    type, name = path.split("/")[-2:]
    print("Type: ", type, " | Name: ", name)
    if os.path.exists(f"results/{type}") == False:
        os.mkdir(f"results/data_v2/{type}")
        os.mkdir(f"results/data_v2/{type}/integer_programming")
    os.system(
        f"python algoritms/integer_programming.py \
            --input_file data/data_v2/{type}/{name} \
            --output_file results/data_v2/{type}/integer_programming/result_{name} \
            --time_limit")
