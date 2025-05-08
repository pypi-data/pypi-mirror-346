
from jinja2 import Template

class PromptTemplate:
    def __init__(self, template_str):
        self.template = Template(template_str)

    def render(self, **kwargs):
        return self.template.render(**kwargs)
