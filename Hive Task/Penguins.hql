SELECT * 
FROM penguins 
LIMIT 10;


SELECT 
    species, 
    island, 
    COUNT(*) AS num_records
FROM penguins
GROUP BY 
    species, 
    island
ORDER BY 
    species, 
    island;


SELECT 
    species,
    ROUND(AVG(body_mass_g), 2)       AS avg_body_mass_g,
    ROUND(AVG(flipper_length_mm), 2) AS avg_flipper_length_mm
FROM penguins
GROUP BY 
    species;


SELECT
    SUM(CASE WHEN bill_length_mm    IS NULL          THEN 1 ELSE 0 END) AS missing_bill_length_mm,
    SUM(CASE WHEN flipper_length_mm IS NULL          THEN 1 ELSE 0 END) AS missing_flipper_length_mm,
    SUM(CASE WHEN body_mass_g       IS NULL          THEN 1 ELSE 0 END) AS missing_body_mass_g,
    SUM(CASE WHEN sex               IS NULL OR sex = '' THEN 1 ELSE 0 END) AS missing_sex
FROM penguins;