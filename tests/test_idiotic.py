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
    # check if all frames in the mutagen object occur in the tag model
    available_std_frames = (list(idiot.text_frames.keys()) +
                            list(idiot.time_frames.keys()) +
                            list(idiot.url_frames.keys()))
    available_std_tags = (list(idiot.text_frames.values()) +
                          list(idiot.time_frames.values()) +
                          list(idiot.url_frames.values()))
    std_frames = [f for f in idiot.mut.tags.values()
                  if type(f) in available_std_frames]
    std_tags = [t for t in idiot.tags if t in available_std_tags]
    arbitrary_frames = [f for f in idiot.mut.tags.values()
                        if type(f) not in available_std_frames]
    arbitrary_tags = [t for t in idiot.tags
                      if t not in available_std_tags]

    assert len(std_tags) == len(std_frames)
    assert len(arbitrary_tags) == len(arbitrary_frames)

    # text frames
    assert type(idiot.tags['artist']) is str
    # time frames
    assert type(idiot.tags['year']) is str
    # url frames
    assert type(idiot.tags['wwwcopyright']) is str

    # arbitrary tags

    for frame in idiot.mut.tags.getall('TXXX'):
        assert frame.desc in idiot.tags
