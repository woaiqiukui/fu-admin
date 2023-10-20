import { defHttp } from '/@/utils/http/axios';

enum PublicAssetsApi {
  prefix = '/api/task/public_assets',
}

/**
 * 获取list
 */
export const getList = (params) => {
  return defHttp.get({ url: PublicAssetsApi.prefix, params });
};

/**
 * 添加任务
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: PublicAssetsApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: PublicAssetsApi.prefix, params });
  }
};

/**
 * 获取任务详情
 */
export const getTaskDetail = (task_id) => {
  return defHttp.get({ url: PublicAssetsApi.prefix + '/' + task_id });
};

/**
 * 中止任务
 */
export const stopTask = (task_id) => {
  return defHttp.post({ url: PublicAssetsApi.prefix + '/stop/' + task_id });
};

/**
 * 删除任务
 */
export const deleteTask = (task_id) => {
  return defHttp.delete({ url: PublicAssetsApi.prefix + '/' + task_id });
};
