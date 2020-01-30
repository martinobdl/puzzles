with open("text.text","r") as f:
    RNA = f.readlines()[0][:-1]

with open("key.txt","r") as f:
    key = f.readlines()[0][:-1]
    key=key+","
    key = key[5:].split(" ")
    key = list(map(lambda x: int(x[:-1]), key))

rna_to_dna = {'U':'A',
            'A':'T',
            'C':'G',
            'G':'C'}

codon_table = {}

DNA_table = { 
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                  
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W', 
} 

RNA_table = {"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
    "UCU":"S", "UCC":"s", "UCA":"S", "UCG":"S",
    "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"*",
    "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
    "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
    "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
    "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
    "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
    "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
    "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
    "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G",}

ammino_name = {"F":"Phenylalanine",
        "L":"Leucine",
        "I":"Isoleucine",
        "M":"Methionine",
        "V":"Valine",
        "S":"Serine",
        "P":"Proline",
        "T":"Threonine",
        "A":"Alanine",
        "Y":"Tyrosine",
        "H":"Histidine",
        "Q":"Glutamine",
        "N":"Asparagine",
        "K":"Lysine",
        "D":"Aspartic acid",
        "E":"Glutamic acid",
        "C":"Cysteine",
        "W":"Tryptophan",
        "R":"Arginine",
        "G":"Glycine"
        }

DNA = "".join(list(map(lambda x: rna_to_dna[x], RNA)))
print("RNA: ",RNA)
def transale_dna(message):
	s=""
	cds = [message[i:i+3] for i in range(0, len(message), 3)]
	for cd in cds:
		if cd in DNA_table.keys():
			s+= DNA_table[cd]
		else:
			s+="*"
	return s

def transale_rna(message):
	s=""
	cds = [message[i:i+3] for i in range(0, len(message), 3)]
	for cd in cds:
		if cd in RNA_table.keys():
			s+= RNA_table[cd]
		else:
			s+="*"
	return s

print("RNA tr: ", transale_rna(RNA))
for k,a in zip(key,transale_rna(RNA)[1:-1]):
    print(ammino_name[a][k-1],end="")
