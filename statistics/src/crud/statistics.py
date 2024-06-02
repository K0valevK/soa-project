from clickhouse import ch_client

import json


async def task_stats(task_id: int):
    query_likes = "SELECT COUNT(*) FROM statistic.likes WHERE task_id == {task_id}"
    query_views = "SELECT COUNT(*) FROM statistic.views WHERE task_id == {task_id}"

    resp_likes = ch_client.execute(query_likes.format(task_id=task_id))
    resp_views = ch_client.execute(query_views.format(task_id=task_id))

    return {"likes_num": resp_likes[0][0], "views_num": resp_views[0][0]}


async def top_tasks(metric_type: str):
    '''
    query = ("SELECT q1.task_id, q2.author, q1.cnt FROM (SELECT task_id, COUNT(*) AS cnt FROM statistic.likes GROUP BY "
             "task_id ORDER BY cnt DESC LIMIT 5) AS q1 LEFT JOIN (SELECT DISTINCT ON (task_id) task_id, author FROM "
             "statistic.likes) AS q2 ON q1.task_id = q2.task_id ORDER BY cnt DESC")
    '''

    query = ("SELECT DISTINCT ON (q1.task_id) q1.task_id, q2.author, q1.cnt FROM (SELECT task_id, COUNT(*) AS cnt "
             "FROM statistic.{metric_type} GROUP BY task_id LIMIT 5) AS q1 LEFT JOIN statistic.{metric_type} AS q2 ON "
             "q1.task_id = q2.task_id ORDER BY cnt DESC")

    resp = ch_client.execute(query.format(metric_type=metric_type))

    return resp


async def top_users():
    query = "SELECT author, COUNT(*) FROM statistic.likes GROUP BY author ORDER BY COUNT(*) DESC LIMIT 3"

    resp = ch_client.execute(query)

    return resp
