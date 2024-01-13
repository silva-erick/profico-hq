-- campaigns per uf
SELECT        u.acronym uf
            , COUNT(c.campaign_id) campaigns
FROM        uf u
LEFT JOIN   campaign c
ON          u.acronym = c.address_state_acronym
WHERE       strftime('%Y', date())!=strftime('%Y', online_date)
GROUP BY    u.acronym
