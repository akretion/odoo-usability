To display your company code with `name_get()` just 
write this code in your custom code according your model


```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        return self.env['res.company']._add_company_code(super())
```
