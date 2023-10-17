import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { useI18n } from '/@/hooks/web/useI18n';
const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: t('common.project.projectNameText'),
    dataIndex: 'project_name',
    width: 110,
  },

  {
    title: t('common.project.projectDescText'),
    dataIndex: 'project_desc',
    width: 110,
  },

  {
    title: t('common.project.projectStatusText'),
    dataIndex: 'project_status',
    width: 110,
    customRender: ({ record }) => {
      const status = record.project_status;
      const enable = ~~status === 1;
      const color = enable ? 'success' : 'error';
      const text = enable
        ? t('common.project.project_status_1')
        : t('common.project.project_status_2');
      return h(Tag, { color: color }, () => text);
    },
  },

  {
    title: t('common.project.createDateText'),
    dataIndex: 'create_datetime',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'name',
    label: t('common.project.projectNameText'),
    component: 'Input',
    colProps: { span: 8 },
  },

  {
    field: 'status',
    label: t('common.project.projectStatusText'),
    component: 'Select',
    componentProps: {
      options: [
        { label: t('common.project.project_status_1'), value: true },
        { label: t('common.project.project_status_2'), value: false },
      ],
    },
    colProps: { span: 8 },
  },
];

export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },

  {
    field: 'parent_id',
    label: t('common.dept.parentText'),
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'name',
        key: 'id',
        value: 'id',
      },
      getPopupContainer: () => document.body,
    },
  },

  {
    field: 'project_name',
    label: t('common.project.projectNameText'),
    component: 'Input',
    required: true,
  },

  {
    field: 'project_desc',
    label: t('common.project.projectDescText'),
    component: 'InputTextArea',
    required: true,
  },

  {
    field: 'project_status',
    label: t('common.project.projectStatusText'),
    component: 'RadioButtonGroup',
    defaultValue: true,
    componentProps: {
      options: [
        { label: t('common.project.project_status_1'), value: true },
        { label: t('common.project.project_status_2'), value: false },
      ],
    },
  },
];
