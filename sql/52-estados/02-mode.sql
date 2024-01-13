-- campaigns per uf: mode
SELECT        address_state_acronym uf
            , COUNT(1) campaigns
            , COUNT(1) FILTER (WHERE mode = 'aon') aon
            , COUNT(1) FILTER (WHERE mode = 'flex') flex
FROM        campaign
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    address_state_acronym
