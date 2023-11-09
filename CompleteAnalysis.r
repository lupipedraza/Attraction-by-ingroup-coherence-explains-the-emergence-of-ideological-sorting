# FUNCTIONS ---------------------------------------------------------------
library(haven)

getCohProportionByPairs <- function(allIssues) {
  cohPropValues = c()
  for (i in 1:(ncol(allIssues)-1)) {
    for (j in (i+1):ncol(allIssues)){
      #Opinions are analyzed in pairs
      op1 = allIssues[,i]
      op2 = allIssues[,j]
      polPosIt = op1*op2
      #The proportion of coherents is computed as #coh / (#coh+#inc)
      value = sum(polPosIt==1,na.rm=TRUE)/(sum(polPosIt==1,na.rm=TRUE)+sum(polPosIt==-1,na.rm=TRUE))
      cohPropValues = append(cohPropValues,value)
    }
  }
  return(cohPropValues)
}

removeConsesusDataForVar <- function(allIssues,varThreshold) {
  varCol = c()
  for (i in 1:ncol(allIssues)) {
    value = var(allIssues[,i],na.rm = TRUE)
    varCol = append(varCol,value)
  }
  #Topics with low variance are removed
  colIndex = varCol>varThreshold
  selectedIssues = allIssues[,colIndex]
  return(selectedIssues)
}

describeData <- function(allIssues,varThreshold) {
  polPosition = rowSums(allIssues,na.rm = TRUE)
  hist(polPosition,breaks=ncol(allIssues)*3)
  print(cor(allIssues, use="complete.obs", method = "spearman"))
}

#  DATA -------------------------------------------------------------------
#  Zimm. et al Study 1 ----------------------------------------------------
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

ZimmSt1 = read.csv("Data_Study1.csv", header = TRUE)
#Arrange data
politicalOpinions = ZimmSt1[ZimmSt1$issue==1,c("opinionFirst_1","opinionFirst_2","opinionFirst_3","opinionFirst_4","opinionFirst_5")]
politicalOpinions = t(t(politicalOpinions) * c(1,1,1,-1,-1))
nonPoliticalOpinions = ZimmSt1[ZimmSt1$issue==0,c("opinionFirst_1","opinionFirst_2","opinionFirst_3","opinionFirst_4","opinionFirst_5")]

#describeData(politicalOpinions)
cohZimmSt1Pol = getCohProportionByPairs(politicalOpinions)
summary(cohZimmSt1Pol)

#describeData(nonPoliticalOpinions)
cohZimmSt1NonPol = getCohProportionByPairs(nonPoliticalOpinions)
summary(cohZimmSt1NonPol)

#  Zimm. et al Online ----------------------------------------------------
ZimmOnlineStAPol = read.csv("OnlinePolA.csv", header = TRUE)
ZimmOnlineStBPol = read.csv("OnlinePolB.csv", header = TRUE)

ZimmOnlineStANonPol = read.csv("OnlineHedA.csv", header = TRUE)
ZimmOnlineStBNonPol = read.csv("OnlineHEdB.csv", header = TRUE)

polA = removeConsesusDataForVar(ZimmOnlineStAPol,0.5)
polB = removeConsesusDataForVar(ZimmOnlineStBPol,0.5)

hedA = removeConsesusDataForVar(ZimmOnlineStANonPol,0.5)
hedB = removeConsesusDataForVar(ZimmOnlineStBNonPol,0.5)

cohZimmOnlinePolA = getCohProportionByPairs(polA)
summary(cohZimmOnlinePolA)

cohZimmOnlinePolB = getCohProportionByPairs(polB)
summary(cohZimmOnlinePolB)

cohZimmOnlineHedA = getCohProportionByPairs(hedA)
summary(cohZimmOnlineHedA)

cohZimmOnlineHedB = getCohProportionByPairs(hedB)
summary(cohZimmOnlineHedB)

#  ANES 2020  ----------------------------------------------------
anes2020Data = read.csv("anes_timeseries_2020_csv_20220210.csv", header = TRUE)
#Arrange data
#V201252 MEDICAL INSURANCE
anesMedical = anes2020Data$V201252
medicalData = replace(anesMedical, anesMedical==-9, NA)
medicalData = replace(medicalData, medicalData==-8, 0)
medicalData = replace(medicalData, medicalData==99, 0)
medicalData = replace(medicalData, medicalData==1, 1)
medicalData = replace(medicalData, medicalData==2, 1)
medicalData = replace(medicalData, medicalData==3, 1)
medicalData = replace(medicalData, medicalData==4, 0)
medicalData = replace(medicalData, medicalData==5, -1)
medicalData = replace(medicalData, medicalData==6, -1)
medicalData = replace(medicalData, medicalData==7, -1)
#V201258 GOV ASSISTANCE TO BLACKS
anesBlacks = anes2020Data$V201258
blacksData = replace(anesBlacks, anesBlacks==-9, NA)
blacksData = replace(blacksData, blacksData==-8, 0)
blacksData = replace(blacksData, blacksData==99, 0)
blacksData = replace(blacksData, blacksData==1, 1)
blacksData = replace(blacksData, blacksData==2, 1)
blacksData = replace(blacksData, blacksData==3, 1)
blacksData = replace(blacksData, blacksData==4, 0)
blacksData = replace(blacksData, blacksData==5, -1)
blacksData = replace(blacksData, blacksData==6, -1)
blacksData = replace(blacksData, blacksData==7, -1)
#V201300 FEDERAL BUDGET SPENDING: SOCIAL SECURITY
anesSecurity = anes2020Data$V201300
securityData = replace(anesSecurity, anesSecurity==-9, NA)
securityData = replace(securityData, securityData==-8, 0)
securityData = replace(securityData, securityData==3, NA)
securityData = replace(securityData, securityData==1, 1)
securityData = replace(securityData, securityData==2, -1)
#V201306 FEDERAL BUDGET SPENDING: TIGHTENING BORDER SECURITY
anesBorder = anes2020Data$V201306
borderData = replace(anesBorder, anesBorder==-9, NA)
borderData = replace(borderData, borderData==-8, 0)
borderData = replace(borderData, borderData==3, NA)
borderData = replace(borderData, borderData==1, -1)
borderData = replace(borderData, borderData==2, 1)
#V201309 FEDERAL BUDGET SPENDING: DEALING WITH CRIME
anesCrime = anes2020Data$V201309
crimeData = replace(anesCrime, anesCrime==-9, NA)
crimeData = replace(crimeData, crimeData==-8, 0)
crimeData = replace(crimeData, crimeData==3, NA)
crimeData = replace(crimeData, crimeData==1, -1)
crimeData = replace(crimeData, crimeData==2, 1)
#V201318 FEDERAL BUDGET SPENDING: AID TO THE POOR
anesPoor = anes2020Data$V201318
poorData = replace(anesPoor, anesPoor==-9, NA)
poorData = replace(poorData, poorData==-8, 0)
poorData = replace(poorData, poorData==3, NA)
poorData = replace(poorData, poorData==1, 1)
poorData = replace(poorData, poorData==2, -1)
#V201336 STD ABORTION
anesAbortion = anes2020Data$V201336
abortionData = replace(anesAbortion, anesAbortion==-9, NA)
abortionData = replace(abortionData, abortionData==-8, 0)
abortionData = replace(abortionData, abortionData==1, -1)
abortionData = replace(abortionData, abortionData==2, -1)
abortionData = replace(abortionData, abortionData==3, 1)
abortionData = replace(abortionData, abortionData==4, 1)
abortionData = replace(abortionData, abortionData==5, NA)
#V201401 GOVERNMENT ACTION ABOUT RISING TEMPERATURES
anesWarming = anes2020Data$V201401
warmingData = replace(anesWarming, anesWarming==-9, NA)
warmingData = replace(warmingData, warmingData==-8, 0)
warmingData = replace(warmingData, warmingData==3, NA)
warmingData = replace(warmingData, warmingData==1, 1)
warmingData = replace(warmingData, warmingData==2, -1)
#V201406 SERVICES TO SAME SEX COUPLES
anesGayServices = anes2020Data$V201406
gayServicesData = replace(anesGayServices, anesGayServices==-9, NA)
gayServicesData = replace(gayServicesData, gayServicesData==-8, 0)
gayServicesData = replace(gayServicesData, gayServicesData==1, -1)
gayServicesData = replace(gayServicesData, gayServicesData==2, 1)
#V201409 TRANSGENDER POLICY
anesTrans = anes2020Data$V201409
transData = replace(anesTrans, anesTrans==-9, NA)
transData = replace(transData, transData==-8, 0)
transData = replace(transData, transData==1, -1)
transData = replace(transData, transData==2, 1)
#V201412 LAWS PROTECT GAYS/LESBIANS AGAINST JOB DISCRIMINATION
anesGayJobs = anes2020Data$V201412
gayJobsData = replace(anesGayJobs, anesGayJobs==-9, NA)
gayJobsData = replace(gayJobsData, gayJobsData==-8, 0)
gayJobsData = replace(gayJobsData, gayJobsData==1, 1)
gayJobsData = replace(gayJobsData, gayJobsData==2, -1)
#V201415 GAY AND LESBIAN COUPLES BE ALLOWED TO ADOPT
anesGayAdopt = anes2020Data$V201415
gayAdoptData = replace(anesGayAdopt, anesGayAdopt==-9, NA)
gayAdoptData = replace(gayAdoptData, gayAdoptData==-8, 0)
gayAdoptData = replace(gayAdoptData, gayAdoptData==1, 1)
gayAdoptData = replace(gayAdoptData, gayAdoptData==2, -1)
#V201416 POSITION ON GAY MARRIAGE
anesGayMarriage = anes2020Data$V201416
gayMarriageData = replace(anesGayMarriage, anesGayMarriage==-9, NA)
gayMarriageData = replace(gayMarriageData, gayMarriageData==-8, 0)
gayMarriageData = replace(gayMarriageData, gayMarriageData==1, 1)
gayMarriageData = replace(gayMarriageData, gayMarriageData==2, NA)
gayMarriageData = replace(gayMarriageData, gayMarriageData==3, -1)
#V201417 US GOVERNMENT POLICY TOWARD UNAUTHORIZED IMMIGRANTS
anesImmigrants = anes2020Data$V201417
immigrantsData = replace(anesImmigrants, anesImmigrants==-9, NA)
immigrantsData = replace(immigrantsData, immigrantsData==-8, 0)
immigrantsData = replace(immigrantsData, immigrantsData==1, -1)
immigrantsData = replace(immigrantsData, immigrantsData==2, NA)
immigrantsData = replace(immigrantsData, immigrantsData==3, NA)
immigrantsData = replace(immigrantsData, immigrantsData==4, 1)
#V201418 FAVOR OR OPPOSE ENDING BIRTHRIGHT CITIZENSHIP
anesBirthright = anes2020Data$V201418
birthrightData = replace(anesBirthright, anesBirthright==-9, NA)
birthrightData = replace(birthrightData, birthrightData==-8, 0)
birthrightData = replace(birthrightData, birthrightData==1, -1)
birthrightData = replace(birthrightData, birthrightData==2, 1)
birthrightData = replace(birthrightData, birthrightData==3, 0)
#V201424 FAVOR OR OPPOSE BUILDING A WALL ON BORDER WITH MEXICO
anesWall = anes2020Data$V201424
wallData = replace(anesWall, anesWall==-9, NA)
wallData = replace(wallData, wallData==-8, 0)
wallData = replace(wallData, wallData==1, -1)
wallData = replace(wallData, wallData==2, 1)
wallData = replace(wallData, wallData==3, 0)
#V201429 BEST WAY TO DEAL WITH URBAN UNREST
anesUnrest = anes2020Data$V201429
unrestData = replace(anesUnrest, anesUnrest==-9, NA)
unrestData = replace(unrestData, unrestData==-8, 0)
unrestData = replace(unrestData, unrestData==99, 0)
unrestData = replace(unrestData, unrestData==1, 1)
unrestData = replace(unrestData, unrestData==2, 1)
unrestData = replace(unrestData, unrestData==3, 1)
unrestData = replace(unrestData, unrestData==4, 0)
unrestData = replace(unrestData, unrestData==5, -1)
unrestData = replace(unrestData, unrestData==6, -1)
unrestData = replace(unrestData, unrestData==7, -1)

allAnes2020Issues = cbind(medicalData,blacksData,securityData,borderData,crimeData,poorData,abortionData,
                  warmingData,gayServicesData,transData,gayJobsData,gayAdoptData,gayMarriageData,
                  immigrantsData,birthrightData,wallData,unrestData)
allData = removeConsesusDataForVar(allAnes2020Issues,0.5)
#describeData(allData)
cohAnes2020Extended = getCohProportionByPairs(allData)
summary(cohAnes2020Extended)

binaryAnes2020Issues = cbind(gayServicesData,transData,wallData,birthrightData,gayAdoptData)
cohAnes2020Binary = getCohProportionByPairs(binaryAnes2020Issues)
summary(cohAnes2020Binary)

#  ANES 2016  ----------------------------------------------------
anes2016Data = read_sav("anes_timeseries_2016.sav")
#Arrange data
#V161113 Healthcare
anesHealthcare = anes2016Data$V161113
anesHealthcare = replace(anesHealthcare, anesHealthcare==1, 1)
anesHealthcare = replace(anesHealthcare, anesHealthcare==2, -1)
anesHealthcare = replace(anesHealthcare, anesHealthcare==3, 0)
anesHealthcare = replace(anesHealthcare, anesHealthcare==-8, NA)
#V161154 Military
anesMilitary = anes2016Data$V161154
anesMilitary = replace(anesMilitary, anesMilitary==1, -1)
anesMilitary = replace(anesMilitary, anesMilitary==2, -1)
anesMilitary = replace(anesMilitary, anesMilitary==3, 0)
anesMilitary = replace(anesMilitary, anesMilitary==4, 1)
anesMilitary = replace(anesMilitary, anesMilitary==5, 1)
anesMilitary = replace(anesMilitary, anesMilitary==-8, 0)
anesMilitary = replace(anesMilitary, anesMilitary==-9, NA)
#V161184 Insurance
anesInsurance = anes2016Data$V161184
anesInsurance = replace(anesInsurance, anesInsurance==1, 1)
anesInsurance = replace(anesInsurance, anesInsurance==2, 1)
anesInsurance = replace(anesInsurance, anesInsurance==3, 1)
anesInsurance = replace(anesInsurance, anesInsurance==4, 0)
anesInsurance = replace(anesInsurance, anesInsurance==5, -1)
anesInsurance = replace(anesInsurance, anesInsurance==6, -1)
anesInsurance = replace(anesInsurance, anesInsurance==7, -1)
anesInsurance = replace(anesInsurance, anesInsurance==99, 0)
anesInsurance = replace(anesInsurance, anesInsurance==-8, 0)
anesInsurance = replace(anesInsurance, anesInsurance==-9, NA)
#V161196 Wall
anesWall = anes2016Data$V161196
anesWall = replace(anesWall, anesWall==1, -1)
anesWall = replace(anesWall, anesWall==2, 1)
anesWall = replace(anesWall, anesWall==3, 0)
anesWall = replace(anesWall, anesWall==-8, 0)
anesWall = replace(anesWall, anesWall==-9, NA)
#V161198 Black
anesBlack = anes2016Data$V161198
anesBlack = replace(anesBlack, anesBlack==1, 1)
anesBlack = replace(anesBlack, anesBlack==2, 1)
anesBlack = replace(anesBlack, anesBlack==3, 1)
anesBlack = replace(anesBlack, anesBlack==4, 0)
anesBlack = replace(anesBlack, anesBlack==5, -1)
anesBlack = replace(anesBlack, anesBlack==6, -1)
anesBlack = replace(anesBlack, anesBlack==7, -1)
anesBlack = replace(anesBlack, anesBlack==-8, 0)
anesBlack = replace(anesBlack, anesBlack==-9, NA)
anesBlack = replace(anesBlack, anesBlack==99, 0)
#V161201 Enviroment
anesEnviroment = anes2016Data$V161201
anesEnviroment = replace(anesEnviroment, anesEnviroment==1, 1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==2, 1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==3, 1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==4, 0)
anesEnviroment = replace(anesEnviroment, anesEnviroment==5, -1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==6, -1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==7, -1)
anesEnviroment = replace(anesEnviroment, anesEnviroment==-8, 0)
anesEnviroment = replace(anesEnviroment, anesEnviroment==-9, NA)
anesEnviroment = replace(anesEnviroment, anesEnviroment==99, 0)
#V161214 Syrian
anesSyrian = anes2016Data$V161214
anesSyrian = replace(anesSyrian, anesSyrian==1, 1)
anesSyrian = replace(anesSyrian, anesSyrian==2, -1)
anesSyrian = replace(anesSyrian, anesSyrian==3, 0)
anesSyrian = replace(anesSyrian, anesSyrian==-8, 0)
anesSyrian = replace(anesSyrian, anesSyrian==-9, NA)
#V161228 TransBathroom
anesTransBathroom = anes2016Data$V161228
anesTransBathroom = replace(anesTransBathroom, anesTransBathroom==1, -1)
anesTransBathroom = replace(anesTransBathroom, anesTransBathroom==2, 1)
anesTransBathroom = replace(anesTransBathroom, anesTransBathroom==-8, 0)
anesTransBathroom = replace(anesTransBathroom, anesTransBathroom==-9, NA)
#V161227 Same Sex Service
anesSameSexService = anes2016Data$V161227
anesSameSexService = replace(anesSameSexService, anesSameSexService==1, -1)
anesSameSexService = replace(anesSameSexService, anesSameSexService==2, 1)
anesSameSexService = replace(anesSameSexService, anesSameSexService==-8, 0)
anesSameSexService = replace(anesSameSexService, anesSameSexService==-9, NA)
#V161193 Birthright
anesBirthright = anes2016Data$V161193
anesBirthright = replace(anesBirthright, anesBirthright==1, -1)
anesBirthright = replace(anesBirthright, anesBirthright==2, 1)
anesBirthright = replace(anesBirthright, anesBirthright==3, 0)
anesBirthright = replace(anesBirthright, anesBirthright==-8, 0)
anesBirthright = replace(anesBirthright, anesBirthright==-9, NA)
#V161204 Affirmative Action
anesAffAction = anes2016Data$V161204
anesAffAction = replace(anesAffAction, anesAffAction==1, 1)
anesAffAction = replace(anesAffAction, anesAffAction==2, -1)
anesAffAction = replace(anesAffAction, anesAffAction==3, 0)
anesAffAction = replace(anesAffAction, anesAffAction==-8, 0)
anesAffAction = replace(anesAffAction, anesAffAction==-9, NA)
#V161213 ISIS
anesIsis = anes2016Data$V161213
anesIsis = replace(anesIsis, anesIsis==1, -1)
anesIsis = replace(anesIsis, anesIsis==2, 1)
anesIsis = replace(anesIsis, anesIsis==3, 0)
anesIsis = replace(anesIsis, anesIsis==-8, 0)
anesIsis = replace(anesIsis, anesIsis==-9, NA)
#V161226 Parental leave
anesParentalLeave = anes2016Data$V161226
anesParentalLeave = replace(anesParentalLeave, anesParentalLeave==1, 1)
anesParentalLeave = replace(anesParentalLeave, anesParentalLeave==2, -1)
anesParentalLeave = replace(anesParentalLeave, anesParentalLeave==3, 0)
anesParentalLeave = replace(anesParentalLeave, anesParentalLeave==-8, 0)
anesParentalLeave = replace(anesParentalLeave, anesParentalLeave==-9, NA)
#V161229 Gay protection
anesGayProtection = anes2016Data$V161229
anesGayProtection = replace(anesGayProtection, anesGayProtection==1, 1)
anesGayProtection = replace(anesGayProtection, anesGayProtection==2, -1)
anesGayProtection = replace(anesGayProtection, anesGayProtection==-8, 0)
anesGayProtection = replace(anesGayProtection, anesGayProtection==-9, NA)
#V161232 Abortion
anesAbortion = anes2016Data$V161232
anesAbortion = replace(anesAbortion, anesAbortion==1, -1)
anesAbortion = replace(anesAbortion, anesAbortion==2, -1)
anesAbortion = replace(anesAbortion, anesAbortion==3, 1)
anesAbortion = replace(anesAbortion, anesAbortion==4, 1)
anesAbortion = replace(anesAbortion, anesAbortion==5, NA)
anesAbortion = replace(anesAbortion, anesAbortion==-8, 0)
anesAbortion = replace(anesAbortion, anesAbortion==-9, NA)
#V161233 death penalty
anesDeath = anes2016Data$V161233
anesDeath = replace(anesDeath, anesDeath==1, -1)
anesDeath = replace(anesDeath, anesDeath==2, 1)
anesDeath = replace(anesDeath, anesDeath==-8, 0)
anesDeath = replace(anesDeath, anesDeath==-9, NA)
#V161343 protesters
anesProtesters = anes2016Data$V161343
anesProtesters = replace(anesProtesters, anesProtesters==1, 1)
anesProtesters = replace(anesProtesters, anesProtesters==2, 1)
anesProtesters = replace(anesProtesters, anesProtesters==3, 0)
anesProtesters = replace(anesProtesters, anesProtesters==4, -1)
anesProtesters = replace(anesProtesters, anesProtesters==5, -1)
anesProtesters = replace(anesProtesters, anesProtesters==-5, NA)
anesProtesters = replace(anesProtesters, anesProtesters==-9, NA)
#V161346 feminism
anesFeminism = anes2016Data$V161346
anesFeminism = replace(anesFeminism, anesFeminism==1, 1)
anesFeminism = replace(anesFeminism, anesFeminism==2, 1)
anesFeminism = replace(anesFeminism, anesFeminism==3, 0)
anesFeminism = replace(anesFeminism, anesFeminism==4, -1)
anesFeminism = replace(anesFeminism, anesFeminism==5, -1)
anesFeminism = replace(anesFeminism, anesFeminism==-5, NA)
anesFeminism = replace(anesFeminism, anesFeminism==-9, NA)
#V162123 Countries like America
anesUS = anes2016Data$V162123
anesUS = replace(anesUS, anesUS==1, -1)
anesUS = replace(anesUS, anesUS==2, -1)
anesUS = replace(anesUS, anesUS==3, 0)
anesUS = replace(anesUS, anesUS==4, 1)
anesUS = replace(anesUS, anesUS==5, 1)
anesUS = replace(anesUS, anesUS==-6, NA)
anesUS = replace(anesUS, anesUS==-7, NA)
anesUS = replace(anesUS, anesUS==-8, 0)
anesUS = replace(anesUS, anesUS==-9, NA)
#V162125x Flag
anesFlag = anes2016Data$V162125x
anesFlag = replace(anesFlag, anesFlag==1, -1)
anesFlag = replace(anesFlag, anesFlag==2, -1)
anesFlag = replace(anesFlag, anesFlag==3, -1)
anesFlag = replace(anesFlag, anesFlag==4, 0)
anesFlag = replace(anesFlag, anesFlag==5, 1)
anesFlag = replace(anesFlag, anesFlag==6, 1)
anesFlag = replace(anesFlag, anesFlag==7, 1)
anesFlag = replace(anesFlag, anesFlag==-6, NA)
anesFlag = replace(anesFlag, anesFlag==-7, NA)
anesFlag = replace(anesFlag, anesFlag==-8, 0)
anesFlag = replace(anesFlag, anesFlag==-9, NA)
#V162150x equal pay
anesEqualPay = anes2016Data$V162150x
anesEqualPay = replace(anesEqualPay, anesEqualPay==1, 1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==2, 1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==3, 1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==4, 0)
anesEqualPay = replace(anesEqualPay, anesEqualPay==5, -1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==6, -1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==7, -1)
anesEqualPay = replace(anesEqualPay, anesEqualPay==-6, NA)
anesEqualPay = replace(anesEqualPay, anesEqualPay==-7, NA)
anesEqualPay = replace(anesEqualPay, anesEqualPay==-8, 0)
anesEqualPay = replace(anesEqualPay, anesEqualPay==-9, NA)
#V162168 free thinkers
anesFreeThinkers = anes2016Data$V162168
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==1, 1)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==2, 1)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==3, 0)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==4, -1)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==5, -1)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==-6, NA)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==-7, NA)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==-8, 0)
anesFreeThinkers = replace(anesFreeThinkers, anesFreeThinkers==-9, NA)
#V162169 forefathers
anesForefathers = anes2016Data$V162169
anesForefathers = replace(anesForefathers, anesForefathers==1, -1)
anesForefathers = replace(anesForefathers, anesForefathers==2, -1)
anesForefathers = replace(anesForefathers, anesForefathers==3, 0)
anesForefathers = replace(anesForefathers, anesForefathers==4, 1)
anesForefathers = replace(anesForefathers, anesForefathers==5, 1)
anesForefathers = replace(anesForefathers, anesForefathers==-6, NA)
anesForefathers = replace(anesForefathers, anesForefathers==-7, NA)
anesForefathers = replace(anesForefathers, anesForefathers==-8, 0)
anesForefathers = replace(anesForefathers, anesForefathers==-9, NA)
#V162170 strong leader
anesLeader = anes2016Data$V162170
anesLeader = replace(anesLeader, anesLeader==1, -1)
anesLeader = replace(anesLeader, anesLeader==2, -1)
anesLeader = replace(anesLeader, anesLeader==3, 0)
anesLeader = replace(anesLeader, anesLeader==4, 1)
anesLeader = replace(anesLeader, anesLeader==5, 1)
anesLeader = replace(anesLeader, anesLeader==-6, NA)
anesLeader = replace(anesLeader, anesLeader==-7, NA)
anesLeader = replace(anesLeader, anesLeader==-8, 0)
anesLeader = replace(anesLeader, anesLeader==-9, NA)
#V162186 business regulation
anesRegulation = anes2016Data$V162186
anesRegulation = replace(anesRegulation, anesRegulation==1, 1)
anesRegulation = replace(anesRegulation, anesRegulation==2, 1)
anesRegulation = replace(anesRegulation, anesRegulation==3, 0)
anesRegulation = replace(anesRegulation, anesRegulation==4, -1)
anesRegulation = replace(anesRegulation, anesRegulation==5, -1)
anesRegulation = replace(anesRegulation, anesRegulation==-6, NA)
anesRegulation = replace(anesRegulation, anesRegulation==-7, NA)
anesRegulation = replace(anesRegulation, anesRegulation==-8, 0)
anesRegulation = replace(anesRegulation, anesRegulation==-9, NA)
#V162210 traditional family
anesFamily = anes2016Data$V162210
anesFamily = replace(anesFamily, anesFamily==1, -1)
anesFamily = replace(anesFamily, anesFamily==2, -1)
anesFamily = replace(anesFamily, anesFamily==3, 0)
anesFamily = replace(anesFamily, anesFamily==4, 1)
anesFamily = replace(anesFamily, anesFamily==5, 1)
anesFamily = replace(anesFamily, anesFamily==-6, NA)
anesFamily = replace(anesFamily, anesFamily==-7, NA)
anesFamily = replace(anesFamily, anesFamily==-8, 0)
anesFamily = replace(anesFamily, anesFamily==-9, NA)
#V162211 help blacks
anesBlacks = anes2016Data$V162211
anesBlacks = replace(anesBlacks, anesBlacks==1, -1)
anesBlacks = replace(anesBlacks, anesBlacks==2, -1)
anesBlacks = replace(anesBlacks, anesBlacks==3, 0)
anesBlacks = replace(anesBlacks, anesBlacks==4, 1)
anesBlacks = replace(anesBlacks, anesBlacks==5, 1)
anesBlacks = replace(anesBlacks, anesBlacks==-6, NA)
anesBlacks = replace(anesBlacks, anesBlacks==-7, NA)
anesBlacks = replace(anesBlacks, anesBlacks==-8, 0)
anesBlacks = replace(anesBlacks, anesBlacks==-9, NA)
#V162221 hispanics
anesHispanics = anes2016Data$V162221
anesHispanics = replace(anesHispanics, anesHispanics==1, 1)
anesHispanics = replace(anesHispanics, anesHispanics==2, 1)
anesHispanics = replace(anesHispanics, anesHispanics==3, 0)
anesHispanics = replace(anesHispanics, anesHispanics==4, -1)
anesHispanics = replace(anesHispanics, anesHispanics==5, -1)
anesHispanics = replace(anesHispanics, anesHispanics==-6, NA)
anesHispanics = replace(anesHispanics, anesHispanics==-7, NA)
anesHispanics = replace(anesHispanics, anesHispanics==-8, 0)
anesHispanics = replace(anesHispanics, anesHispanics==-9, NA)
#V162244 equality
anesEquality = anes2016Data$V162244
anesEquality = replace(anesEquality, anesEquality==1, -1)
anesEquality = replace(anesEquality, anesEquality==2, -1)
anesEquality = replace(anesEquality, anesEquality==3, 0)
anesEquality = replace(anesEquality, anesEquality==4, 1)
anesEquality = replace(anesEquality, anesEquality==5, 1)
anesEquality = replace(anesEquality, anesEquality==-6, NA)
anesEquality = replace(anesEquality, anesEquality==-7, NA)
anesEquality = replace(anesEquality, anesEquality==-8, 0)
anesEquality = replace(anesEquality, anesEquality==-9, NA)
#V162266 traditions
anesTraditions = anes2016Data$V162266
anesTraditions = replace(anesTraditions, anesTraditions==1, -1)
anesTraditions = replace(anesTraditions, anesTraditions==2, -1)
anesTraditions = replace(anesTraditions, anesTraditions==3, 0)
anesTraditions = replace(anesTraditions, anesTraditions==4, 1)
anesTraditions = replace(anesTraditions, anesTraditions==5, 1)
anesTraditions = replace(anesTraditions, anesTraditions==-6, NA)
anesTraditions = replace(anesTraditions, anesTraditions==-7, NA)
anesTraditions = replace(anesTraditions, anesTraditions==-8, 0)
anesTraditions = replace(anesTraditions, anesTraditions==-9, NA)
#V162268 immigrants economy
anesImmigrantsEconomy = anes2016Data$V162268
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==1, 1)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==2, 1)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==3, 0)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==4, -1)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==5, -1)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==-6, NA)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==-7, NA)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==-8, 0)
anesImmigrantsEconomy = replace(anesImmigrantsEconomy, anesImmigrantsEconomy==-9, NA)
#V162270 immigrants crime
anesImmigrantsCrime = anes2016Data$V162270
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==1, -1)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==2, -1)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==3, 0)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==4, 1)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==5, 1)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==-6, NA)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==-7, NA)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==-8, 0)
anesImmigrantsCrime = replace(anesImmigrantsCrime, anesImmigrantsCrime==-9, NA)
#V162276 differences
anesDifferences = anes2016Data$V162276
anesDifferences = replace(anesDifferences, anesDifferences==1, 1)
anesDifferences = replace(anesDifferences, anesDifferences==2, 1)
anesDifferences = replace(anesDifferences, anesDifferences==3, 0)
anesDifferences = replace(anesDifferences, anesDifferences==4, -1)
anesDifferences = replace(anesDifferences, anesDifferences==5, -1)
anesDifferences = replace(anesDifferences, anesDifferences==-6, NA)
anesDifferences = replace(anesDifferences, anesDifferences==-7, NA)
anesDifferences = replace(anesDifferences, anesDifferences==-8, 0)
anesDifferences = replace(anesDifferences, anesDifferences==-9, NA)
#V162295 torture
anesTorture = anes2016Data$V162295
anesTorture = replace(anesTorture, anesTorture==1, -1)
anesTorture = replace(anesTorture, anesTorture==2, 1)
anesTorture = replace(anesTorture, anesTorture==3, 0)
anesTorture = replace(anesTorture, anesTorture==-6, NA)
anesTorture = replace(anesTorture, anesTorture==-7, NA)
anesTorture = replace(anesTorture, anesTorture==-8, 0)
anesTorture = replace(anesTorture, anesTorture==-9, NA)

allAnes2016Issues = cbind(anesHealthcare, anesMilitary, anesInsurance, anesWall, anesBlack,
                          anesEnviroment, anesSyrian, anesTransBathroom, anesSameSexService, anesBirthright,
                          anesAffAction, anesIsis, anesParentalLeave, anesGayProtection, anesAbortion,
                          anesDeath, anesProtesters, anesFeminism, anesUS, anesFlag, anesEqualPay,
                          anesFreeThinkers, anesForefathers, anesLeader, anesRegulation, anesFamily,
                          anesBlacks, anesHispanics, anesEquality, anesTraditions, anesImmigrantsEconomy, 
                          anesImmigrantsCrime, anesDifferences, anesTorture)
allData = removeConsesusDataForVar(allAnes2016Issues,0.5)
#describeData(allData)
cohAnes2016Extended = getCohProportionByPairs(allData)
summary(cohAnes2016Extended)

binaryAnes2016Issues = cbind(anesHealthcare, anesWall, anesSyrian, anesTransBathroom, anesSameSexService, anesBirthright, 
                             anesAffAction, anesIsis, anesParentalLeave, anesGayProtection, anesDeath, anesTorture)
allDataBinary = removeConsesusDataForVar(binaryAnes2016Issues,0.5)
cohAnes2016Binary = getCohProportionByPairs(allDataBinary)
summary(cohAnes2016Binary)

#  Freira et al  ----------------------------------------------------
FreiraArg = read.csv("FreiraArg.csv", header = TRUE)
FreiraBra = read.csv("FreiraBra.csv", header = TRUE)
FreiraUru = read.csv("FreiraUru.csv", header = TRUE)
FreiraUSA = read.csv("FreiraUSA.csv", header = TRUE)

selectedFreiraArg = removeConsesusDataForVar(FreiraArg,0.5)
#describeData(selectedFreiraArg)
cohFreiraArg = getCohProportionByPairs(selectedFreiraArg)
summary(cohFreiraArg)

selectedFreiraBra = removeConsesusDataForVar(FreiraBra,0.5)
#describeData(selectedFreiraBra)
cohFreiraBra = getCohProportionByPairs(selectedFreiraBra)
summary(cohFreiraBra)

selectedFreiraUru = removeConsesusDataForVar(FreiraUru,0.5)
#describeData(selectedFreiraUru)
cohFreiraUru = getCohProportionByPairs(selectedFreiraUru)
summary(cohFreiraUru)

selectedFreiraUSA = removeConsesusDataForVar(FreiraUSA,0.5)
#describeData(selectedFreiraUSA)
cohFreiraUSA = getCohProportionByPairs(selectedFreiraUSA)
summary(cohFreiraUSA)

#  Pew 2020 Government  ----------------------------------------------------
dataset = read_sav("March 24-29 2020 public.sav")
#a. The Centers for Disease Control and Prevention, the CDC
#b. The Department of Homeland Security
#c. The Internal Revenue Service, the IRS
#d. The Justice Department
#e. The Department of Health and Human Services, the HHS
#f. The Census Bureau
#g. The Postal Service
#h. The Federal Reserve
#i. The Department of Veterans Affairs, the VA
#j. The Immigration and Customs Enforcement, known as ICE [PRONOUNCED: ‘ice’]
responses = dataset[,7:16]
arrayTypeResponses=array(unlist(responses), dim=dim(responses))
#Arrange data
pew2020data = replace(arrayTypeResponses, arrayTypeResponses==1, 1)
pew2020data = replace(pew2020data, pew2020data==2, 1)
pew2020data = replace(pew2020data, pew2020data==3, -1)
pew2020data = replace(pew2020data, pew2020data==4, -1)
pew2020data = replace(pew2020data, pew2020data==5, NA)
pew2020data = replace(pew2020data, pew2020data==8, NA)
pew2020data = replace(pew2020data, pew2020data==9, NA)

selectedPew2020 = removeConsesusDataForVar(pew2020data,0.5) #.75
#describeData(selectedPew2020)
cohPew2020 = getCohProportionByPairs(selectedPew2020)
summary(cohPew2020)

#  Pew 2014 Behavior  ----------------------------------------------------
dataset = read_sav("ATP W6.sav")
#Donate money, White lie, Lose your temper, Eat too much, Meditate
responses = dataset[,19:23]
arrayTypeResponses=array(unlist(responses), dim=dim(responses))
pew2014data = replace(arrayTypeResponses, arrayTypeResponses==2, -1)
pew2014data = replace(pew2014data, pew2014data==99, NA)

selectedPew2014 = removeConsesusDataForVar(pew2014data,0.5)
#describeData(selectedPew2014)
cohPew2014 = getCohProportionByPairs(selectedPew2014)
summary(cohPew2014)

#  Export For Python ----------------------------------------------------
cohProportion = c(cohZimmSt1Pol,cohZimmSt1NonPol,cohZimmOnlinePolA,cohZimmOnlinePolB,cohZimmOnlineHedA,cohZimmOnlineHedB,
                  cohAnes2020Extended,cohAnes2020Binary,cohAnes2016Extended,cohAnes2016Binary,cohFreiraArg,cohFreiraBra,cohFreiraUru,cohFreiraUSA,cohPew2020,cohPew2014)
cohLabel = c(
  replicate(length(cohZimmSt1Pol), "cohZimmSt1Pol"),
  replicate(length(cohZimmSt1NonPol), "cohZimmSt1NonPol"),
  replicate(length(cohZimmOnlinePolA), "cohZimmOnlinePolA"),
  replicate(length(cohZimmOnlinePolB), "cohZimmOnlinePolB"),
  replicate(length(cohZimmOnlineHedA), "cohZimmOnlineHedA"),
  replicate(length(cohZimmOnlineHedB), "cohZimmOnlineHedB"),
  replicate(length(cohAnes2020Extended), "cohAnes2020Extended"),
  replicate(length(cohAnes2020Binary), "cohAnes2020Binary"),
  replicate(length(cohAnes2016Extended), "cohAnes2016Extended"),
  replicate(length(cohAnes2016Binary), "cohAnes2016Binary"),
  replicate(length(cohFreiraArg), "cohFreiraArg"),
  replicate(length(cohFreiraBra), "cohFreiraBra"),
  replicate(length(cohFreiraUru), "cohFreiraUru"),
  replicate(length(cohFreiraUSA), "cohFreiraUSA"),
  replicate(length(cohPew2020), "cohPew2020"),
  replicate(length(cohPew2014), "cohPew2014")
)
isPol = c(
  replicate(length(cohZimmSt1Pol), 1),
  replicate(length(cohZimmSt1NonPol), 0),
  replicate(length(cohZimmOnlinePolA), 1),
  replicate(length(cohZimmOnlinePolB), 1),
  replicate(length(cohZimmOnlineHedA), 0),
  replicate(length(cohZimmOnlineHedB), 0),
  replicate(length(cohAnes2020Extended), 1),
  replicate(length(cohAnes2020Binary), 1),
  replicate(length(cohAnes2016Extended), 1),
  replicate(length(cohAnes2016Binary), 1),
  replicate(length(cohFreiraArg), 1),
  replicate(length(cohFreiraBra), 1),
  replicate(length(cohFreiraUru), 1),
  replicate(length(cohFreiraUSA), 1),
  replicate(length(cohPew2020), 1),
  replicate(length(cohPew2014), 0)
)
#Merge and save data
df <- data.frame(cohProportion,cohLabel,isPol)
#write.csv(df, "ExportForPython.csv", row.names=FALSE)