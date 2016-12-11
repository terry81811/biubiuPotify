library(plyr)
library(ggplot2)
data <- read.csv("metaData_all.tsv", sep="\t", header=F)
data <- data[, c(2:ncol(data))]
data$V6 <- as.Date(data$V6, '%Y-%m-%d')
colnames(data) <- c('userId','restaurantId', 'rating', 'label', 'date')
head(data)
summary(data)

restaurant <- ddply(data, c("restaurantId"), summarise, 
                    nreview = length(userId), 
                    filtered = sum(label==-1),
                    unfiltered = sum(label==1),
                    avgRating = mean(rating),
                    filteredRatio = sum(label==-1)/length(label),
                    reviewTimespan = max(date)-min(date))
summary(restaurant[which(restaurant$highFiltered==FALSE),])
head(restaurant[order(-restaurant$filteredRatio),],10)
restaurant$highFiltered <- restaurant$filteredRatio>0.2
restaurant$singleton <- restaurant$nreview==1

#Number of review distribution
qplot(data=restaurant, x=nreview, binwidth=100)

#Number of restaurants by filtered review ratio
qplot(data=restaurant.reviewcap, x=filteredRatio, binwidth=0.05)

cdat <- ddply(restaurant, "highFiltered", summarise, avgRating.mean=mean(avgRating))
ggplot(restaurant, aes(x=avgRating, fill=highFiltered)) +
  geom_histogram(binwidth=.5, alpha=.5, position="identity") +
  geom_vline(data=cdat, aes(xintercept=avgRating.mean,  colour=highFiltered),
             linetype="dashed", size=1)

ggplot(restaurant, aes(x=nreview, fill=highFiltered)) +
  geom_histogram(binwidth=100, position="stack")

cdat <- ddply(restaurant, "highFiltered", summarise, reviewTimespan.mean=mean(reviewTimespan))
ggplot(restaurant, aes(x=reviewTimespan, fill=highFiltered)) +
  geom_histogram(binwidth=100, alpha=.5, position="identity") +
  geom_vline(data=cdat, aes(xintercept=reviewTimespan.mean,  colour=highFiltered),
             linetype="dashed", size=1)
#Review level plots
reviewf <- read.csv("review_features_labeled.tsv", sep="\t", header=T)
head(reviewf)
reviewf$label <- as.factor(reviewf$label)

for(i in 6:(ncol(reviewf)-1)){
  ggplot(reviewf, aes_string(colnames(reviewf)[i], colour = "label")) + stat_ecdf()
  ggsave(file=paste(colnames(reviewf)[i],".png", sep=""))
}

restaurantf <- read.csv("restaurant_features_labeled.tsv", sep="\t", header=T)
restaurantf$label <- restaurantf$fraction<=0.2
for(i in 5:(ncol(restaurantf)-2)){
  ggplot(restaurantf, aes_string(colnames(restaurantf)[i], colour = "label")) + stat_ecdf()
  ggsave(file=paste(colnames(restaurantf)[i],".png", sep=""))
}