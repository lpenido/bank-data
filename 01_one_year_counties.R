# Lucas Penido
# 2019.11.08
# Loading a Shapefile
# Packages used: tidyverse, sf

# install.packages("dyplr")

library(tidyverse)
library(sf)
library(tmap)
# library(ggplot2)
# library(rgdal)
# library(rgeos)
# library(maptools)


rm(list=ls())

main_dir = "C:\\Users\\lpenido\\Documents\\Deposits"
map_dir  = "C:\\Users\\lpenido\\Documents\\Deposits\\US_County_Boundaries"
deposits = "ALL_2018.csv"
county_map = "US_County_Boundaries.shp"

# Lining up the FIPS Deposit Data
setwd(main_dir)
deps = read_csv(deposits)
cnty_dep = aggregate(x = deps$DEPSUMBR, by = list(deps$STCNTYBR), FUN = sum)
st_dep = aggregate(x = deps$DEPSUMBR, by = list(deps$STALPBR), FUN = sum)

# Getting the Shapefile up
setwd(map_dir)
s.sf = st_read(county_map)
head(s.sf, n=4)









