from storage.database import Database


class FileRepository:
    """
    Repository for file operations.
    Manages interactions with the database for file-related tasks.
    """
    
    def __init__(self):
        self.db =Database()
        self.mongo_db = self.db.get_mongo_db("vault")
        self.fs = self.db.fs

    def save_file(self, file_model):
        """
        Save a file to the database.
        :return: Confirmation of file save.
        """
        try:
            file_data = file_model.to_dict()
            self.mongo_db.files.insert_one(file_data)
            return f"File '{file_data['file_name']}' saved successfully."
        except Exception as e:
            return f"Error saving file to database: {str(e)}"
    
    def upload_file(self, file, file_name):
        """
        Upload a file to the GridFS storage.
        """
        try:
            file_id = self.fs.put(file, filename=file_name, content_type='application/octet-stream')
            return file_id 
        except Exception as e:
            return f"Error uploading file: {str(e)}"

        
    def get_file(self, file_name):
        """
        Retrieve a file from the database.
        :param file_name: Name of the file to retrieve.
        :return: File data if found, otherwise None.
        """
        try:
            file = self.mongo_db.file.find_one({"file_name": file_name})
            if file:
                return file
            return None
        except Exception as e:
            return f"Error retrieving file: {str(e)}"

    def retrieve_file(self, file_name):
        """
        Retrieve a file from GridFS storage.
        :param file_name: Name of the file to retrieve.
        :return: File content if found, otherwise None.
        """
        try:
            file = self.fs.find_one({"filename": file_name})
            if file:
                return file.read()
            return None
        except Exception as e:
            return f"Error retrieving file from GridFS: {str(e)}"
        
    def delete_file(self, file_name, file_id):
        """
        Delete a file from the database.
        :param file_name: Name of the file to delete.
        :return: Confirmation of deletion.
        """
        try:
            result = self.mongo_db.files.delete_one({"file_name": file_name})
            if result.deleted_count > 0 and not self.fs.delete(file_id):
                return None
        except Exception as e:
            return f"Error deleting file: {str(e)}"
        
    def update_file(self, file_name, new_file_data):
        """
        Update a file's metadata in the database.
        :param file_name: Name of the file to update.
        :param new_file_data: New data for the file.
        :return: Confirmation of update.
        """
        try:
            result = self.mongo_db.files.update_one({"file_name": file_name}, {"$set": new_file_data})
            if result.modified_count > 0:
                return f"File '{file_name}' updated successfully."
            return "No changes made to the file."
        except Exception as e:
            return f"Error updating file: {str(e)}"


    