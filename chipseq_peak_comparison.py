import bionumpy as bnp
from bionumpy.arithmetics.similarity_measures import forbes, jaccard

# These are the transcription factors with good motif scores (and some bad ones)
filenames = {"CREM": "ENCFF324ELP.bed.gz",
             "ZNF263": "ENCFF295XBK.bed.gz",
             "FOXA1": "ENCFF497OQD.bed.gz",
             "NR3C1": "ENCFF201BGD.bed.gz"}


# Download all the files :)

# ! wget https://www.encodeproject.org/files/ENCFF843VHC/@@download/ENCFF843VHC.bed.gz
# ! wget https://www.encodeproject.org/files/ENCFF324ELP/@@download/ENCFF324ELP.bed.gz
# ! wget https://www.encodeproject.org/files/ENCFF201BGD/@@download/ENCFF201BGD.bed.gz
# ! wget https://www.encodeproject.org/files/ENCFF295XBK/@@download/ENCFF295XBK.bed.gz
# ! wget https://www.encodeproject.org/files/ENCFF497OQD/@@download/ENCFF497OQD.bed.gz
# ! wget https://raw.githubusercontent.com/igvteam/igv/master/genomes/sizes/hg38.chrom.sizes

# This is the filename for our ctcf tf file
ctcf_filename = "ENCFF843VHC.bed.gz"

# We need the size of the chromosomes in order to do similarity_measures
chrom_sizes = bnp.open("hg38.chrom.sizes").read()

# Since peak files are not sorted, we need to sort them
sort_order = chrom_sizes.name.tolist()
ctcf_peaks = bnp.arithmetics.sort_all_intervals(
    bnp.open(ctcf_filename).read(), sort_order=sort_order)


# Now to calculate scores
scores = {}
jaccards = {}
for name, filename in filenames.items():
    tf_peaks = bnp.arithmetics.sort_all_intervals(
        bnp.open(filename).read(),
        sort_order=sort_order)

    scores[name] = forbes(chrom_sizes, ctcf_peaks, tf_peaks)
    jaccards[name] = jaccard(chrom_sizes, ctcf_peaks, tf_peaks)

# Maybe the good motif scores predict good peak overlap?

print(scores)
print(jaccards)