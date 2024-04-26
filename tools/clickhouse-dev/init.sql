CREATE DATABASE IF NOT EXISTS statistic;

CREATE TABLE IF NOT EXISTS statistic.views
(
    id UUID,
    time_stamp  DateTime('Europe/Moscow'),
    user_login String,
    task_id UInt64
)
ENGINE = MergeTree()
PRIMARY KEY (id)
;

CREATE TABLE IF NOT EXISTS statistic.likes
(
    id UUID,
    time_stamp  DateTime('Europe/Moscow'),
    user_login String,
    task_id UInt64
)
ENGINE = MergeTree()
PRIMARY KEY (id)
;