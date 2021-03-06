-- name: get-person-by-id^
SELECT  id,
        family,
        name,
        patronimic_name,
        bdate,
        docser,
        docno,
        docdt,
        snils,
        inn,
        status,
        task_id
FROM people
WHERE id = :person_id;


-- name: get-people-by-task-id
SELECT  id,
        family,
        name,
        patronimic_name,
        bdate,
        docser,
        docno,
        docdt,
        snils,
        inn,
        status,
        task_id
FROM people
WHERE task_id = :task_id;

-- name: get-good-people-by-task-id
SELECT  id,
        family,
        name,
        patronimic_name,
        bdate,
        docser,
        docno,
        docdt,
        snils,
        inn,
        status,
        task_id
FROM people
WHERE task_id = :task_id and status='ok';

-- name: get-person-for-work-by-task-id^
SELECT  id,
        family,
        name,
        patronimic_name,
        bdate,
        docser,
        docno,
        docdt,
        snils,
        inn,
        status,
        task_id
FROM people
WHERE task_id = :task_id and status='new'
ORDER BY id 
LIMIT 1;

-- name: create-new-person<!
INSERT INTO people (family, name, patronimic_name, bdate, docser, docno, docdt, snils, inn, status, task_id)
VALUES (:family, :name, :patronimic_name, :bdate, :docser, :docno, :docdt, :snils, :inn, :status, :task_id)
RETURNING
    id, task_id;


-- name: update-person-inn-and-status<!
UPDATE
    people
SET status  = :new_status,
    inn = :new_inn
WHERE id = :person_id;
