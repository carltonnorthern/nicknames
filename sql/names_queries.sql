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


-- The table "nicknames_normalized" contains RDF triples with name1, relationship, name2
-- All canonical names in this repo
select name1 
from nicknames_normalized
where relationship = 'has_nickname'
group by name1
order by name1 ;

-- All nicknames for alexander (N rows with 1 nickname each)
select name2 as nickname
from nicknames_normalized
where name1 = 'alexander' and relationship = 'has_nickname' ;

-- All canonical names for which 'al' is a nickname
select name1 as canonical_name
from nicknames_normalized
where name2 = 'al' and relationship = 'has_nickname' ;
