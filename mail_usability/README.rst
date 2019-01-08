# Mail Usability

Take back the control on your email

## Feature

- do not follow automatically a object when sending an email
- add the option 'All Messages Except Notifications' on partner and use it by default to avoid sending unwanted mail to partner
- better email preview, allow to select between the whole database object and not only the last 10
- use a light template version for notification without link (link should be explicit)
- add some additional style in the white list when santizing html field (see tools.py)
- make the email template by default not 'auto_delete'

## TIPS

Never, never tick the 'auto_delete' on mail template because it fucking hard to debug
and understand what have been sent (we should create a module with a crontask, that drop them latter)

If the template of mail do not look like the same when saving it in odoo, maybe the sanitize style have drop some balise
please run odoo with "LOG_STYLE_SANITIZE=True odoo" to understand what have been drop, magic warning logger will tell you everthing
