##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016, 2025 XCG Consulting <https://xcg-consulting.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
from collections.abc import Mapping
from typing import Any

from odoo import models  # type: ignore[import-untyped]
from odoo.addons.converter import Converter
from odoo.tools.mimetypes import guess_mimetype  # type: ignore[import-untyped]


def image(value: bytes):
    # get MIME type associated with the decoded_data.
    image_base64 = base64.b64decode(value)
    mimetype = guess_mimetype(image_base64)
    return {"body": value.decode("ascii"), "mime-type": mimetype}


class ImageFile(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(
        self, instance: models.Model, ctx: Mapping | None = None
    ) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return {}

        return image(value)


class ImageDataURL(Converter):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def odoo_to_message(
        self, instance: models.Model, ctx: Mapping | None = None
    ) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return ""

        content = base64.b64decode(value)
        mimetype = guess_mimetype(content)

        return "data:{};base64,{}".format(mimetype, value.decode("ascii"))
