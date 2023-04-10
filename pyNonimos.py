#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Projeto da Prefeitura de Santa Maria de Jetibá - ES, para tarjar e anonimizar documento PDF de forma automatizada. 

Usando a bliblioteca fitz (pymupdf), tkinter e os
    
@autor: Ewerton Lyrio Nascimento
"""

# Import Libraries
from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz


def extract_info(input_file: str):
    """
    Extrai informações do arquivo.
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    output = {
        "File": input_file, "Encrypted": ("True" if pdfDoc.isEncrypted else "False")
    }
    # If PDF is encrypted the file metadata cannot be extracted
    if not pdfDoc.isEncrypted:
        for key, value in pdfDoc.metadata.items():
            output[key] = value

    with open('logs\log.txt', 'a', encoding="utf-8") as log:
        log.write("## Informações do Arquivo ############################################\n")
        log.write("\n".join("{}:{}".format(i, j) for i, j in output.items()) )
        log.write("\n**********************************************************************\n")

    return True, output

def search_for_text(lines, search_str):
    """
    Search for the search string within the document lines
    """
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result

def redact_matching_data(page, matched_values):
    """
    Redacts matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.search_for(val)
        # Redact matching values
        [page.add_redact_annot(area, text=" ", fill=(0, 0, 0))
         for area in matching_val_area]
    # Apply the redaction
    page.apply_redactions()
    return matches_found

def process_data(input_file: str, output_file: str, search_str: str, pages: Tuple = None, action: str = 'Highlight'):
    """
    Process the pages of the PDF File
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0
    # Iterate through pages
    for pg in range(pdfDoc.page_count):
        # If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        # Select the page
        page = pdfDoc[pg]
        # Get Matching Data
        # Split page by lines
        page_lines = page.get_text("text").split('\n')
        for palavra in search_str:
            matched_values = search_for_text(page_lines, palavra)
            matches_found = redact_matching_data(page, matched_values)
            total_matches += matches_found

    with open('logs\log.txt', 'a', encoding='utf-8') as log:
        log.write(f"{total_matches} Correspondência(s) encontradas(s) para a(s) palavra(s) {search_str}. Com o arquivo de entrada: {input_file} \n")
        log.write(
            "\n######################################################################\n")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())

def process_file(**kwargs):
    """
    To process one single file
    Redact, Frame, Highlight... one PDF File
    Remove Highlights from a single PDF File
    """
    input_file = kwargs.get('input_file')
    output_file = kwargs.get('output_file')
    if output_file is None:
        arquivo = os.path.basename(input_file)
        caminho = os.path.dirname(input_file)
        output_file =caminho+'\/anonimizado_'+arquivo
    
    pages = kwargs.get('pages')
    # Redact
    action = kwargs.get('action')

    search_str = kwargs.get('search_str')
    
    process_data(input_file=input_file, output_file=output_file,
                     search_str=search_str, pages=pages, action=action)

#if __name__ == '__main__':

    #input_file = 'sample2.pdf'
    #output_file = 'anonimizado_'+input_file
    #search_str ='Ewerton'
   # pages= None
   # action = 'Redact'
    
   # if os.path.isfile(input_file):
    #    extract_info(input_file=input_file)
        # Process a file
   #     process_file(
    #        input_file=input_file, output_file=output_file,
    #        search_str=search_str,
    #        pages=pages, action=action
    #    )