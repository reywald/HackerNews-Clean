from django.views.generic import TemplateView



class HomePageView(TemplateView):
    """ Renders the home page 
    
    Parameters
    ----------
    template_name : The name of the template .html file to use
    """
    template_name = "index.html"
