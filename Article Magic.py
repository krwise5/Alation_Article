# -*- coding: utf-8 -*-
import pandas as pd

from AlationInstance import AlationInstance
from Article import Article
from alationutil import log_me

# import the necessary packages
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True, help="username")
ap.add_argument("-p", "--password", required=True, help="password")
ap.add_argument("-H", "--host", required=True, help="URL of the Alation instance")
ap.add_argument("-v", "--username2", required=False, help="username2")
ap.add_argument("-w", "--password2", required=False, help="password2")
ap.add_argument("-x", "--host2", required=False, help="URL of the 2nd Alation instance")
args = vars(ap.parse_args())

url_1    = args['host']
user_1   = args['username']
passwd_1 = args['password']



al_in = AlationInstance(url_1, user_1, passwd_1)
#al_in.download_datadict()
desired_template = "ABOK Article"
allArticles  = al_in.getArticles(template=desired_template) # download all articles
A = Article(allArticles)                    # convert to Article class
#s = A.get_references()
A.to_csv(desired_template+".csv")
allTemplates = al_in.getTemplates()          # download all templates (with their custom fields)
# We need to have quite detailed information to create the template!

custom_fields = al_in.getCustomFields_from_template(desired_template) # this way we also get the template info

# Next, we put the objects we want. We need to start with the custom fields, then the template,
# then the articles, and finally the glossaries.
target = AlationInstance(args['host2'], args['username2'], args['password2'])
c_fields = target.putCustomFields(custom_fields) # returns a list of field IDs (existing or new)
desired_template_pd = allTemplates[allTemplates.title==desired_template]
t = target.putCustomTemplate(desired_template_pd, c_fields) # returns the ID of the (new) template
#target.putGlossaries(glossaries)
result = target.putArticles(A, desired_template, c_fields)
log_me(result.content)