import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { useI18n } from '/@/hooks/web/useI18n';
const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: t('common.public_assets.taskNameText'),
    dataIndex: 'task_name',
    width: 200,
  },

  {
    title: t('common.public_assets.assets'),
    dataIndex: 'assetsText',
    width: 180,
  },

  {
    title: t('common.public_assets.createTimeText'),
    dataIndex: 'create_time',
    width: 100,
  },

  {
    title: t('common.public_assets.updateTimeText'),
    dataIndex: 'update_time',
    width: 100,
  },

  {
    title: t('common.public_assets.taskStatusText'),
    dataIndex: 'task_status',
    width: 100,
    customRender: ({ record }) => {
      const status = record.task_status;
      let color, text;
      if (status === 1) {
        color = 'success';
        text = t('common.public_assets.taskStatusText_1');
      } else if (status === 2) {
        color = 'error';
        text = t('common.public_assets.taskStatusText_2');
      } else if (status === 3) {
        color = 'warning'; // You can choose an appropriate color for status 3
        text = t('common.public_assets.taskStatusText_3');
      } else {
        color = 'default'; // You can choose a default color for other statuses
        text = t('common.public_assets.taskStatusText_default');
      }
      return h(Tag, { color: color }, () => text);
    },
  },
];

export const formSchema: FormSchema[] = [
  {
    field: 'task_name',
    label: t('common.public_assets.taskNameText'),
    component: 'Input',
    required: true,
  },
  {
    field: 'assets',
    label: t('common.public_assets.assetsText'),
    component: 'InputTextArea',
    required: true,
    componentProps: {
      placeholder: '请输入目标单位的根域名或 IP，以换行符隔开', // 添加提示语句
    },
  },
  {
    field: 'task_status',
    label: t('common.public_assets.taskStatusText'),
    component: 'RadioButtonGroup',
    defaultValue: 1,
    componentProps: {
      options: [
        { label: t('common.public_assets.taskStatusText_1'), value: 1 },
        { label: t('common.public_assets.taskStatusText_2'), value: 2 },
        { label: t('common.public_assets.taskStatusText_3'), value: 3 },
      ],
    },
  },
];
