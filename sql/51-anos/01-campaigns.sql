-- campaigns per year
SELECT        strftime('%Y', online_date) year
            , COUNT(1) campaigns
FROM        campaign
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    strftime('%Y', online_date)
