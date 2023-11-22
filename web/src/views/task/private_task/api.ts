import { defHttp } from '/@/utils/http/axios';

enum PrivateTaskApi {
  prefix = '/api/task/private_task/',
}

/**
 * 获取任务信息及结果
 */
export const getTaskResult = (params) => {
  return defHttp.post({ url: PrivateTaskApi.prefix + '/', params });
};
