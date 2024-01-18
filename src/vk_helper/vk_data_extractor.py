import vk
from dotenv import load_dotenv
import os, re
from urllib.parse import urlparse
from .errors import InvalidLink, PageNotFound
import requests
from html import unescape
from datetime import datetime

load_dotenv()


class VkDataExtractor:
    """
    This class is a VK data extractor that retrieves information about a VK page based on a provided URL.

    Attributes:
    - name (str): The name of the VK page.
    - photo (str): The URL of the page's profile photo.
    - page_type (str): The type of the VK page (either "user" or "group").
    - id (int): The ID of the VK page.
    - created_date (str): The creation date of the VK page.

    """

    name: str
    photo: str
    page_type: str
    id: int
    created_date: str

    VK_TOKEN = os.getenv("VK_API_TOKEN")

    def __init__(self, url: str) -> None:
        self.api = vk.API(self.VK_TOKEN, v=5.131)
        if self._validate_url(url) and self._is_page_exists(url):
            (
                self.page_type,
                self.id,
            ) = (
                self._page_info["type"],
                self._page_info["object_id"],
            )
            self._get_page_data()

    def _validate_url(self, url: str) -> bool:
        vk_regex = re.compile(r"^(https?://)?(www\.)?vk\.com/[^/?]+$")
        if not vk_regex.match(url):
            raise InvalidLink(url)
        return True

    def _is_page_exists(self, url: str) -> bool:
        if self._get_page_info(self._get_username(url)) == []:
            raise PageNotFound(url)
        return True

    def _get_username(self, url: str) -> str:
        parsed_url = urlparse(url)
        self._username = parsed_url.path.strip("/")
        return self._username

    def _get_page_info(self, username: str) -> dict:
        self._page_info = self.api.utils.resolveScreenName(screen_name=username)
        return self._page_info

    def _get_group_data(self):
        group_data = self.api.groups.getById(group_id=self.id, fields="photo_max_orig")
        self.name = group_data[0]["name"]
        self.photo = group_data[0]["photo_max_orig"]
        return group_data

    def _get_created_date(self):
        try:
            response = requests.get(f"https://vk.com/foaf.php?id={self.id}")
            response.raise_for_status()
            response_content = response.content.decode("WINDOWS-1251")
            response_content = unescape(response_content)
            # XML parser не смог корректно обрабатывать реквесты
            # пришлось костылять свой парсер))
            start_tag = '<ya:created dc:date="'
            end_quote = '"'

            start_index = response_content.find(start_tag)
            if start_index == -1:
                return None

            start_index += len(start_tag)
            end_index = response_content.find(end_quote, start_index)

            if end_index == -1:
                return None

            created_date = response_content[start_index:end_index]

            created_datetime = datetime.fromisoformat(created_date)
            formatted_date = created_datetime.strftime("%d-%m-%Y")
            return formatted_date
        except Exception:
            return None

    def _get_user_data(self):
        user_data = self.api.users.get(user_id=self.id, fields="photo_max_orig")
        self.name = user_data[0]["first_name"] + " " + user_data[0]["last_name"]
        self.photo = user_data[0]["photo_max_orig"]
        self.created_date = self._get_created_date()

    def _get_page_data(self):
        if self.page_type == "user":
            self._get_user_data()
        else:
            self._get_group_data()


if __name__ == "__main__":
    page = VkDataExtractor("http://vk.com/durov")
    output = (
        f"ID: {page.id}\nType: {page.page_type}\nName: {page.name}\nPhoto: {page.photo}"
    )
    if hasattr(page, "created_date"):
        output += f"\nCreated Date: {page.created_date}"
    print(output)
