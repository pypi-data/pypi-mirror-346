import requests
import json
import re

class usrinfo:
    @staticmethod
    def getinf(user_id):
        # Headers and data for the request
        headers = {
            'Host': 'i.instagram.com',
            'User-Agent': 'Instagram 278.0.0.22.117 Android (25/7.1.2; 240dpi; 720x1280; Asus; ASUS_I003DD; ASUS_I003DD; intel; en_US; 471827263)',
            'Authorization': 'Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjM5MDUzNTY3OTUiLCJzZXNzaW9uaWQiOiI2MzkwNTM1Njc5NSUzQVZXN1JDZ0k4eHRLMVZtJTNBMTMlM0FBWWNHaGo2M1lqNzhJUFd1UDRNTDRCRy1yX2RveVdsNmFYQzJ1aWY4TUEifQ==',
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

            # Print "dev @rootsecc" at the end
            print("dev @rootsecc")

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
