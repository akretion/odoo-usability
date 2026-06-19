# Copyright 2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Profile by Akretion',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Base module set selected by Alexis de Lattre',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        # PARTNER
        'partner_firstname',  # OCA/partner-contact
        'partner_email_duplicate_warn',  # OCA/partner-contact
        'partner_mobile_duplicate_warn',  # OCA/partner-contact
        'contacts',  # official addons
        # AUTH
        'auth_admin_passkey',  # OCA/server-auth
        # REMOVE or FIX BAD NATIVE STUFF
        'disable_odoo_online',  # OCA/server-brand
        'remove_odoo_enterprise',  # OCA/server-brand
        'mail_debrand',   # OCA/mail
        'partner_disable_gravatar',  # OCA/partner-contact
        'base_technical_features',  # OCA/server-ux
        ### WEB
        'web_responsive',  # OCA/web
        'web_environment_ribbon',  # OCA/web
        'web_no_bubble',  # OCA/web
        'web_dialog_size',  # OCA/web
        'web_chatter_position',  # OCA/web
        'web_refresher',  # OCA/web
         ### MISC
        'base_usability_akretion',  # akretion/odoo-usability
        'mail_usability_akretion',  # akretion/odoo-usability
        'eradicate_quick_create',  # akretion/odoo-usability
        'base_company_extension',  # akretion/odoo-usability
        'password_security',  # OCA/server-auth
        ],
    'installable': True,
}
