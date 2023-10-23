import { FormSchema } from '/@/components/Form';

export const step1Schemas: FormSchema[] = [
  {
    field: 'project',
    component: 'Select',
    label: '关联项目',
    required: true,
    defaultValue: '1',
    componentProps: {
      options: [
        {
          label: 'anncwb@126.com',
          value: '1',
        },
      ],
    },
    colProps: {
      span: 24,
    },
  },
  {
    field: 'fac',
    component: 'InputGroup',
    label: '收款账户',
    required: true,
    defaultValue: 'test@example.com',
    slot: 'fac',
    colProps: {
      span: 24,
    },
  },
  {
    field: 'pay',
    component: 'Input',
    label: '',
    defaultValue: 'zfb',
    show: false,
  },
  {
    field: 'payeeName',
    component: 'Input',
    label: '收款人姓名',
    defaultValue: 'Vben',
    required: true,
    colProps: {
      span: 24,
    },
  },
  {
    field: 'money',
    component: 'Input',
    label: '转账金额',
    defaultValue: '500',
    required: true,
    renderComponentContent: () => {
      return {
        prefix: () => '￥',
      };
    },
    colProps: {
      span: 24,
    },
  },
];
