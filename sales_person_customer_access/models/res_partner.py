# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    salesperson_ids = fields.Many2many(
        'res.users',
        string="Salespersons"
    )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        restricted_customer = self.env.user.has_group('sales_person_customer_access.group_restricted_customer')
        if restricted_customer:
            args = [('salesperson_ids','in',self.env.user.id)] + list(args)
        return super(ResPartner, self)._search(args, offset, limit, order, count, access_rights_uid)
