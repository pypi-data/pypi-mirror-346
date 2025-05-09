功能特点：

- 基于 `https://github.com/lucasheld/uptime-kuma-api` 改进,以便支持2.0 API
- 支持 Uptime Kuma 2.0.0-beta.2 版本
- 注意使用try/finally关闭链接,否则会导致timeout问题,原因未知,可能是uptime的问题


# 超时问题解决:
```py
from uptime_kuma_api_v2 import UptimeKumaApi
if __name__ == '__main__':
    try:
        api = UptimeKumaApi('http://localhost:3001')
        api.login('admin', 'admin')
        monitor_list = api.get_monitors() # get all monitors
        print(monitor_list)
    except Exception as e:
        # print("Connection was unsuccessfull")
        raise e
    finally:
        # !!任务结束后自动断开链接,防止阻塞程序(不断开会引起下一次操作timeout)
        api.disconnect()

```