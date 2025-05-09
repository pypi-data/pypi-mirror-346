
import os
import logging
import pathlib
import extern
from tqdm.contrib.concurrent import process_map

def process_a_genome(params):
    pfam_search, tigrfam_search, hmms_and_names, output, log = params
    logging.debug("Processing genome: " + genome)

    pathlib.Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.dirname(log)).mkdir(parents=True, exist_ok=True)

    cmd = "python scripts/get_matches_no_dup.py " \
        "--pfam-search {} ".format(pfam_search) + \
        "--tigrfam-search {} ".format(tigrfam_search) + \
        "--hmm-list {} ".format(hmms_and_names) + \
        "--output {} ".format(output) + \
        "&> {}".format(log)
    extern.run(cmd)


genomes = snakemake.params.genome_ids
pfam_search_directory = snakemake.params.pfam_search_directory
tigrfam_search_directory = snakemake.params.tigrfam_search_directory
hmms_and_names = snakemake.params.hmms_and_names
output_dir = snakemake.params.output_dir
logs_dir = snakemake.params.logs_dir
num_threads = snakemake.threads

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

logging.info(os.path.basename(__file__) + ": Processing {} genomes with {} threads".format(len(genomes), num_threads))

param_sets = []
for genome in genomes:
    pfam_search = os.path.join(pfam_search_directory, f"{genome}.tsv")
    tigrfam_search = os.path.join(tigrfam_search_directory, f"{genome}.tsv")
    output_tsv = os.path.join(output_dir, f"{genome}.fam")
    log = os.path.join(logs_dir, f"{genome}_matching.log")
    # pfam_search, tigrfam_search, hmms_and_names, output, log
    param_sets.append((pfam_search, tigrfam_search, hmms_and_names, output_tsv, log))

process_map(process_a_genome, param_sets, max_workers=num_threads, chunksize=1)

logging.info('done')

# touch snakemake.output[0]
with open(snakemake.output[0], 'w') as _: pass
