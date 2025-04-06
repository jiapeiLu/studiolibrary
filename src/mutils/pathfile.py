import logging

import mutils
from pathlib import Path
try:
    import maya.cmds as cmds
except Exception:
    import traceback
    traceback.print_exc()
    
logger = logging.getLogger(__name__)




class PathFile(mutils.TransferObject):
    kReferencenew = "Reference(new)"
    kReference = "Reference"
    kImport = "Import"
    kOpen = "Open"

    @classmethod
    def get_mode(cls):
        return [ value  for key, value in  cls.__dict__.items() if key.startswith('k')]

    def operation(self, mode:str, filepath:str, ns = ""):
        '''
        Args:
        mode: 'Reference(new)'|'Reference'|'Import'|'Open'|
        '''
        if not ns:
            ns = ":"
        #check file exist:
        if not Path(filepath).exists():
            cmds.warning(f'File not vaild: {filepath}')
            return

        if mode == self.kReference :
            cmds.file(filepath, reference=True, namespace=ns, f=True)
        elif mode == self.kReferencenew:
            cmds.file(new=True, f=True)
            cmds.file(filepath, reference=True, namespace=ns, f=True)
        elif mode == self.kImport:
            cmds.file(filepath, i=True, namespace=ns, f=True)
        elif mode == self.kOpen:
            cmds.file(filepath, o=True,f=True)

    def file_operation_exec( self, fileOptions:str, filepath,namespace):
        self.operation(fileOptions, filepath, namespace)

    
    def load(self,mode, filepath, namespace):
        super().load()
        self.file_operation_exec(mode, filepath, namespace)

    def save(self, namespace, filepath):
        '''This save is only for rig file.'''
        #logger.info("Saving pose: %s" % self.path())

        savePath = Path(self.path())
        dirname = savePath.parent
        if not dirname.exists():
            dirname.mkdir(parents=True,exist_ok=True)
        data = {
            "namespace":namespace,
            "filepath":filepath
        }
        with open(self.path(), "w") as f:
            f.write(self.dump(data))