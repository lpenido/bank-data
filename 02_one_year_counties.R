# Lucas Penido
# 2019.11.08
# Exploring Deposits and Branches in Regions
# 
# The goal is to test some potential measures and make a crude viz 

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

# I want to sum all the branches and deposits per region per bank
# state_deps_total = state_deps_bank %>%
#   group_by(STCNTYBR) %>%
#   summarise(
#     Branches = sum(Branches),
#     Deposits = sum(Deposits),
#   )

# head(state_deps_total)

# I want to sum all banks, branches, and deposits per region
state_deps_bank = deps %>%
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
LookBook = state_deps_bank %>%
  group_by(STCNTYBR, STALPBR) %>%
  summarise(
    BranchSkew = mean(BranchSkew),
    DepositSkew = mean(DepositSkew),
    BranchSpread = mean(BranchSpread),
    DepositSpread = mean(DepositSpread),
    BranchPearson = mean(BranchPearson),
    DepositPearson = mean(DepositPearson)) %>%
  mutate(
    Landscape = DepositSkew - BranchSkew) #%>%
  # print(n = Inf)

print(head(LookBook))


# ggplot(data = LookBook, mapping = aes(x = BranchSpread, y = DepositSpread, color = STALPBR)) +
#   geom_point(alpha = 1/4)# +
#   # geom_smooth(se = TRUE, method = "loess", level = 0.95)

ggplot(data = LookBook, aes(x = BranchPearson)) +
  geom_histogram(color = "black", fill = "white", bins = 30) + 
  # geom_density(alpha = 0.2, fill = "#063268") +
  geom_vline(aes(xintercept = mean(BranchPearson)),
             color ="red", linetype ="dashed", size = 1) +
  geom_vline(aes(xintercept = median(BranchPearson)),
             color ="blue", linetype ="dashed", size = 1)

# Getting the Shapefile up
# setwd(map_dir)
# s.sf = st_read(county_map)
# head(s.sf, n=4)   

