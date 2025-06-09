from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Prestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Préstamo de libro'
    _order = 'fecha_prestamo desc'
    
    name = fields.Char(string='Referencia', readonly=True, default='Nuevo')
    libro_id = fields.Many2one(
        'biblioteca.libro', string='Libro', required=True,
        domain="[('estado','=','disponible')]")
    partner_id = fields.Many2one(
        'res.partner', string='Usuario', required=True)
    fecha_prestamo = fields.Date(
        string='Fecha de préstamo', default=fields.Date.today)
    fecha_devolucion = fields.Date(string='Fecha de devolución')
    fecha_devolucion_esperada = fields.Date(
        string='Fecha esperada de devolución', compute='_compute_fecha_devolucion_esperada',
        store=True)
    estado = fields.Selection([
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
        ('perdido', 'Perdido')],
        string='Estado', default='prestado')
    notas = fields.Text(string='Notas')
    dias_prestamo = fields.Integer(
        string='Días de préstamo', default=15)
    
    @api.depends('fecha_prestamo', 'dias_prestamo')
    def _compute_fecha_devolucion_esperada(self):
        for prestamo in self:
            if prestamo.fecha_prestamo:
                prestamo.fecha_devolucion_esperada = prestamo.fecha_prestamo + timedelta(days=prestamo.dias_prestamo)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('biblioteca.prestamo') or 'Nuevo'
            
            # Cambiar estado del libro a prestado
            libro = self.env['biblioteca.libro'].browse(vals.get('libro_id'))
            libro.write({'estado': 'prestado'})
        
        return super().create(vals_list)
    
    def write(self, vals):
        if 'estado' in vals and vals['estado'] == 'devuelto':
            vals['fecha_devolucion'] = fields.Date.today()
            for prestamo in self:
                prestamo.libro_id.write({'estado': 'disponible'})
        return super().write(vals)
    
    @api.onchange('libro_id')
    def _onchange_libro(self):
        if self.libro_id:
            return {'warning': {
                'title': _("Información del libro"),
                'message': _("Asegúrese de que el libro esté en buen estado antes del préstamo.")}}
    
    @api.constrains('fecha_prestamo', 'fecha_devolucion')
    def _check_fechas(self):
        for prestamo in self:
            if prestamo.fecha_devolucion and prestamo.fecha_devolucion < prestamo.fecha_prestamo:
                raise ValidationError(_('La fecha de devolución no puede ser anterior a la fecha de préstamo.'))
    
    def action_marcar_devuelto(self):
        self.write({'estado': 'devuelto', 'fecha_devolucion': fields.Date.today()})
    
    def action_marcar_retrasado(self):
        self.write({'estado': 'retrasado'})