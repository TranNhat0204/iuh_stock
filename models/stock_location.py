# from . import # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class StockLocation(models.Model):
    _inherit = 'stock.location'

    weight = fields.Float('Weight')
    allow_user_ids = fields.Many2many(
        'res.users',
        'location_security_stock_location_users',
        'location_id',
        'user_id',
        'Users Allow')
    volume_original = fields.Float('Volume of Location')
    percent_available = fields.Float('Percent available of Location')
    volume = fields.Float('Volume', compute='_compute_volume_available')
    sum_volume = fields.Float(compute='_compute_volume_prod_total', string='Volume Used')
    volume_free = fields.Float('Volume Free', compute='_compute_volume_free')
    volume_uom_name = fields.Char(string='Volume unit of measure label', compute='_compute_volume_uom_name')
    stock_quant_ids = fields.One2many(
        'stock.quant',
        'location_id',
        'Stock Quant')

    @api.depends('volume_original', 'percent_available')
    def _compute_volume_available(self):
        for volume in self:
            volume.volume = volume.volume_original * (volume.percent_available/100)

    @api.depends('stock_quant_ids.volume_prod')
    def _compute_volume_prod_total(self):
        for rec in self:
            rec.sum_volume = sum(rec.stock_quant_ids.mapped('volume_prod'))

    @api.depends('volume', 'sum_volume')
    def _compute_volume_free(self):
        for volume in self:
            volume.volume_free = volume.volume - volume.sum_volume

    @api.model
    def create(self, vals):
        res = super(StockLocation, self).create(vals)
        if res.allow_user_ids:
            res.allow_user_ids.write({
                'restrict_locations': True
            })
            group_id = self.env.ref('iuh_stock.group_restrict_warehouse')
            group_id.users = [(4, uid) for uid in res.allow_user_ids.ids]
        return res

    def write(self, vals):
        res = super(StockLocation, self).write(vals)
        if 'allow_user_ids' in vals:
            self.allow_user_ids.write({
                'restrict_locations': True
            })
            group_id = self.env.ref('iuh_stock.group_restrict_warehouse')
            group_id.users = [(4, uid) for uid in self.allow_user_ids.ids]
        return res

