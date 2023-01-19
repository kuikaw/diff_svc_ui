import os
import gdown
from zipfile import ZipFile

#
#	Installs checkpoints needed by Diff-SVC 22kHz/44kHz models.
#

id='1AKZod8klKvKxVC93YZR95IaQNPqYwC-D'
output='checkpoints.zip'

gdown.download(id=id, output=output, quiet=False)

if os.path.exists('checkpoints'):
	pass
else:
	os.mkdir('checkpoints')

with ZipFile('checkpoints.zip') as ckpt:
	for file in ckpt.namelist():
		ckpt.extract(file, 'checkpoints')

os.remove('checkpoints.zip')

print('\nCheckpoints Installed!\n')