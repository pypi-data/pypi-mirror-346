import subprocess
from bidscramble import console_scripts, drmaa_nativespec


def test_cli_help():
    print(scripts := console_scripts(True))
    assert 'scramble' in scripts
    assert 'merge' in scripts
    for command in scripts:
        process = subprocess.run(f"{command} -h", shell=True, capture_output=True, text=True)
        print(f"{command} -h\n{process.stderr}\n{process.stdout}")
        assert process.stdout
        assert process.returncode == 0


def test_drmaa_nativespec():

    class DrmaaSession:
        def __init__(self, drmaaImplementation):
            self.drmaaImplementation = drmaaImplementation

    specs = drmaa_nativespec('-l walltime=00:10:00,mem=2gb', DrmaaSession('PBS Pro'))
    assert specs == '-l walltime=00:10:00,mem=2gb'

    specs = drmaa_nativespec('-l walltime=00:10:00,mem=2gb', DrmaaSession('Slurm'))
    assert specs == '--time=00:10:00 --mem=2000'

    specs = drmaa_nativespec('-l mem=200,walltime=00:10:00', DrmaaSession('Slurm'))
    assert specs == '--mem=200 --time=00:10:00'

    specs = drmaa_nativespec('-l walltime=00:10:00,mem=2gb', DrmaaSession('Unsupported'))
    assert specs == ''
