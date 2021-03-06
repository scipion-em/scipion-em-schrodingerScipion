# **************************************************************************
# *
# * Authors:     Carlos Oscar Sorzano (coss@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

"""
This package contains protocols interfacing Schrodinger's Maestro
"""

# Useful reference: http://www.bi.cs.titech.ac.jp/mga_glide/xglide_mga.py

import glob
import os
import pwem
import pyworkflow.utils as pwutils
from .bibtex import _bibtexStr

_logo = 'schrodinger.png'

class Plugin(pwem.Plugin):
    _homeVar = 'SCHRODINGER_HOME'

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar('SCHRODINGER_HOME', 'schrodinger2019-4')

    @classmethod
    def defineBinaries(cls, env):
        pass

    @classmethod
    def getEnviron(cls, schrodingerFirst=True):
        """ Create the needed environment for Schrodinger programs. """
        environ = pwutils.Environ(os.environ)
        pos = pwutils.Environ.BEGIN if schrodingerFirst else pwutils.Environ.END
        environ.update({
            'SCHRODINGER': cls.getHome(''),
            'PATH': cls.getHome(''),
            'LD_LIBRARY_PATH': cls.getMMshareDir('lib/Linux-x86_64')+':'+cls.getHome('internal/lib'),
            'PYTHONPATH': cls.getSitePackages()
        }, position=pos)
        return environ

    @classmethod
    def getMMshareDir(cls, fn):
        fileList = glob.glob(cls.getHome('mmshare*'))
        if len(fileList)==0:
            return None
        else:
            return os.path.join(fileList[0],fn)

    @classmethod
    def getSitePackages(cls):
        fileList = glob.glob(cls.getHome('internal/lib/python3.*'))
        if len(fileList) == 0:
            return None
        else:
            return os.path.join(fileList[0], 'site-packages')

    @classmethod
    def getPluginHome(cls, path=""):
        import schrodingerScipion
        fnDir = os.path.split(schrodingerScipion.__file__)[0]
        return os.path.join(fnDir,path)


    @classmethod
    def runSchrodinger(cls, protocol, program, args, cwd=None):
        """ Run rdkit command from a given protocol. """
        protocol.runJob(program, args, env=cls.getEnviron(), cwd=cwd)
