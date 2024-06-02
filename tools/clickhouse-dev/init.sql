CREATE DATABASE IF NOT EXISTS statistic;

CREATE TABLE IF NOT EXISTS statistic.views
(
    time_stamp  DateTime('Europe/Moscow'),
    user_login String,
    task_id UInt64,
    author String
)
ENGINE = MergeTree()
PRIMARY KEY (task_id)
;

CREATE TABLE IF NOT EXISTS statistic.likes
(
    time_stamp  DateTime('Europe/Moscow'),
    user_login String,
    task_id UInt64,
    author String
)
ENGINE = MergeTree()
PRIMARY KEY (task_id)
;