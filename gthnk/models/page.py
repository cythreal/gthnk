# -*- coding: utf-8 -*-
# gthnk (c) 2014-2016 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from .. import db
from PIL import Image


class Page(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    sequence = db.Column(db.Integer)
    binary = db.Column(db.Binary)
    title = db.Column(db.Unicode(1024))
    thumbnail = db.Column(db.Binary)
    preview = db.Column(db.Binary)
    extension = db.Column(db.String(32))

    def set_image(self, binary):
        self.binary = binary
        with Image(self.binary) as img:
            self.extension = img.format.lower()

            # flatten image
            flattened = img.copy().convert("RGB")

            # flattened = Image(background=Color("white"),
            #     height=img.height, width=img.width)
            # flattened.composite(img, left=0, top=0)
            # flattened.format = "jpeg"
            # flattened.compression_quality = 50

            # create 150x200 thumbnail
            size = (150, 200)
            thumb = flattened.copy()
            thumb.thumbnail(size)
            thumb_buf = StringIO.StringIO()
            thumb.save(thumb_buf, "JPEG")
            self.thumbnail = thumb_buf.getvalue()

            # thumbnail = flattened.clone()
            # thumbnail.transform(resize='150x200>')
            # self.thumbnail = thumbnail.make_blob()

            # create preview
            size = (612, 792)
            preview = flattened.copy()
            preview.thumbnail(size)
            preview_buf = StringIO.StringIO()
            preview.save(preview_buf, "JPEG")
            self.preview = preview_buf.getvalue()

            # preview = flattened.clone()
            # preview.gaussian_blur(radius=1, sigma=0.5)
            # preview.transform(resize='612x792>')
            # self.preview = preview.make_blob()

        # write to DB
        self.save()

    def filename(self, extension=None):
        if not extension:
            extension = self.extension
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, extension)

    def content_type(self):
        if self.extension == 'pdf':
            return 'application/pdf'
        elif self.extension == 'gif':
            return 'image/gif'
        elif self.extension == 'png':
            return 'image/png'
        elif self.extension == 'jpg':
            return 'image/jpeg'

    def __repr__(self):
        if self.sequence is not None:
            return '<Page filename: %s-%d.pdf>' % (self.day.date, self.sequence)
        else:
            return '<Page filename: %s-xxx.pdf>' % (self.day.date)

    def __unicode__(self):
        return repr(self)
