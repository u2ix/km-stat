#######################################################################
# Copyright Lukas Bürgi 2019
#
# This file is part of km-stat.
#
# km-stat is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# km-stat is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with km-stat.  If not, see
# <https://www.gnu.org/licenses/>.
########################################################################

from django.db import models
from django.conf import settings
import json

# does this belong here?
class apiData():
  """The data that is returned by an API query. Methods to add data and return json of accumulated data. Does some sanity checks on the data.
  The JSON contains exactly the following dict:
    {
    'total' : amount of results on all pages
    'cnames' : [column title 1, ..., column title n,],
    'ctypes' :   [ country code, country name, date, money, untreated ],
    'countries' :
      {
        'country code 1' : 0,
        'country code 2' : 1,
        ...
        'country code m' : m-1,
      }
    'data' :
      [
        [data country 1 column 1, ..., data country 1 column n],
        ...
        [data country m column 1, ..., data country m column n],
      ]
    }
  The 'ctypes' entry has the types of the columns in order.
  The 'countries' entry exists only if we know the countries are unique in all data rows and need to index the data by country. """
  
  """This attribute is the one that is converted to json and sent."""
  def __init__(self, uniqueCountry, columnNames, columnTypes):
    self.data = dict()
    assert(len(columnNames) == len(columnTypes))
    if(uniqueCountry):
      self.data['countries'] = dict()
      self.uniqueCountry = True
    else:
      self.uniqueCountry = False
    self.data['total'] = None
    self.data['cnames'] = columnNames
    self.data['ctypes'] = columnTypes
    self.countryCodeColumn = None
    for (index, t) in enumerate(columnTypes):
      if(t=='country code'):
        if(self.countryCodeColumn == None):
          self.countryCodeColumn = index
        else:
          # doesn't make sense to have multiple
          raise(ValueError)
    if(self.countryCodeColumn == None):
      raise(ValueError)
      
    self.data['data'] = []

  def addRow(self, row):
    if(self.uniqueCountry):
      self.data['countries'][row[self.countryCodeColumn]] = len(self.data['data'])
    self.data['data'].append(row)

  def addRows(self, rows):
    for row in rows:
      self.addRow(row)

  def setTotal(self, total):
    self.data['total'] = total
  
  def getJSON(self):
    """ Returns a string that is the JSON representation of self.data. """
    if(self.data['total'] == None):
      raise(RuntimeError("Need to know a total."))
    if(settings.DEBUG):
      return(json.dumps(self.data, indent=2))
    else:
      return(json.dumps(self.data, separators=(',', ':')))

class Uebersetzungen(models.Model):
  """ Enthält alles, was übersetzt werden muss. """

  de = models.TextField(blank=True)
  fr = models.TextField(blank=True)
  it = models.TextField(blank=True)
  en = models.TextField(blank=True)

  def __str__(self):
    """ Sollte je nach Spracheinstellung die richtige Sprache zurückgeben und dann auf andere Sprachen zurückfallen wenn es diese nicht gibt. TODO. """
    return(self.de)

  class Meta:
    verbose_name = 'Übersetzung'
    verbose_name_plural = 'Übersetzungen'

class Laendergruppen(models.Model):
  """ Groups of countries for easy selection, say "Africa", "European Union" or "Middle East". """
  name = models.ForeignKey(Uebersetzungen, on_delete=models.PROTECT)
  """ Name of the group. """
  code = models.CharField(max_length=2)
  """ Two character made up id. It's ok if they collide with country codes."""

  def __str__(self):
    return(self.code)
  
  class Meta:
    verbose_name = 'Ländergruppe'
    verbose_name_plural = 'Ländergruppen'

class Laender(models.Model):
  """ Liste der Länder, in die exportiert wird. """
  code = models.CharField(max_length=2)
  """ Ländercode, 2 Grossbuchstaben. ISO 3166-1 alpha-2 (hoffentlich)"""
  name = models.ForeignKey(Uebersetzungen, on_delete=models.PROTECT)
  """ Voller Name des Landes. """
  gruppen = models.ManyToManyField(Laendergruppen)
  """ Groups that this country is a member of. """
  breitengradMin = models.FloatField()
  """ Der minimale Breitengrad, der dieses Land schneidet. """
  breitengradMax = models.FloatField()
  """ Der maximale Breitengrad, der dieses Land schneidet. """
  laengengradMin = models.FloatField()
  """ Der minimale Längengrad, der dieses Land schneidet. """
  laengengradMax = models.FloatField()
  """ Der maximale Längengrad, der dieses Land schneidet. """


  def __str__(self):
    return(self.code)
  
  class Meta:
    verbose_name = 'Land'
    verbose_name_plural = 'Länder'
