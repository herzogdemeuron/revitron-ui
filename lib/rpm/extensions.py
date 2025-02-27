from rpm import config
from pyrevit import script
from pyrevit.coreutils import logger
from datetime import datetime
import os
import json
import subprocess
from .git_manager import install_or_update

mlogger = logger.get_logger(__name__)


class ExtensionsManager:

	def __init__(self):
		self.json = config.RPM_EXTENSIONS_DIR + '\\rpm.json'

	def getInstalled(self):
		try:
			with open(self.json) as jsonFile:
				data = json.load(jsonFile)
		except:
			data = {'installed': dict()}
		return data['installed']

	def removeAll(self):
		for key, ext in self.getInstalled().items():
			try:
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				startupinfo.wShowWindow = 0
				subprocess.check_output(
				    'rmdir /Q /S {}'.format(ext['path']),
				    stderr=subprocess.STDOUT,
				    shell=True,
				    cwd='C:\\',
				    startupinfo=startupinfo
				)
				mlogger.info('Removed extension {}'.format(key))
			except:
				mlogger.error('Error removing extension {}'.format(key))
		data = {'installed': dict()}
		script.dump_json(data, self.json)

	def install(self, name, repo, extType):
		repo = repo.replace('.git', '') + '.git'
		types = {'ui': 'extension', 'lib': 'lib'}
		folder_name = name + '.' + types.get(extType, 'extension')
		path = config.RPM_EXTENSIONS_DIR + '\\' + folder_name

		if not os.path.isdir(path):
			if install_or_update(repo, path) is True:
				mlogger.info('Installed extension {}'.format(name))
			else:
				mlogger.error('Failed to install extension {}'.format(name))
		else:
			mlogger.error('{} is not empty!'.format(path))
		self.register(name, repo, extType, path)


	def register(self, name, repo, extType, path):
		data = {'installed': self.getInstalled()}
		data['installed'][os.path.basename(path)] = {
		    'name': name,
		    'type': extType,
		    'repo': repo,
		    'path': path,
		    'date': str(datetime.now())
		}
		script.dump_json(data, self.json)
