# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models

class Company(models.Model):
	_inherit = 'res.company'

	so_double_validation_amount = fields.Float(string="SO Double validation Amount")
	finance_validation_amount = fields.Float(string="Finance Validation Amount")
	director_validation_amount = fields.Float(string="Director Validation Amount")
	three_step_approval = fields.Boolean(string="Three Step Approval")
	sale_approval_email_temp_id = fields.Many2one('mail.template',string="Sale Manager Approval Email Template")
	sale_finance_approval_email_temp_id = fields.Many2one('mail.template',string="Finance Manager Approval Email Template")
	sale_director_approval_email_temp_id = fields.Many2one('mail.template',string="Director  Approval Email Template")
	sale_refuse_email_temp_id = fields.Many2one('mail.template',string="Sale Refuse Email Template")