import requests
import aiohttp
import base64

# 下载图像并转为base64
def encode_image_from_url(image_url):
    # 下载图像
    response = requests.get(image_url)
    if response.status_code == 200:
        # 将图像内容转为base64
        return "data:image/jpeg;base64," + base64.b64encode(response.content).decode('utf-8')
    else:
        return None
    

async def async_encode_image_from_url(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_data = await response.read()
                base64_str = base64.b64encode(image_data).decode('utf-8')
                return "data:image/jpeg;base64," + base64_str
            else:
                return None
