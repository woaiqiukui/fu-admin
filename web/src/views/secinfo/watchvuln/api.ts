import { defHttp } from '/@/utils/http/axios';

enum WatchVulnApi {
  prefix = '/api/watchvuln/webhook',
}

/**
 * 获取漏洞list
 */
export const getList = () => {
  return defHttp.get({ url: WatchVulnApi.prefix });
};
