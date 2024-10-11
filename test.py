import json

import requests

api_url = "http://localhost/v1/workflows/run"
api_key = "app-HjTLvDPziSu8OAvh0umxsOSF"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
part = "There are an increasing number of domains in which artificial intelligence (AI) systems both surpass human ability and accurately model human behavior. This combination of machine mastery over a domain and computational understanding of human behavior in it introduces the possibility of algorithmic ally-informed teaching and learning. AI-powered aids could guide people along reliable and efficient improvement paths, synthesized from their knowledge of both human trajectories and objective performance. Relatable AI partners, on the other hand, could learn to act alongside human counterparts in synergistic and complementary ways."
data = {
            "inputs": {'yuan': part},
            "user": "abc-123"
        }
try:
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # 检查请求是否成功
    translated_part0 = response.json()["data"]["outputs"]["yuan"]
    translated_part1 = response.json()["data"]["outputs"]["text"]
    combined_translated_part = f"{translated_part0}\n\n{translated_part1}"
    print(f"翻译结果: {combined_translated_part}")
except Exception as e:
    print(f"翻译过程中发生错误: {e}")
    translated_part = "翻译失败"