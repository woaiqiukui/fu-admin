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
    console.log(params);
    return defHttp.put({ url: ProjApi.prefix + '/' + params.uuid, params });
  } else {
    return defHttp.post({ url: ProjApi.prefix, params });
  }
};

/**
 * 删除特定项目
 */
export const deleteItem = (uuid) => {
  return defHttp.delete({ url: ProjApi.prefix + '/' + uuid });
};

/**
 * 获取项目详情
 */
export const getDetail = (uuid) => {
  return defHttp.get({ url: ProjApi.prefix + '/' + uuid });
};
