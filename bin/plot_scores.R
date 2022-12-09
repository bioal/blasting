#!/home/chiba/etc/hc-utils/rscript

x = t$V1
y = t$V2
bbh = t$V3

plot(x, y, xlab="", ylab="BLAST score"
     , xlim=c(1,21)
     # , ylim=c(0,max(y))
     , ty = "n"
     , xaxt = "n"
     )

abline(v=1:21, lty=3, col="gray")
abline(h=seq(100,1500,by=100), lty=2, col="gray")

hit_x = x[bbh==0]
hit_y = y[bbh==0]
bbh_x = x[bbh==1]
bbh_y = y[bbh==1]
points(hit_x, hit_y)
points(bbh_x, bbh_y, col="red")

axis(side=1
     , las=2
     , at=c(
         1, 2, 3, 4, 5, 6, 7, 8
         , 9, 10, 11, 12, 13
         , 14, 15
         , 16, 17, 18, 19
         , 20
         , 21
         )
     , labels=c(
         'human','chimp', 'monkey', 'mouse','rat','dog', 'cow', 'chicken'
         , 'Xenopus', 'zebrafish', 'Drosophila', 'mosquito', 'nematode'
         , 'yeast', ''
         , '', '', '', ''
         , 'plant', ''
         ))
