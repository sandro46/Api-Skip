import sys , json, requests, time

from rest_framework import status
from rest_framework.test import APIClient
import pytest

client = APIClient()
server_addr = 'http://127.0.0.1:8000/api/v1'


pytestmark = pytest.mark.django_db

class TestReleaseFrozenButsches:
    def test_release_frozen_butches_returns_200ok(self):
        params = {
            "ttl": 2,
            "source_id": 39
        }
        response = client.get(server_addr+'/release-frozen-batch', params)
        res = response.json()
        print('[test_release_frozen_butches_returns Respone is ', res)
        assert response.status_code == 200


@pytest.mark.skip(reason="Temporary skip")
class TestWebKeys:
    def test_get_web_keys_returns_set(self):
        params = {
            "limit": 2,
            "source_id": 39
        }
        response = client.get(server_addr+'/web-keys', params)
        res = response.json()
        print('[tes_get_web_keys_returns_set Respone is ', res)
        assert response.status_code == 200


@pytest.mark.skip(reason="Temporary skip")
class TestCapcha:
    @pytest.mark.skip(reason="Temporary skip")
    def test_recapcha_api_returns_result(self):
        params = {
            'key': '2df8c426d6637dc8969b5a5d5255991b',
            'method': 'base64',
            'phrase': 0,
            'regsense': 0,
            'numeric': 4,
            'min_len': 5,
            'max_len': 5,
            'language': 1,
            'json': 1,
            'body': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//gA+Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2ODApLCBkZWZhdWx0IHF1YWxpdHkK/9sAQwAIBgYHBgUIBwcHCQkICgwUDQwLCwwZEhMPFB0aHx4dGhwcICQuJyAiLCMcHCg3KSwwMTQ0NB8nOT04MjwuMzQy/9sAQwEJCQkMCwwYDQ0YMiEcITIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy/8AAEQgAPADIAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A97ztByOnvSrnjIP4mkGc9cYHPPH+elJznHBJ9R/KgBeSfUD8MUOBwpP0rA1TTdZns7kWOomK4aNvLcE4Vj0OK8fv7/x94OWS7uNSaa2mcI0rMs4yegO4bh0OOlaxpc2zMXWs7NHuzX9p8379WK84U9fb68UlrqFvcsVQsrhclGHI/wAkivOtHt/EF98P11KS+iGpX0haFnjBWNCPlHHfjIPPUZz0pmjWHjCESw6xrgSJ41Cm2VRI+eCQ+0EHgj19OxqvZK2jI9tJP3jv21lVZ1W3cMGI5wPpUlhdXE5cyQBV5w4/lz/OvG9e+JVzYam9pY26ym3PltPcMXLsvHYg+2SeSKy0+LPiMNiX7KynsySYPuDu96v2OmhCrSvdn0NtXrwc81gX0Ak1na5+Vyo4A4HHTn2rynTvi3qcFwD/AGVHIf4gkzc/Xg4rtfD/AItXxVZDUntPsrrIYni80uOADwcdCCKmNKUGOpUU4nnHjewbUvilLo8M/liSWC3j8wllXciemcfM3Qf/AF62F+FPjDTZlTTdXgWPksyXEkWOc4IA/l/hWNJqtonxofULxjHDHfsxLtgArkLkj3AH4167bfEXwzPKI31S2jGcbi+FPOOp/p61cnNJWCKptu558vhT4p29/FLHqtw7KdokN/uTAPdSentg17JZRXSabbx30qzXKxqJpEXAZ8ckD61T1fWP7M0G41O1t5NREUe9IrU5MnToR27k88A9a81b44TQlornw2yzA4XNyVBP0KZ/z2rJ81TZG3u092euSoJIZEJABXafbrXLi0aeaW2CGRsFG+XAIxj/AD9aztR8ReJL7w1YTaPb2UWoXCq06yt/qwRn5QeD26njng9RxX/CQ/EDVPE39jf2jb6fqFmjPKpCqnQckANv6jjBHf3qqcJK5lVcJ2Zyx+H3iSXV7rT7TSp5Ft5SvmPtVcZ4IZiAQRg16v4W8Pah4X8LQ6fqEq+e9y0oVX3CJcL8ufXIJ445o8a6jrFr4Mtry21kW+qWao9w8QAS4J+VgMgZ5OQMc+mcYzfBTa1eaW+r63dzTm/I8gSsSVRSwyFPABPYYzjPpV3lJXZE+WKdil8SNXNr4Zi0yJnD3k4LqCMbF5x0/vbTWf8ABbR2k1y51Z45HjhhMSSDBUSHGRnOc7fbv9BWD8TL03fihbddxjtI1jOW4yfm/kw/L8u0+CGz7Lq423O+VoyWZf3QAzgBs/eyTx6Ac1U9KbCjrJXPW8hwAOT+lKzYwQTnPIpeo+XGPrQcBgTgYriO0bkgjB/A96DnYOcduPWgEHAJHHpSg9GJ9+mKAEBOT69PailySOM5H60UAJz/AA5XnvS5/ujGOPSkJIbrz+tIcYGcZxk84wRQAuTwMEg9xxiuW8XaAmpaXewNkpcKR0+4eob3wea6oYXk5HPbvUd0VW2kLY27TnNVCTi9CKkVKOp4j8PfEtzp7y+EtRTAErtAWPMTgncmPTqR7/Wu1iv2l1e508q3+jQx9enzF/WvNfiO9tp/iW1n08CO88oTPIh+bdnCn68fyrNuPF0tz4ih1OOW4tUmSJbmKLPzBCdwAz37Z9a7eW+qOFtsl0e9sbD4hXkmqxRSQtcTRb5lysblj82MEdiB6ZHpWp8UGs4ry1t4bfbcGMFmKcKgztA4wcljn6CszwpcWniD4i2U2oQRQwXM7ExBBsDbSVHPuFGevNbnxahuILi03TK0CySKsYXBVhjLE5yc+n880fasFna52elXNqLyHRrGzZLi202CfCjPmKUX24IOOvXP1rmPhfdi917V9MEYt5JXN0sQ+7GA2GXGOOqgD2r0PwXaWQ0SwuY447i4FhDGdQ8oLJIuPuFsZIGAOv8AKrWleDtL0bxDqOtWgl+032fMDsCi5bLbeM8kDgk1h7W10dHsb6nlOo/CfxHqfizUJVWGCymuXkW4kkXlSx5AGTnB6cfWt4/A7TY7W5K6tctduMQyGNdqt/tL359CMV6qQOR19T0oOACThVHXpgVDrTZoqMEfPnh/VdX+GniWG31EuNNnb96qsWjdMhd698jqeAe2Oa9a8d+GIfF/haRIdjXUS+dZyrg5OM4B9GHH5HtXm/xZl/c6YoVVkZ5WX5uMYX0/CvVPBTOfBWiCRssLOPGOeMcD8Bx+FaVdLTW5nRfMnFnnnw88aPc3Eel6uj/bbcHY7kZcKcFT33Ln8QOeetO2k8j463yDLRzeaQpxhswbv6D86Z8YYbXRvE2majp2231GRWllMeATgja2PU/Nn1xXE3PiCSXxENcSNFvAASv8LSBNuQPToce/XvWkVzLmXUyleLcTtPG18/iPW7DwxpSmSXzv3xHIL9unZRkn8fSvTb2C2sYLaytV+S1jEQBxwAAB9TXjPw71waH4y829Rg17btAJnBwCzBgSTzyVxXs11YmG2SeRmDMSdpYng9zxxSkrSQvsWR87+Ip1n8T6nOp3f6S69OwJANfQHwzjaP4d6SjBVIWQ4Uf9NW/pXzhId0sjSbS7MdxyCM+ufrX0h8NI5Yfh/pnnT+aHVnXA+6pY4FLEfCjSh8R1jcjHX/Gm8hupPGRxz0p4yPTPpikBHCluo6HvXIdYdzjGaATgjg9iM0deduc9T7Un8I44I6elACnvgZNFDYJyRjHfNFAAOV/2j6dqXtycjocU3A7nrxwO1APU9s8UAKuTzzke3Suc8Y69b6FpElzK4wik7c8yN/Co9yf5UvjPxXF4R0U38tvLO8h8qNVHG7GeT2HBr558SeJ9U8S3f2i8kG3+CJPlVPf68Dn8K3o023zPY5609OVHa/DzwtJ4z1S917XIxJa7mUA5HmSMP4cdlGOOfTtXE61pcsHi260m0tyP9LMcMS85BI2j6HOc16hpPjHTtG+GcD2iXssNlN9lljwAxZsvkkYAXkjP09a87fxWtx4zXXzaRsqsD5LN94AAdcdec+me1bx5m2zGVkkkdn8SfBNtoNlYazolp9nihZVl2uxdWzlXySeB049RWN451r/hIfDOi6g/Mru6SgD+MAZ/UZHtW/qnxE0bUfCOBYzStI7RNbOwAUFQckg5we2Ocg/WvONU1eG80620200+K1ggLSHaxcu5xzk+w+vA9MUQTtqKbTd0fRPgWSK48FaTJbCFYTaxqY41ChXA+c8dy3NdCQMDr7f4189aB8SX0a1tbL+zkSCBAjGGQK7dSW7jnrg9yea9XPj7SbbwJF4iDTNA37uONgBIzgkbcZI7E9elc9Sk09Op0U6qa16HXnnI545rF1rWbWytH3zJHCgzJIT8o9s/59K8o1L4y393GY7PTUt1PQvIWBPbgAfzrmoIPFfxBugsYuLnB6n5IYue56A/mTVwo21kROq5e7EtzNc/Efxrb2NuDFaYKqzD/Vxg5Zzz39PUge9fQMMNvpemxW8YEFrawhFLHhFVccn2A61zHgLwLaeELWWZi0upTDZNORgADHyoM8LkZ55OOewHnHxH+Itzq9xPoemrJb2MblJ2ztkmYHn3C57dT39KUr1ZWjsiopUo3e4mk+b4++I91q8ylrKB/wB0jqCuMkRpz6jn61m/EHw0+m+MEhSNI479UeIRpgKSArDjjO7n8a1vhFrDW17Pp1tpxluJld/tBkJVGCnaHHQAnIzn+KuW8Ua34i8Sa8rajE4ubc7IoYomXy/cd+vfJzWyupWWyMXZrme56R438IDVfCMmpRtGbuwj3ArnDqBlhjoODn8OtTeCfGFt4k8JyaNqUofULePaQ7YM8XTIPqAcHv0PesvwjqXxAv8AR9YtMBXWBXtHvIQmG3jI5X5gV3deAQPWuV0/wd4utdb+2x6aftCOwcvLGoJIIYdcEEHqOOam17qT2D4Y6dTjZEjWRkByuTjHUfXNfTPw+nnn8A6PJPBHARDtRYgQCgJCnHqQAT9a+dJNG1JtWl0cWVw+oxvsaCNNzBhwce3v0xjmvpLwVaavp3hKztdaMf2mJNqooHyRjhVJBwSB6eoFLENcqNKCd2b7fKxY8fXB9aQjLcDk+tOy3IxjHYUdxzgE5ArkOoUrkfMB+fWk44J6kZ4pGJIwcgA0qk/xdTQAHOMED2FFBbaVB65HSigAOOh9cmlIxg8/hQp4J9s01lBLn9PwoArahpdjq1o1rqFrHc27YJSVcj8K5+X4c+EpYDGdFhUdmR2VvqCD9K6on/We3T8qQnMe7vmmpNbMTinujO/4R/SE0mXSk062j0+XiSFI9qt7nHfjr1rmj8JPB3OLGfLNkN9qkO39a7c8nkD72KawAcrgY4/wpqUlsxOKe6OZj+HfhVdKGntpaG33+bkyNuzjH3s56dulY3/CnPCfkBCl6Dn7/ncjn6Y/SvQ2HQdiaSQ4AHqcGmpyXUOSPY5PTfhv4W0uJVTSork5zvuv3p46dePyFaureG9K1vTU03ULNJbaMhkjUFAhxgFcdO449a1Ax259mOP8/WnHhsdeO9Lmbd7j5Va1jl7L4e+ErBlaLRYCy8jzmaUf+PkiumghihgSGGJI40ACogAVfoBSliUOe4HH40pGWH0pNt7gklsL94D5eO4NY03hbQbm6ku5dGspLiQljKYVyW7k+59a2UOSQegA4ppyFDZJOM0JtbA0nuUrHRrDTS/2O0jhBJY7FAyemcDvjv8A/WpkujQyzPIrOmW+6MYH0rTxnPJ5NRn+I+n+JFPmlvcl04tWsUE0mNEdTM7BlKEAgdevNVjosokbEoIB4BGAR+HetzP8s0xgFY4A6Zp+0kS6MHpYoafbPbZ891c7dowvOPr1/CtHsMk89TTFYsAc457fh/jTsdQCRzjI/Cpbu7mkYqKsgGc9R17UcbRjJA7jk0mf3jD0GfxoLEMBnjIFIYbhnOOc4JpDncQMc4yachLAZ75ppP7zb6Y/pQA7kJyc/QUUhbDFMDGcfy/xooA//9k=',
        }
        response = requests.post("http://rucaptcha.com/in.php", params)
        # requests = client.get("http://rucaptcha.com/in.php")
        res = response.json()
        print('[i] Respone is ', res)
        assert response.status_code == 200
        assert len(res) > 0
        assert res['status'] == 1

        failed = True
        params = {
            'key': '2df8c426d6637dc8969b5a5d5255991b',
            'action': 'get',
            'json': 1,
            'id': res['request']
        }
        for i in range(7):
            time.sleep(5)
            response = requests.get("http://rucaptcha.com/res.php", params)
            assert response.status_code == 200
            if response.status_code == 200:
                res = response.json()
                print('[i] Response capcha result is', res)
                if res['status'] == 1:
                    failed = False
                    break
        assert not failed

    def test_api_capcha_returns_recognized_capcha(self):
        params = {
            'capcha_img': 'data:image/jpeg;base64,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',
        }
        response = client.post(server_addr+'/capcha-recognize', params)
        res = response.json()
        print('[test_api_capcha_returns_recognized_capcha] Respone is ', res)
        assert response.status_code == 200
        assert res['payload'] == 'жт5ж7'

@pytest.mark.skip(reason="Temporary skip")
class TestSearch:

    def test_get_SearchItems_returns_200_ok(self):
        response = client.get(server_addr+'/search-items')
        assert response.status_code == 200
#
    def test_get_SearchItems_returns_json(self):
        response = client.get(server_addr+'/search-items')
        assert len(response.json()) > 0

    def test_get_SearchItems_returns_json(self):
        response = client.get(server_addr+'/search-items')
        res = response.json()
        assert len(res) > 0
#
    def test_get_SearchItems_by_fssp_source_and_limit_1_returns_json_with_object(self):
        response = client.get(server_addr + '/search-items?source_id=39&limit=1')
        res = response.json()
        print('[I] Length fio is ', len(res['payload'][0]['fio']))
        assert len(res['payload'][0]['fio']) > 0

@pytest.mark.skip(reason="Temporary skip")
class TestTasks:

    def test_get_tasks_returns_200_ok(self):
        response = client.get(server_addr+'/tasks')
        assert response.status_code == 200

    def test_get_tasks_returns_json(self):
        response = client.get(server_addr+'/tasks')
        res = response.json()
        assert len(res) > 0

    def test_set_task_returns_ok(self):
        params = {
            'tplName': 'Тест'
        }
        response = client.put(server_addr + '/template', params)
        res = response.json()
        print('[I] response is ', res)
        res = response.json()

        assert len(res) > 0


@pytest.mark.skip(reason="Temporary skip")
class TestTemplate:

    def test_get_template_returns_200_ok(self):
        response = client.get(server_addr+'/template')
        assert response.status_code == 200

    def test_get_template_returns_json(self):
        response = client.get(server_addr+'/template')
        assert len(response.json()) > 0

    # def test_post_template_returns_200(self):
    #     response = client.post(server_addr+'/template', )
    #     assert len(response.json()) > 0


