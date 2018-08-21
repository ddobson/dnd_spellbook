from django.core.cache import cache
from django.db import connection, models
from django.contrib.postgres.fields import ArrayField, JSONField


class Spell(models.Model):
    DISTINCT_CLASS_CACHE_KEY = "distinct_spell_classes"

    class Meta:
        ordering = ["id"]

    casting_time = models.CharField(blank=True, null=True, max_length=128)
    classes = ArrayField(
        models.CharField(max_length=24, blank=True), default=list, size=24
    )
    components = JSONField(default=dict)
    description = models.CharField(blank=True, null=True, max_length=10240)
    higher_levels = models.CharField(blank=True, null=True, max_length=1024)
    duration = models.CharField(blank=True, null=True, max_length=128)
    level = models.SmallIntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=128)
    spell_range = models.CharField(blank=True, null=True, max_length=128)
    ritual = models.BooleanField(default=False)
    school = models.CharField(blank=True, null=True, max_length=128)
    spell_type = models.CharField(blank=True, null=True, max_length=128)

    @classmethod
    def distinct_classes(cls, force=False):
        def get_distinct_classes():
            cursor = connection.cursor()
            raw_query = """SELECT UNNEST(spell_classes.classes) as distinct_classes
                FROM (SELECT classes FROM spells_spell) AS spell_classes GROUP BY distinct_classes;
            """
            cursor.execute(raw_query)
            return [row[0] for row in cursor]

        if force:
            cache.delete(cls.DISTINCT_CLASS_CACHE_KEY)

        return cache.get_or_set(cls.DISTINCT_CLASS_CACHE_KEY, get_distinct_classes)

    def save(self, *args, **kwargs):
        cache.delete(self.DISTINCT_CLASS_CACHE_KEY)
        return super().save(*args, **kwargs)
