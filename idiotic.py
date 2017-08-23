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

    def _get_tag_dictionary(self, mut):
        tag_dict = {}
        for frame in mut.tags.values():
            # try for text frames
            try:
                self._populate_text_tags(mut, tag_dict, frame)
                continue
            except KeyError:
                pass

            # try for time frames
            try:
                self._populate_time_tags(mut, tag_dict, frame)
                continue
            except KeyError:
                pass

            # try for url frames
            try:
                self._populate_url_tags(mut, tag_dict, frame)
                continue
            except KeyError:
                pass

            # try for genre frame
            try:
                self._populate_genre_tag(mut, tag_dict, frame)
            except AssertionError:
                pass

        self._populate_comment_tag(mut, tag_dict)
        self._populate_arbitrary_tags(mut, tag_dict, 'TXXX', 'text')
        self._populate_arbitrary_tags(mut, tag_dict, 'WXXX', 'url')

        return tag_dict

    # TODO: handle uurl_frames and other irregular frames (cf. puddletag)
    # don't forget about __ tags when converting back to mutagen

    def _populate_text_tags(self, mut, tag_dict, frame):
        plain_tag = self.text_frames[type(frame)]
        tag_dict[plain_tag] = ' ;; '.join(frame.text)

    def _populate_time_tags(self, mut, tag_dict, frame):
        plain_tag = self.time_frames[type(frame)]
        tag_content_list = [time.text for time in frame.text]
        tag_content = ' ;; '.join(tag_content_list)
        tag_dict[plain_tag] = tag_content

    def _populate_url_tags(self, mut, tag_dict, frame):
        plain_tag = self.url_frames[type(frame)]
        tag_dict[plain_tag] = frame.url

    def _populate_genre_tag(self, mut, tag_dict, frame):
        # pseudo-"if" for unified EAFP-approach
        assert type(frame) is mutid3.TCON
        tag_dict['genre'] = ' ;; '.join(frame.genres)

    def _populate_comment_tag(self, mut, tag_dict):
        for frame in mut.tags.getall('COMM'):
            if frame.desc == '':
                tag_dict['comment'] = ' ;; '.join(frame.text)
            else:
                tag_name = 'comment' + '__' + frame.desc
                tag_dict[tag_name] = ' ;; '.join(frame.text)

    def _populate_arbitrary_tags(self, mut, tag_dict,
                                 base_frame, content_field):
        """Add non-standardized tags to $tag_dict."""
        for frame in mut.tags.getall(base_frame):
            if frame.desc not in tag_dict.keys():
                content_list = getattr(frame, content_field)
                tag_dict[frame.desc] = ' ;; '.join(content_list)
            else:
                tag_name = frame.FrameID + '__' + frame.desc
                tag_dict[tag_name] = ' ;; '.join(frame.text)
