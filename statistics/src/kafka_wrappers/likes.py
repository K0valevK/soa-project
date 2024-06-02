from clickhouse import ch_client

import json


query = "INSERT INTO statistic.likes VALUES ({timestamp}, '{user_login}', {task_id}, '{author}')"


async def likes_clickhouse_wrapper(msg, response_producer):
    message = json.loads(msg.value.decode("ascii"))

    ch_client.execute(query.format(**message))
