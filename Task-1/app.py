from flask import Flask, jsonify, request
import asyncio
import requests

app = Flask(__name__)

async def fetch_data_from_url(url):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data:
                return set(data["numbers"])
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
    return set()

async def fetch_all_data(urls):
    tasks = [fetch_data_from_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return set().union(*results)

@app.route('/numbers')
def get_numbers():
    urls = request.args.getlist('url')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        merged_numbers = loop.run_until_complete(fetch_all_data(urls))
        return jsonify(numbers=sorted(list(merged_numbers)))
    finally:
        loop.close()

if __name__ == '__main__':
    app.run(host='localhost', port=8008)
