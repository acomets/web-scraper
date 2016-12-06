"""
Author: Antoine Comets
Date: 12/05/2016

This file contains the source code for pdfgen which generates a pdf with the relevant extracts
returned by relevantExtracts given as input, using the reportlib library.
"""

from os import mkdir, chdir
from os.path import exists, join
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm
from reportlab.platypus.paragraph import Paragraph

h1 = PS(name = 'Heading1',
              fontSize = 12,
              leading = 14)

def pdfgen(relevant_extracts, sector, keywords):
    today = datetime.datetime.today()
    today.replace(second=0, microsecond=0)
    
    outputdir = join('..', 'output')
    if not exists(outputdir):
        mkdir(outputdir)
    chdir(outputdir)
    
    doc = SimpleDocTemplate('%s_%s.pdf' % (sector, today.strftime("%Y-%m-%d_%H.%M")))
    template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')])
    doc.addPageTemplates(template)
    
    Story = [Spacer(1,0.5*inch)]
    styleSheet=getSampleStyleSheet()
    style = styleSheet['BodyText']
    title = Paragraph('<para align=center><b>%s Industry Earnings Call Transcripts Report</b></para>' % sector,
                      style)
    Story.append(title)
    subtitle = Paragraph('<para align=center>Keywords: %s</para>' % ", ".join(keywords),
                         style)
    Story.append(subtitle)
    Story.append(Spacer(1,0.5*inch))
    
    
    for extract in relevant_extracts:
        Story.append(Paragraph("From %s" % extract["title"], h1))
        Story.append(Paragraph("Published on %s at %s" % (extract["date"], extract["time"]), h1))
        text = Preformatted(extract["bodyContent"].encode('utf8'), style, maxLineLength=100)
        Story.append(text)
        Story.append(Spacer(1,0.2*inch))
    
    doc.build(Story)
    

