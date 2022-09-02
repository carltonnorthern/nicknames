-- Sample queries indicating how to use the tables with nickname data:
--   * nicknames 
--   * nicknames_normalized


-- The table "nicknames" is exactly parallel to the file names.csv.
-- All canonical names in this repo
select canonical_name 
from nicknames 
order by canonical_name ;

-- All nicknames for alexander (1 row with N non-null values)
select * 
from nicknames
where canonical_name = 'alexander' ;


-- The table "nicknames_normalized" converts names.csv into a normalized structure
-- All canonical names in this repo
select canonical_name 
from nicknames_normalized
group by canonical_name
order by canonical_name ;

-- All nicknames for alexander (N rows with 1 nickname each)
select nickname
from nicknames_normalized
where canonical_name = 'alexander' ;

-- All canonical names for which 'al' is a nickname
select canonical_name
from nicknames_normalized
where nickname = 'al' ;
