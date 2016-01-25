from __future__ import print_function
from apiclient import errors
from apiclient.http import MediaFileUpload

import httplib2
import os
import base64

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# try:
# 	import argparse

# 	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
# 	flags = None
flags = None


class DriveApi(object):
	SCOPES = 'https://www.googleapis.com/auth/drive.file'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Drive API'

	def insert_file(self, service, title, description, parent_id, mime_type, filename):
		media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
		body = {
			'title': title,
			'description': description,
			'mimeType': mime_type,
			"parents": [{
				"kind": "drive#fileLink",
				"id": "0B1vBxa7BraUAUTNwM2VaZFRDZWM"
			}]

		}
		# Set the parent folder.
		if parent_id:
			body['parents'] = [{'id': parent_id}]

		try:
			file = service.files().insert(
					body=body,
					media_body=media_body).execute()

			# Uncomment the following line to print the File ID
			print('File ID: %s' % file['id'])

			return file
		except errors.HttpError, error:
			# print('An error occured: %s' % error)
			return None

	def get_credentials(self):
		home_dir = os.getcwd()
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									   'drive-python-quickstart.json')

		store = oauth2client.file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else:  # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			# print('Storing credentials to ' + credential_path)
		return credentials

	def upload(self, base, username):
		with open('index.jpeg', "wb") as file:
			file.write(base64.b64decode(base))
		credentials = self.get_credentials()
		http = httplib2.Http()
		http = credentials.authorize(http)
		service = discovery.build('drive', 'v2', http=http)
		mime_type = 'https://www.googleapis.com/auth/drive.file'
		filename = 'index.jpeg'
		title = username + '.jpeg'
		description = 'uploading photo'
		file = self.insert_file(service, title, description, None, mime_type, filename)
		os.remove('index.jpeg')
		if not file:
			return False
		else:
			return True

	def download(self, username):

