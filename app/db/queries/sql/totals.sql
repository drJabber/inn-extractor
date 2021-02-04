-- name: get-people-totals^
SELECT  
    sum(if(inn>0,1,0)) has_inn,
    sum(if(inn=0,1,0)) no_inn,
    sum(status is null) processed,
    sum(status is null and inn=0 and docdt!='') to_process,
    count(id) total
FROM people;

-- name: get-people-totals-for-task^
SELECT  
    sum(if(inn>0,1,0)) has_inn,
    sum(if(inn=0,1,0)) no_inn,
    sum(status is null) processed,
    sum(status is null and inn=0 and docdt!='') to_process,
    count(id) total
FROM people
where task_id=:task_id
;
