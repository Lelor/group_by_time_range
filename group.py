from datetime import datetime, timedelta
from itertools import groupby

from json import load, dump


with open('test.json', 'r') as f:
    data = load(f)


def group_messages_by_user(usr):
    messages = filter(
        lambda msg: msg['user'] == usr, data
    )
    return sorted(messages, key=lambda x: float(x['ts']))


def is_within_2min(ts1, ts2):
    interval = datetime.fromtimestamp(float(ts1)) - datetime.fromtimestamp(float(ts2))
    return interval <= timedelta(minutes=2) and interval >= timedelta(minutes=-2)


def create_subgroups(usr_messages):
    ts = usr_messages[0]['ts']
    result = {ts: []}
    for msg in usr_messages:
        if is_within_2min(ts, msg['ts']):
            result[ts].append(msg)
        else:
            ts = msg['ts']
            result[ts] = [msg]
    return result
        

if __name__ == '__main__':
    users = set(map(lambda x: x['user'], data))

    for user in users:
        messages = group_messages_by_user(user)
        subgroups = create_subgroups(messages)
        
        with open(f'output/{user}.json', 'w') as f:
            dump(subgroups, f)
