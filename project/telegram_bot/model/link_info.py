class LinkInfo:
    def __init__(self, id, name, link):
        self.id = id
        self.name = name
        self.link = link

    def __repr__(self):
        return f"LinkInfo(id={self.id}, name='{self.name}', link='{self.link}')"


def parse_linkinfo_json(data):
    return [LinkInfo(**item) for item in data]
