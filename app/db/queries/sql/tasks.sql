-- name: get-task-by-id^
select  id,
        dt,
        state,
--        file,
        updated_at,
        created_at
FROM tasks
WHERE id=:task_id
LIMIT 1;

-- name: get-all-tasks^
select  id,
        dt,
        state,
--        file,
        updated_at,
        created_at
FROM tasks;

-- name: get-tasks-for-work^
select  id,
        dt,
        state,
--        file,
        updated_at,
        created_at
FROM tasks
where state<>'done';

-- name: create-new-task<!
INSERT INTO tasks (dt, state)
VALUES (:dt, :state)
RETURNING
    id, created_at, updated_at;

-- name: update-task-state<!
UPDATE
    tasks
SET state   = :new_state,
WHERE id = :task_id
RETURNING
    updated_at;
