import heapq

priorities = {
    ":and:": 1,
    ":or:": 1,
    ":not:": 2
}


def sort_query(query, default_op=":and:"):
    selected_priority = priorities[default_op]
    selected_operation = default_op
    heap = []
    for query_part in query:
        if query_part in priorities.keys():
            selected_priority = priorities[query_part]
            selected_operation = query_part
        else:
            heapq.heappush(heap, (selected_priority, selected_operation + " " + query_part))
            selected_priority = priorities[default_op]
            selected_operation = default_op

    return " ".join([heapq.heappop(heap)[1] for _iteration in range(len(heap))]).split(" ", 1)[1].split()

if __name__ == "__main__":
    test_query = "testing :or: not something :not: hype :or: random :not: python"
    print(sort_query(test_query.split()))
