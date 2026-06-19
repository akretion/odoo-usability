# Copyright 2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Profile for France',
    'version': '18.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Module set for accounting for a French company',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        ### MISC
        'date_range_account',  # OCA/server-ux
        'account_usability_akretion',  # akretion/odoo-usability
        'account_usability',  # OCA/account-financial-tools
        'l10n_fr_siret_lookup',  # OCA/l10n-france
        'account_payment_base_oca',  # OCA/bank-payment-alternative
        'account_move_name_sequence',  # OCA/account-financial-tools
        'account_lock_date_update',  # OCA/account-financial-tools
        'account_move_csv_import',  # akretion/account-move-import
        'account_move_line_reconcile_manual',  # OCA/account-reconcile
        'account_dashboard_banner',  # OCA/account-financial-tools
        ### INVOICING
        'account_fiscal_position_vat_check',  # OCA/account-financial-tools
        'account_invoice_facturx',  # OCA/edi
        ### FINANCIAL REPORTS
        'account_financial_report',  # OCA/account-financial-reporting
        'account_balance_ebp_csv_export',  # OCA/l10n-france
        # 'l10n_fr_mis_reports',  # OCA/l10n-france
        'l10n_fr_fec_oca',  # OCA/l10n-france
        ### BANK STATEMENTS
        'account_statement_completion_label_simple',  # akretion/bank-statement-reconcile-simple
        #'account_statement_completion_label_simple_sale',  # akretion/bank-statement-reconcile-simple
        'account_statement_import_file_reconcile_oca',  # OCA/bank-statement-import
        'account_statement_import_ofx',  # OCA/bank-statement-import
        'account_statement_import_fr_cfonb',  # OCA/l10n-france
        # 'account_statement_import_api_qonto',  # akretion/bank-statement-import-api
        # 'account_statement_import_api_bridge',  # akretion/bank-statement-import-api
        'account_reconcile_oca',  # OCA/account-reconcile
        'account_reconcile_oca_add_default_filters',  # OCA/account-reconcile
        'account_reconcile_oca_usability_akretion',  # akretion/odoo-usability
        ### CURRENCY RATES
        'currency_rate_update',  # OCA/currency
        'currency_old_rate_notify',  # OCA/currency
        ### INVOICE IMPORT
        'l10n_fr_business_document_import',  # OCA/l10n-france
        'account_invoice_import_simple_pdf',  # OCA/edi
        'account_invoice_import_ubl',  # OCA/edi
        'l10n_fr_account_invoice_import_facturx',  # OCA/l10n-france
        ### OVERDUE
        'account_invoice_overdue_warn',  # OCA/credit-control
        #'account_invoice_overdue_warn_sale',  # OCA/credit-control
        'account_invoice_overdue_reminder',  # OCA/credit-control
        ### FRENCH DECLARATIONS
        'l10n_fr_account_vat_return_teledec',  # OCA/l10n-france
        'l10n_fr_account_vat_return_einvoice_generate',  # OCA/l10n-france
        # 'intrastat_product' depends on 'sale_stock' and 'purchase_stock', so I don't add
        # as a depend on this module
        # 'l10n_fr_intrastat_product',  # OCA/l10n-france
        # 'product_net_weight',  # OCA/product-attribute
        'l10n_fr_intrastat_service',  # OCA/l10n-france
        'l10n_fr_das2',  # OCA/l10n-france
        # ANALYTIC
        #'account_analytic_distribution_manual',  # OCA/account-analytic
        ### INVOICE IMPORT
        #'account_invoice_download_ovh',  # OCA/edi
        #'account_invoice_download_scaleway',  # OCA/edi
        ### PAYMENT ORDERS and DEBIT ORDERS
        #'partner_bank_acc_type_constraint',  # OCA/partner-contact
        #'account_payment_base_oca_sale',  # OCA/bank-payment-alternative
        #'account_payment_sepa_credit_transfer',  # OCA/bank-payment-alternative
        #'account_payment_sepa_direct_debit',  # OCA/bank-payment-alternative
        #'account_payment_batch_oca_reconcile',  # OCA/bank-payment-alternative
        #'account_payment_fr_lcr',  # OCA/l10n-france
        #'l10n_fr_account_payment_intl_credit_transfer',  # OCA/l10n-france
        ### PY3O
        #'account_invoice_facturx_py3o',  # OCA/edi
        ### CHORUS
        #'l10n_fr_chorus_account',  # OCA/l10n-france
        #'l10n_fr_chorus_sale',  # OCA/l10n-france
        #'l10n_fr_chorus_facturx',  # OCA/l10n-france
        ### CUTOFF
        #'account_cutoff_start_end_dates',  # OCA/account-closing
        #'account_cutoff_picking',  # OCA/account-closing
        #'account_cutoff_accrual_subscription',  # OCA/account-closing
        ### MISC
        #'account_check_deposit',  # OCA/account-financial-tools
        #'account_cash_deposit',  # OCA/account-financial-tools
        #'account_invoice_pricelist',  # OCA/account-invoicing
        #'account_asset_management',  # OCA/account-financial-tools
        ### MOONCARD
        #'mooncard_payment_card',  # akretion/odoo-mooncard-connector
        #'l10n_fr_base_newgen_payment_card',  # akretion/odoo-mooncard-connector
        #'base_newgen_payment_card_start_end_dates',  # akretion/odoo-mooncard-connector
        ],
    'excludes': [
        #'l10n_fr_fec',
        'account_edi_ubl_cii',
        ],
    'installable': True,
}
