# Copyright 2020 by Kurt Rathjen. All Rights Reserved.
#
# This library is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. This library is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
"""
NOTE: Make sure you register this item in the config.
"""

import os
import logging
from pathlib import Path

import maya.cmds

from studiolibrarymaya import baseitem

import mutils


logger = logging.getLogger(__name__)


class PathItem(baseitem.BaseItem):

    NAME = "Path File"
    TYPE = NAME
    EXTENSION = ".path"
    ICON_PATH = os.path.join(os.path.dirname(__file__), "icons", "file.png")
    TRANSFER_BASENAME = "path.json"
    TRANSFER_CLASS = mutils.PathFile
    def getFolderName(self):
        '''return foldername'''
        return Path(self.transferPath()).parent.stem
    
    def loadSchema(self, **kwargs):
        """
        Get the schema used for loading the example item.

        :rtype: list[dict]
        """
        lPathObject = mutils.pathfile.PathFile()
        lPathObject.setPath(self.transferPath())
        lPathObject.read()
        namespace = self.getFolderName()
        filepath = lPathObject.data().get("filepath")
        schema = [
            {
                "name": "optionsGroup",
                "title": "Options",
                "type": "group",
                "order": 2,
            },
            {
                "name": "namespace",
                "type": "string",
                "layout":"horizontal", #"vertical",
                "value": namespace,
            },
            {
                "name": "filepath",
                "type": "label",
                "layout": "horizontal",
                "value": filepath,

            },
            {
                "name": "fileOptions",
                "type": "radio",
                "value": "From file",
                "items": mutils.PathFile.get_mode(),
                "persistent": True,
                "persistentKey": "BaseItem",

            },

        ]
        return schema
    
    @mutils.showWaitCursor
    def load(self, **kwargs):
        """
        The load method is called with the user values from the load schema.

        :type kwargs: dict
        """
        #logger.info("Loading %s %s", self.transferPath(), kwargs)
        lPathObject = mutils.pathfile.PathFile()
        lPathObject.setPath(self.transferPath())
        lPathObject.read()
        fileOptions = kwargs.get("fileOptions")
        namespace = kwargs.get("namespace")
        filepath = lPathObject.data().get("filepath")
        lPathObject.load(fileOptions,filepath,namespace)

    def saveSchema(self, **kwargs):
        """
        Get the schema used for saving the example item.

        :rtype: list[dict]
        """

        currentFile = maya.cmds.file(q=True, sn=True)
        namespace = "No Recommend( File Not Saved )"
        filepath = ""
        if currentFile:
            namespace = os.path.basename(currentFile).split(".")[0]
            filepath = currentFile

        return [
            # The 'name' field and the 'folder' field are both required by
            # the BaseItem. How this is handled may change in the future.
            {
                "name": "folder",
                "type": "path",
                "layout": "vertical",
                "visible": False,
            },
            {
                "name": "name",
                "type": "string",
                "layout": "horizontal",
            },
            {
                "name": "Recommand",
                "type": "label",
                "layout": "horizontal",
                "value": namespace,
            },
            {
                "name": "filepath",
                "type": "text",
                "layout": "horizontal",
                "value": filepath,

            },

        ]
    def saveValidator(self, **kwargs):
        
        fields= super().saveValidator(**kwargs)
        if not kwargs.get("filepath"):
            fields.append({
                "name": "filepath",
                "error": "No filepath specified. Please set a path before saving.",
            })
        return fields
    
    def save(self, **kwargs):
        """
        The save method is called with the user values from the save schema.

        :type kwargs: dict
        """
        
        super().save(**kwargs)
        lPathObject = mutils.pathfile.PathFile()
        lPathObject.setPath(self.transferPath())
        namespace = kwargs.get("name") # use folder name insdead
        filepath = kwargs.get("filepath")
        lPathObject.save(namespace,filepath)




