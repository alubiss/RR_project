
library("readxl")
library(dplyr)

dane <- read_excel("/Users/alubis/Desktop/dane_semi2.xlsx")
dane$x= as.numeric(dane$x)
dane$y= as.numeric(dane$y)
dane$cena = as.numeric(gsub(",", ".", dane$cena, fixed=TRUE))
dane$N = dane$`wielkosc ruchu`
dane$`liczba gwiazdek` = as.numeric(gsub(",", ".", dane$`liczba gwiazdek`, fixed=TRUE))
dane$`średni spędzany czas (min)`=as.numeric(dane$`średni spędzany czas (min)`)
dane.sp = dane[1:103,]
dane.sp = dane.sp %>% dplyr::select(c("x","y"))

dane <- read.csv("/Users/alubis/geo_project/dane_ost.csv", sep=",")
dane = cbind(dane, dane.sp)

dane$r<-runif(dim(dane)[1])
# nowe obiekty są klasy SpatialPointsDataFrame:
train <- dane[dane$r<0.8, ] # wybranie 80% danych na zbiór treningowy 
test <- dane[dane$r>0.8, ] # wybranie 20% danych na zbiór testowy

modelformula <- ruch ~ TOT + cena + stars + czas_avg + min_odl_trunk + max_odl_trunk +
avg_odl_trunk + min_odl_primary + max_odl_primary + avg_odl_primary + od_centrum + 
od_stacji_min + od_stacji_max + ile_stacji_r5 + ile_stacji_r10

library(randomForest)
model<-randomForest(modelformula, data=train, ntree=500) 
model

library(sperrorest)
resamp<-partition_cv(train, nfold=5, repetition=1, seed1=1) 
plot(resamp, train, coords = c("x","y"))

res_rf_cv<-sperrorest(modelformula,
                      data = train,
                      model_fun = randomForest, 
                      model_args = list(ntree = 50,
                                        mtry = 90), 
                      smp_fun = partition_cv,
                      smp_args=list(repetition = 100, nfold = 5, seed1 = 1234),
                      err_fun=err_default,
                      #error_rep = TRUE,
                      progress = 'all')
round(summary(res_rf_cv$error_rep), 3)


# losowanie oparte na k-średnich
resamp <- partition_kmeans(train, nfold = 5, coords = c('x', 'y'),
                           repetition = 1, seed1 = 1234)
plot(resamp, train, coords = c("x","y"))


set.seed(1234)
res_rf_kmeans<-sperrorest(modelformula, data=train, 
                          model_fun=randomForest, 
                          model_args=list(ntree=150, mtry=90), 
                          smp_fun=partition_kmeans, 
                          progres='all', 
                          smp_args=list(repetition=100, nfold=5, seed1=1234))
                          #error_rep=TRUE)
round(summary(res_rf_kmeans$error_rep), 3)



