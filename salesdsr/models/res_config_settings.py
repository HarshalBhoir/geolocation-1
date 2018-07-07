# -*- coding: utf:8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    geolocation_api = fields.Char('GeoLocation API Key', help="Geolocation API Key for integration of Distance Matrix API with SalesDSR.")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            geolocation_api=self.env['ir.config_parameter'].sudo().get_param('geolocation_api'),
        )
        return res
        
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('geolocation_api', self.geolocation_api)


