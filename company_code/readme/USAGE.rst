To display your company code in with `name_get()` just 
produce this code in your custom according your model


```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        return self.env['res.company']._add_company_code(super())
```
