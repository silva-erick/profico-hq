-- campaigns per year: mode and state
SELECT        strftime('%Y', online_date) year
            , COUNT(1) campaigns
            , COUNT(1) FILTER (WHERE mode = 'aon') aon
            , 100.0 * COUNT(1) FILTER (WHERE mode = 'aon' AND state != 'failed')/COUNT(1) FILTER (WHERE mode = 'aon') aon_success_rate
            , COUNT(1) FILTER (WHERE mode = 'flex') flex
            , 100.0 * COUNT(1) FILTER (WHERE mode = 'flex' AND state != 'failed')/COUNT(1) FILTER (WHERE mode = 'flex') flex_success_rate
FROM        campaign
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    strftime('%Y', online_date)