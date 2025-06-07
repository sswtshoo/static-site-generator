class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        parts = [f'{key}="{value}"' for key, value in self.props.items()]
        return " ".join(parts)
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value:str, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("missing value")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>" if self.tag != 'img' else f"<{self.tag} {props_str}/>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>" if self.tag != 'img' else f"<{self.tag}/>"
        

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict = None):
        super().__init__(tag = tag, children = children, props = props)
    
    def to_html(self):

        if self.tag is None:
            raise ValueError("missing value")
        
        # for child in self.children:
        #     if child.value is None:
        #         raise ValueError("one or more children are missing required value property")

        
        self_props = self.props_to_html()
        if self_props:
            open_tag = f"<{self.tag} {self_props}>"
        else:
            open_tag = f"<{self.tag}>"
        
        inner_html = ""
        
        for child in self.children:
            inner_html += child.to_html()

        return f"{open_tag}{inner_html}</{self.tag}>"
        
    def __eq__(self, other):
        return True if self.to_html() == other.to_html() else False
