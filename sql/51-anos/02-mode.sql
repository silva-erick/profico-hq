-- campaigns per year: mode
SELECT        strftime('%Y', online_date) year
            , COUNT(1) campaigns
            , COUNT(1) FILTER (WHERE mode = 'aon') aon
            , COUNT(1) FILTER (WHERE mode = 'flex') flex
FROM        campaign
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    strftime('%Y', online_date)
