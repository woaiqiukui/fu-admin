import { defHttp } from '/@/utils/http/axios';

enum ProjApi {
  prefix = '/api/project/',
}

/**
 * 获取项目list
 */
export const getList = () => {
  return defHttp.get({ url: ProjApi.prefix });
};

/**
 * 保存或更新项目
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: ProjApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: ProjApi.prefix, params });
  }
};

/**
 * 删除特定项目
 */
export const deleteItem = (id) => {
  return defHttp.delete({ url: ProjApi.prefix + '/' + id });
};

/**
 * 获取项目详情
 */
export const getDetail = (id) => {
  return defHttp.get({ url: ProjApi.prefix + '/' + id });
};
