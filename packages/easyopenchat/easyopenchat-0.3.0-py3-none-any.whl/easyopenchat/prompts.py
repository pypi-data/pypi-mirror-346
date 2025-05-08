
# from jinja2 import Template

# class PromptTemplate:
#     def __init__(self, template_str):
#         self.template = Template(template_str)

#     def render(self, **kwargs):
#         return self.template.render(**kwargs)



from jinja2 import Template, Environment, FileSystemLoader
import os

class PromptTemplate:
    def __init__(self, template_str=None, template_name=None):
        """
        Initialize a prompt template.
        
        Args:
            template_str (str): Raw template string.
            template_name (str): Name of template file in templates directory.
        """
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        if template_name:
            self.template = self.env.get_template(f"{template_name}.j2")
        elif template_str:
            self.template = Template(template_str)
        else:
            raise ValueError("Either template_str or template_name must be provided")

    def render(self, **kwargs):
        """
        Render the template with provided variables.
        
        Returns:
            str: Rendered prompt.
        """
        return self.template.render(**kwargs)