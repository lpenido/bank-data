# Lucas Penido
# 2019.11.08
# Exploring Deposits and Branches in Regions
# 
# The goal is to test some potential measures and make a crude viz 


library(tidyverse)

rm(list=ls())

main_dir = "C:\\Users\\lpenido\\Documents\\Deposits"
map_dir  = "C:\\Users\\lpenido\\Documents\\Deposits\\US_County_Boundaries"
deposits = "ALL_2018.csv"
county_map = "US_County_Boundaries.shp"

# Getting the Shapefile up
setwd(map_dir)
s.sf = st_read(county_map)
head(s.sf, n=4)


# Lining up the FIPS Deposit Data
setwd(main_dir)
deps = read_csv(deposits)
cnty_dep = aggregate(x = deps$DEPSUMBR, by = list(deps$STCNTYBR), FUN = sum)

# Adding a few market measures to tibble
state_deps_bank = deps %>%
  group_by(STALPBR, NAMEFULL) %>%
  summarise(
        Branches = n_distinct(UNINUMBR),
        Deposits = sum(DEPSUMBR)) %>%
  mutate(
        BranchShare = Branches / sum(Branches),
        DepositShare = Deposits / sum(Deposits),
        BranchSkew = mean(BranchShare) - median(BranchShare),
        DepositSkew = mean(DepositShare) - median(DepositShare),
        BranchSpread = sd(BranchShare),
        DepositSpread = sd(DepositShare))

# Reformatting the tibble without Bank names 
LookBook = state_deps_bank %>%
  group_by(STALPBR) %>%
  summarise(
    BranchSkew = mean(BranchSkew),
    DepositSkew = mean(DepositSkew),
    BranchSpread = mean(BranchSpread),
    DepositSpread = mean(DepositSpread)) %>%
  mutate(
    Landscape = DepositSkew - BranchSkew) %>%
  print(n = Inf)

LookBook = LookBook[-c(4,12,14,26,30,45,46,54),] # Dropping Territories

LookBook2 = LookBook %>%
  summarise(
    AvgBranchSkew = mean(BranchSkew),
    AvgDepositSkew = mean(DepositSkew),
    AvgBranchSpread = mean(BranchSpread),
    AvgDepositSpread = mean(DepositSpread)) %>%
  print(n = Inf)


# Plotting histogram
ggplot(data = LookBook, aes(x = DepositSkew)) +
  geom_histogram(color = "black", fill = "white", bins = 30) + 
  geom_density(alpha = 0.2, fill = "#063268") +
  geom_vline(aes(xintercept=mean(DepositSkew)),
             color="red", linetype="dashed", size=1) +
  geom_vline(aes(xintercept=median(DepositSkew)),
             color="blue", linetype="dashed", size=1)







