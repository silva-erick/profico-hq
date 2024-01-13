-- campaigns per year: mode and state
SELECT        strftime('%Y', online_date) year
            , COUNT(1) campaigns
            , COUNT(1) FILTER (WHERE mode = 'aon' AND state != 'failed') aon_success
            , COUNT(1) FILTER (WHERE mode = 'aon' AND state = 'failed') aon_failed
            , COUNT(1) FILTER (WHERE mode = 'flex' AND state != 'failed') flex_success
            , COUNT(1) FILTER (WHERE mode = 'flex' AND state = 'failed') flex_failed
FROM        campaign
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    strftime('%Y', online_date)
