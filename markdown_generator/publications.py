
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# 
# TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
# 

# ## Data format
# 
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# 
# - `excerpt` and `paper_url` can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`


# ## Import pandas
# 
# We are using the very handy pandas library for dataframes.

# In[2]:

import pandas as pd


# ## Import TSV
# 
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# 
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# In[3]:

publications = pd.read_csv("mfe_bib.tsv", sep="\t", header=0, keep_default_na=False)


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


# ## Creating the markdown files
# 
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page. If you don't want something to appear (like the "Recommended citation")

# In[5]:

import os
import datetime
for row, item in publications.iterrows():
    
    year = item.Year

    month = item.Month
    if month == '':
        month = "01"
    else:
        month = str(datetime.datetime.strptime(item.Month, '%B').month).zfill(2)
    paper_id = item.Abbreviation
    filename = "{year}-{month}-{paper_id}".format(year=year, month=month, paper_id=paper_id)
    md_filename = "{}.md".format(filename)
    html_filename = "{}.html".format(filename)
    
    ## YAML variables

    md = "---\ntitle: \""   + item.Title + '"'

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

    md += "\nauthors: \""   + authors_str + '"'
    
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
        "tro": "IEEE Transactions on Robotics and Automation (TRO)",
        "lcss": "IEEE Control Systems Letters (L-CSS)",
        "acc": "American Controls Conference (ACC)",
        "cdc": "Conference on Decision and Control (CDC)",
    }

    if item.Venue in venue_dict:
        venue_str = venue_dict[item.Venue]
    else:
        venue_str = item.Venue

    md += "\nvenue: \""   + venue_str + '"'
    md += "\nyear: \""   + str(year) + '"'
    md += "\nstatus: \""   + item.Status + '"'
    md += "\narxiv: \""   + item['Arxiv link'] + '"'
    md += "\nofficial_link: \""   + item['Official Link'] + '"'
    md += "\ndoi: \""   + item['DOI'] + '"'
    md += "\nvolume: \""   + item['Volume'] + '"'
    md += "\nnumber: \""   + item['Number'] + '"'
    md += "\npages: \""   + item['Pages'] + '"'
    md += "\npublisher: \""   + item['Publisher'] + '"'
    md += "\nmonth: \""   + month + '"'
    md += "\naddress: \""   + item['Address'] + '"'
    md += "\ntype: \""   + item['Type'] + '"'
    md += "\nschool: \""   + item['School'] + '"'
    md += "\nawards: \""   + item['Awards'] + '"'
    md += "\nnotes: \""   + item['Notes'] + '"'
    
    md += "\nimage: \""   + item['Image Filename'] + '"'

    md += """\ncollection: publications"""
    
    md += """\npermalink: /publication/""" + html_filename
    
    # if len(str(item.excerpt)) > 5:
    #     md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
    # md += "\ndate: " + str(item.pub_date) 
    
    # md += "\nvenue: '" + html_escape(item.venue) + "'"
    
    # if len(str(item.paper_url)) > 5:
    #     md += "\npaperurl: '" + item.paper_url + "'"
    
    # md += "\ncitation: '" + html_escape(item.citation) + "'"
    
    md += "\n---"
    
    ## Markdown description for individual page
    
    # if len(str(item.paper_url)) > 5:
    #     md += "\n\n<a href='" + item.paper_url + "'>Download paper here</a>\n" 
        
    # if len(str(item.excerpt)) > 5:
    #     md += "\n" + html_escape(item.excerpt) + "\n"
        
    # md += "\nRecommended citation: " + item.citation
    
    md_filename = os.path.basename(md_filename)
       
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)


