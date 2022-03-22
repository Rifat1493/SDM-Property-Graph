# bin/bash

# code used to import the graph (A.1)
neo4j-admin import --database=dblp --delimiter "," --array-delimiter "|" --id-type INTEGER  --force --nodes=journal="journal.csv" --nodes=:conference="conference.csv" --nodes=:author="authors.csv" --nodes=:article="articles.csv" --nodes=:keyword="keywords.csv" --relationships=writtenby="author_writes_article.csv" --relationships=reviewedby="article_reviewedby_author.csv" --relationships=published_inj="article_publishedin_journal.csv" --relationships=published_inc="article_publishedin_conference.csv" --relationships=contains="article_keywords.csv" --relationships=cites="article_cites.csv" --skip-duplicate-nodes
