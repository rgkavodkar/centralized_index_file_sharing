import util.rfc_info as r
import util.construct_response as cresp
import util.construct_request as creq
import datetime
import util.constants as c

# TODO: Remove this file!


def test_responses():

    print("RESPONSES\n")
    # status_code, status_phrase, date, os, last_modified, content_length, content_type, data
    print(cresp.construct_p2p_get_response("200", "Success", datetime.datetime.now().ctime(), "Ubuntu", datetime.datetime.today().ctime(), "4562", "text/plain", c.LOREM_IPSUM))
    print()

    a = list()
    a.append(r.Rfc_info("1", "Hello World1", "aaa", "222"))
    a.append(r.Rfc_info("2", "Hello World2", "aaa", "222"))
    a.append(r.Rfc_info("3", "Hello World3", "aaa", "222"))
    print(cresp.construct_p2s_list_response("123", "ABABA", a))
    print()

    a.append(r.Rfc_info("4", "Hello World4", "aaa", "222"))
    print(cresp.construct_p2s_lookup_response("123", "ABABA", a))


def test_requests():

    print("REQUESTS\n")
    print(creq.construct_p2p_get_request("3245", "101.122.154.21", "Ubuntu 14.04"))
    print()
    print(creq.construct_p2s_add_request("3265", "101.122.154.21", "46558", "A Test Title"))
    print()
    print(creq.construct_p2s_lookup_request("3265", "101.122.154.21", "46558", "A Test Title"))
    print()
    print(creq.construct_p2s_list_request("122.545.2.124", "5611"))


test_requests()

test_responses()