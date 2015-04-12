# emailfdw
===========
**emailfdw** is a PostgreSQL foreign data wrapper for translating SQL to IMAP/SMTP.

The feat that emailfdw accomplishes is the abstraction of email protocols to SQL queries, e.g.:

```
$ SELECT flags, subject, payload  
  FROM gmail 
  WHERE from = 'max@pooshield.com'
  AND subject LIKE '%Daily digest%' 
  LIMIT 5;

$ INSERT INTO gmail (from, to, subject, payload)
  VALUES (
  	"max@pooshield.com",
  	"myfriend@example.com",
  	"you should try out emailfdw!",
  	"RFC 2822 message"
  );
```

**emailfdw** accomplishes this by using [Multicorn](http://multicorn.org/), a PostgreSQL extension for writing foreign data wrappers in Python.

With [PostgreSQL 9.3+](https://wiki.postgresql.org/wiki/What%27s_new_in_PostgreSQL_9.3#Writeable_Foreign_Tables), foreign data wrappers can perform SQL *write* operations (INSERT, UPDATE, DELETE) in addition to *reads* (SELECT) against a remote data store.

Together, **emailfdw** supports the four basic [CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations for persisting and manipulating email data--something that has historically been an obnoxious, pedantic task.

By reducing email to basic operations on a datastore, we hope to rejuvenate people's enthusiasm for developing email-driven applications!

----

### "How email works" addendum

Reading and writing of email data is done over two protocols, and these are what **emailfdw** leverages under the covers:

- **IMAP**, or Internet Mail Access Protocol, is the dominant protocol for interacting with hosted email accounts and their data (e.g. Gmail, Yahoo, etc.). The equivalent SQL operations supported by IMAP are *SELECT*, *UPDATE*, and *DELETE*.
- **SMTP**, or Simple Mail Transport Protocol, is the dominant protocol for sending emails from a self-identified sender to one or more recipients.

### Installation

- Install PostgreSQL 9.4.
- Install multicorn
- CREATE EXTENSION emailfdw;

