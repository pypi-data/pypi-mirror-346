import os
from readdat.read import autodetect_file_format

HERE = os.path.dirname(__file__)
FILESAMPLES = {
    "SEG2FILE": os.path.join(HERE, "..", 'filesamples', 'seg2file.sg2'),
    "SEG2FILE_MUSC": os.path.join(HERE, "..", 'filesamples', 'seg2file_musc.sg2'),
    "SEG2FILE_MUSC1": os.path.join(HERE, "..", 'filesamples', 'seg2file_musc1.sg2'),
    "SEG2FILE_ONDULYS": os.path.join(HERE, "..", 'filesamples', 'seg2file_ondulys.sg2'),
    "SEG2FILE_CODA": os.path.join(HERE, "..", 'filesamples', 'seg2file_coda.sg2'),
    "SEG2FILE_CODA1": os.path.join(HERE, "..", 'filesamples', 'seg2file_coda1.sg2'),
    "SEG2FILE_MUST": os.path.join(HERE, "..", "filesamples", "seg2file_must.sg2"),
    # "SEG2FILE_CDZ": os.path.join(HERE, "..", "filesamples", "seg2file_cdz.sg2"),
    "SEG2FILE_TOMAG": os.path.join(HERE, "..", "filesamples", "seg2file_tomag.sg2"),
    "TUSFILE": os.path.join(HERE, "..", "filesamples", "tusmusfile.tus"),
    "MUSFILE": os.path.join(HERE, "..", "filesamples", "tusmusfile.mus"),
    "MSEEDFILE": os.path.join(HERE, "..", "filesamples", "mseedfile.mseed"),
    "BINFILE": os.path.join(HERE, "..", "filesamples", "RDP_Wenner_2.bin"),
    "MATFILE": os.path.join(HERE, "..", "filesamples", "matquantum1.mat"),
    "SIGFILE": os.path.join(HERE, "..", "filesamples", "sigfile.sig"),
    "SEGDFILE": os.path.join(HERE, "..", "filesamples", "segdfile.segd"),
    "SEGDFILE_30": os.path.join(HERE, "..", "filesamples", "segdfile_rev3_0.segd"),
    }


def test_filesamples_exist():
    for name, filename in FILESAMPLES.items():
        assert os.path.isfile(filename), filename


def test_autodetect_file_format():

    assert autodetect_file_format(FILESAMPLES['SEG2FILE']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_MUSC']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_MUSC1']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_ONDULYS']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_CODA']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_CODA1']) == "SEG2"
    # assert autodetect_file_format(FILESAMPLES['SEG2FILE_CDZ']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_TOMAG']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['SEG2FILE_MUST']) == "SEG2"
    assert autodetect_file_format(FILESAMPLES['TUSFILE']) == "TUS"
    assert autodetect_file_format(FILESAMPLES['MUSFILE']) == "MUS"
    assert autodetect_file_format(FILESAMPLES['MSEEDFILE']) == "MSEED"
    assert autodetect_file_format(FILESAMPLES['BINFILE']) == "BIN"
    assert autodetect_file_format(FILESAMPLES['MATFILE']) == "MAT"
    assert autodetect_file_format(FILESAMPLES['SIGFILE']) == "SIG"
    assert autodetect_file_format(FILESAMPLES['SEGDFILE']) == "SEGD"
    assert autodetect_file_format(FILESAMPLES['SEGDFILE_30']) == "SEGD"





































