from app.core.requester.data import GetFriendsQuery


def decrease_batch(qp: GetFriendsQuery):
    qp.batch_size //= 2
    return qp


def increase_timeout(qp: GetFriendsQuery):
    qp.timeout_step += 1
    return qp


def rebuild_queries_closure():
    errors_handler = {
        1: decrease_batch,
        6: increase_timeout,
        10: decrease_batch,
        13: decrease_batch,
    }
    tracked_errors = set(errors_handler)

    def inner(errors: dict):
        # if errors:
        #     pprint.pprint(errors)
        rebuilt_queries = []
        handled_errors = set(errors).intersection(tracked_errors)
        for handled_error in handled_errors:
            for qp in errors[handled_error]:
                rebuilt_qp = errors_handler[handled_error](qp)
                rebuilt_queries.append(rebuilt_qp)
        return rebuilt_queries

    return inner


rebuild_queries = rebuild_queries_closure()
