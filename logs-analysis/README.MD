### Project Overview
In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

## Getting ready

#### Prerequisites:
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or clone the [fullstack-nanodegree-vm](https://github.com/sh4rkfx/udacity-fsnd/tree/master/3/vm) repository.
  3. Download the [project folder](https://github.com/sh4rkfx/udacity-fsnd/tree/master/3/project_1).
  4. Unzip `newsdata.sql` inside of its parent directory.
  5. Move the project folder's contents inside of the `vm/vagrant` directory.

#### Launching the Virtual Machine:
  1. Open up a command line/secure shell/terminal
  
  2. Navigate into the VM's vagrant folder:

  ```
    $ cd path/to/../vm/vagrant
  ```
  3. Launch the Virtual Machine:

  ```
    $ vagrant up
  ```
  4. Then login using a secure shell:

  ```
    $ vagrant ssh
  ```
  5. Navigate to the vagrant folder:
  ```
    $ cd /vagrant
  ```

#### Setting up the database and creating views:
  1. Import the SQL queries into the local database:

  ```
    $ psql -d news -f newsdata.sql
  ```

  2. Connect to the database:
  ```
    $ psql -d news
  ```

  3. Create view view_article using:
  ```
    CREATE VIEW view_article AS
    SELECT articles.title, articles.author, count(*) AS views
    FROM articles, log
    WHERE log.path
    LIKE concat('%', articles.slug)
    GROUP BY articles.title, articles.author
    ORDER BY views DESC;
  ```
  | Column  | Type    |
  | :-------| :-------|
  | title   | text    |
  | author  | text    |
  | views   | Integer |

  4. Create view view_log using:
  ```
    CREATE VIEW view_log AS
    SELECT date(time), round(100.0 * sum(CASE log.status WHEN '200 OK' THEN 0 ELSE 1 END)/count(log.status), 2)
    AS "Error Percentage"
    FROM log
    GROUP BY date(time)
    ORDER BY "Error Percentage" DESC;    
  ```
  | Column           | Type    |
  | :----------------| :-------|
  | date             | date    |
  | Error Percentage | float   |

### Running the queries and generating the reports
  1. Execute report.py:
  ```
    $ python report.py
  ```

### Results
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

"Princess Shellfish Marries Prince Handsome": 1201

"Baltimore Ravens Defeat Rhode Island Shoggoths": 915

"Political Scandal Ends In Political Scandal": 553

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

Ursula La Multa: 2304

Rudolf von Treppenwitz: 1985

Markoff Chaney: 1723

Anonymous Contributor: 1023

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)

July 29, 2016: 2.5
