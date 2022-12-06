import bionumpy as bnp
from pyjaspar import jaspardb
from bionumpy.sequence.position_weight_matrix import PWM, get_motif_scores
import numpy as np
import plotly.express as plx

# Get the ctcf bed file
# ! wget https://www.encodeproject.org/files/ENCFF843VHC/@@download/ENCFF843VHC.bed.gz

peaks = bnp.open("ENCFF843VHC.bed.gz").read()
reference_genome = bnp.open_indexed("/home/knut/Data/hg38.fa")

sequences = reference_genome.get_interval_sequences(peaks)

# Get all human motifs :)
jdb_obj = jaspardb(release="JASPAR2020")
human_motifs = jdb_obj.fetch_motifs(collection="CORE", species=["9606"]) # 9606 is human

counts = []
lengths = []
# Calculate the motif scores for each sequence
for i, motif in enumerate(human_motifs):
    if i % 10 == 0:
        print(i)
    pwm = PWM.from_dict(motif.pwm)
    motif_scores = get_motif_scores(sequences, pwm)
    counts.append((motif_scores.max(axis=-1) > np.log(4)).sum())
    lengths.append(motif.length)


# Check that lentghts are not an influencing factor
plx.scatter(lengths, counts).show()


names = [m.name for m in human_motifs]

# Sort by number of significant hit
args = np.argsort(counts)
sorted_names = [names[i] for i in args]
