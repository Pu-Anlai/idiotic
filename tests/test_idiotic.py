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


def test_frame_to_tag_transfer(idiot):
    # create a dict of all frame-tag-dicts and a list of values and keys
    combined_frame_dicts = {}
    combined_frame_dicts.update(idiot.text_frames)
    combined_frame_dicts.update(idiot.time_frames)
    combined_frame_dicts.update(idiot.url_frames)
    available_std_frames = (list(combined_frame_dicts.keys()))
    available_std_tags = (list(combined_frame_dicts.values()))

    # create lists of tags/frames present in the object
    std_frames = [f for f in idiot.mut.tags.values()
                  if type(f) in available_std_frames]
    std_tags = [t for t in idiot.tags if t in available_std_tags]
    arbitrary_frames = [f for f in idiot.mut.tags.values()
                        if type(f) not in available_std_frames]
    arbitrary_tags = [t for t in idiot.tags
                      if t not in available_std_tags]

    # assert there's a corresponding tag for each frame
    for frame in std_frames:
        assert combined_frame_dicts[type(frame)] in std_tags

    # come up with a way to test tranfer or arbitrary frames
    # might be very hard to do as we are deliberately dropping some
    # (any other than APIC actually?)
    # for frame in arbitrary_frames:
    #     assert combined_frame_dicts[type(frame)] in arbitrary_tags

    # assert len(std_tags) == len(std_frames)
    # assert len(arbitrary_tags) == len(arbitrary_frames)

    # arbitrary tags
    for frame in idiot.mut.tags.getall('TXXX'):
        assert frame.desc in idiot.tags


def test_imported_tag_types(idiot):
    # assert no wrongly named tag keys
    assert '' not in idiot.tags.keys()

    # text frames
    assert type(idiot.tags['artist']) is str
    # time frames
    assert type(idiot.tags['year']) is str
    # url frames
    assert type(idiot.tags['wwwcopyright']) is str
