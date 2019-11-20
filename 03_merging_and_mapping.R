# Lucas Penido
# 2019.11.13
# 
# 

# Setting up Environment
library(tidyverse)
library(sf)
library(tmap)
# (list=ls())

# Finding the paths to the files 
deposits = "ALL_2018.csv"
county_address = "US_County_Boundaries.shp"

# Getting the data and formatting columns
# setwd(main_dir)
# deps = read_csv(deposits)
county_data = aggregate(x = deps$DEPSUMBR, by = list(deps$STCNTYBR), FUN = sum)
colnames(county_data)[colnames(county_data) == "Group.1"] = "CTFIPS"
colnames(county_data)[colnames(county_data) == "x"] = "Deposits"

county_shares = deps %>%
  group_by(STCNTYBR, STALPBR, NAMEFULL) %>%
  summarise(
    Branches = n_distinct(UNINUMBR),
    Deposits = sum(DEPSUMBR)) %>%
  mutate(
    BranchShare = Branches / sum(Branches),
    DepositShare = Deposits / sum(Deposits),
    BranchSkew = mean(BranchShare) - median(BranchShare),
    DepositSkew = mean(DepositShare) - median(DepositShare),
    BranchSpread = sd(BranchShare),
    DepositSpread = sd(DepositShare),
    BranchPearson = (3*(mean(BranchShare)-median(BranchShare)) / sd(BranchShare)),
    DepositPearson = (3*(mean(DepositShare)-median(DepositShare)) / sd(DepositShare)))

# Overview
LookBook = county_shares %>%
  group_by(STCNTYBR, STALPBR) %>%
  summarise(
    BranchSkew = mean(BranchSkew),
    DepositSkew = mean(DepositSkew),
    BranchSpread = mean(BranchSpread),
    DepositSpread = mean(DepositSpread),
    BranchPearson = mean(BranchPearson),
    DepositPearson = mean(DepositPearson)) %>%
  mutate(
    Landscape = DepositSkew - BranchSkew)
LookBook[is.na(LookBook)] = 0

setwd(desktop)
write.csv(LookBook, file = "CountyDeposits.csv")

# Loading the Shapefile data up and merging the deposits onto it 
setwd(map_dir)
county_map = st_read(county_address)
county_map = merge(county_map, county_data, by = "CTFIPS")

# Filtering out non-Continental values
county_map = county_map %>%
                filter(
                  STATE != "Alaska",
                  STATE != "Puerto Rico",
                  STATE != "Hawaii")

county_csv = county_map %>%
                select(CTFIPS, Deposits)
county_csv = as_tibble(county_csv)
county_csv = county_csv %>% 
                select(CTFIPS, Deposits)

# head(county_csv)


# Mapping the data
# tm_shape(county_map) + 
#   tm_polygons(col = "Deposits", border.col = "black")


