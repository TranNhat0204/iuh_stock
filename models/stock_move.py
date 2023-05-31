from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class ModelName(models.Model):
    _inherit = 'stock.move'

    product_id = fields.Many2one('product.product', string='Product')
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location')
    reserved_volume = fields.Float(string='Reserved Volume', compute='_count_volume_reserved')
    volume_lot = fields.Float('Volume of Lot', compute='_count_volume_lot')
    volume = fields.Float(string='Volume', related='product_id.volume')
    volume_free = fields.Float('Volume Free', compute='_count_volume_free')
    total_line = fields.Integer('Total line', compute='_count_line')
    total_capacity = fields.Integer('Total line capacity', compute='_count_line_capacity')
    check_button = fields.Boolean('Check Button', default=False, readonly=True)

    @api.onchange('total_line','total_capacity')
    def onchange_total_line(self):
        for line in self:
            message = _(
                'Lô hàng của bạn vượt quá sức chứa của kho '
                'Vui lòng chọn địa điểm lưu trữ khác!!!')
            if line.total_line == line.total_capacity:
                line.check_button = True

            else:
                line.check_button = False
                UserError(message)

    @api.depends('reserved_availability')
    def _count_volume_reserved(self):
        for volume in self:
            volume.reserved_volume = volume.volume * volume.reserved_availability

    @api.depends('quantity_done')
    def _count_volume_lot(self):
        for volume in self:
            volume.volume_lot = volume.volume * volume.quantity_done

    @api.depends('move_line_nosuggest_ids.volume_free')
    def _count_volume_free(self):
        for volume in self:
            volume.volume_free = volume.move_line_nosuggest_ids.volume_free

    @api.depends('move_line_nosuggest_ids.number')
    def _count_line(self):
        for rec in self:
            rec.total_line = sum(rec.move_line_nosuggest_ids.mapped('number'))

    @api.depends('move_line_nosuggest_ids.check_capacity')
    def _count_line_capacity(self):
        for rec in self:
            rec.total_capacity = sum(rec.move_line_nosuggest_ids.mapped('check_capacity'))


