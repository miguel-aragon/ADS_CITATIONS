#
#
# Simple web scraper.
#
# Written by Miguel A. Aragon-Calvo (2017)
#
#

import time
import urllib2


#response = urllib2.urlopen('http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author=Aragon-Calvo&object=&start_mon=&start_year=2014&end_mon=&end_year=2016&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1')

response = urllib2.urlopen('http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author=aragon-calvo&object=&start_mon=&start_year=&end_mon=&end_year=&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1')
html = response.read()
html_splitted = html.split('"')

bibtex = []

i=1
#--- Loop over the items separated by quota
for item in html_splitted:
    #--- Filter only the right link
    if ('link_type=ABSTRACT' in item) and ('amp' in item):
        print 'PAPER',i,': ', item
        i = i+1

        #--- Be a nice robot
        time.sleep(1)

        #--- Retrieve paper and get citations
        response_i = urllib2.urlopen(item)
        html_i = response_i.read()
        html_i_splitted = html_i.split('"')
        
        for item_i in html_i_splitted:
            if ('link_type=CITATIONS' in item_i):
                
                #--- Clean and fix string
                item_i = item_i.replace("data", "ref").replace("link_type","amp;refs").replace("db_key","amp;db_key").replace("#38;","")

                try:
                    response_ii = urllib2.urlopen(item_i)
                except: 
                    print 'FAILED!'
                    continue
                html_ii = response_ii.read()
                html_ii_splitted = html_ii.split('"')

                #--- Loop over citations for this article
                for item_ii in html_ii_splitted:
                    if ('link_type=ABSTRACT' in item_ii) and ('amp' in item_ii):
                        print '  CITE: ', item_ii

                        #--- Be a nice robot
                        time.sleep(0.2)

                        #--- Read this cite and get its bibtex file
                        response_iii = urllib2.urlopen(item_ii)
                        html_iii = response_iii.read()
                        html_iii_splitted = html_iii.split('"')

                        
                        for item_iii in html_iii_splitted:
                            if ('data_type=BIBTEX' in item_iii):

                                #--- Get the bibtex file
                                response_iiii = urllib2.urlopen(item_iii)
                                html_iiii = response_iiii.read()
                                html_iiii = html_iiii.replace("Query Results from the ADS Database","").replace("Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.","")                               
                                bibtex.append(html_iiii)


        print '---------------------------------'
        fo = file("myads_bbitex.bib", "w")
        fo.writelines( "%s\n" % item for item in bibtex)
        fo.close()

#print bibtex

#fo = file("myads_bbitex.bib", "w")
#fo.writelines( "%s\n" % item for item in bibtex )


        
