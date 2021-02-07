-- name: get-people-totals^
SELECT  
    sum(
        case
          when inn<>'0' then 1
          else 0
        end  
    ) has_inn,
    sum(
        case
          when inn='0' then 1
          else 0
        end  
    ) no_inn,
    sum(
        case
          when status<>'new' then 1
          else 0
        end  
    ) processed,
    sum(        
        case
          when status='new' and inn='0' and docdt!='' then 1
          else 0
        end  
    ) to_process,
    count(id) total
FROM people;

-- name: get-people-totals-for-task^
SELECT  
    sum(
        case
          when inn<>'0' then 1
          else 0
        end  
    ) has_inn,
    sum(
        case
          when inn='0' then 1
          else 0
        end  
    ) no_inn,
    sum(
        case
          when status<>'new' then 1
          else 0
        end  
    ) processed,
    sum(        
        case
          when status='new' and inn='0' and docdt!='' then 1
          else 0
        end  
    ) to_process,
    count(id) total
FROM people
where task_id=:task_id
;
