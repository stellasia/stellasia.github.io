---
layout: post
title: "Logging the result of a PostgreSQL procedure into a table"
tags: sql data
summary: How to write a PostgreSQL procedure that will both return results and log them into a table
date: 2020-02-01 22:08:08:00
---


In a recent project, some part of the data pipeline had to be done at the database level for each client request. The algorithm was kind of complex and had to be wrapped into a PostgreSQL procedure but it was also important to us to log the client calls and the response we were sending back to them. The solution lies into the procedure syntax.

The input data was stored into a table `app_data` whose structure looks like (with much more columns):

```sql
CREATE TABLE app_data
(
    id serial,
    user_id integer NOT NULL,
    record_date timestamp NOT NULL,
    value real NOT NULL
);
```

To simplify, let's assume we want our procedure to take one parameter, the user ID, and return for this user the number of records and the average of `value`. In a logging system, we also want it to return the execution timestamp. We would like to call this procedure like this:

    SELECT user_id, exec_date, n_records, avg_value FROM app_my_procedure(1);

and app_my_procedure should fill a log table whose structure is:

```sql
CREATE TABLE app_my_procedure_log
(
    id serial,
    user_id integer NOT NULL,
    exec_date timestamp NOT NULL,
    n_records int NOT NULL,
    avg_value real NOT NULL
);
```

The working procedure to do this job is shown below, with comments:

```sql
CREATE OR REPLACE FUNCTION app_my_procedure(in_user_id int)
RETURNS SETOF app_my_procedure_log -- this defines the columns to be returned by the function

AS $$
	BEGIN

	RAISE NOTICE 'Starting app_my_procedure at %', now();

    RETURN QUERY -- this tells postgres that the function will return the result of the following query

	-- we start from selecting the data for the selected user_id
	-- NB: this is not strictly necessary but when the complexity of the
	-- query growns, it helps making it more understandable
	WITH data AS (
		SELECT *
		FROM app_data
		WHERE user_id = in_user_id
	),
	-- we then compute the aggregated values (our result)
	-- again, this could be done in one single step with the previous operation
	aggregates AS (
		SELECT
			user_id,
			count(*) as n_records,
			avg(value) as avg_value
		FROM data
		GROUP BY user_id
	)
	INSERT INTO app_my_procedure_log(user_id, exec_date, n_records, avg_value) -- here we insert the result into the log table
	-- before doing the final select that will be returned by the query
	-- that's were we set the exec_date to now(), the timestamp when this final
	-- select is performed
	SELECT user_id, now() as exec_date, n_records, avg_value
	FROM aggregates
	RETURNING *
	;

	RAISE NOTICE 'Ending app_my_procedure at %', now();

	END;

$$ LANGUAGE plpgsql;
```

Let's create some toy data to play with and test everythink works as expected:
```sql
INSERT INTO app_data (user_id, record_date, value) VALUES 
(1, '20120-01-28', 1),
(1, '20120-01-29', 1),
(1, '20120-01-30', 2),
(1, '20120-01-31', 3),
(1, '20120-02-01', 3),
(2, '20120-02-01', 1)
;
```

We can then call our newly created procedure and see the results:

```sql
SELECT * FROM app_my_procedure(1);

NOTICE:  Starting app_my_procedure at 2020-02-01 21:50:03.45689+01
NOTICE:  Ending app_my_procedure at 2020-02-01 21:50:03.45689+01
 id | user_id |         exec_date         | n_records | avg_value 
----+---------+---------------------------+-----------+-----------
  1 |       1 | 2020-02-01 21:50:03.45689 |         5 |         2
(1 row)
```

To check that the log table was filled as expected, just check its content:
```sql
SELECT * FROM app_my_procedure_log;

 id | user_id |         exec_date         | n_records | avg_value 
----+---------+---------------------------+-----------+-----------
  1 |       1 | 2020-02-01 21:50:03.45689 |         5 |         2
(1 row)
```

If you happen to call the procedure on a non existing user, say 3, it will return 0 rows and do not perform any insertion into the log table.

That's probably a lot of responsibilities for a single procedure (getting the data, aggregate it, log the results and return it!). If you end up in this situation, I would encourage you to rethink your process in order to split those operations, but if no other solution is possible in a short term vision, that can be useful!
