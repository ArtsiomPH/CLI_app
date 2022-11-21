from pprint import pprint
from urlextract import URLExtract

from aiohttp import ClientSession
import asyncio
import sys


def validate_string(string: str):
    url_extractor = URLExtract()
    url = url_extractor.find_urls(string, with_schema_only=True)
    if [string] == url:
        return True
    return False


def get_result_dict(responses: list):
    result_dict = dict()

    for dct in responses:
        result_dict = {**dct, **result_dict} if dct is not None else result_dict
    return result_dict if result_dict else 'There were no urls among the strings'


async def get_status_codes(string: str):
    if not validate_string(string):
        print(f"'{string}' is not url")
        return None

    status_codes_dict = {f'{string}': {}}
    async with ClientSession() as session:
        async with session.get(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.post(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.put(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.patch(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.delete(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.head(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
        async with session.options(string) as resp:
            if resp.status != 405:
                status_codes_dict[f'{string}'].update({resp.method: resp.status})
    return status_codes_dict


async def main():
    strings = sys.argv[1:]
    if not strings:
        sys.stderr.write('Please enter urls.')
        sys.exit()

    tasks = []

    for string in strings:
        task = asyncio.create_task(get_status_codes(string))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    result = get_result_dict(responses)
    pprint(result)


if __name__ == '__main__':
    asyncio.run(main())
