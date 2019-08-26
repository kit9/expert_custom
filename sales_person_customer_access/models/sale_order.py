# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    salesperson_ids = fields.Many2many(
        'res.users',
        string="Salespersons"
    )

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        res = super(SaleOrder, self).onchange_partner_shipping_id()
        if self.partner_id.salesperson_ids:
            self.salesperson_ids=[(6, 0, self.partner_id.salesperson_ids.ids)]
        else:
            self.salesperson_ids=[]

    @api.multi
    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        result.update({'salesperson_ids': [(6, 0, self.salesperson_ids.ids)]})
        return result

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        res.update({'salesperson_ids': [(6, 0, sale_orders.salesperson_ids.ids)]})
        return res
