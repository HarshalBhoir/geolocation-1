# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta

import googlemaps
from datetime import datetime


class CRMSalesPersonGeolocation(models.Model):
    _name = 'crm.salesperson.geolocation'
    _description = 'CRM SalesPerson Geolocation'
    _rec_name = 'name'

    name = fields.Char('Name')
    counter = fields.Integer('Counter', default=0)
    mode = fields.Selection([('transit', 'Transit')], string="Mode", default='transit')
    longitude = fields.Float('Longitude', help='Longitude of Current Position')
    latitude = fields.Float('Latitude', help='Lattitude of Current Position')


class salesdsr(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char('Opportunity', required=False, default='New Lead')  # to make name field not required

    agency = fields.Many2one('res.partner', 'Agency')
    product = fields.Many2one('product.product', 'Product')

    type = fields.Selection(selection_add=[('dsr', 'DSR')])
    date = fields.Date('Date', default=datetime.now().strftime('%Y-%m-%d'))
    task = fields.Char('Task', track_visibility='onchange')
    unit_time = fields.Float('Hours', help="Total Time Consume in current Activity")

    # for kms
    kms = fields.Integer('KMS', compute='_compute_kms', help='Total Distance Covered')
    location = fields.Many2many('crm.salesperson.geolocation', string='Location', help='Location of SalesPerson at specified time')

    @api.one
    @api.onchange('location')
    def _compute_kms(self):
        api_key = self.env['res.config.settings'].geolocation_api  # recheck configure it
        gmaps = googlemaps.Client(key=api_key)
        now = datetime.now()
        distance = 0.0
        records = self.location
        if len(records) < 2 or records[1].longitude == 0:
            return
        orig_coord = str(records[0].latitude) + ',' + str(records[0].longitude)
        for record in records[1:]:
            dest_coord = str(record.latitude) + ',' + str(record.longitude)
            directions_result = gmaps.distance_matrix(orig_coord, dest_coord,
                                        mode="driving",
                                        avoid="ferries",
                                        departure_time=now
                                        )
            driving_distance = directions_result['rows'][0]['elements'][0]['distance']['value']
            orig_coord = dest_coord 
            distance += driving_distance
        self.kms = distance / 1000.0

    @api.one
    def update_location(self, latitude=0.0, longitude=0.0, record=None):
        if record:
            rec = self.location.browse(record)
            if rec.counter == 0:
                rec.write({'latitude': latitude, 'longitude': longitude, 'counter': 1})
