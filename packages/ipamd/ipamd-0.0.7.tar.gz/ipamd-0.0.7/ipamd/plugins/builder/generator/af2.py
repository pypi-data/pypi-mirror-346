import subprocess
import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from ipamd.public.utils.output import info
import re
from shutil import copyfile
configure = {
    "schema": 'io',
}
def func(name, sequence, working_dir):
    fasta_path = os.path.join(working_dir, name + '.fasta')
    output_dir = os.path.join(working_dir, name + '-af')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    seq = Seq(sequence)
    seq_record = SeqRecord(seq,
                           id=name,
                           name=name,
                           description='')
    with open(fasta_path, "w") as output_handle:
        SeqIO.write(seq_record, output_handle, "fasta")
    info(f'running alphafold2 on sequence {sequence}')
    subprocess.run(
        [
            'colabfold_batch',
            fasta_path,
            output_dir,
            '--amber'
        ],
        capture_output=True
    )
    info('Alphafold2 finished')
    files = os.listdir(output_dir)
    for file in files:
        pattern = re.compile(rf'^{name}_relaxed.*001.*.pdb$')
        if pattern.match(file):
            pdb_path = os.path.join(output_dir, file)
            new_pdb_path = os.path.join(working_dir, f"{name}.pdb")
            copyfile(pdb_path, new_pdb_path)
