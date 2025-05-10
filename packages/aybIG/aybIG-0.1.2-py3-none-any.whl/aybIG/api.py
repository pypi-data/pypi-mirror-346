import requests
import json
import re
import os
import random
from uuid import uuid4
from secrets import token_hex
from user_agent import generate_user_agent  # Assuming you have a way to generate a user-agent string


class usrinfo:
    @staticmethod
    def getuid(user):
        try:
            # Simulate random IP and proxy (can be customized)
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
            port = random.choice(pl)
            proxy = ip + ":" + str(port)
            uid = uuid4().hex.upper()
            csr = token_hex(8) * 2
            miid = token_hex(13).upper()
            dtr = token_hex(13)

            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ar,en;q=0.9',
                'cookie': f'ig_did={uid}; datr={dtr}; mid={miid}; ig_nrcb=1; csrftoken={csr}; ds_user_id=56985317140; dpr=1.25',
                'referer': f'https://www.instagram.com/{user}/?hl=ar',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.138", "Google Chrome";v="112.0.5615.138", "Not:A-Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': generate_user_agent(),
                'viewport-width': '1051',
                'x-asbd-id': '198387',
                'x-csrftoken': csr,
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
            }

            # Request to get the user ID from the username
            rr = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user}', headers=headers, proxies={'http': proxy})

            # Extract user ID from the response
            user_id = rr.json()['data']['user']['id']
            return user_id
        except Exception as e:
            print(f"Error fetching user ID for username {user}: {e}")
            return None

    @staticmethod
    def getinf(user):
        # Get user ID from the username
        user_id = usrinfo.getuid(user)
        if not user_id:
            return None
        
        # Fetch the token from environment variable
        token = os.getenv('IG_BEARER_TOKEN')
        if not token:
            raise ValueError("Instagram token not found in environment variable IG_BEARER_TOKEN")

        headers = {
            'Host': 'i.instagram.com',
            'User-Agent': 'Instagram 278.0.0.22.117 Android (25/7.1.2; ...)',
            'Authorization': f'Bearer IGT:2:{token}',
        }

        data = {
            'is_prefetch': 'false',
            'entry_point': 'profile',
            'from_module': 'search_typeahead',
        }

        try:
            # Make the request to fetch the user data
            response = requests.post(
                f'https://i.instagram.com/api/v1/users/{user_id}/info_stream/',
                headers=headers,
                data=data
            )
            response.raise_for_status()  # Raise an exception if the request was unsuccessful

            # Extract user info from the response text
            user_info = usrinfo.extract_user_info(response.text)

            # Add "dev by @rootsecc" to the information
            user_info["dev_by"] = "dev by @rootsecc"

            # Print the user information along with the developer message
            #print(json.dumps(user_info, indent=4))
            return user_info
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def extract_user_info(json_response):
        # Split the response into individual JSON objects
        json_objects = re.split(r'}\s*{', json_response.strip())
        json_objects = [json_objects[0] + '}' if i == 0 else '{' + obj + '}' if i == len(json_objects) - 1 else '{' + obj + '}' for i, obj in enumerate(json_objects)]
        
        user_info = {}
        for json_str in json_objects:
            try:
                # Parse each JSON object
                data = json.loads(json_str)
                user = data.get("user", {})

                # Extract relevant user information
                if "username" in user:
                    user_info["username"] = user.get("username", "")
                if "full_name" in user:
                    user_info["full_name"] = user.get("full_name", "")
                if "pk" in user:
                    user_info["user_id"] = user.get("pk", "")
                if "is_private" in user:
                    user_info["is_private"] = user.get("is_private", False)
                if "is_verified" in user:
                    user_info["is_verified"] = user.get("is_verified", False)
                if "is_business" in user:
                    user_info["is_business"] = user.get("is_business", False)
                if "account_type" in user:
                    user_info["account_type"] = "business" if user.get("is_business") else ("creator" if user.get("account_type") == 2 else "personal")
                if "biography" in user:
                    user_info["biography"] = user.get("biography", "")
                if "category" in user:
                    user_info["category"] = user.get("category", "")
                if "hd_profile_pic_url_info" in user or "profile_pic_url" in user:
                    hd_profile_pic = user.get("hd_profile_pic_url_info", {}).get("url", "")
                    user_info["profile_pic_url"] = hd_profile_pic if hd_profile_pic else user.get("profile_pic_url", "")
                if "follower_count" in user:
                    user_info["follower_count"] = user.get("follower_count", 0)
                if "following_count" in user:
                    user_info["following_count"] = user.get("following_count", 0)
                if "media_count" in user:
                    user_info["media_count"] = user.get("media_count", 0)
                if "total_clips_count" in user:
                    user_info["reels_count"] = user.get("total_clips_count", 0)
                if "total_igtv_videos" in user:
                    user_info["igtv_count"] = user.get("total_igtv_videos", 0)
                if "external_url" in user:
                    user_info["external_url"] = user.get("external_url", "")
                if "bio_links" in user:
                    user_info["bio_links"] = [
                        {
                            "title": link.get("title", ""),
                            "url": link.get("url", "")
                        } for link in user.get("bio_links", [])
                    ]
            except json.JSONDecodeError:
                continue
        return user_info if user_info else None
