import json
import requests
import os

class GameUploader:

    def __init__(self, config_file="config.json"):
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.GAME_UPLOADING_COOKIE = self.config["GAME_UPLOADING_COOKIE"]
        self.MAIN_MODULE_UPLOADING_COOKIE = self.config["MAIN_MODULE_UPLOADING_COOKIE"]
        self.MAIN_MODULE_UPLOADING_GROUPID = self.config["MAIN_MODULE_UPLOADING_GROUPID"]
        self.COMMUNITY_GROUP_ID = self.config["COMMUNITY_GROUP_ID"]
        self.GAME_NAME = self.config["GAME_NAME"]
        self.GAME_DESCRIPTION = self.config["GAME_DESCRIPTION"]
        self.GAME_DESCRIPTION = """✅ | COMMUNITY GROUP: https://www.roblox.com/groups/33843149/Cosmic-studio#!/about
        💸  | GAMEPASSES: 
        All gamepasses are free in Brick Bronze, simply join our official community group above!
        ❤️ | FREE MONSTER: 
        For a Monster, join the official Community Group, and then head over to the far right house in Silvent City and talk to the man inside.
        💳 | CODES:
        For all codes in Brick Bronze, join our official Community Server below, which can be found in our Social Links in the game's overview!
        🔥 | DATA: 
        All data in this game is automatically restored and used in the next upload.
        💬 | TAGS:
        Pokemon, Pokemon Brick Bronze, Project Bronze, Project Brick Bronze, Project Pokemon, Pokemon Brick Bronze, Project Ultima, Pokemon, Pikachu, Project Bronze Forever, Project Pokemon, Project, Pokemon, Brick, Bronze, Brick Bronze, Bronze Forever, Mewtwo, Bronze Pokemon, Brick Bronze Pokemon, Forever Bronze, Forever, Roria, Roria League
        """

        self.MAX_SERVER_SIZE = self.config["MAX_SERVER_SIZE"]
        self.icon_file = self.config["ICON_FILE_PATH"]
        self.thumbnail_file = self.config["THUMBNAIL_FILE_PATH"]
        self.game_file = self.config["GAME_FILE_PATH"]
        self.MAIN_MODULE_FILE_PATH = self.config["MAIN_MODULE_FILE_PATH"]
        self.DISGUISE_FILE_PATH = self.config["DISGUISE_FILE_PATH"]
        self.DEFAULT_HEADERS = {
            "User-Agent": "Roblox/WinInet",
            "Accept": "application/json",
            "cookie": f".ROBLOSECURITY={self.GAME_UPLOADING_COOKIE}",
        }
        
        self.DEV_RPODUCTS = [{"name": "Starter", "price": 15},{"name": "TenBP", "price": 10},{"name": "FiftyBP", "price": 20},{"name": "TwoHundredBP", "price": 50},{"name": "TwoThousandBP", "price": 75},{"name": "UMV1", "price": 5},{"name": "UMV3", "price": 10},{"name": "UMV6", "price": 15},{"name": "_10kP", "price": 10},{"name": "_50kP", "price": 40},{"name": "_100kP", "price": 75},{"name": "_200kP", "price": 120},{"name": "PBSpins1", "price": 5},{"name": "PBSpins5", "price": 20},{"name": "PBSpins10", "price": 30},{"name": "AshGreninja", "price": 75},{"name": "Hoverboard", "price": 10},{"name": "MasterBall", "price": 10},{"name": "LottoTicket", "price": 15},{"name": "BuyTix", "price": 125},{"name": "RouletteSpinBasic", "price": 7},{"name": "RouletteSpinBronze", "price": 25},{"name": "RouletteSpinSilver", "price": 60},{"name": "RouletteSpinGold", "price": 85},{"name": "RouletteSpinDiamond", "price": 125},{"name": "EXP1", "price": 15},{"name": "EXP2", "price": 20},{"name": "Hatching1", "price": 10},{"name": "Hatching2", "price": 15},{"name": "pokedollars1", "price": 20},{"name": "pokedollars2", "price": 35},{"name": "EV1", "price": 10},{"name": "EV2", "price": 15},{"name": "ShinyBoosts", "price": 30},{"name": "Legendaries", "price": 45}]

        if self.MAIN_MODULE_UPLOADING_GROUPID == 0:
            self.MAIN_MODULE_UPLOADING_GROUPID = ""

    def send_webhook_request(self,webhook_url, data):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=data, headers=headers)
        if response.status_code == 204:
            print("POST request sent successfully.")
        else:
            print(f"Error sending POST request. Status code: {response.status_code}")
            print(response.text)

    def upload_place(self,place_id, game_file):
        url = f"https://data.roblox.com/Data/Upload.ashx?assetid={place_id}&type=Place&name=Game.rbxl"

        headers = {
            "Content-Type": "application/octet-stream",
            "Accept": "application/json",
            "User-Agent": "Roblox/WinInet",
            "X-CSRF-Token": self.get_csrf_token(),
            "cookie": f".ROBLOSECURITY={self.GAME_UPLOADING_COOKIE}",
        }

        upload_response = requests.post(url, data=game_file, headers=headers)

        if upload_response.status_code == 200:
            try:
                parsed = upload_response.json()
                return parsed
            except json.JSONDecodeError:
                raise ValueError(f'Could not parse JSON, returned body: {upload_response.text}')
        else:
            print(upload_response.status_code)
            raise ValueError('Upload failed, confirm that all item options, asset options, and upload data are valid.')
        
    def create_place(self,universe_id):
        # URL for creating a new place in Roblox
        url = f"https://www.roblox.com/ide/places/createV2?universeId={universe_id}&templatePlaceIdToUse=95206881"

        # Headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Roblox/WinInet",
            "X-CSRF-Token": self.get_csrf_token(),
            "cookie": f".ROBLOSECURITY={self.GAME_UPLOADING_COOKIE}",
        }

        try:
            # Send POST request
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Raise error for any bad response status

            # Parse response JSON and extract PlaceId
            place_id = response.json()["PlaceId"]
            return place_id
        except requests.exceptions.RequestException as e:
            print(f"Failed to create place: {e}")
            return None
        
    def anims_upload(self,data,name):
        url = f"https://www.roblox.com/ide/publish/uploadnewanimation?AllID=1"
        headers = {
        "X-CSRF-Token": self.get_csrf_token(),
            'Content-Type': 'application/xml',
            'User-Agent': 'RobloxStudio/WinInet RobloxApp/0.483.1.425021 (GlobalDist; RobloxDirectDownload)',
            "cookie": f".ROBLOSECURITY={self.GAME_UPLOADING_COOKIE}",
        }
        body = data
        params = {
                'assetTypeName': 'Animation',
                'genreTypeId': 1,
                'name': name,
                'description': '',
                'ispublic': True,
                'allowComments': True,
                'groupId': ''
            }

        response = requests.post(url, data=body, headers=headers, params=params)
        if response.status_code == 200:
            result_id = int(response.text)
            return result_id
    def run(self):
        print(self.get_csrf_token(self.MAIN_MODULE_UPLOADING_COOKIE))
        universe_response = self.create_universe()
        universe_id = universe_response["universeId"]
        root_place_id = universe_response["rootPlaceId"]
        self.activate_universe(universe_id)

        self.set_server_size(root_place_id, int(self.MAX_SERVER_SIZE))

        self.upload_icon_to_roblox(self.icon_file, root_place_id, self.GAME_UPLOADING_COOKIE)

        self.upload_thumbnail_to_roblox(self.thumbnail_file, root_place_id, self.GAME_UPLOADING_COOKIE)

        self.enable_api_services(self.GAME_NAME, self.GAME_DESCRIPTION, universe_id, self.GAME_UPLOADING_COOKIE)
        main_game_id = self.create_place(universe_id=universe_id)
        self.upload_dev_products(universe_id)

        main_module_id = self.upload_main_module()["AssetId"]

        self.save_results_to_server([main_module_id],"mainmodule")
        self.save_results_to_server([main_game_id],"placeid")
        
        with open(self.DISGUISE_FILE_PATH, "rb") as file:
            self.upload_place(root_place_id,file.read())

        with open(self.game_file, "rb") as file:
            self.upload_place(main_game_id,file.read())

        self.set_server_size(main_module_id, int(self.MAX_SERVER_SIZE))

        self.upload_icon_to_roblox(self.icon_file, main_module_id, self.GAME_UPLOADING_COOKIE)

        self.upload_thumbnail_to_roblox(self.thumbnail_file, main_module_id, self.GAME_UPLOADING_COOKIE)

        #self.send_webhook_request("https://discord.com/api/webhooks/1196511689655464037/FzFNtsB1zkXd8R_U85cPNelf3CH8tfMh-vlz3CoEepv5CaydjHv4xmoFmctyVd8nQs39",data={
        #     "content": f"https://www.roblox.com/games/{root_place_id}"
        #})
        #self.send_webhook_request("https://discord.com/api/webhooks/1196512085799092295/8vv-9v6C1nSSbR-b89Eqn8gRcFy9kdavGA8_m7SBwLjayJrHJ4NDm6VNMJNVLS7oJoDV",data = {
        #    "content": "@every1\n\n**__The game has been reuploaded. Everything should work as intended.__**\nPlay the game in: <#1190444089624244419>\nIf you come across any, report any worthwhile bugs in: <#1190645249488453642>\n\nThank you for your patience."
        #})
        print("Run completed successfully! id:"+root_place_id)

    def create_universe(self):
        try:
            url = "https://apis.roblox.com/universes/v1/universes/create"
            headers = {
                **self.DEFAULT_HEADERS,
                "Content-Type": "application/json",
                "X-CSRF-Token": self.get_csrf_token(),
            }

            response = requests.post(
                url,
                json={"templatePlaceId": 95206881},
                headers=headers
            )
            print(response.text)
            return response.json()
        except Exception as error:
            raise ValueError("Error creating the universe: " + str(error))

    def activate_universe(self, universe_id):
        config = {
            "method": "post",
            "url": f"https://develop.roblox.com/v1/universes/{universe_id}/activate",
            "headers": {
                **self.DEFAULT_HEADERS,
                "X-CSRF-Token": self.get_csrf_token(),
            },
        }

        try:
            response = requests.request(**config)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Failed to activate universe {universe_id}: {error}")

    def get_csrf_token(self, cookie=None):
        return requests.post("https://auth.roblox.com/v2/login",
                         headers=self.DEFAULT_HEADERS if cookie is None else {
                             "User-Agent": "Roblox/WinInet",
                             "Accept": "application/json",
                             "cookie": f".ROBLOSECURITY={cookie}",
                         }).headers['X-CSRF-TOKEN']

    
    def upload_dev_products(self, universe_id):
        results = {} 

        for product in self.DEV_RPODUCTS:
            name = product["name"]
            description = " "
            price_in_robux = product["price"]
            prod = self.create_developer_product(
                universe_id, name, price_in_robux, description
            )
            prod = self.get_id_from_response_data(prod)
            
            results[name] = prod 
        for filename in os.listdir("./animations"):
            if filename.endswith(".rbxm"): 
                animation_path = os.path.join("./animations", filename)
                with open(animation_path, 'rb') as file:
                    content = file.read()
                    name = os.path.splitext(os.path.basename(animation_path))[0]
                    results[name] = self.anims_upload(content,name) 
        self.save_results_to_server([results],"dev_products")


    def save_results_to_server(self,results, json_name):
        try:
            url = f"http://77.91.100.12:2656/upload/{json_name}"
            response = requests.post(url, json=results)
            response.raise_for_status()
            print("Results saved to the server successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to save results to the server: {e}")
       

    def create_developer_product(
        self, universe_id, product_name, product_price, product_description
    ):
        url = f"https://apis.roblox.com/developer-products/v1/universes/{universe_id}/developerproducts?name={product_name}&description={product_description}&priceInRobux={product_price}&description={product_description}"
        headers = {
                **self.DEFAULT_HEADERS,
                "Content-Type": "application/json",
                "X-CSRF-Token": self.get_csrf_token(),
            }
        response = requests.request("POST", url, headers=headers)
        try:
            return response.json()["id"]
        except:
            return 0
    def get_id_from_response_data(self, product_id):
        try:
            url = f"https://apis.roblox.com/developer-products/v1/developer-products/{product_id}"
            headers = {
                **self.DEFAULT_HEADERS,
                "Content-Type": "application/json",
                "X-CSRF-Token": self.get_csrf_token(),
            }
            response = requests.get(url, headers=headers)
            response_data = response.json()
            return response_data["id"]
        except Exception as error:
            print(error)
            return None



    
    def set_server_size(self, place_id, max_players):
        payload = {
            "maxPlayerCount": max_players,
            "socialSlotType": "Automatic",
            "customSocialSlotsCount": 10,
        }
        try:
            response = requests.patch(
                f"https://develop.roblox.com/v2/places/{place_id}",
                json=payload,
                headers={
                    **self.DEFAULT_HEADERS,
                    "X-CSRF-Token": self.get_csrf_token(),
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Failed to set server size of place {place_id}: {error}")

    def upload_icon_to_roblox(self, icon_file, place_id, cookie):
        files = {'iconImageFile': open(icon_file, 'rb')}
        data = {'placeId': place_id}
        headers = {
            **self.DEFAULT_HEADERS,
            "X-CSRF-Token": self.get_csrf_token(),
            'cookie': f'.ROBLOSECURITY={cookie}',
            'origin': 'https://create.roblox.com',
            'referer': 'https://create.roblox.com/'
        }

        try:
            response = requests.post(
                'https://www.roblox.com/places/icons/add-icon',
                files=files,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            print("Icon Uploaded Successfully!")
        except requests.exceptions.HTTPError as error:
            print(f"Failed To Add Icon: {error}")

    def upload_thumbnail_to_roblox(self, thumbnail_file, place_id, cookie):
        files = {'thumbnailImageFile': open(thumbnail_file, 'rb')}
        data = {'id': place_id}
        headers = {
            **self.DEFAULT_HEADERS,
            'X-CSRF-Token': self.get_csrf_token(),
            'cookie': f'.ROBLOSECURITY={cookie}',
            'origin': 'https://create.roblox.com',
            'referer': 'https://create.roblox.com/'
        }

        try:
            response = requests.post(
                'https://www.roblox.com/places/thumbnails/add-image',
                files=files,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            print("Thumbnail Uploaded Successfully!")
        except requests.exceptions.HTTPError as error:
            print(f"Failed To Upload Thumbnail: {error}")

    def enable_api_services(self, game_name, game_description, universe_id, cookie):
        url = f"https://develop.roblox.com/v2/universes/{universe_id}/configuration"
        headers = {
            **self.DEFAULT_HEADERS,
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={cookie}",
            "X-CSRF-Token": self.get_csrf_token(),
        }
        payload = {
            "name": game_name,
            "description": game_description,
            "studioAccessToApisAllowed": True,
        }

        try:
            response = requests.patch(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Failed To Enable API Services: {error}")
            return
    def upload_main_module(self):
        upload_headers = {
            **self.DEFAULT_HEADERS,
            "Content-Type": "application/octet-stream",
            "X-CSRF-Token": self.get_csrf_token(self.MAIN_MODULE_UPLOADING_COOKIE),
            "cookie": f".ROBLOSECURITY={self.MAIN_MODULE_UPLOADING_COOKIE}",
        }

        with open(self.MAIN_MODULE_FILE_PATH, "rb") as file:
            contents = file.read()

        upload_response = requests.post(
            f'https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1&name=MainModule&description=Main&ispublic=True&allowComments=False&groupId={str(self.MAIN_MODULE_UPLOADING_GROUPID)}',
            headers=upload_headers,
            data=contents
        )

        if upload_response.status_code == 200:
            try:
                parsed = upload_response.json()
                return parsed
            except json.JSONDecodeError:
                raise ValueError(f'Could not parse JSON, returned body: {upload_response.text}')
        else:
            print(upload_response.text)
            raise ValueError('Upload failed, confirm that all item options, asset options, and upload data are valid.')

# Run the uploader
uploader = GameUploader()
uploader.run()

"""
 for filename in os.listdir(directory):
            if filename.endswith(".animation"):  # Assuming all animation files have the .animation extension
                animation_path = os.path.join(directory, filename)"""