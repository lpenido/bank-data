# Lucas Penido
# 2019.11.13
#

# Setting up Environment
library(tidyverse)
library(sp)
library(sf)
library(spdep)
library(nngeo)
# rm(list=ls())

deposits = "ALL_2018.csv"
county_map = "US_County_Boundaries.shp"
county_address = "US_County_Boundaries.shp"

setwd(map_dir)
county_map = st_read(county_address)
florida = county_map %>%
  filter(
    STATE == "Florida")
head(florida)

get_national_data = function(){
  national_data = deps %>%
    group_by(NAMEFULL) %>%
    summarise(
      Branches = n_distinct(UNINUMBR),
      Deposits = sum(DEPSUMBR)) %>%
    mutate(
      ShareBranches = (Branches / sum(Branches)) * 100,
      ShareDeposits = (Deposits / sum(Deposits)) * 100
    )
  
  colnames(national_data)[colnames(national_data)=="NAMEFULL"] = "Bank"
  national_data = national_data[order(national_data$Deposits, decreasing = TRUE),]
  # deps[deps$STCNTYBR == county_code,]
  return(national_data)
}

get_county_name = function(county_code){
  county_row = rownames(county_map[county_map$CTFIPS == county_code,])
  county_row = as.numeric(county_row)
  county_name = county_map$COUNTY[county_row]
  return(county_name)
}

get_county_code = function(county_name, state_name){
  county_row = rownames(county_map[(county_map$COUNTY == county_name & county_map$STATE == state_name),])
  county_row = as.numeric(county_row)
  county_code = county_map$CTFIPS[county_row]
  return(county_code)
}

get_county_data_by_name = function(county_name, state_name){
  county_code = get_county_code(county_name, state_name)
  county_data = deps %>%
    filter(STCNTYBR == county_code) %>%
    group_by(NAMEFULL) %>%
    summarise(
      Branches = n_distinct(UNINUMBR),
      Deposits = sum(DEPSUMBR)) %>%
    mutate(
      ShareBranches = (Branches / sum(Branches)) * 100,
      ShareDeposits = (Deposits / sum(Deposits)) * 100
    )
    
  colnames(county_data)[colnames(county_data)=="NAMEFULL"] = "Bank"
  county_data = county_data[order(county_data$Deposits, decreasing = TRUE),]
  # deps[deps$STCNTYBR == county_code,]
  return(county_data)
}

get_county_data_by_name("Okeechobee","Florida")

get_county_codes_by_city = function(city_name, state_abbrev){
  geography = deps %>%
    filter(STALPBR == state_abbrev,
           CITYBR  == city_name) %>%
    dplyr::select(CITYBR,
                  STCNTYBR,
                  STALPBR)
  county_codes = as.vector(unique(geography$STCNTYBR))
  return(county_codes)
}

get_county_codes_by_city('Atlanta','GA')

for (code in get_county_codes_by_city('Atlanta','GA')){
  code = as.numeric(code)
  print(code)
  print(get_county_code(get_county_name(code),'Georgia'))
}

get_national_data()[1:20,]

'''
Getting the ratings and schedules into one data set could be done using get_county_data().

For a given FIPS, return list of Bank names. Use those names to return the FIPS codes of all other branches.
This kinda blows up for Large Banks. John said to look at Banks with $3B in Deposits, it would be great to merge
exam methods onto bank names (return 2 tables before merging)

'''
# nb.FOQ = poly2nb(florida, queen = TRUE, row.names = florida$CTFIPS)
# nb.FOQ
# gTouches(county_map, byid = TRUE)
# lake = county_map[(county_map$CTFIPS == get_county_code("Lake","Florida")),]
# st_nn(lake, florida, sparse = TRUE, k = 1, maxdist = 100000, returnDist = TRUE, progress = TRUE)