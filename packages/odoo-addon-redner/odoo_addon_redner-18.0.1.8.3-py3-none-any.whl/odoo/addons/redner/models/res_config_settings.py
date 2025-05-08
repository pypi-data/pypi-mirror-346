##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016 XCG Consulting <https://xcg-consulting.fr>
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

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    redner_server_url = fields.Char(
        string="Redner Server URL",
        config_parameter="redner.server_url",
    )

    redner_account = fields.Char(
        string="Redner Account Name",
        config_parameter="redner.account",
    )

    redner_api_key = fields.Char(
        string="Redner API Key",
        config_parameter="redner.api_key",
    )
