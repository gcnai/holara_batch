import base64
import io
import json
import sys
import urllib.parse
from datetime import datetime
import PIL.Image
import PIL.PngImagePlugin


def array_to_dict(a):
    return dict(zip(map(lambda i: i['name'], a), map(lambda i: i['value'], a)))


def array_to_dict2(a):
    return dict(zip(map(lambda i: i['name'], a), map(lambda i: urllib.parse.unquote_plus(i['value']), a)))


if __name__ == '__main__':
    with io.open(sys.argv[1], "rb") as fp:
        j = json.load(fp)

        def entry_filter(e):
            return e['request']['url'] == 'https://holara.ai/holara/api/1.0/generate_image'\
                and e['response']['status'] == 200

        for entry in filter(entry_filter, j["log"]["entries"]):
            content = json.loads(entry['response']['content']['text'])
            if content['status'] != 'success':
                continue
            headers = array_to_dict(entry['response']['headers'])
            dt = datetime.strptime(headers['date'], '%a, %d %b %Y %H:%M:%S %Z')
            params = array_to_dict2(entry['request']['postData']['params'])
            metaStr = "%s\nNegative prompt: %s\nSteps: %s, Sampler: , CFG scale: %s, Seed: %s, Size: %sx%s" \
                      % (params['prompt'], params['negative_prompt'], params['steps'], params['cfg_scale'], params['seed'], params['width'], params['height'])
            i = 0
            for im in content['images']:
                name = "%s_%02d.png" % (dt.strftime("%Y%d%H%M%S"), i)
                data = base64.b64decode(im)
                with PIL.Image.open(io.BytesIO(data)) as pim:
                    info = PIL.PngImagePlugin.PngInfo()
                    info.add_text('parameters', metaStr)
                    with io.open(name, "wb") as f:
                        pim.save(f, pnginfo=info)
                i += 1
