from django.core.files.uploadhandler import FileUploadHandler, StopUpload
class QuotaUploadHandler(FileUploadHandler):
	""" This upload handler terminates the connection if more than a quota is uploaded. """
	QUOTA = 1 * 2**20 # 1 MB

	def __init__(self, request=None):
		super(QuotaUploadHandler, self).__init__(request)
		self.total_upload = 0

	def receive_data_chunk(self, raw_data, start):
		self.total_upload += len(raw_data)
		if self.total_upload >= self.QUOTA:
			raise StopUpload(connection_reset=True)
		return raw_data

	def file_complete(self, file_size):
		return None