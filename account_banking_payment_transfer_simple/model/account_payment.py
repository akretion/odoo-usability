# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 EduSense BV (<http://www.edusense.nl>).
#              (C) 2011 - 2013 Therp BV (<http://therp.nl>).
#              (C) 2014 ACSONE SA (<http://acsone.eu>).
#              (C) 2014 Akretion (www.akretion.com)
#
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _


class PaymentOrder(orm.Model):
    _inherit = 'payment.order'

#    @api.multi
#    def get_partial_reconcile_ids(self):
#        self.ensure_one()
#        reconcile_partial_ids = [line.move_line_id.reconcile_partial_id.id
#                                 for line in self.line_ids if
#                                 line.move_line_id.reconcile_partial_id.id]
#        return reconcile_partial_ids

#    @api.one
#    def get_partial_reconcile_count(self):
#        self.partial_reconcile_count = len(self.get_partial_reconcile_ids())

    def action_rejected(self, cr, uid, ids, context=None):
        return True

#    @api.multi
#    def action_done(self):
#        for line in self.line_ids:
#            line.date_done = fields.Date.context_today(self)
#        self.date_done = fields.Date.context_today(self)
        # state is written in workflow definition
#        return True

#    @api.multi
#    def _get_transfer_move_lines(self):
#        """
#        Get the transfer move lines (on the transfer account).
#        """
#        res = []
#        for order in self:
#            for order_line in order.line_ids:
#                move_line = order_line.transfer_move_line_id
#                if move_line:
#                    res.append(move_line)
#        return res

#    @api.multi
#    def get_transfer_move_line_ids(self, *args):
#        '''Used in the workflow for trigger_expr_id'''
#        return [move_line.id for move_line in self._get_transfer_move_lines()]

#    @api.multi
#    def test_done(self):
#        """
#        Test if all moves on the transfer account are reconciled.
#
#        Called from the workflow to move to the done state when
#        all transfer move have been reconciled through bank statements.
#        """
#        return all([move_line.reconcile_id for move_line in
#                    self._get_transfer_move_lines()])

#    @api.multi
#    def test_undo_done(self):
#        return not self.test_done()

    def _prepare_transfer_move(self, cr, uid, order, context=None):
        # TODO question : can I use self.mode.xxx in an @api.model ??
        # It works, but I'm not sure we are supposed to do that !
        # I didn't want to use api.one to avoid having to
        # do self._prepare_transfer_move()[0] in action_sent
        # I prefer to just have to do self._prepare_transfer_move()
        vals = {
            'journal_id': order.mode.transfer_journal_id.id,
            'ref': '%s %s' % (
                order.payment_order_type[:3].upper(), order.reference)
            }
        return vals

    def _prepare_move_line_transfer_account(
            self, cr, uid, order, amount, move_id, payment_lines, labels,
            context=None):
        payment_order_type = order.payment_order_type
        if len(payment_lines) == 1:
            partner_id = payment_lines[0].partner_id.id
            name = _('%s line %s') % (
                labels[payment_order_type], payment_lines[0].name)
        else:
            partner_id = False
            name = '%s %s' % (
                labels[payment_order_type], order.reference)
        vals = {
            'name': name,
            'move_id': move_id,
            'partner_id': partner_id,
            'account_id': order.mode.transfer_account_id.id,
            'credit': (payment_order_type == 'payment' and
                       amount or 0.0),
            'debit': (payment_order_type == 'debit' and
                      amount or 0.0),
            }
        return vals

    def _prepare_move_line_partner_account(
            self, cr, uid, line, move_id, labels, context=None):
        payment_order_type = line.order_id.payment_order_type
        if line.move_line_id:
            account_id = line.move_line_id.account_id.id
        else:
            if payment_order_type == 'debit':
                account_id = line.partner_id.property_account_receivable.id
            else:
                account_id = line.partner_id.property_account_payable.id
        vals = {
            'name': _('%s line %s') % (
                labels[payment_order_type], line.name),
            'move_id': move_id,
            'partner_id': line.partner_id.id,
            'account_id': account_id,
            'credit': (payment_order_type == 'debit' and
                       line.amount or 0.0),
            'debit': (payment_order_type == 'payment' and
                      line.amount or 0.0),
            }
        return vals

#    @api.model
#    def action_sent_no_move_line_hook(self, pay_line):
#        """This function is designed to be inherited"""
#        return

    def action_done(self, cr, uid, ids, context=None):
        """
        Create the moves that pay off the move lines from
        the debit order. This happens when the debit order file is
        generated.
        """
        am_obj = self.pool['account.move']
        aml_obj = self.pool['account.move.line']
        pl_obj = self.pool['payment.line']
        labels = {
            'payment': _('Payment order'),
            'debit': _('Direct debit order'),
            }
        for order in self.browse(cr, uid, ids, context=context):
            if order.mode.transfer_journal_id and order.mode.transfer_account_id:
                # prepare a dict "trfmoves" that can be used when
                # self.mode.transfer_move_option = date or line
                # key = unique identifier (date or True or line.id)
                # value = [pay_line1, pay_line2, ...]
                trfmoves = {}
                if order.mode.transfer_move_option == 'line':
                    for line in order.line_ids:
                        trfmoves[line.id] = [line]
                else:
                    if order.date_prefered in ('now', 'fixed'):
                        trfmoves[True] = []
                        for line in order.line_ids:
                            trfmoves[True].append(line)
                    else:  # date_prefered == due
                        for line in order.line_ids:
                            if line.date in trfmoves:
                                trfmoves[line.date].append(line)
                            else:
                                trfmoves[line.date] = [line]

                for identifier, lines in trfmoves.iteritems():
                    mvals = self._prepare_transfer_move(
                        cr, uid, order, context=context)
                    move_id = am_obj.create(cr, uid, mvals, context=context)
                    total_amount = 0
                    for line in lines:
                        # TODO: take multicurrency into account

                        # create the payment/debit counterpart move line
                        # on the partner account
                        partner_ml_vals = self._prepare_move_line_partner_account(
                            cr, uid, line, move_id, labels, context=context)
                        partner_move_line_id = aml_obj.create(
                            cr, uid, partner_ml_vals, context=context)
                        total_amount += line.amount

                        # register the payment/debit move line
                        # on the payment line and call reconciliation on it
                        line.write({'transit_move_line_id': partner_move_line_id})

                        if line.move_line_id:
                            pl_obj.debit_reconcile(cr, uid, line.id, context=context)
                        #else:
                        #    self.action_sent_no_move_line_hook(line)

                    # create the payment/debit move line on the transfer account
                    trf_ml_vals = self._prepare_move_line_transfer_account(
                        cr, uid, order, total_amount, move_id, lines, labels,
                        context=context)
                    aml_obj.create(cr, uid, trf_ml_vals, context=context)

                    # post account move
                    am_obj.post(cr, uid, [move_id], context=context)

            # State field is written by act_sent_wait
            order.write({'state': 'done'})
        return True

#    @api.multi
#    def partial(self):
#        self.ensure_one()
#        view_id = self.env.ref('account.view_move_line_tree').id
#        reconcile_partial_ids = self.get_partial_reconcile_ids()
#        reconcile_partial_domain = [('reconcile_partial_id', 'in',
#                                     reconcile_partial_ids)]
#        return {
#            'name': _('Partial Reconcile Moves Line'),
#            'context': self.env.context,
#            'domain': reconcile_partial_domain,
#            'view_type': 'form',
#            'view_mode': 'tree,form',
#            'res_model': 'account.move.line',
#            'views': [(view_id, 'tree')],
#            'type': 'ir.actions.act_window',
#            'target': 'current',
#        }
