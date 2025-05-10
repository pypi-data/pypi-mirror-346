import shutil
import random
from tqdm import tqdm
from pathlib import Path
from bids import BIDSLayout
from . import get_inputfiles


def scramble_swap(inputdir: str, outputdir: str, select: str, grouping: list, bidsvalidate: bool=False, dryrun: bool=False, **_):

    # Defaults
    inputdir  = Path(inputdir).resolve()
    layout    = BIDSLayout(inputdir, validate=bidsvalidate)
    outputdir = Path(outputdir).resolve()

    # Use a tempdir to catch inplace editing
    print(f"Swapping BIDS data in: {outputdir}")
    if outputdir == inputdir:
        outputdir = outputdir/'tmpdir_swap'

    # Swap all sets of inputfiles
    swapped    = []                 # Already swapped input files
    inputfiles, _ = get_inputfiles(inputdir, select, '*', bidsvalidate)
    for inputfile in tqdm(inputfiles, unit='file', colour='green', leave=False):

        if inputfile in swapped:
            continue

        # Get the inputset and swap it
        entities = layout.parse_file_entities(inputfile)
        for entity in grouping:
            entities.pop(entity, None)
        inputset  = [Path(fname) for fname in layout.get(**entities, return_type='filename') if Path(fname) in inputfiles]
        outputset = random.sample(inputset, len(inputset))

        # Save the swapped output files
        for n, inputfile_ in enumerate(inputset):
            outputfile = outputdir/outputset[n].relative_to(inputdir)
            if not dryrun:
                outputfile.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(inputfile_, outputfile)
            swapped.append(inputfile_)

    # Move the tempdir files to the outputdir
    if outputdir.name == 'tmpdir_swap' and not dryrun:
        for outputfile in [tmpfile for tmpfile in outputdir.rglob('*') if tmpfile.is_file()]:
            outputfile.replace(outputdir.parent/outputfile.relative_to(outputdir))
        shutil.rmtree(outputdir)
