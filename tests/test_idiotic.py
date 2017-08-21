import os
import idiotic
import pytest
import mutagen
import tempfile
import shutil


@pytest.fixture(params=['sound/test_sound_std.mp3',
                        'sound/test_sound_uni.mp3'])
def idiot(request):
    tmp_folder = os.path.abspath(tempfile.mkdtemp())
    tmp_file = os.path.join(tmp_folder, os.path.basename(request.param))

    shutil.copy2(request.param, tmp_file)
    idiot = idiotic.Id3(tmp_file)
    yield idiot
    shutil.rmtree(tmp_folder)


def test_mut_attr(idiot):
    assert type(idiot.mut) == mutagen.id3.ID3FileType

def test_imported_tag_types(idiot):
    # text frames
    assert type(idiot.tags['artist']) is str
    # time frames
    assert type(idiot.tags['year']) is str
    # url frames
    assert type(idiot.tags['wwwcopyright']) is str

