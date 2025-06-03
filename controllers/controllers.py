# -*- coding: utf-8 -*-
# from odoo import http


# class PruebaModulo(http.Controller):
#     @http.route('/prueba_modulo/prueba_modulo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prueba_modulo/prueba_modulo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('prueba_modulo.listing', {
#             'root': '/prueba_modulo/prueba_modulo',
#             'objects': http.request.env['prueba_modulo.prueba_modulo'].search([]),
#         })

#     @http.route('/prueba_modulo/prueba_modulo/objects/<model("prueba_modulo.prueba_modulo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prueba_modulo.object', {
#             'object': obj
#         })
