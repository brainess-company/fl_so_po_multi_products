# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api

class SelectProducts(models.TransientModel):
    _name = 'select.products'
    _description = 'Select Products'

    product_lines = fields.One2many('select.products.line', 'wizard_id', string='Products')
    flag_order = fields.Char('Flag Order')

    def select_products(self):
        if self.flag_order == 'so':
            order_id = self.env['sale.order'].browse(self._context.get('active_id', False))
            for line in self.product_lines:
                self.env['sale.order.line'].create({
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.price_unit,
                    'product_uom_qty': line.quantity,
                    'order_id': order_id.id
                })
        elif self.flag_order == 'po':
            order_id = self.env['purchase.order'].browse(self._context.get('active_id', False))
            for line in self.product_lines:
                product_name = line.product_id.display_name
                if line.product_id.description_purchase:
                    product_name += '\n' + line.product_id.description_purchase
                self.env['purchase.order.line'].create({
                    'product_id': line.product_id.id,
                    'name': product_name,
                    'date_planned': order_id.date_planned or datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'product_uom': line.product_id.uom_po_id.id if line.product_id.uom_po_id else line.product_id.uom_id.id,
                    'price_unit': line.price_unit,
                    'product_qty': line.quantity,
                    'display_type': False,
                    'order_id': order_id.id
                })


class SelectProductsLine(models.TransientModel):
    _name = 'select.products.line'
    _description = 'Select Products Line'

    wizard_id = fields.Many2one('select.products', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=lambda self: self.product_id.lst_price)
