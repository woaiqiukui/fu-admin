import { ref } from 'vue';
import { FormSchema } from '/@/components/Form';

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
    defaultValue: '1',
    // componentProps: {
    //   options: ref([]), // 使用 ref 创建响应式引用
    // },
    colProps: {
      span: 24,
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
