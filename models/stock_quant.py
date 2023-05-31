from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_id = fields.Many2one('product.product', string='Product')
    volume = fields.Float(string='Thể tích', related='product_id.volume')
    volume_prod = fields.Float(
        'Thể tích của lô',
        compute='_compute_volume_lot')

    @api.depends('volume', 'quantity')
    def _compute_volume_lot(self):
        for volume in self:
            volume.volume_prod = volume.volume * volume.quantity


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location')
    volume = fields.Float(string='Volume', related='product_id.volume')
    volume_free = fields.Float('Volume Free', related='location_dest_id.volume_free')
    volume_lot = fields.Float('Volume of Lot', compute='_count_volume_lot')
    check_capacity = fields.Boolean('Check Capacity', default=False, readonly=True)
    number = fields.Integer('Number', default='1', readonly=True)

    @api.depends('qty_done')
    def _count_volume_lot(self):
        for volume in self:
            volume.volume_lot = volume.volume * volume.qty_done

    @api.onchange('volume_lot','volume_free')
    def onchange_volume_lot(self):
        for volume in self:
            message = _(
                'Lô hàng của bạn vượt quá sức chứa của kho '
                '"%s".'
                'Vui lòng chọn địa điểm lưu trữ khác.')
            if volume.volume_lot <= volume.volume_free:
                volume.check_capacity = True

            else:
                volume.check_capacity = False
                raise ValidationError(message % volume.location_dest_id.name)






