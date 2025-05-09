import json

import pytest

from ey_commerce_lib.dxm.constant.order import ORDER_SEARCH_APPROVAL_BASE_FORM, \
    ORDER_SEARCH_PENDING_PROCESSING_BASE_FORM, ORDER_SEARCH_SELF_WAREHOUSE_BASE_FORM, \
    ORDER_SEARCH_OVERSEA_WAREHOUSE_BASE_FORM, ORDER_SEARCH_HAVE_GOODS_BASE_FORM, ORDER_SEARCH_OUT_OF_STOCK_BASE_FORM, \
    ORDER_SEARCH_DELIVERY_FAILURE_BASE_FORM, ORDER_SEARCH_DELIVERY_SUCCESS_BASE_FORM, DxmOrderRuleType
from ey_commerce_lib.dxm.main import DxmClient
from ey_commerce_lib.dxm.schemas.order import DxmOrderSearchForm
from ey_commerce_lib.dxm.schemas.warehouse import WarehouseProductQuery, PurchasingAllQuery

cookies = {
    'dxm_i': 'MTAyNzg5NiFhVDB4TURJM09EazIhZjc5ZTMxMjZmN2Q3NTk5OGZlMDg4YjQzNzNlNzlmOWY',
    'dxm_t': 'MTcxNDk2NDU4MiFkRDB4TnpFME9UWTBOVGd5IWIzZWRjYTc3YTdjYWE0MmIxMWYwNjFhOTlmMDgxZjY5',
    'dxm_c': 'TWVOMVpiclYhWXoxTlpVNHhXbUp5VmchNmM5MmM5ODc1MDBkODVjOWJmOTFlMzdhNGJiNWI3Njk',
    'dxm_w': 'ZDc3NWVhOTdkOTEyNGE4ZmRkODBmYzc2YmFlOGVjZjEhZHoxa056YzFaV0U1TjJRNU1USTBZVGhtWkdRNE1HWmpOelppWVdVNFpXTm1NUSFmZWZiZGZiMTEwMzhlN2M4M2MzYjZmYjAxYTcxMjViMw',
    'dxm_s': 'aMHO7LWKAQe6NzFrV3O4cceXkBriLGNmwondOR7INWs',
    'MYJ_MKTG_fapsc5t4tc': 'JTdCJTdE',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxMDU5MDc1MjU0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTA1OTA3NTQyNCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTE2JTdE',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxMDU5MDc1MTEwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTA1OTA3NTk5NiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTE2JTdE',
    '_dxm_ad_client_id': '7AEFA0B78CE1B35075D391C5226612CED',
    'Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b': '1731459796,1731547149,1731590878,1731893161',
    'HMACCOUNT': 'F266E8F609D8D8B1',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxOTAxNDMzMTk3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTExNiU3RA==',
    'Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b': '1731901433',
    'JSESSIONID': 'CD9C8372185D453012E5EEFBA64E2C9C',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.dianxiaomi.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.dianxiaomi.com/sys/index.htm?go=m420',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


# XM7WJA451012,XM7WJA451092,XM7WJA451089
@pytest.mark.asyncio
async def test_order():
    async with DxmClient(cookies=cookies, headers=headers) as dxm:
        data = await dxm.list_order_detail_async(ORDER_SEARCH_SELF_WAREHOUSE_BASE_FORM)
        for item in data:
            print(item)
        # print(await dxm.get_warehouse_dict())
