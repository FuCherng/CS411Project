library(dplyr)
library(plyr) #ddply
library(caret)
# library(lattice)
# library(ggplot2)
#------ read features
db=read.csv('/Users/fuyincherng/Documents/EPFLCourse/DigitalEducation/R/Dataset and Scripts-20161108/OutputTable.csv', stringsAsFactors = F)

#------ sort submissions
db=db[order(db$UserID,db$ProblemID,db$SubmissionNumber),]

#--- replace NA values with 0
db[is.na(db)]=0

#----- remove first submissions
db= filter(db,db$SubmissionNumber>0)

#---- remove cases when there is no video or forum activity between two submissions
#d$Guzzler <- factor(ifelse(d$MPG.city > median(d$MPG.city),"GUZZLER","ECONOMY"))
db$NVideoAndForum<- db$NVideoEvents+db$NForumEvents
db= filter(db,db$NVideoAndForum>0)  

#----- make a catgorical vribale, indicating if grade improved
db$improved = factor(ifelse(db$GradeDiff>0 ,'Yes', 'No' ))
table(db$improved)

#----- visualize features per each category
boxplot(db$TimeSinceLast ~ db$improved, main="improve by TimeSinceLast", horizontal = T, outline=F)
boxplot(db$NForumEvents ~ db$improved , main="improve by NForumEvents", horizontal = T, outline=F)
boxplot(db$NVideoEvents ~ db$improved , main="improve by NVideoEvents", horizontal = T, outline=F)
boxplot(db$NumberOfThreadViews ~ db$improved , main="improve by NumberOfThreadViews", horizontal = T, outline=F)


#============ train a classifier to predict 'improved' status =============

# ----- 1. split data into train and test set
set.seed(1234)
tr.index= sample(nrow(db), nrow(db)*0.6) 
#return the number of row in db; sample(sampleRange, how many number generate(Rounded:5.5->5))
#so the above line means there are 60% of all data token as train data. 40% as the test data
db.train= db[tr.index,]
db.test = db[-tr.index,]


#-----
# Train a classifier to identify which features are most predictive
# of an increase versus decrease of the grade. Try different methods, 
# model parameters, features set and find the best classifier (highest 'kappa' value on test set.)
# try to achieve a model with kappa > 0.5 

#----- Train the model and tuning the model (more info: https://topepo.github.io/caret/model-training-and-tuning.html)
#TrainControl is to set the validation method
fitControl <- trainControl( ##10-flod CV
                           method = "repeatedcv",
                           number=1,
                           ##repeated ten times
                           repeats=1,
                           savePred=T,
                           classProbs=T,
                           summaryFunction = twoClassSummary
                          )
gbmfit1 <- train(improved ~ ., data=db.train,
                 method = "svmRadial",
                 tuneLength = 9,
                 preProc = c("center","scale"),
                 #metric="ROC",
                 trControal = fitControl
                 )

gbmfit1
#----- Test the model
#predict(model, newdata=db.test)






