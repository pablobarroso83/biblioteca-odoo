from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'
    _order = 'fecha_publicacion desc, name'
    
    name = fields.Char(string='Título', required=True)
    isbn = fields.Char(string='ISBN', help='International Standard Book Number')
    autor = fields.Char(string='Autor', required=True)
    fecha_publicacion = fields.Date(string='Fecha de publicación')
    paginas = fields.Integer(string='Número de páginas')
    editorial = fields.Char(string='Editorial')
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('perdido', 'Perdido'),
        ('reparacion', 'En reparación')],
        string='Estado', default='disponible')
    imagen = fields.Binary(string='Portada del libro')
    active = fields.Boolean(string='Activo', default=True)
    
    # Relaciones
    prestamo_ids = fields.One2many(
        'biblioteca.prestamo', 'libro_id', string='Préstamos')
    
    # Restricción para ISBN único
    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'El ISBN debe ser único para cada libro.'),
    ]
    
    @api.constrains('paginas')
    def _check_paginas(self):
        for libro in self:
            if libro.paginas <= 0:
                raise ValidationError(_('El número de páginas debe ser mayor que cero.'))
    
    def name_get(self):
        result = []
        for libro in self:
            name = f"{libro.name} ({libro.autor})"
            result.append((libro.id, name))
        return result