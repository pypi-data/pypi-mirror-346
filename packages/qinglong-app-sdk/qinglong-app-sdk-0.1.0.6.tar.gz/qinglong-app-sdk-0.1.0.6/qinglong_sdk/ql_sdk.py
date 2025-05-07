import json
import time

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class QL:
    def __init__(self, address: str, app_id: str, app_secret: str) -> None:
        """
        初始化
        """
        self.auth = None
        self.address = address
        self.id = app_id
        self.secret = app_secret
        self.login()

    def _request(self, method: str, api_path: str,
                 params_dict: dict = None,
                 payload_dict: dict | str = None,
                 **kwargs) -> dict:
        headers = {"Authorization": self.auth, "content-type": "application/json"}
        api_url = f"{self.address}{api_path}"
        if payload_dict and not isinstance(payload_dict, str):
            payload = json.dumps(payload_dict)
        else:
            payload = payload_dict

        response = requests.request(method, api_url, headers=headers, params=params_dict, data=payload, **kwargs)
        if response.status_code != 200:
            raise Exception(f"请求失败：{response.text}")
        return response.json().get('data', {})

    def _get(self, api_path: str, params_dict: dict = None, **kwargs) -> dict:
        return self._request("GET", api_path, params_dict, **kwargs)

    def _post(self, api_path: str, payload_dict: dict | str = None, **kwargs) -> dict:
        return self._request("POST", api_path, None, payload_dict, **kwargs)

    def _delete(self, api_path: str, payload_dict: dict = None, **kwargs) -> dict:
        return self._request("DELETE", api_path, None, payload_dict, **kwargs)

    def _put(self, api_path: str, payload_dict: dict | str = None, **kwargs) -> dict:
        return self._request("PUT", api_path, None, payload_dict, **kwargs)

    def login(self) -> None:
        """
        登录
        """
        path = f"/open/auth/token"
        params_dict = {
            'client_id': self.id,
            'client_secret': self.secret
        }
        rjson = self._get(path, params_dict)
        self.auth = f"{rjson['token_type']} {rjson['token']}"
        return True

    def crons_search(self, search_value: str, query_string:str=''):
        """
        http://workspc.sbat.top:5700/api/crons?searchValue=tiktok_jlqc_odin_video_report_spider&page=1&size=50
        :param search_value:
        :param query_string:
        :return:
        """
        path = f"/open/crons"
        params_dict = {
            'searchValue': search_value,
            'page': 1,
            'size': 200
            # 'queryString': query_string
        }
        rt = self._get(path, params_dict)
        return rt

    def crons_get_all(self):
        path = f"/open/crons"
        rt = self._get(path)
        return rt

    def crons_get_task_detail(self, cron_id: int):
        path = f"/open/crons/{cron_id}"
        rt = self._get(path)
        return rt

    def crons_add(self, command: str, schedule: str, name: str,
                  labels: list[str] = None,
                  sub_id: int = None,
                  extra_schedules: list[str] = None,
                  task_before: list[int] = None,
                  task_after: list[int] = None):

        payload_dict = {
            'command': command,
            'schedule': schedule,
            'name': name,
            'labels': labels,
            'sub_id': sub_id,
            'extra_schedules': extra_schedules,
            'task_before': task_before,
            'task_after': task_after
        }
        path = f"/open/crons"
        rt = self._post(path, payload_dict)
        return rt

    def crons_update(self, _id, command: str, schedule: str, name: str,
                     labels: list[str] = None,
                     sub_id: int = None,
                     extra_schedules: list[str] = None,
                     task_before: list[int] = None,
                     task_after: list[int] = None):

        payload_dict = {
            'id': _id,
            'command': command,
            'schedule': schedule,
            'name': name,
            'labels': labels,
            'sub_id': sub_id,
            'extra_schedules': extra_schedules,
            'task_before': task_before,
            'task_after': task_after
        }
        path = f"/open/crons"
        rt = self._put(path, payload_dict)
        return rt

    def crons_delete(self, cron_id: int | list[int]):
        path = f"/open/crons"
        cron_id = [cron_id] if isinstance(cron_id, int) else cron_id
        rt = self._delete(path, cron_id)
        return rt

    def crons_run(self, cron_id: int | list[int]):
        path = f"/open/crons/run"
        cron_id = [cron_id] if isinstance(cron_id, int) else cron_id
        rt = self._put(path, cron_id)
        return rt

    def crons_stop(self, cron_id: int | list[int]):
        path = f"/open/crons/stop"
        cron_id = [cron_id] if isinstance(cron_id, int) else cron_id
        rt = self._put(path, cron_id)
        return rt

    def crons_add_labels(self, ids: list[int], tags: str | list[str]):
        path = f"/open/crons/labels"
        if isinstance(ids, int):
            ids = [ids]
        if isinstance(tags, str):
            tags = [tags]

        payload_dict = {
            'ids': ids,
            'labels': tags
        }
        rt = self._post(path, payload_dict)
        return rt

    def crons_remove_labels(self, ids: list[int], tags: str | list[str]):
        path = f"/open/crons/labels"
        if isinstance(ids, int):
            ids = [ids]

        if isinstance(tags, str):
            tags = [tags]

        payload_dict = {
            'ids': ids,
            'labels': tags
        }
        rt = self._delete(path, payload_dict)
        return rt

    def crons_enable(self, ids: int | list[int]):
        path = f"/open/crons/enable"
        if isinstance(ids, int):
            ids = [ids]
        rt = self._put(path, ids)
        return rt

    def crons_disable(self, ids: int | list[int]):
        path = f"/open/crons/disable"
        if isinstance(ids, int):
            ids = [ids]
        rt = self._put(path, ids)
        return rt

    def crons_get_logs(self, _id: int):
        path = f"/open/crons/{_id}/logs"
        rt = self._get(path)
        return rt

    def crons_get_log(self, _id: int):
        path = f"/open/crons/{_id}/log"
        rt = self._get(path)
        return rt

    # views
    def crons_get_views(self):
        path = f"/open/crons/views"
        rt = self._get(path)
        return rt

    def crons_add_view(self, view_name: str, filters: [[str]]):
        path = f"/open/crons/views"
        """
        https://github.com/whyour/qinglong/blob/b733937691c8d48f531acea7f9325cead85b565e/src/pages/crontab/viewCreateModal.tsx#L30
          { name: intl.get('命令'), value: 'command' },
          { name: intl.get('名称'), value: 'name' },
          { name: intl.get('定时规则'), value: 'schedule' },
          { name: intl.get('状态'), value: 'status', onlySelect: true },
          { name: intl.get('标签'), value: 'labels' },
          { name: intl.get('订阅'), value: 'sub_id', onlySelect: true },
          
          { name: intl.get('包含'), value: 'Reg' },
          { name: intl.get('不包含'), value: 'NotReg' },
          { name: intl.get('属于'), value: 'In', type: 'select' },
          { name: intl.get('不属于'), value: 'Nin', type: 'select' },
        """
        new_filters = []
        for cond in filters:
            new_filters.append({
                "property": cond[0],
                "operation": cond[1],
                "value": cond[2]
            })
        payload_dict = {"name": view_name,
                        "filters": new_filters,
                        "filterRelation": "and"}

        rt = self._post(path, payload_dict)
        return rt

    def crons_del_view(self, view_ids: int | list):
        path = f"/open/crons/views"
        view_ids = [view_ids] if isinstance(view_ids, int) else view_ids
        rt = self._delete(path, view_ids)
        return rt

    def logs_get_all(self):
        path = f"/open/logs"
        rt = self._get(path)
        return rt

    def logs_get_detail(self, directory: str, filename: str):
        path = f"/open/logs/detail"
        params_dict = {
            'file': filename,
            'path': directory
        }
        rt = self._get(path, params_dict)
        return rt

    def subs_get_all(self):
        """subscriptions
        https://github.com/whyour/qinglong/blob/develop/back/api/subscription.ts
        """
        path = f"/open/subscriptions"
        rt = self._get(path)
        return rt

    def subs_add(self,
                 type: str,
                 url: str,
                 schedule_type: str,
                 alias: str,
                 schedule: str = None,
                 interval_schedule: dict = None,
                 name: str = None,
                 whitelist: str = None,
                 blacklist: str = None,
                 branch: str = None,
                 dependences: str = None,
                 pull_type: str = None,
                 pull_option: dict = None,
                 extensions: str = None,
                 sub_before: str = None,
                 sub_after: str = None,
                 proxy: str = None,
                 autoAddCron: bool = False,
                 autoDelCron: bool = False):

        """
        type: Joi.string().required(),
        schedule: Joi.string().optional().allow('').allow(null),
        interval_schedule: Joi.object({
          type: Joi.string().required(),
          value: Joi.number().min(1).required(),
        })
          .optional()
          .allow('')
          .allow(null),
        name: Joi.string().optional().allow('').allow(null),
        url: Joi.string().required(),
        whitelist: Joi.string().optional().allow('').allow(null),
        blacklist: Joi.string().optional().allow('').allow(null),
        branch: Joi.string().optional().allow('').allow(null),
        dependences: Joi.string().optional().allow('').allow(null),
        pull_type: Joi.string().optional().allow('').allow(null),
        pull_option: Joi.object().optional().allow('').allow(null),
        extensions: Joi.string().optional().allow('').allow(null),
        sub_before: Joi.string().optional().allow('').allow(null),
        sub_after: Joi.string().optional().allow('').allow(null),
        schedule_type: Joi.string().required(),
        alias: Joi.string().required(),
        proxy: Joi.string().optional().allow('').allow(null),
        autoAddCron: Joi.boolean().optional().allow('').allow(null),
        autoDelCron: Joi.boolean().optional().allow('').allow(null),
        """
        path = f"/open/subscriptions"
        payload_dict = {
            'type': type,
            'schedule': schedule,
            'interval_schedule': interval_schedule,
            'name': name,
            'url': url,
            'whitelist': whitelist,
            'blacklist': blacklist,
            'branch': branch,
            'dependences': dependences,
            'pull_type': pull_type,
            'pull_option': pull_option,
            'extensions': extensions,
            'sub_before': sub_before,
            'sub_after': sub_after,
            'schedule_type': schedule_type,
            'alias': alias,
            'proxy': proxy,
            'autoAddCron': autoAddCron,
            'autoDelCron': autoDelCron
        }
        rt = self._post(path, payload_dict)
        return rt

    def subs_update(self,
                    _id: int,
                    type: str,
                    url: str,
                    schedule_type: str,
                    alias: str,
                    schedule: str = None,
                    interval_schedule: dict = None,
                    name: str = None,
                    whitelist: str = None,
                    blacklist: str = None,
                    branch: str = None,
                    dependences: str = None,
                    pull_type: str = None,
                    pull_option: dict = None,
                    extensions: str = None,
                    sub_before: str = None,
                    sub_after: str = None,
                    proxy: str = None,
                    autoAddCron: str = None,
                    autoDelCron: str = None):

        """
        type: Joi.string().required(),
        schedule: Joi.string().optional().allow('').allow(null),
        interval_schedule: Joi.object({
          type: Joi.string().required(),
          value: Joi.number().min(1).required(),
        })
          .optional()
          .allow('')
          .allow(null),
        name: Joi.string().optional().allow('').allow(null),
        url: Joi.string().required(),
        whitelist: Joi.string().optional().allow('').allow(null),
        blacklist: Joi.string().optional().allow('').allow(null),
        branch: Joi.string().optional().allow('').allow(null),
        dependences: Joi.string().optional().allow('').allow(null),
        pull_type: Joi.string().optional().allow('').allow(null),
        pull_option: Joi.object().optional().allow('').allow(null),
        extensions: Joi.string().optional().allow('').allow(null),
        sub_before: Joi.string().optional().allow('').allow(null),
        sub_after: Joi.string().optional().allow('').allow(null),
        schedule_type: Joi.string().required(),
        alias: Joi.string().required(),
        proxy: Joi.string().optional().allow('').allow(null),
        autoAddCron: Joi.boolean().optional().allow('').allow(null),
        autoDelCron: Joi.boolean().optional().allow('').allow(null),
        """
        path = f"/open/subscriptions"
        payload_dict = {
            'id': _id,
            'type': type,
            'schedule': schedule,
            'interval_schedule': interval_schedule,
            'name': name,
            'url': url,
            'whitelist': whitelist,
            'blacklist': blacklist,
            'branch': branch,
            'dependences': dependences,
            'pull_type': pull_type,
            'pull_option': pull_option,
            'extensions': extensions,
            'sub_before': sub_before,
            'sub_after': sub_after,
            'schedule_type': schedule_type,
            'alias': alias,
            'proxy': proxy,
            'autoAddCron': autoAddCron,
            'autoDelCron': autoDelCron
        }
        rt = self._put(path, payload_dict)
        return rt

    def subs_delete(self, sub_id: int | list[int]):
        path = f"/open/subscriptions"
        sub_id = [sub_id] if isinstance(sub_id, int) else sub_id
        rt = self._delete(path, sub_id)
        return rt

    def subs_run(self, sub_id: int | list[int]):
        path = f"/open/subscriptions/run"
        sub_id = [sub_id] if isinstance(sub_id, int) else sub_id
        rt = self._put(path, sub_id)
        return rt

    def subs_stop(self, sub_id: int | list[int]):
        path = f"/open/subscriptions/stop"
        sub_id = [sub_id] if isinstance(sub_id, int) else sub_id
        rt = self._put(path, sub_id)
        return rt

    def subs_enable(self, sub_id: int | list[int]):
        path = f"/open/subscriptions/enable"
        sub_id = [sub_id] if isinstance(sub_id, int) else sub_id
        rt = self._put(path, sub_id)
        return rt

    def subs_disable(self, sub_id: int | list[int]):
        path = f"/open/subscriptions/disable"
        sub_id = [sub_id] if isinstance(sub_id, int) else sub_id
        rt = self._put(path, sub_id)
        return rt

    def subs_detail(self, sub_id: int):
        path = f"/open/subscriptions/{sub_id}"
        rt = self._get(path)
        return rt

    def subs_get_log(self, sub_id: int):
        path = f"/open/subscriptions/{sub_id}/log"
        rt = self._get(path)
        return rt

    def cfg_get_all(self):
        path = f"/open/configs/files"
        rt = self._get(path)
        return rt

    def cfg_get_detail(self, config_name: str):
        path = f"/open/configs/detail"
        params_dict = {
            'path': config_name
        }
        rt = self._get(path, params_dict)
        return rt

    def cfg_save(self, config_name: str, content: str):
        path = f"/open/configs/save"
        payload_dict = {
            'name': config_name,
            'content': content
        }
        rt = self._post(path, payload_dict)
        return rt

    def env_add(self, name: str, value: str, remarks: str = ''):
        path = f"/open/envs"
        payload_dict = {
            'name': name,
            'value': value,
            'remarks': remarks
        }

        rt = self._post(path, [payload_dict])
        return rt[0]

    def env_get(self, _id: int = None, search_value: str = None):
        if search_value:
            path = f"/open/envs"
            params_dict = {
                'searchValue': search_value
            }
            rt = self._get(path, params_dict)
        elif _id:
            path = f"/open/envs/{_id}"
            rt = self._get(path)
        else:
            path = f"/open/envs"
            rt = self._get(path)

        return rt

    def env_update(self, _id, name: str, value: str, remarks: str = ''):
        path = f"/open/envs"
        payload_dict = {
            'id': _id,
            'name': name,
            'value': value,
            'remarks': remarks
        }

        rt = self._put(path, payload_dict)
        return rt

    def env_disable(self, ids: int | list[int]):
        path = f"/open/envs/disable"
        ids = [ids] if isinstance(ids, int) else ids
        rt = self._put(path, ids)
        return rt

    def env_enable(self, ids: int | list[int]):
        path = f"/open/envs/enable"
        ids = [ids] if isinstance(ids, int) else ids
        rt = self._put(path, ids)
        return rt

    def env_delete(self, ids: int | list[int]):
        path = f"/open/envs"
        ids = [ids] if isinstance(ids, int) else ids
        rt = self._delete(path, ids)
        return rt

    def user_notification(self, _type: str, key: str):
        path = f"open/user/notification"
        if _type == 'lark':
            payload_dict = {
                'type': _type,
                'larkKey': key
            }
        else:
            raise Exception(f"不支持的通知类型: {_type}")
        rt = self._post(path, payload_dict)
        return rt

    def sys_reload(self):
        path = f"/open/system/reload"
        rt = self._put(path)
        return rt

    def test(self):
        rt = self.crons_search('spider')
        print(rt)
        self.crons_get_views()
        rt = self.crons_add_view('test', [['name', 'Reg', 'test']])
        self.crons_del_view(rt['id'])
        self.crons_get_all()
        task_test = {
            'command': 'echo hello, world!',
            'schedule': '30 0 * * *',
            'name': 'test',
            'labels': ['tag1'],
            'sub_id': None,
            'extra_schedules': None,
            'task_before': None,
            'task_after': None
        }
        rjson = self.crons_add(**task_test)
        cron_id = rjson['id']
        task_test['_id'] = cron_id
        task_test['name'] = 'test2'
        rt = self.crons_update(**task_test)

        assert rt['name'] == 'test2'
        self.crons_run(cron_id)
        self.crons_add_labels(ids=[cron_id], tags='test')
        self.crons_remove_labels(ids=[cron_id], tags='test')

        while rt := self.crons_get_task_detail(cron_id):
            status = rt['status']
            if status == 1:
                break

        self.crons_disable(ids=cron_id)
        self.crons_enable(ids=cron_id)

        self.logs_get_all()

        rt = self.crons_get_logs(_id=cron_id)
        logger.info(rt)
        directory = rt[0]['directory']
        filename = rt[0]['filename']
        rt = self.logs_get_detail(directory, filename)
        logger.info(rt)
        rt = self.crons_get_log(cron_id)
        logger.info(rt)

        self.crons_stop(cron_id)
        self.crons_delete(cron_id)

        # subscriptions
        rt = self.subs_get_all()
        logger.info(rt)
        subs_dict = {
            'url': 'https://github.com/xx299x/qinglong-app-sdk.git',
            'alias': 'test',
            'autoAddCron': False, 'autoDelCron': False,
            'blacklist': None, 'branch': 'master',
            'dependences': None, 'extensions': None,
            'interval_schedule': None,
            'name': 'test',
            'proxy': None,
            'pull_option': {'password': '***', 'username': '****'},
            'pull_type': 'user-pwd',
            'schedule': '* * * * 1',
            'schedule_type': 'crontab',
            'sub_after': None,
            'sub_before': None,
            'type': 'private-repo',
            'whitelist': None
        }
        rt = self.subs_add(**subs_dict)

        logger.info(rt)
        sub_id = rt['id']
        subs_dict['_id'] = sub_id
        subs_dict['name'] = 'test2'
        rt = self.subs_update(**subs_dict)
        assert rt['name'] == 'test2'

        #
        # self.subs_run(sub_id)
        # while rt := self.subs_detail(sub_id):
        #     status = rt['status']
        #     if status == 1:
        #         break

        self.subs_stop(sub_id)
        self.subs_enable(sub_id)
        self.subs_disable(sub_id)
        self.subs_get_log(sub_id)

        self.subs_delete(sub_id)

        # config
        rt = self.cfg_get_all()
        config_name = 'config.sh'

        rt = self.cfg_get_detail(config_name)

        rt = self.cfg_save(config_name, rt)

        # env
        rt = self.env_get()
        logger.info(rt)
        rt = self.env_add('test', 'test')
        logger.info(rt)
        e_id = rt['id']
        rt = self.env_get(e_id)
        logger.info(rt)

        rt = self.env_update(rt['id'], 'test2', 'test2')
        logger.info(rt)

        self.env_disable(rt['id'])
        self.env_enable(rt['id'])

        self.env_delete(rt['id'])

        # user
        _type = 'a'
        key = 'a'
        # rt = self.user_notification(_type, key)
        logger.info(rt)

        # system
        rt = self.sys_reload()
        logger.info(rt)
        time.sleep(30)


if __name__ == "__main__":
    import os

    url = os.getenv("QL_CLIENT_ADDRESS")
    client_id = os.getenv("QL_CLIENT_ID")
    client_secret = os.getenv("QL_CLIENT_SECRET")
    ql = QL(url, client_id, client_secret)
    ql.test()
