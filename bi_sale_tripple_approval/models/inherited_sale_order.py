# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models,api, _
import datetime

class SaleOrder(models.Model):

	_inherit = 'sale.order'

	state = fields.Selection([
		('draft', 'Quotation'),
		('sent', 'Quotation Sent'),
		('approve','To Approval'),
		('second_approve','Finance Approval'),
		('third_approve','Director Approval'),
		('sale', 'Sales Order'),
		('done', 'Locked'),
		('cancel', 'Cancelled'),
		], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
	
	sale_department_manager_id = fields.Many2one('res.users',string="Sales Department Manager")
	finance_manager_id = fields.Many2one('res.users',string="Finance Manager")
	sale_director_id = fields.Many2one('res.users',string="Director Manager")
	sale_manager_approval_date = fields.Datetime(string="Manager Approval Date")
	finance_manager_id_approval_date = fields.Datetime(string="Finance Manager Approval Date")
	sale_director_id_approval_date = fields.Datetime(string="Director Manager Approval Date")
	refused_by_id = fields.Many2one('res.users',string="Refused By")
	refause_date = fields.Datetime(string="Refused Date")
	sale_manager = fields.Boolean(string="Manager",default=False)
	finance_manager =fields.Boolean(string="finance",default=False)
	sale_director = fields.Boolean(string="director",default=False)
	refuse_reason = fields.Char(string="Refuse Reason")


	


	@api.multi
	def action_refause(self):
		template_id = self.company_id.sale_refuse_email_temp_id
		self.refused_by_id = self.user_id
		self.refause_date = datetime.datetime.now()
		if template_id.id :
			template_id.send_mail(self.id, force_send=True)
		return self.write({'state': 'cancel'})


	@api.multi
	def action_confirm(self):
		for order in self :
			if order.company_id.three_step_approval == True and order.amount_total > order.company_id.so_double_validation_amount :
				order.write({
				'state': 'approve','sale_manager':True,'sale_manager_approval_date':datetime.datetime.now()})
				
				template_id = order.company_id.sale_approval_email_temp_id
				if template_id.id :

					send = template_id.send_mail(order.id, force_send=True)
					
			else :
				self._action_confirm()
				if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
					self.action_done()
			   
		return True

	@api.multi	
	def action_first_approve(self):
		if self.amount_total > self.company_id.so_double_validation_amount :
			self.write({'state':'second_approve','finance_manager':True,'sale_manager_approval_date':datetime.datetime.now()})
			template_id = self.company_id.sale_finance_approval_email_temp_id
			if template_id.id :
				send = template_id.send_mail(self.id, force_send=True)
		else :
			self._action_confirm()
			if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
				self.action_done()
		return True

	@api.multi	
	def action_second_approve(self):
		if self.amount_total > self.company_id.finance_validation_amount :
			self.write({'state':'third_approve','sale_director':True,'finance_manager_id_approval_date':datetime.datetime.now()})
			template_id = self.company_id.sale_director_approval_email_temp_id
			if template_id.id :
				send = template_id.send_mail(self.id, force_send=True)
		else :
			self._action_confirm()
			if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
				self.action_done()
		return True

	@api.multi	
	def action_third_approve(self): 
		self._action_confirm()
		self.sale_director_id_approval_date = datetime.datetime.now()
		if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
			self.action_done()
		return True


	