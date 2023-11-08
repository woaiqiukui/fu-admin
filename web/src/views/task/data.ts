import { ref } from 'vue';
import { FormSchema } from '/@/components/Form';
import { getList as getProjectList } from '../project/api';

export const projectOptions = ref([]);

export const step1Schemas: FormSchema[] = [
  {
    field: 'task_name',
    component: 'Input',
    label: '任务名称',
    required: true,
    colProps: {
      span: 24,
    },
    helpMessage: '请输入当前任务名称',
    componentProps: {
      placeholder: '20231102 杭州市城市建设投资集团有限公司公网资产收集任务',
    },
  },
  {
    field: 'project',
    component: 'Select',
    label: '关联项目',
    required: true,
    componentProps: {
      options: projectOptions,
    },
    colProps: {
      span: 24,
    },
    helpMessage: '选择与当前任务相关联的项目',
  },
  {
    field: 'task_desc',
    component: 'InputTextArea',
    label: '任务描述',
    required: false,
    colProps: {
      span: 24,
    },
    helpMessage: '请输入当前任务描述',
    componentProps: {
      placeholder: '当前任务目标为收集杭州市城市建设投资集团有限公司公网数据资产',
    },
  },
  {
    field: 'task_type',
    component: 'Select',
    label: '任务类型',
    required: true,
    defaultValue: '1',
    componentProps: {
      options: [
        {
          label: '公网资产监控',
          value: '1',
        },
        {
          label: '内网资产扫描',
          value: '2',
        },
      ],
    },
  },
  {
    field: 'task_status',
    component: 'Select',
    label: '任务状态',
    required: true,
    defaultValue: '1',
    componentProps: {
      options: [
        {
          label: '进行中',
          value: '1',
        },
        {
          label: '已终止',
          value: '2',
        },
        {
          label: '已完成',
        },
      ],
    },
  },
];

export const publicSchemas: FormSchema[] = [
  {
    field: 'full_company_name_input',
    component: 'Input',
    label: '公司全称',
    helpMessage: '请输入完整的公司全称，用于获取备案信息',
    componentProps: {
      placeholder: '杭州市城市建设投资集团有限公司',
      style: 'width: 400px',
    },
  },
  {
    field: 'root_domain_input',
    component: 'InputTextArea',
    label: '根域名',
    helpMessage: '请输入根域名，可以不填\n根域名格式为：xxx.com，或者 xxx.gov.cn\n换行符隔开',
    componentProps: {
      placeholder: 'dfcfw.com\nbaidu.com',
      style: 'height: 200px; width: 400px;',
    },
  },
  {
    field: 'ip_input',
    component: 'InputTextArea',
    label: 'IP',
    helpMessage:
      '请输入IP，可以不填\nIP格式为：xxx.xxx.xxx.xxx，或者 xxx.xxx.xxx.xxx/16\n换行符隔开',
    componentProps: {
      placeholder: '192.168.2.11\n211.12.212.34\n211.12.32.9/24',
      style: 'height: 200px; width: 400px;',
    },
  },
  {
    field: 'domain_brute_force',
    component: 'Checkbox',
    label: '域名爆破',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'historical_domain_query',
    component: 'Checkbox',
    label: '历史域名查询',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'port_scanning',
    component: 'Checkbox',
    label: '端口扫描',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'framework_identification',
    component: 'Checkbox',
    label: '框架识别',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'fingerprint_identification',
    component: 'Checkbox',
    label: '指纹识别',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'fofa',
    component: 'Checkbox',
    label: 'FOFA',
    defaultValue: true,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'hunter',
    component: 'Checkbox',
    label: 'Hunter',
    defaultValue: false,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
  {
    field: 'quake',
    component: 'Checkbox',
    label: 'Quake',
    defaultValue: true,
    labelWidth: 100,
    componentProps: {
      style: 'width: 50px;',
    },
  },
];

export const privateSchemas: FormSchema[] = [
  {
    field: 'task_target',
    component: 'Input',
    label: '任务目标',
    required: true,
    defaultValue: 1,
  },
];

export async function getProjectOptions() {
  const response = await getProjectList();
  console.log(response);
  projectOptions.value = response.items.map((item) => ({
    label: `${item.project_name} --- ${item.project_desc} --- ${
      item.project_status ? '进行中' : '已完成'
    }`,
    value: item.id,
    disabled: !item.project_status,
  }));
}
