-- Sample queries indicating how to use the tables with nickname data:
--   * nicknames 
--   * nicknames_normalized

-- The table "name_relationships" is exactly parallel to the file names.csv.
-- Get all nicknames for alexander
select * 
from name_relationships
where 
    relationship = 'has_nickname' AND
    name1 = 'alexander'
order by name1, name2;
-- alexander,has_nickname,al
-- alexander,has_nickname,alec
-- alexander,has_nickname,alex
-- alexander,has_nickname,sandy

-- The table "nicknames" has one row per canonical name with all nicknames in N non-null columns.
-- Get all nicknames for alexander
select * 
from nicknames
where canonical_name = 'alexander' ;
-- alexander,al,alec,alex,sandy
