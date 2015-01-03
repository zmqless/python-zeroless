import pytest

from zeroless import(connect, bind)

class TestExceptions:
    def test_port_under_range(self):
        with pytest.raises(ValueError):
            connect(1023).pull()

        with pytest.raises(ValueError):
            bind(1023).pull()

    def test_port_on_range(self):
        sock1 = connect(1024).pull()
        sock2 = connect(7000).pull()
        sock3 = connect(65535).pull()

    def test_port_after_range(self):
        with pytest.raises(ValueError):
            connect(65536).pull()

        with pytest.raises(ValueError):
            bind(65536).pull()

    def test_port_already_used(self):
        sock1 = bind(65000).pull()

        with pytest.raises(ValueError):
            bind(65000).pull()

    def test_data_is_not_bytes(self):
        push = connect(7050).push()

        with pytest.raises(TypeError):
            push(u'msg')

    def test_published_topic_is_not_bytes(self):
        bind(7099).pub(topic=b'topic1')

        with pytest.raises(TypeError):
            bind(7100).pub(topic=u'topic1')

    def test_subscribed_topics_are_not_bytes(self):
        connect(7099).sub(topics=[b'topic1'])

        with pytest.raises(TypeError):
            connect(7100).sub(topics=[u'topic1'])

        with pytest.raises(TypeError):
            connect(7101).sub(topics=[b'topic1', u'topic2'])
