# importing the necessary libraries
from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template


# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}, raw=False):
    """
    Convert an HTML template to a PDF document.

    This function takes an HTML template source, fills it with context data, and converts it into a PDF document.
    The generated PDF can be returned as bytes or as an HttpResponse object, depending on the 'raw' parameter.

    Args:
        template_src (str): The path to the HTML template or the HTML content itself.
        context_dict (dict, optional): A dictionary containing context data to populate
            the template variables. Default is an empty dictionary.
        raw (bool, optional): If True, the raw PDF bytes will be returned. If False,
            an HttpResponse object with the PDF content will be returned. Default is False.

    Returns:
        bytes or HttpResponse or None: Depending on the 'raw' parameter, the function returns either the raw PDF bytes,
        an HttpResponse containing the PDF content, or None if there was an error during the PDF generation.

    Note:
        This function requires the 'get_template' function to fetch the HTML template, and the 'pisa' module to convert
        HTML to PDF.

    Example:
        pdf_bytes = html_to_pdf('template.html', {'variable': 'value'})
        response = html_to_pdf('template.html', {'variable': 'value'}, raw=False)
    """
    
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        if raw:
            return result.getvalue()
        else:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None