README
================
Aleksandra Lubicka, Rafał Kaczmarek

Introduction
============

The purpose of this paper is to replicate the study described in the
paper titled [‘A Machine Learning-Based Approach for Spatial Estimation
Using the Spatial Features of Coordinate
Information’](https://www.mdpi.com/2220-9964/9/10/587). The authors of
the study compare two spatial data modeling methods and they are kriging
and spatial machine learning. This article was selected because it
presents a very interesting area of analysis and its replication is
possible using data available for Poland.

**Stages of analysis:**

![](https://www.mdpi.com/ijgi/ijgi-09-00587/article_deploy/html/images/ijgi-09-00587-g001.png)
1.Preparation of spatial data.

2.Preparing a kriging model in R.

3.Preparing a spatial machine learning model in python.

4.Comparison of the results obtained between the different models.

5.Summary of findings and comparison of results with those obtained in
the original study using R markdown.

Data
====

The data used for the study is also spatial character, but it covers a
different area. The use of the spatial models described in the paper for
the location data of **gas stations in Warsaw** will be investigated.
Data was collected on *station address, geographic coordinates, average
traffic per week, and number of customers by time of day and day of
week*. The **Open Street Maps** API was connected to calculate the
density of stations in the vicinity of the point, the distance to
neighboring units, the distance to the center, and major access roads,
which allowed the distance to be determined based on the distance a car
must travel when driving on the nearest possible road. Data on the size
of the population in Warsaw was also used for the study. In addition,
the variables characterizing each outlet were fuel price, opening hours,
and average rating given by consumers.

Hypotheses
----------

We expect that the extracted **spatial features improve the performance
of MLA for spatial estimation** because they have characteristics of
spatial correlation represented by distances. To verify the proposed
approach, indicator **Kriging was used as a benchmark model**, and each
performance of MLA was compared when using raw coordinates, distance
vector, and spatial features extracted from distance vector as inputs.
Thus, it is one thing **to improve estimation performance by including
spatial variables**, and another to say that **spatial machine learning
models produce more accurate estimates than basic spatial models**.

Research metods
---------------

The paper mainly describes two research methods:

### Kriging

Among the geostatistical techniques for spatial estimation, indicator
Kriging is a non-parametric approach that can be applied when the sample
dataset is skewed or when it does not have a normal distribution.

### Spatial Machine Learning with Random Forest Model

The random forest approach, which solves a problem by learning multiple
decision trees, is a representative ensemble technique and data-based
statistical method.Spatial cross-validation will also be used in this
case, and the split between the test and training sample will be done
taking into account the spatial nature of the variables.

Report structure
================

**Files:**

\*README - project description file

\*kriging.R - first part of code

\*model.ipynb - second part of code

\*summary.Rmd - summary of the project

\*gitignore

------------------------------------------------------------------------

Sources:

1.*Katarzyna Kopczewska. Przestrzenne metody ilościowe w R: statystyka,
ekonometria, uczenie maszynowe, analiza danych*

2.*Seongin Ahn,Dong-Woo Ryu, Sangho Lee. A Machine Learning-Based
Approach for Spatial Estimation Using the Spatial Features of Coordinate
Information.*
