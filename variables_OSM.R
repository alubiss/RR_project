library("readxl")
library(dplyr)
library(tidyverse)
library(sf)
library(osmdata)    
#devtools::install_github('osmdatar/osmdata')
library(ggmap)
library(leaflet) 
library(rgdal)
library(GISTools)
library(sp)
library(spdep)
library(spatialreg)
library(corrplot)
library(caret)
library(dismo)
library(fields)
library(gridExtra)
#library(gstat)
library(pgirmess)
library(raster)
library(rasterVis)
library(rgeos)
library(shapefiles)
library(geoR)
library(maptools)
library(spdep)
source("/Users/alubis/Desktop/OneDrive/mag/functions.R")

dane <- read_excel("/Users/alubis/Desktop/dane_semi2.xlsx")
dane$x= as.numeric(dane$x)
dane$y= as.numeric(dane$y)
dane$cena = as.numeric(gsub(",", ".", dane$cena, fixed=TRUE))
dane$N = dane$`wielkosc ruchu`
dane$`liczba gwiazdek` = as.numeric(gsub(",", ".", dane$`liczba gwiazdek`, fixed=TRUE))
dane$`średni spędzany czas (min)`=as.numeric(dane$`średni spędzany czas (min)`)

pop <- readOGR("/Users/alubis/Desktop/OneDrive/mag/PD_STAT_GRID_CELL_2011.shp", "PD_STAT_GRID_CELL_2011")
pop <- spTransform(pop, CRS("+proj=longlat +datum=NAD83"))
pop.df <- as.data.frame(pop) %>% dplyr::select(SHAPE_Leng, SHAPE_Area, CODE, TOT, TOT_15_64)
pop.grid <- as(pop, "SpatialPolygons")

dane.sp <- dane
coordinates(dane.sp) <- c("x","y") 
proj4string(dane.sp) <- CRS("+proj=longlat +datum=NAD83")
dane.sp <- spTransform(dane.sp, CRS("+proj=longlat +datum=NAD83"))
locs.lim <- over(dane.sp, pop.grid.warsaw)
dane$grid <- locs.lim  
dane$nazwa=as.factor(dane$nazwa)


#options(osrm.server = "http://router.project-osrm.org/", osrm.profile = "driving")
#Charakterystyki dotyczące położenia stacji względem siebie:
library(osrm)
distance = dane %>% dplyr:: select('adres stacji', 'x', 'y')
odleg = data.frame()
for(i in 1:length(distance$`adres stacji`)){
  nazwa = distance[i,1]$`adres stacji`
  temp <- distance %>% dplyr::filter(`adres stacji` != nazwa)
  dist=osrmTable(src=distance[i,],dst=temp,measure = 'distance')
  odl = as.data.frame(as.matrix(dist$durations))
  odl$min_odl_stacji <- do.call(pmin, c(odl, na.rm = TRUE))
  odl$max_odl_stacji <- do.call(pmax, c(odl, na.rm = TRUE))
  odl$avg_odl_stacji <- rowMeans(odl, na.rm = TRUE)
  odl$ile_stacji_r5= apply(odl[,1:119], 1, function(x)sum(x <= 5))
  odl$ile_stacji_r10= apply(odl[,1:119], 1, function(x)sum(x <= 10))
  odl = odl %>% dplyr:: select(min_odl_stacji, max_odl_stacji, avg_odl_stacji, ile_stacji_r5,ile_stacji_r10)
  odleg=rbind(odleg,odl)
}
d = as.data.frame(odleg)

names <- rownames(d)
rownames(d) <- NULL
od_stacji<- cbind(names,d)

# Charakterystyki dotyczące położenia stacji względem centrum miasta:
a <- c('palac_kultury')
x <- c(21.0057997)
y <- c(52.2317641)
palac= data.frame(a,x,y)

od_centrum <- osrmTable(src=distance[1:120,],dst=palac,measure = 'distance')
od_centrum = as.data.frame(od_centrum)
d = od_centrum[,1:2]

names <- rownames(d)
rownames(d) <- NULL
od_centrum <- cbind(names,d)

setwd("/Users/alubis/Desktop/OneDrive/mag")
load("od_centrum.Rdata")
load("od_stacji.Rdata")

# Charakterystyki dotyczące położenia stacji względem najbliższej trasy:
# współrzędne geograficzne
# https://wiki.openstreetmap.org/wiki/Map_Features
# amenity post_office
# building commercial, office, public, school
# highway trunk, primary
a = getOSMData("Warszawa, Poland", f_key = "highway", f_value = 'trunk') %>% plotLeafletMap_points()
x <- a$x$calls[[2]]$args[[2]]
y <- a$x$calls[[2]]$args[[1]]
id <- seq(1,length(x),1)
trunk=data.frame(id,x,y)
a = getOSMData("Warszawa, Poland", f_key = "highway", f_value = 'primary') %>% plotLeafletMap_points()
x <- a$x$calls[[2]]$args[[2]]
y <- a$x$calls[[2]]$args[[1]]
id <- seq(1,length(x),1)
primary=data.frame(id,x,y)

primary1=primary[1:200,]
odl_primary = data.frame()
for(i in 1:length(distance$`adres stacji`)){
 nazwa = distance[i,1]$`adres stacji`
 temp <- distance %>% dplyr::filter(`adres stacji` != nazwa)
 dist=osrmTable(src=distance[i,],dst=primary1,measure = 'distance')
 odl = as.matrix(dist$durations)
 odl = as.data.frame(odl)
 odl$min_odl_primary <- do.call(pmin, c(odl, na.rm = TRUE))
 odl$max_odl_primary <- do.call(pmax, c(odl, na.rm = TRUE))
 odl$avg_odl_primary <- rowMeans(odl, na.rm = TRUE)
 d = odl %>% dplyr:: select(min_odl_primary, max_odl_primary, avg_odl_primary)
 names <- rownames(d)
 rownames(d) <- NULL
 odl <- cbind(names,d)
 odl_primary=rbind(odl_primary,odl)
}
odl_primary = as.data.frame(odl_primary)

setwd("/Users/alubis/Desktop/OneDrive/mag")
load("odl_trasy.RData")

library(dplyr)
dane = dane %>% dplyr:: left_join(odl_trunk,by= c('adres stacji'='names') )
dane = dane %>% dplyr:: left_join(odl_primary,by= c('adres stacji'='names') )
dane = dane %>% dplyr:: left_join(od_centrum,by= c('adres stacji'='names') )
dane = dane %>% dplyr:: left_join(od_stacji,by= c('adres stacji'='names') )