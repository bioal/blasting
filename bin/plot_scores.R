#!/home/chiba/etc/hc-utils/rscript

x = t$V1
y = t$V2

plot(x, y, xlab="", ylab="BLAST score"
     , xlim=c(1,21)
     , xaxt = "n"
     )

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
