
# coding: utf-8

import pandas as pd
import os
import datetime


def build_sheet_url(doc_id, sheet_id):
    return f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=tsv&gid={sheet_id}'


def write_df_to_local(df, file_path):
    df.to_csv(file_path, sep='\t', index=False)

doc_id = '1yQSM7kXSDZcthXFZ0esCsdv-X3CnzVfzGJDpmfoYkWc'
sheet_id = '0'
sheet_url = build_sheet_url(doc_id, sheet_id)
publications = pd.read_csv(sheet_url, sep="\t", header=0, keep_default_na=False)
file_path = 'mfe_bib.tsv'
write_df_to_local(publications, file_path)


# ## Escape special characters
# 
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# In[4]:

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


# Delete all files from /_publications directory so we don't get duplicates on changes
import glob
files = glob.glob('../_publications/*.md')
for f in files:
    os.remove(f)

bibtex_str = ''

for row, item in publications.iterrows():
    
    year = item.Year

    month = item.Month
    if month == '':
        month = "12"
    else:
        month = str(datetime.datetime.strptime(item.Month, '%B').month).zfill(2)
    paper_id = item.Abbreviation
    filename = "{year}-{month}-{paper_id}".format(year=year, month=month, paper_id=paper_id)
    md_filename = "{}.md".format(filename)
    html_filename = "{}.html".format(filename)
    
    # YAML variables

    md = "---\ntitle: \"" + item.Title + '"'

    # Authors
    if ',' in item.Authors:
        authors_str = ''
        authors = item.Authors.split('and')
        for author in authors:
            last_name, first_name = author.split(',')
            authors_str += first_name.strip() + " " + last_name.strip() + " and "
        authors_str = authors_str[:-5]
    else:
        authors_str = item.Authors

    authors_str = authors_str.replace(' and ', ', ')

    md += "\nauthors: \"" + authors_str + '"'
    
    # Venue
    venue_dict = {
        "mitme": "Massachusetts Institute of Technology, Department of Mechanical Engineering",
        "iros": "IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)",
        "icra": "IEEE International Conference on Robotics and Automation (ICRA)",
        "icml": "International Conference on Machine Learning (ICML)",
        "corl": "Conference on Robot Learning (CoRL)",
        "ijrr": "International Journal of Robotics Research (IJRR)",
        "ieeeaccess": "IEEE Access",
        "tnnls": "IEEE Transactions on Neural Networks and Learning Systems (TNNLS)",
        "ral": "IEEE Robotics and Automation Letters (RA-L)",
        "tro": "IEEE Transactions on Robotics (TRO)",
        "thri": "ACM Transactions on Human-Robot Interaction (T-HRI)",
        "lcss": "IEEE Control Systems Letters (L-CSS)",
        "acc": "American Controls Conference (ACC)",
        "cdc": "IEEE Conference on Decision and Control (CDC)",
        "neurips": "Conference on Neural Information Processing Systems (NeurIPS)",
        "ojcs": "IEEE Open Journal of Control Systems (OJ-CSYS)",
    }

    if item.Venue in venue_dict:
        venue_str = venue_dict[item.Venue]
    else:
        venue_str = item.Venue

    md += "\nvenue: \"" + venue_str + '"'
    md += "\nyear: \"" + str(year) + '"'
    md += "\nstatus: \"" + item.Status + '"'
    md += "\narxiv: \"" + item['Arxiv link'] + '"'
    md += "\nofficial_link: \"" + item['Official Link'] + '"'
    md += "\ndoi: \"" + item['DOI'] + '"'
    md += "\nvolume: \"" + item['Volume'] + '"'
    md += "\nnumber: \"" + item['Number'] + '"'
    md += "\npages: \"" + item['Pages'] + '"'
    md += "\npublisher: \"" + item['Publisher'] + '"'
    md += "\nmonth: \"" + month + '"'
    md += "\naddress: \"" + item['Address'] + '"'
    md += "\ntype: \"" + item['Type'] + '"'
    md += "\nschool: \"" + item['School'] + '"'
    md += "\nawards: \"" + item['Awards'] + '"'
    md += "\nnotes: \"" + item['Notes'] + '"'
    
    include_on_website = "true" if item['Include on Website'] == "Y" else "false"
    md += "\ninclude_on_website: " + include_on_website
    
    md += "\nimage: \"" + item['Image Filename'] + '"'
    md += "\nlinks_to_code: \"" + item['Links to Code'] + '"'
    md += "\nlinks_to_video: \"" + item['Links to Video'] + '"'

    md += """\ncollection: publications"""
    
    md += """\npermalink: /publication/""" + html_filename
    
    md += "\n---"
    
    md_filename = os.path.basename(md_filename)
       
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)

    '''
    Generate bibtex entry in mfe.bib for that publication
    '''
    this_bibtex_str = ''

    bibtex_pages_str = None
    if item['Pages'] != "N/A":
        bibtex_pages_str = item['Pages']
    if item.Status != "published":
        bibtex_pages_str = '(' + item.Status + ')'

    bibtex_arxiv_link = None
    if item['Arxiv link'] == 'N/A' and item['Official Link'] != '':
        bibtex_arxiv_link = item['Official Link']
    elif item['Arxiv link'] != '' and item['Arxiv link'] != 'N/A':
        bibtex_arxiv_link = item['Arxiv link']

    bibtex_month = None
    if item['Month'] != '':
        bibtex_month = item['Month']

    bibtex_address = None
    if item['Address'] != '':
        bibtex_address = item['Address']

    bibtex_year = None
    if item['Year'] != '':
        bibtex_year = str(item['Year'])

    bibtex_volume = None
    if item['Volume'] != '':
        bibtex_volume = item['Volume']

    bibtex_number = None
    if item['Number'] != '':
        bibtex_number = item['Number']

    bibtex_doi = None
    if item['DOI'] != '':
        bibtex_doi = item['DOI']

    bibtex_awards = None
    if item['Awards'] != '' and item['Awards'] != 'N/A':
        bibtex_awards = item['Awards']

    bibtex_school = None
    if item['School'] != '' and item['School'] != 'N/A':
        bibtex_school = "Massachusetts Institute of Technology, Department of Mechanical Engineering"

    if item.Type == "conference" or item.Type == "workshop":
        this_bibtex_str += '\n@inproceedings{' + item.Abbreviation + ','
        this_bibtex_str += '\n  entrysubtype = {' + item.Type + '},'
        this_bibtex_str += '\n  Author = {' + item.Authors + '},'
        this_bibtex_str += '\n  Booktitle = {' + venue_str + '},'
        this_bibtex_str += '\n  Title = {' + item['Title'] + '},'
        if bibtex_pages_str:
            this_bibtex_str += '\n  Pages = {' + bibtex_pages_str + '},'
        if bibtex_month:
            this_bibtex_str += '\n  Month = {' + bibtex_month + '},'
        if bibtex_address:
            this_bibtex_str += '\n  Address = {' + bibtex_address + '},'
        if bibtex_year:
            this_bibtex_str += '\n  Year = {' + bibtex_year + '},'
        if bibtex_arxiv_link:
            this_bibtex_str += '\n  Url = {' + bibtex_arxiv_link + '},'
        if bibtex_doi:
            this_bibtex_str += '\n  Doi = {' + bibtex_doi + '},'
        if bibtex_awards:
            this_bibtex_str += '\n  awards = {' + bibtex_awards + '},'
        this_bibtex_str += '\n}\n'
    elif item.Type == "journal":
        this_bibtex_str += '\n@article{' + item.Abbreviation + ','
        this_bibtex_str += '\n  entrysubtype = {' + item.Type + '},'
        this_bibtex_str += '\n  Author = {' + item.Authors + '},'
        this_bibtex_str += '\n  Journal = {' + venue_str + '},'
        this_bibtex_str += '\n  Title = {' + item['Title'] + '},'
        if bibtex_pages_str:
            this_bibtex_str += '\n  Pages = {' + bibtex_pages_str + '},'
        if bibtex_year:
            this_bibtex_str += '\n  Year = {' + bibtex_year + '},'
        if bibtex_volume:
            this_bibtex_str += '\n  Volume = {' + bibtex_volume + '},'
        if bibtex_number:
            this_bibtex_str += '\n  Number = {' + bibtex_number + '},'
        if bibtex_arxiv_link:
            this_bibtex_str += '\n  Url = {' + bibtex_arxiv_link + '},'
        if bibtex_doi:
            this_bibtex_str += '\n  Doi = {' + bibtex_doi + '},'
        if bibtex_awards:
            this_bibtex_str += '\n  awards = {' + bibtex_awards + '},'
        this_bibtex_str += '\n}\n'
    elif item.Type == "mastersthesis" or item.Type == "phdthesis":
        this_bibtex_str += '\n@' + item.Type + '{' + item.Abbreviation + ','
        this_bibtex_str += '\n  Author = {' + item.Authors + '},'
        this_bibtex_str += '\n  School = {' + bibtex_school + '},'
        this_bibtex_str += '\n  Title = {' + item['Title'] + '},'
        if bibtex_month:
            this_bibtex_str += '\n  Month = {' + bibtex_month + '},'
        if bibtex_year:
            this_bibtex_str += '\n  Year = {' + bibtex_year + '},'
        if bibtex_arxiv_link:
            this_bibtex_str += '\n  Url = {' + bibtex_arxiv_link + '},'
        this_bibtex_str += '\n}\n'

    bibtex_str += this_bibtex_str

bibtex_str = bibtex_str[1:]
with open("../mfe.bib", "w") as f:
    f.write(bibtex_str)
