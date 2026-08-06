
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        out = ""
        if self.tag:
            out = out + f"tag = {self.tag}\n"
        if self.value:
            out = out + f"value = {self.value}\n"
        if self.children:
             out = out + f"children = {self.children}\n"
        if self.props:
             out = out + f"properties = {self.props}\n"
        return out

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        out = ""
        if not self.props:
            return out
        for prop in self.props:
            out = out + f" {prop}=\"{self.props[prop]}\""
        return out

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />" 
        if not self.value:
            raise ValueError("No text for child node provided")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        out = ""
        if self.tag:
            out = out + f"tag = {self.tag}\n"
        if self.value:
            out = out + f"value = {self.value}\n"
        if self.props:
             out = out + f"properties = {self.props}\n"
        return out

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag for parent node provided")
        if not self.children:
            raise ValueError("No children for parent node provided")
        out = f"<{self.tag}>"
        for child in self.children:
            out = out + child.to_html()
        return out + f"</{self.tag}>"