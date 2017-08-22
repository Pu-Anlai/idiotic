from mutagen import id3 as mutid3


class Id3(object):
    """Wraps mutagen's id3 class as a simple dictionary, which is stored as the
    'tags' attribute. This mimics the behavior of mutagen's flac, ogg…
    classes."""

    def __init__(self, filepath, lang=None, encoding=None):
        super().__init__()
        self.lang = lang or 'eng'
        self.encoding = encoding or 3
        self.mut = mutid3.ID3FileType(filepath)
        self.text_frames = {
            mutid3.TALB: 'album',
            mutid3.TBPM: 'bpm',
            mutid3.TCOM: 'composer',
            mutid3.TCOP: 'copyright',
            mutid3.TDAT: 'date',
            mutid3.TDLY: 'audiodelay',
            mutid3.TENC: 'encodedby',
            mutid3.TEXT: 'lyricist',
            mutid3.TFLT: 'filetype',
            mutid3.TIME: 'time',
            mutid3.TIT1: 'grouping',
            mutid3.TIT2: 'title',
            mutid3.TIT3: 'version',
            mutid3.TKEY: 'initialkey',
            mutid3.TLAN: 'language',
            mutid3.TLEN: 'audiolength',
            mutid3.TMED: 'mediatype',
            mutid3.TMOO: 'mood',
            mutid3.TOAL: 'originalalbum',
            mutid3.TOFN: 'filename',
            mutid3.TOLY: 'author',
            mutid3.TOPE: 'originalartist',
            mutid3.TORY: 'originalyear',
            mutid3.TOWN: 'fileowner',
            mutid3.TPE1: 'artist',
            mutid3.TPE2: 'albumartist',
            mutid3.TPE3: 'conductor',
            mutid3.TPE4: 'arranger',
            mutid3.TPOS: 'discnumber',
            mutid3.TPRO: 'producednotice',
            mutid3.TPUB: 'organization',
            mutid3.TRCK: 'track',
            mutid3.TRDA: 'recordingdates',
            mutid3.TRSN: 'radiostationname',
            mutid3.TRSO: 'radioowner',
            mutid3.TSIZ: 'audiosize',
            mutid3.TSOA: 'albumsortorder',
            mutid3.TSOP: 'performersortorder',
            mutid3.TSOT: 'titlesortorder',
            mutid3.TSRC: 'isrc',
            mutid3.TSSE: 'encodingsettings',
            mutid3.TSST: 'setsubtitle',
            mutid3.TYER: 'year'}
        self.time_frames = {
            mutid3.TDEN: 'encodingtime',
            mutid3.TDOR: 'originalreleasetime',
            mutid3.TDRC: 'year',
            mutid3.TDRL: 'releasetime',
            mutid3.TDTG: 'taggingtime'}
        self.url_frames = {
            mutid3.WCOP: 'wwwcopyright',
            mutid3.WOAF: 'wwwfileinfo',
            mutid3.WOAS: 'wwwsource',
            mutid3.WORS: 'wwwradio',
            mutid3.WPAY: 'wwwpayment',
            mutid3.WPUB: 'wwwpublisher'}
        self.tags = self._get_tag_dictionary(self.mut)


        # TODO: Go through the mutagen id3 frames and populate the dictionary.

    def _get_tag_dictionary(self, mut):
        tag_dict = {}
        for frame in mut.tags.values():
            # try for text frames
            try:
                plain_tag = self.text_frames[type(frame)]
                tag_content_list = frame.text
                tag_dict[plain_tag] = ';; '.join(tag_content_list)
                continue
            except KeyError:
                pass

            # try for time frames
            try:
                plain_tag = self.time_frames[type(frame)]
                tag_content_list = [time.text for time in frame.text]
                tag_content = ';; '.join(tag_content_list)
                tag_dict[plain_tag] = tag_content
                continue
            except KeyError:
                pass

            # try for url frames
            try:
                plain_tag = self.url_frames[type(frame)]
                tag_content = frame.url
                tag_dict[plain_tag] = tag_content
                continue
            except KeyError:
                pass

            # TODO: handle frames that allow duplicates: TXXX, WXXX,
            # uurl_frames

        return tag_dict
