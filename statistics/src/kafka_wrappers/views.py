from clickhouse import ch_client

import json


query = "INSERT INTO statistic.views VALUES ({timestamp}, '{user_login}', {task_id}, '{author}')"


async def views_clickhouse_wrapper(msg, response_producer):
    message = json.loads(msg.value.decode("ascii"))

    ch_client.execute(query.format(**message))

