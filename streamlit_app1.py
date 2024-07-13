def delete_file(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True  # Indicates successful deletion
        except HttpError as error:
            print(f'An error occurred while deleting: {error}')
            return False 