import { defHttp } from '/@/utils/http/axios';

enum TaskApi {
  prefix = '/api/task/task/',
}

/**
 * 获取项目list
 */
export const getList = () => {
  return defHttp.get({ url: TaskApi.prefix });
};

/**
 * 暂停项目
 */
export const pauseItem = (uuid) => {
  return defHttp.post({ url: TaskApi.prefix + '/pause/' + uuid });
};

/**
 * 恢复项目
 */

export const resumeItem = (uuid) => {
  return defHttp.post({ url: TaskApi.prefix + '/resume/' + uuid });
};

/**
 * 保存或更新项目
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    console.log(params);
    return defHttp.put({ url: TaskApi.prefix + '/' + params.uuid, params });
  } else {
    return defHttp.post({ url: TaskApi.prefix, params });
  }
};

/**
 * 删除特定项目
 */
export const deleteItem = (uuid) => {
  return defHttp.delete({ url: TaskApi.prefix + '/' + uuid });
};

/**
 * 获取项目详情
 */
export const getDetail = (uuid) => {
  return defHttp.get({ url: TaskApi.prefix + '/' + uuid });
};
