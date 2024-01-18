class InvalidLink(Exception):
    def __init__(self, link):
        self.link = link
        super().__init__(f"Ссылка '{self.link}' не валидна.")


class PageNotFound(Exception):
    def __init__(self, page_link):
        self.page_link = page_link
        super().__init__(f"Страница {self.page_link} не существует")
