#!/usr/bin/env python3

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                 globdef                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2006-2009 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os,os.path,sys, wx

#
# Les deuxlignes suivantes permettent de lancer le script PyVot.py depuis n'importe
# quel répertoire (par exemple : C:\python .\0.3\PyVot.py) sans que l'utilisation de chemins
# relatifs ne soit perturbée
#
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    PATH = os.path.dirname(os.path.abspath(sys.executable))
    RESOURCE_PATH = getattr(sys, "_MEIPASS", SOURCE_PATH)
else:
    PATH = SOURCE_PATH
    RESOURCE_PATH = SOURCE_PATH

installed_resources = os.path.join(sys.prefix, "share", "pyvot")
if not os.path.isdir(os.path.join(RESOURCE_PATH, "Images")) \
        and os.path.isdir(os.path.join(installed_resources, "Images")):
    RESOURCE_PATH = installed_resources
#PATH = os.path.split(PATH)[0]
os.chdir(PATH)
sys.path.append(PATH)
print("Chemin de l'application :",PATH)

if getattr(sys, "frozen", False):
    SAMPLEPATH = os.path.join(RESOURCE_PATH, "Exemples")
    HELPPATH = os.path.join(RESOURCE_PATH, "Aide")
else:
    SAMPLEPATH = os.path.join(PATH,"../Exemples")
    HELPPATH = os.path.join(PATH,"../Aide")

#
# Définition du numéro de version
#
MAJOR=0
MINOR=62
VERSION="%i.%i"%(MAJOR,MINOR)

#
# Langue par en cours
#
ENCODING="" #encodage de la langue
LANGUAGE=None

#
# Diverses options
#
INSTALLED_LANG = None #le language installé par défaut
USE_PSYCO=True # utilisation optionnelle de psyco pour exécuter le programme plus rapidement (mais empreinte mémoire plus importante)

#
# Option d'analyse
#

DUREE_ANIMATION_MONTAGE = 2  # en secondes
FRAME_RATE = 20 # en images/secondes
DISTANCE_DEMONTAGE_ENSEMBLE = 680 # en pixels
DISTANCE_DEMONTAGE_RLT_COURT = 280
DISTANCE_DEMONTAGE_RLT_LONG = 500

#
# Option pour l'affichage
#

HACHURER_EN_EDITION = True

# Tags utilisés pour reconnaitre les items appartenant à l'arbre ou à l'alésage
TAG_ARBRE = "GrpArbre"
TAG_ALESAGE = "GrpAlesage"

#
# Curseurs
#

CURSEUR_DEFAUT = wx.CURSOR_ARROW
CURSEUR_INTERDIT = wx.CURSOR_NO_ENTRY
CURSEUR_ORIENTATION = wx.CURSOR_SIZEWE
CURSEUR_OK = wx.CURSOR_CROSS
