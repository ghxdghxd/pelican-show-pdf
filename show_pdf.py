# -*- coding: utf-8 -*-
"""
show pdf
"""

import os
import re

from pelican import signals

def show_pdf(pdf_elem, curpath, linefeed='\n', delim=',', classes=[''], limit=5):
    words = pdf_elem.split(" ")
    if words[1] != "pdf":
        print(pdf_elem + "error!")
        return

    id = [id for id in words if "id" in id][0].split("id=")[1]
    src = [src for src in words if "src" in src][0].split("src=")[1]
    
    pdf_string = '<embed id=' + id + ' src=' + src + ' type="application/pdf" width = "100%" height = "600px" internalinstanceid = "17">'

    return pdf_string


def loadpdf(data_passed_from_pelican):
    """A function to read through each page and post as it comes through from Pelican, 
        find all instances of triple-backtick (```...```) code blocks, 
        and add an HTML wrapper to each line of each of those code blocks"""

    # If the item passed from Pelican has a "content" attribute (i.e., if it's not an image file or something else like that)
    if data_passed_from_pelican._content:
        # NOTE: `data_passed_from_pelican.content` seems to be read-only, whereas `data_passed_from_pelican._content` is able to be overwritten. (Mentioned by Jacob Levernier in his Better Code-Block Line Numbering Plugin)
        page_content = data_passed_from_pelican._content
        curpath = os.path.dirname(data_passed_from_pelican.get_relative_source_path())
    else:
        # Exit the function, essentially passing over the (non-text) file.
        return

    # re.DOTALL puts python's regular expression engine ('re') into a mode where a dot ('.') matches absolutely anything, including newline characters.
    all_pdf_elements = re.findall('{% pdf .*? %}', page_content, re.DOTALL)

    if(len(all_pdf_elements) > 0):
        updated_page_content = page_content

    for pdf_elem in all_pdf_elements:
        replacement = show_pdf(pdf_elem, curpath)
        updated_page_content = updated_page_content.replace(pdf_elem, replacement)

        data_passed_from_pelican._content = updated_page_content

def register():
    signals.content_object_init.connect(loadpdf)
