# Thesauri RTVE

This repository contains the programming code (Python) and the resulting data to unify RTVE thesauri. For copyright reasons, the files with the original thesaurus structure cannot be published.

Introduction
============

The repository includes all the scripts needed to transform CSV files of several thesauri belonging to different facets (people, places, topics, series) to unify them into one thesaurus for each processed facet. Language tagging is also performed, as well as searching for reconciliation with entities in Wikidata. The results are prepared for further processing and conversion according to the SKOS model.

Files and folders
=================
* process.py: Python code to process the original CSV files and create data files with the results.
* stats.py: Python code to process the results data files to obtain statistics.
* results.zip: Files with the results data.

Author
=======
* Juan-Antonio Pastor-Sánchez (University of Murcia, Spain)

License
=======
Python code is available under GNU General Public LIcense v3.0. Data is available under Creative Commons BY-SA 4.0
