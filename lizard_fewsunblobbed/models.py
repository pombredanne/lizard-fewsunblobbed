# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# $Id$

import logging
from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext as _

from composite_pk import composite
from treebeard.al_tree import AL_Node
from lizard_map import coordinates

logger = logging.getLogger(__name__)


class Filter(AL_Node):
    """Fews filter object."""

    # treebeard expects (hardcoded) fields 'id' and 'parent', while
    # fews exposes fkey and parentfkey.
    id = models.IntegerField(primary_key=True, db_column='fkey')
    # since 'id' is already used, we remap 'id' to 'fews_id'.
    fews_id = models.CharField(max_length=64, unique=True, db_column='id')
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    issubfilter = models.BooleanField()
    # treebeard requirement (see 'id')
    parent = models.ForeignKey('Filter', null=True, blank=True,
                               db_column='parentfkey')
    isendnode = models.BooleanField()
    node_order_by = ['name']

    class Meta:
        verbose_name = _("Filter")
        verbose_name_plural = _("Filters")
        db_table = u'filter'

    def __unicode__(self):
        return u'%s (id=%s)' % (self.name, self.fews_id)

    @property
    def has_parameters(self):
        """Return whether there is at least one connected timeserie.

        Note: parameters of descendants are not counted."""
        return Timeserie.objects.filter(filterkey=self.id).exists()

    @classmethod
    def get_database_engine(cls):
        """Overriding treebeard: it grabs the 'default' database engine."""
        engine = settings.DATABASES['fews-unblobbed']['ENGINE']
        return engine.split('.')[-1]

    # This method is overriden from the class AL_Node in al_tree.py from the
    # django-treebeard application.  The method fixes checks first if the
    # field sib_order exist before deleting, which the original version
    # doesn't do (which causes a bug).

    @classmethod
    def dump_bulk(cls, parent=None, keep_ids=True):
        """
        Dumps a tree branch to a python data structure.

        See: :meth:`treebeard.Node.dump_bulk`
        """

        # not really a queryset, but it works
        qset = cls.get_tree(parent)

        ret, lnk = [], {}
        pos = 0
        for pyobj in serializers.serialize('python', qset):
            node = qset[pos]
            depth = node.get_depth()
            # django's serializer stores the attributes in 'fields'
            fields = pyobj['fields']
            del fields['parent']
            if 'sib_order' in fields:
                del fields['sib_order']
            if 'id' in fields:
                del fields['id']
            fields['has_parameters'] = node.has_parameters
            newobj = {'data': fields}
            if keep_ids:
                newobj['id'] = pyobj['pk']

            if ((not parent and depth == 1) or
                (parent and depth == parent.get_depth())):
                ret.append(newobj)
            else:
                parentobj = lnk[node.parent_id]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[node.id] = newobj
            pos += 1
        return ret


class Location(models.Model):
    """Fews location object.
    """

    lkey = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256, blank=True)
    parentid = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True)
    shortname = models.CharField(max_length=256, blank=True)
    tooltiptext = models.CharField(max_length=1000, blank=True)
    x = models.FloatField(blank=True)
    y = models.FloatField(blank=True)
    z = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        db_table = u'location'

    def __unicode__(self):
        return u'%s (lkey=%s)' % (self.name, self.lkey)

    def google_coords(self):
        return coordinates.rd_to_google(self.x, self.y)


class Parameter(models.Model):
    """Fews parameter object."""

    pkey = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256, blank=True)
    shortname = models.CharField(max_length=256, blank=True)
    unit = models.CharField(max_length=64, blank=True)
    parametertype = models.CharField(max_length=64, blank=True)
    parametergroup = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")
        db_table = u'parameter'

    def __unicode__(self):
        return u'%s (pkey=%s)' % (self.name, self.pkey)


class Timeserie(models.Model):
    """Fews timeserie object. Specifies a time series of a specific parameter.

    Examples of parameters are water discharge, zinc concentration and chloride
    concentration.

    To get to the events that belong to the current Timeserie, use the implicit
    attribute 'timeseriedata', which is a Manager for the events.
    """

    tkey = models.IntegerField(primary_key=True)
    moduleinstanceid = models.CharField(max_length=64, blank=True)
    timestep = models.CharField(max_length=64, blank=True)
    filterkey = models.ForeignKey(Filter, db_column='filterkey')
    locationkey = models.ForeignKey(Location, db_column='locationkey')
    parameterkey = models.ForeignKey(Parameter, db_column='parameterkey')

    class Meta:
        verbose_name = _("Timeserie")
        verbose_name_plural = _("Timeseries")
        db_table = u'timeserie'

    def __unicode__(self):
        return u'%s: %s' % (self.locationkey.name, self.parameterkey.name)

    @property
    def name(self):
        """Return name for use in graph legends"""
        return u'%s (%s): %s' % (self.parameterkey.name,
                                self.parameterkey.unit,
                                self.locationkey.name)

    @property
    def shortname(self):
        """Return name for use in graph legends"""
        return u'%s' % (self.locationkey.name)

    def data_count(self):
        return self.timeseriedata.all().count()

    @classmethod
    def has_data_dict(cls, ignore_cache=False):
        """
        Return for each timeserie id if it has data.

        If a timeserie has data, its id is listed in the returned
        dict. Handy when looping over great amounts of timeseries.
        """
        cache_key = 'lizard_fewsunblobbed.models.timeserie_hasdata'
        result = cache.get(cache_key)
        if result is None or ignore_cache:
            logger.info('Populating Timeserie.has_data_dict...')
            tsd = Timeseriedata.objects.all().values('tkey').distinct()
            tsd_dict = {}
            for row in tsd:
                tsd_dict[row['tkey']] = None  # Just make an entry
            cache.set(cache_key, tsd_dict, 8 * 60 * 60)
            result = tsd_dict
        return result

    @property
    def has_data(self):
        """
        Return true if this timeserie has data, false otherwise.

        Uses has_data_dict index.
        """
        if self.pk in self.has_data_dict():
            return True
        else:
            return False
        # too slow
        #return self.timeseriedata.exists()


class Timeseriedata(composite.CompositePKModel):
    """Fews timeseriedata object. Specifies the value of a parameter at
    a specific time.

    Note that a WaterbalanceTimeserieData does not specify the parameter
    itself, only its value at a specific time.

    Instance variables:
      * value *
        value of the parameter
      * time *
        time at which the value was measured
      * timeserie *
        link to the time serie

    ..todo::

      lizard_fewsunblobbeb.Timeseriedata has two primary keys although Django
      does not support multiple primary keys. This means that we can use this
      model to read from a FEWS unblobbed database but not write to.

      http://code.djangoproject.com/ticket/373 describes the lack of support
      for multiple keys and also a workaround.

      One example where this will affect you is when you try to create and save
      a Timeseriedata programmatically. Django will report

        ValidationError: [u'Enter a valid date/time in YYYY-MM-DD
        HH:MM[:ss[.uuuuuu]] format.']

      because it has to work with a dictionarity of values - the two primary
      keys - where it expects a single value.

      This issue is also reported in Trac in ticket:2590 and ticket:2674.

    """
    tkey = models.ForeignKey(Timeserie,
                             primary_key=True,
                             db_column='tkey',
                             related_name='timeseriedata')

    # ^^^ TODO: this is mighty slow in the django admin.  It grabs all the
    # timeserie names/ids.
    tsd_time = models.DateTimeField(primary_key=True, db_column='tsd_time')
    tsd_value = models.FloatField(blank=True)
    tsd_flag = models.IntegerField(blank=True)
    tsd_detection = models.BooleanField()
    tsd_comments = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = _("Timeserie data")
        verbose_name_plural = _("Timeseries data")
        db_table = u'timeseriedata'
        unique_together = (('tkey', 'tsd_time'), )

    def __unicode__(self):
        return u'Data for %s: %s = %s' % (self.tkey,
                                          self.tsd_time,
                                          self.tsd_value)
