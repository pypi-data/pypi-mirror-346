import json
import requests

    
class API:
    BASE_URL = "https://api.verblaze.com" # TODO: change to https://api.verblaze.com
    
    async def checkCLISecret(cli_secret: str) -> bool:
        url = f"{API.BASE_URL}/api/cli/checkCLISecret"
        response =  requests.get(url, params={"cliSecretToken": cli_secret})
        if response.status_code == 200:
            return True
        else: 
            return False
        
    async def initLanguage(cli_secret: str, translations: list) -> dict:
        url = f"{API.BASE_URL}/api/cli/initLanguage"
        response =  requests.post(url,headers={"Authorization": "Bearer " + cli_secret}, json={"translations": translations})
        if response.status_code == 200:
            return {"success": True, "message": "Language initialized successfully", "translations": response.json()["translations"]}
        else: 
            return {"success": False, "message": "Language initialization failed"}
        
    @staticmethod
    async def import_language(secret_key, language_code, content):
        """
        Import language translations from JSON or ARB file
        """
        url = f"{API.BASE_URL}/api/cli/importLanguage"
        payload = {
            "languageCode": language_code,
            "content": json.dumps(content),
            "format": "json"
        }
        
        response =  requests.post(
            url,
            headers={"Authorization": "Bearer " + secret_key},
            json=payload
        )
        
        if response.status_code == 200:
            return True, None
        else:
            error_message = response.json().get('message', 'Unknown error occurred')
            return False, error_message
        
    async def generate_keys(secret_key:str, values:list[str]) -> dict:
        url = f"{API.BASE_URL}/api/cli/generateKeys"
        headers = {"Authorization": "Bearer " + secret_key}
        response = requests.post(url, json={"values": values}, headers=headers)
        
        if response.status_code == 200:
            return response.json()["values"]
        else:
            error_message = response.json().get('message', 'Unknown error occurred')
            raise Exception(error_message)
        