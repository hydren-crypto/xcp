import sys, os, requests
from subprocess import call

FOR_VERSION = 3

# get filename passed to the script
filename = sys.argv[-1];

# send file to the API
with open(filename, 'rb') as f:
	response = requests.post('http://compress-or-die.com/api-v3', data=f, headers={'X-DOCUMENT-NAME': os.path.basename(filename)})

# parse the answer to get the session id
lines = response.text.splitlines()
answer = {}
for line in lines:
	parts = line.split(':', 1);
	answer[parts[0]] = parts[1]

# check version
if (int(answer['_VERSION']) != FOR_VERSION):
	print('Aborting: This script is for version ' + str(FOR_VERSION) + ', but the current version is ' + answer['_VERSION'] + '.', file=sys.stderr)
	exit(1)


# open the browser to show the image on compress-or-die.com
from sys import platform
if platform == "darwin":
	call(['open', answer['_URL'] + '?session=' + answer['_SESSION']])
elif platform == "win32":
	call(['cmd.exe', '/c', 'start', answer['_URL'] + '?session=' + answer['_SESSION']])
