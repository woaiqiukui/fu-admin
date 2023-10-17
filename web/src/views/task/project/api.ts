import { defHttp } from '/@/utils/http/axios';

enum DeptApi {
  prefix = '/api/task/project',
}

/**
 * 获取list
 */
export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

/**
 * 保存或更新
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: DeptApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: DeptApi.prefix, params });
  }
};

/**
 * 删除
 */
export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};

/**
 * 获取项目详情
 */
export const getDetail = (id) => {
  return defHttp.get({ url: DeptApi.prefix + '/' + id });
};
