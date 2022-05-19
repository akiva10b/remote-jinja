from remote_jinja import render_remote

def test_fetch_page_fail():
    try:
        r = render_remote("http://httpstat.us/403")
        print(r)
    except Exception as e:
        assert "Cannot fetch remote template for url http://httpstat.us/403 Exception: 403" in str(e)


def test_fetch_page_with_param():
    r = render_remote("https://akivas-initial-project-7c4990.webflow.io/", name="test-name")
    assert "test-name" in r

def test_fetch_page_without_param():
    r = render_remote("https://akivas-initial-project-7c4990.webflow.io/")
    assert "test-name" not in r