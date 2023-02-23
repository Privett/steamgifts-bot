import fake_useragent


try:
    fa = fake_useragent.UserAgent(browsers=['chrome', 'opera', 'google']).random
except fake_useragent.FakeUserAgentError:
    while True:
        try:
            fa = fake_useragent.UserAgent(browsers=['chrome', 'opera', 'google']).random
            break
        except fake_useragent.FakeUserAgentError:
            fa = fake_useragent.UserAgent(browsers=['chrome', 'opera', 'google']).random