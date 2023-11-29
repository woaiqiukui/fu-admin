import { defHttp } from '/@/utils/http/axios';

enum WatchVulnApi {
  prefix = '/api/event/webhook',
}

/**
 * 获取漏洞list
 */
export const getSecInfoList = () => {
  return defHttp.get({ url: WatchVulnApi.prefix });
};
