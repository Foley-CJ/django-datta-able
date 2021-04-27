'use strict';
$(document).ready(function() {
    setTimeout(function() {
    // [ bar-simple ] chart start
    Morris.Bar({
        element: 'morris-bar-chart5',
        data: graph5,
        xkey: 'TweetNumber',
        barSizeRatio: 0.70,
        barGap: 3,
        resize: true,
        responsive:true,
        ykeys: ['SentimentScore'],
        labels: ['SentimentScore'],
        barColors: ["0-#1de9b6-#1dc4e9"]
    });
    // [ bar-simple ] chart end

        }, 700);
});



