

## Needed Imports
from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers

import requests, json

import pandas as pd


#Get the research industry you are looking into and # of works to lookup
keyword_search = input("keyword: ").lower()


number_search = int(input("number of works: "))

print(keyword_search)
print(number_search)

#creates a page of #number_search of works related to keyword

pager = Works().search(keyword_search).paginate(per_page=number_search)

#create empty DF to collect authors name and id
authorsDF = pd.DataFrame({'id':[], 'name':[]})

#fill authorsDF with unique list of names and ids

#version - only unique authors
for page in pager:
    first_time = 0
    for work in page:
        authors = dict(work)['authorships']
        for author in authors:
            author_dict = author['author']
            new_row = {'id':author_dict['id'], 'name':author_dict['display_name']}
            if first_time==0:
                authorsDF=pd.concat([authorsDF,pd.DataFrame([new_row])],ignore_index=True)
                first_time+=1
            elif authorsDF['id'].str.contains(new_row['id']).any():
                pass
            else:
                authorsDF=pd.concat([authorsDF,pd.DataFrame([new_row])],ignore_index=True)
    break
        


#list of author IDs
author_id_list = authorsDF.loc[:,'id']

#empty DF to collect stats on authors
authorStatDF = pd.DataFrame({'id':[], 'works_count':[], 'cited_by_count':[], '2yr_mean_citedness':[],
                          'h_index':[], 'i10_index':[]})




#get each author statistics
#gets works_count, cited_by_count, 2yr_mean_citedness, h_index, i10_index

#use this to get each author info
#careful, takes about 3-5 minutes to run for ~520 elements
for au_id in author_id_list:
    auth_dict = dict(Authors()[au_id])
    new_row = {'id':auth_dict['id'], 'works_count':auth_dict['works_count'], 'cited_by_count':auth_dict['cited_by_count'],
          '2yr_mean_citedness':auth_dict['summary_stats']['2yr_mean_citedness'],
           'h_index':auth_dict['summary_stats']['h_index'], 'i10_index':auth_dict['summary_stats']['i10_index']}
    authorStatDF=pd.concat([authorStatDF,pd.DataFrame([new_row])],ignore_index=True)
    



final_authorDF = authorsDF.merge(authorStatDF)

print(final_authorDF.head())
print('all done')
