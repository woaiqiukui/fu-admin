import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';

export const columns: BasicColumn[] = [
  {
    title: '任务名称',
    dataIndex: 'task_name',
    width: 110,
  },

  {
    title: '任务描述',
    dataIndex: 'task_desc',
    width: 110,
  },

  {
    title: '任务状态',
    dataIndex: 'task_status',
    width: 110,
    customRender: ({ record }) => {
      const status = record.task_status;
      let text, color;
      switch (status) {
        case '1':
          text = '进行中';
          color = 'success';
          break;
        case '2':
          text = '已终止';
          color = 'error';
          break;
        case '3':
          text = '已完成';
          color = 'success';
          break;
        default:
          text = '未知状态';
          color = 'default';
      }
      return h(Tag, { color: color }, () => text);
    },
  },

  {
    title: '创建时间',
    dataIndex: 'create_datetime',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    colProps: { span: 8 },
  },

  {
    field: 'status',
    label: '任务状态',
    component: 'Select',
    componentProps: {
      options: [
        { label: '进行中', value: '1' },
        { label: '已终止', value: '2' },
        { label: '已完成', value: '3' },
      ],
    },
  },
];

export const formSchema: FormSchema[] = [
  {
    field: 'task_uuid',
    label: 'task_uuid',
    component: 'Input',
    show: false,
  },

  {
    field: 'task_name',
    label: '任务名称',
    component: 'Input',
    required: true,
  },

  {
    field: 'task_desc',
    label: '任务描述',
    component: 'InputTextArea',
  },

  {
    field: 'task_status',
    label: '任务状态',
    component: 'Select',
    componentProps: {
      options: [
        { label: '进行中', value: '1' },
        { label: '已终止', value: '2' },
        { label: '已完成', value: '3' },
      ],
    },
    required: true,
  },

  {
    field: 'create_datetime',
    label: '创建时间',
    component: 'DatePicker',
    componentProps: {
      showTime: true,
    },
    required: true,
  },
];
