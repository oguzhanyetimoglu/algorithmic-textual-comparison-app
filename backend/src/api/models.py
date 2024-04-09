from django.db import models


class CreatedAtUpdatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NAICSCode(models.Model):
    naics_code = models.PositiveIntegerField(blank=True,
                                             db_index=True,
                                             null=True,
                                             unique=True)
    description = models.CharField(db_index=True, max_length=1000, null=True)


class SICCode(models.Model):
    sic_code = models.PositiveIntegerField(blank=True,
                                           db_index=True,
                                           null=True,
                                           unique=True)
    office = models.CharField(db_index=True, max_length=1000, null=True)
    industry_title = models.CharField(db_index=True,
                                      max_length=1000,
                                      null=True)


class TenK(models.Model):
    is_active = models.BooleanField(blank=True,
                                    db_index=True,
                                    default=True,
                                    null=True)
    cik = models.PositiveIntegerField(blank=True, db_index=True, null=True)
    trading_symbol = models.CharField(blank=True,
                                      db_index=True,
                                      max_length=20,
                                      null=True)
    company = models.CharField(blank=True, max_length=500, null=True)
    exchange = models.CharField(blank=True,
                                db_index=True,
                                max_length=50,
                                null=True)
    filing_date = models.DateField(blank=True, db_index=True, null=True)
    currency = models.CharField(blank=True,
                                db_index=True,
                                max_length=20,
                                null=True)
    filing_type = models.CharField(blank=True,
                                   db_index=True,
                                   max_length=10,
                                   null=True)
    period_of_report = models.DateField(blank=True, db_index=True, null=True)
    sic = models.IntegerField(blank=True, db_index=True, null=True)
    state_of_inc = models.CharField(blank=True,
                                    db_index=True,
                                    max_length=100,
                                    null=True)
    content = models.TextField(blank=True, null=True)
    state_location = models.CharField(blank=True,
                                      db_index=True,
                                      max_length=100,
                                      null=True)
    fiscal_year_end = models.CharField(blank=True,
                                       db_index=True,
                                       max_length=4,
                                       null=True)
    filing_html_index = models.URLField(blank=True, null=True)
    htm_filing_link = models.URLField(blank=True, null=True)
    complete_text_filing_link = models.URLField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    item_1 = models.TextField(blank=True, null=True)
    item_1A = models.TextField(blank=True, null=True)
    item_1B = models.TextField(blank=True, null=True)
    item_2 = models.TextField(blank=True, null=True)
    item_3 = models.TextField(blank=True, null=True)
    item_4 = models.TextField(blank=True, null=True)
    item_5 = models.TextField(blank=True, null=True)
    item_6 = models.TextField(blank=True, null=True)
    item_7 = models.TextField(blank=True, null=True)
    item_7A = models.TextField(blank=True, null=True)
    item_8 = models.TextField(blank=True, null=True)
    item_9 = models.TextField(blank=True, null=True)
    item_9A = models.TextField(blank=True, null=True)
    item_9B = models.TextField(blank=True, null=True)
    item_10 = models.TextField(blank=True, null=True)
    item_11 = models.TextField(blank=True, null=True)
    item_12 = models.TextField(blank=True, null=True)
    item_13 = models.TextField(blank=True, null=True)
    item_14 = models.TextField(blank=True, null=True)
    item_15 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'TenK({", ".join(f"{field.name}={getattr(self, field.name)}" for field in TenK._meta.fields)})'

    class Meta:
        unique_together = (('cik', 'filing_date'),)

class TenKFileUpload(CreatedAtUpdatedAtMixin):
    is_in_db = models.BooleanField(blank=False,
                                   db_index=True,
                                   default=False,
                                   null=False)
    file = models.FileField(upload_to='tenk_files/')
