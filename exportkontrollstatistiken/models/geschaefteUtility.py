from django.db import models
from django.conf import settings

from .utility import *
from .geschaefte import Laender
from .geschaefte import GueterArten
from .geschaefte import Geschaefte

class Geschaeftslaendersummen(models.Model):
  """Hilfsmodell, das Teilsummen pro Land, Jahr und Güterart enthält. TODO: Neues Feld für nur die Summe von dem Jahr."""
  endempfaengerstaat = models.ForeignKey(Laender, on_delete=models.PROTECT)
  gueterArt = models.ForeignKey(GueterArten, on_delete=models.PROTECT)
  umfang = models.PositiveIntegerField()
  """Summe aller Exporte bis zu dem Jahr inklusive."""
  jahr = models.PositiveIntegerField()

  @staticmethod
  def recalculate():
    """Delete all entries and calculate new entries from Geschaefte entries.
    This needs to be run after any relevant changes to the Geschaefte entries.
    So it's not performance-relevant, allowed to run for tens of seconds or longer."""
    Geschaeftslaendersummen.objects.all().delete()
    geschaefte = Geschaefte.objects.all().order_by("endempfaengerstaat", "exportkontrollnummer__kontrollregime__gueterArt", "beginn")

    # get the first separately
    firstG = next(geschaefte.__iter__())
    curSum = Geschaeftslaendersummen(endempfaengerstaat=firstG.endempfaengerstaat, gueterArt=firstG.exportkontrollnummer.kontrollregime.gueterArt, umfang=firstG.umfang, jahr=firstG.beginn.year)
    curSum.save()
    # then iterate over the rest
    for g in geschaefte:
      if(g.beginn.year!=curSum.jahr):
        if(g.endempfaengerstaat!=curSum.endempfaengerstaat or g.exportkontrollnummer.kontrollregime.gueterArt!=curSum.gueterArt):
          curSum = Geschaeftslaendersummen(endempfaengerstaat=g.endempfaengerstaat, gueterArt=g.exportkontrollnummer.kontrollregime.gueterArt, umfang=g.umfang, jahr=g.beginn.year)
          curSum.save()
        else:
          curSum = Geschaeftslaendersummen(endempfaengerstaat=g.endempfaengerstaat, gueterArt=g.exportkontrollnummer.kontrollregime.gueterArt, umfang=curSum.umfang+g.umfang, jahr=g.beginn.year)
          curSum.save()
      else:
        curSum.umfang += g.umfang
        curSum.save()
    # now all the entries that change are here, but zero entries and
    # entries that have zero difference to the previous year are still missing
    for country in Laender.objects.all():
      for gueterArt in GueterArten.objects.all():
        cur=None
        for jahr in range(2000, 2020):
          try:
            cur=Geschaeftslaendersummen.objects.filter(jahr=jahr, gueterArt=gueterArt, endempfaengerstaat=country).get()
          except Geschaeftslaendersummen.DoesNotExist:
            if(cur==None):
              cur=Geschaeftslaendersummen(endempfaengerstaat=country, gueterArt=gueterArt, jahr=jahr, umfang=0)
              cur.save()
            else:
              # copy cur with new year
              cur.pk=None
              cur.jahr=jahr
              cur.save()

  @staticmethod
  def getJSONSummed(p):
    """Sum transactions per country.

    Begin and end are both inclusive.

    Algorithm:
        * Get entries for year2 sorted by country
        * Get entries for (year1-1) sorted by country
        * Slice both of them correctly
        * Iterate through both sets in parallel
            * subtract the latter from the former in each entry
            * add up the selected types
        * Sort according to p.sortBy
    """

    queryset2 = Geschaeftslaendersummen.objects.filter(jahr=p.year2)
    queryset2 = queryset2.filter(p.getTypes("gueterArt__name"))
    queryset2 = queryset2.filter(p.countries)
    queryset2 = queryset2.order_by("endempfaengerstaat")

    queryset1 = Geschaeftslaendersummen.objects.filter(jahr=(p.year1-1))
    queryset1 = queryset1.filter(p.getTypes("gueterArt__name"))
    queryset1 = queryset1.filter(p.countries)
    queryset1 = queryset1.order_by("endempfaengerstaat")
    # TODO: Should I make a method for the above duplicate code?

    # TODO: This can be done more elegantly with the new apiData class
    sums = dict()
    for country in zip(queryset1, queryset2):
        if(country[0].endempfaengerstaat.code in sums):
            sums[country[0].endempfaengerstaat.code][1] += country[1].umfang - country[0].umfang
        else:
            sums[country[0].endempfaengerstaat.code]=[country[0].endempfaengerstaat, (country[1].umfang-country[0].umfang)]

    
    if(p.sortBy=="-umfang"):
        reverse=True
    else:
        reverse=False

    order = sorted(sums, key=lambda key : sums.get(key)[1], reverse=reverse)

    result = apiData(True, ["id", "Name", "Exporte"], ['country code', 'country name', 'money'])
    result.setTotal(len(order))
    for country in p.getPage(order):
        result.addRow([country, sums[country][0].name.de, sums[country][1]])
    return(result.getJSON())


class Geschaeftssummen(models.Model):
  """Hilfsmodell, das Teilsummen pro Jahr und Güterart enthält."""
  gueterArt = models.ForeignKey(GueterArten, on_delete=models.PROTECT)
  umfang = models.PositiveIntegerField()
  """Summe aller Exporte bis zu dem Jahr inklusive."""
  jahr = models.PositiveIntegerField()

  def recalculate():
    """Delete all entries and calculate new entries Geschaeftssummen."""
    pass # TODO

class GeschaefteImport(models.Model):
  """Hilfsmodell zum Import der alten Daten, hat gleiche Struktur wie "export" Tabelle dort."""
  code = models.CharField(max_length=2)
  art = models.CharField(max_length=40)
  system = models.CharField(max_length=10)
  kategorie = models.CharField(max_length=15)
  datum = models.DateField()
  betrag = models.PositiveIntegerField()
  
