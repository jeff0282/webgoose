
# This file is part of Webgoose.
# 
# Webgoose is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 
# of the License, or (at your option) any later version.
# 
# Webgoose is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with Webgoose. If not, see <https://www.gnu.org/licenses/>. 



#
# BASIC SCRIPT TO GRAB VERSION STRING FROM PROJECT METADATA
#
# Gets the version string from the `pyproject.toml` file
#

from    importlib.metadata      import      version

__version__ = version("webgoose")

