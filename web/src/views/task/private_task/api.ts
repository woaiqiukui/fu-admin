import { defHttp } from '/@/utils/http/axios';

enum PrivateTaskApi {
  prefix = '/api/task/private_task/',
}

/**
 * 获取端口信息
 */
export const getPortInfo = (params) => {
  return defHttp.get({ url: PrivateTaskApi.prefix + 'getPort', params });
};
