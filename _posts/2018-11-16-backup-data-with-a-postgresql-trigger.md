---
layout: post
title: "A trigger for some data backup in PostgreSQL"
tags: sql
summary: How to use SQL triggers to maintain a backup table.
date: 2018-11-16 11:00:00
---

# Use case

I have an SQL table that was filled automatically by some smart code. However, there were some cases where the algorithm didn't work. In order to avoid the 80/20 rule caveat, ie spending 80% of the project allowed time on less than 20% of the problems, I decided to manually solve the remaining issues.

Now, in my table, I have both rows that were created automatically with code, and manually created rows. That's not a problem, even if I want to identify them, I could just add a flag. That's basically what I did.

In order to be sure not to loose this manually created data, even if rebuilding the automatically created ones, I wanted to backup them in another table. And PostgreSQL has a magic tool for this: triggers! Let's have a look.


# Solution

## Preparation

Let's use a table that looks like:

    CREATE TABLE data (
        id SERIAL PRIMARY KEY,
        name CHARACTER VARIING
    );


First, I added a new column to keep a track of the manually inserted rows:

    ALTER TABLE data ADD COLUMN manually_created BOOLEAN;
    UPDATE data SET manually_created = false;


After this, I create the backup table having the same schema as the initial one:

    CREATE TABLE data_backup LIKE data;

Ok, good, now we can think of filling this backup table.


## What are triggers and how they work

Triggers are a very nice SQL feature. They allow the user to define action to be executed at a certain time when an event is fired in the database. Supported events are: INSERT, DELETE, UPDATE and even, for PostgreSQL, TRUNCATE. Sounds like what we are looking for: each time a row in inserted, deleted or updated in our main table, we will be able to do something else, maybe perform the same action on our backup table?

In details, to define a trigger, you first need to define a `FUNCTION`, then you bind this function to a table and action with a trigger. You can also define if the function should be executed before or after the action is performed.

Inside the function, you can access the current row data: depending on the operation, `NEW` and `OLD` objects are available. For instance, in an update statement changing name from 'toto" to 'tata', we'll have `NEW.name='tata'` and `OLD.name = 'toto'`. Perfect! 

## Example in this particular case

Enough theory, let's create our first trigger! First, we will automatically insert new rows in the backup table each time a row is inserted in the main table.

We start by writting the function that will execute this action:


    CREATE OR REPLACE FUNCTION backup_data_func() RETURNS trigger AS $rval$
        BEGIN
            IF (NEW.manually_created = true) THEN -- remember we only want to backup the manually created rows
                INSERT INTO data_backup(id, name, manually_created)
                VALUES(NEW.id, NEW.name, NEW.manually_created);
            END IF;
            RETURN NULL; -- result is not important for AFTER triggers, like the one we will use
        END;
    $rval$ LANGUAGE plpgsql;


This function called `backup_data_func` takes a row of the data table and just insert the same data in the `data_backup` table. Now we can bind this function to an action:

    CREATE TRIGGER data_table_backup
    AFTER INSERT ON data
    FOR EACH ROW EXECUTE PROCEDURE backup_data_func();

So our trigger will execute the function `backup_data_func` for each affected rows after each `INSERT` statemennt on the `data` table. So easy :)

Note that I choose an AFTER trigger just to make sure it will not interfere with the main table actions, which are still the most important ones.


Now, what if we also want the backup data to be modified when the a row in main table is updated or even deleted? For this, we can use other special variables whose list is defined [here in the PG10 doc](https://www.postgresql.org/docs/10/plpgsql-trigger.html). Interesting for us here is `TG_OP`telling us the operation for which the trigger was fired. Let's modify our function to deal with `UPDATE` and `DELETE` statements:


    CREATE OR REPLACE FUNCTION backup_data_func() RETURNS trigger AS $rval$
        BEGIN
	    IF (TG_OP = 'INSERT') THEN
                IF (NEW.manually_created = true) THEN -- remember we only want to backup the manually created rows
                    INSERT INTO data_backup(id, name, manually_created)
                    VALUES(NEW.id, NEW.name, NEW.manually_created);
                END IF;
	    -- new things start here
	    ELSIF (TG_OP = 'UPDATE') THEN 
                IF (NEW.manually_created = true) THEN -- still dealing ony with manually modified rows
                    UPDATE data_backup
		    SET id = NEW.id, name=NEW.name, manually_created=NEW.manually_created
                END IF;
	    ELSIF (TG_OP = 'DELETE') THEN 
            -- our trigger calls this function AFTER the statement is executed, so for the delete statement, we can only access the OLD instance!
                IF (OLD.manually_created = true) THEN
		    DELETE FROM data_backup WHERE id = OLD.id;
                END IF;	        
            END IF;
            RETURN NULL;
        END;
    $rval$ LANGUAGE plpgsql;

And we should also modify our trigger for the function to be executed after update as well:

    CREATE TRIGGER data_table_backup
    AFTER INSERT OR UPDATE OR DELETE ON data
    FOR EACH ROW EXECUTE PROCEDURE backup_data_func();


Here we go, now we have our manually inserted data automatically backuped!
