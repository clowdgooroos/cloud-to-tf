import requests
import uuid

from . import aes

class Logger:
    """A logging class
    """
    
    def __init__(self, url):
        self.url = url


    def __get_token(self):
        """ Get a one-time use encryption token

        Returns:
            tuple: (token, uuid) the token for encryption as well as the UUID
        """
        
        # Generate a UUID
        random_uuid = str(uuid.uuid4())
    
        request = requests.get(f'{ self.url }/key?id={ random_uuid }', verify=False)
        token = request.text
        
        return token, random_uuid
    
    
    def __encrypt_data(self, token, plain_text):
        """ Encrypt data using the built in AES class """

        crypt_handler = aes.AESCipher(token)
        data = crypt_handler.encrypt(plain_text)
        
        return data
    

    def log_message(self, log_msg):
        """Log a message using a one-time encryption key

        Args:
            log_msg (str): The message to log
        """
        
        token, random_uuid = self.__get_token()

        encrypted_log = self.__encrypt_data(token, log_msg).decode()
    
        request = requests.post(f'{ self.url }/status?id={ random_uuid }', encrypted_log, verify=False)
        
    
