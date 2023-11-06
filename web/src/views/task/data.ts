import { ref } from 'vue';
import { FormSchema } from '/@/components/Form';
import { getList as getProjectList } from '../project/api';

const projectOptions = ref([]);

export const step1Schemas: FormSchema[] = [
  {
    field: 'task_name',
    component: 'Input',
    label: '任务名称',
    required: true,
    defaultValue: 'test',
    colProps: {
      span: 24,
    },
  },
  {
    field: 'project',
    component: 'Select',
    label: '关联项目',
    required: true,
    defaultValue: '选择关联的项目',
    componentProps: {
      options: projectOptions,
    },
    colProps: {
      span: 24,
    },
  },
  {
    field: 'project_id',
    component: 'Input',
    label: '',
    required: true,
    defaultValue: '',
    colProps: {
      span: 0,
    },
    componentProps: {
      style: { display: 'none' }, // 使用 style 属性将字段隐藏
    },
  },
  {
    field: 'task_desc',
    component: 'InputTextArea',
    label: '任务描述',
    required: false,
    defaultValue: '项目目的及用途描述',
    colProps: {
      span: 24,
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
    field: 'task_target',
    component: 'Input',
    label: '任务目标',
    required: true,
    defaultValue: 1,
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
  projectOptions.value = response.items.map((item) => ({
    label: `${item.project_name} --- ${item.project_desc} --- ${
      item.project_status ? '进行中' : '已完成'
    }`,
    value: item.id,
  }));
}
