Hao-0
================
Bruce Hao
September 1, 2016

Lab 0 setup:

``` r
source('more/arbuthnot.R')
```

<i>Exercise 1: What command would you use to extract just the counts of girls baptized?</i>

``` r
arbuthnot$girls
```

    ##  [1] 4683 4457 4102 4590 4839 4820 4928 4605 4457 4952 4784 5332 5200 4910
    ## [15] 4617 3997 3919 3395 3536 3181 2746 2722 2840 2908 2959 3179 3349 3382
    ## [29] 3289 3013 2781 3247 4107 4803 4881 5681 4858 4319 5322 5560 5829 5719
    ## [43] 6061 6120 5822 5738 5717 5847 6203 6033 6041 6299 6533 6744 7158 7127
    ## [57] 7246 7119 7214 7101 7167 7302 7392 7316 7483 6647 6713 7229 7767 7626
    ## [71] 7452 7061 7514 7656 7683 5738 7779 7417 7687 7623 7380 7288

<i>Exercise 2: Is there an apparent trend in the number of girls baptized over the years? How would you describe it?</i>

As illustrated in the chart below, the number of girls baptized appears to increase with time, except for a sharp drop around 1650.

``` r
plot(arbuthnot$year, arbuthnot$girls, type='l')
```

![](Hao-0_files/figure-markdown_github/unnamed-chunk-3-1.png)

<i>Exercise 3: Now, make a plot of the proportion of boys over time. What do you see?</i>

While the proportion oscillates between a minimum of 0.5027 and maximum of 0.5362 with a mean of 0.5210, it's interesting that the ratio of boys never drops below 50% in any year.

``` r
summary(arbuthnot$boys / (arbuthnot$boys + arbuthnot$girls))
```

    ##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
    ##  0.5027  0.5118  0.5157  0.5170  0.5210  0.5362

``` r
plot(arbuthnot$year, arbuthnot$boys / (arbuthnot$boys + arbuthnot$girls), type='l')
```

![](Hao-0_files/figure-markdown_github/unnamed-chunk-4-1.png)
