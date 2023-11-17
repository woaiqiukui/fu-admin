<template>
  <div>
    <BasicTable @register="registerTable" @fetch-success="onFetchSuccess">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button
            type="error"
            v-auth="['post:delete']"
            preIcon="ant-design:delete-outlined"
            @click="handleBulkDelete"
          >
            {{ t('common.delText') }}
          </a-button>
        </Space>
      </template>
      <template #toolbar>
        <a-button type="primary" @click="expandAll">{{ t('common.expandText') }}</a-button>
        <a-button type="primary" @click="collapseAll">{{ t('common.collapseText') }}</a-button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'button',
                color: 'link',
                auth: ['dept:update'],
                icon: 'ant-design:eye-outlined',
                placement: 'left',
                onClick: handleDetail.bind(null, record.uuid),
                tooltip: {
                  title: '查看详情',
                  placement: 'left',
                },
              },
              {
                type: 'button',
                color: 'primary',
                auth: ['dept:update'],
                icon: 'ant-design:pause-outlined',
                disabled: record.task_status === '2',
                onClick: handlePause.bind(null, record.uuid),
                tooltip: {
                  title: '暂停任务',
                  placement: 'left',
                },
              },
              {
                type: 'button',
                color: 'dashed',
                auth: ['dept:update'],
                icon: 'ant-design:play-circle-outlined',
                disabled: record.task_status === '1',
                onClick: handleResume.bind(null, record.uuid),
                tooltip: {
                  title: '恢复任务',
                  placement: 'left',
                },
              },
              {
                type: 'button',
                color: 'primary',
                auth: ['dept:update'],
                icon: 'clarity:note-edit-line',
                onClick: handleEdit.bind(null, record.uuid),
              },
              {
                type: 'button',
                color: 'error',
                auth: ['dept:delete'],
                icon: 'ant-design:delete-outlined',
                placement: 'left',
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.uuid),
                },
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <TaskDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent, nextTick } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';

  import { useDrawer } from '/@/components/Drawer';
  import TaskDrawer from './drawer.vue';
  import { columns, searchFormSchema } from './data';
  import { getList, deleteItem, pauseItem, resumeItem } from './api';
  import { message, Space } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useI18n } from '/@/hooks/web/useI18n';

  export default defineComponent({
    name: 'TaskManagement',
    components: { BasicTable, TaskDrawer, TableAction, Space },
    setup() {
      const { t } = useI18n();
      const [registerDrawer, { openDrawer }] = useDrawer();
      const { createConfirm } = useMessage();
      const [registerTable, { reload, expandAll, collapseAll, getSelectRows }] = useTable({
        title: '任务列表',
        api: getList,
        columns,
        formConfig: {
          labelWidth: 100,
          schemas: searchFormSchema,
        },
        rowSelection: {
          type: 'checkbox',
        },
        isTreeTable: true,
        pagination: false,
        striped: false,
        useSearchForm: true,
        showTableSetting: true,
        bordered: true,
        showIndexColumn: false,
        canResize: false,
        tableSetting: { fullScreen: true },
        actionColumn: {
          align: 'left',
          width: 150,
          title: t('common.operationText'),
          dataIndex: 'action',
          fixed: undefined,
        },
      });

      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      function handleDetail(task_uuid) {
        openDrawer(true, {
          record,
          isDetail: true,
        });
      }

      async function handlePause(task_uuid) {
        await pauseItem(task_uuid);
        message.success(t('common.successText'));
        await reload();
      }

      async function handleResume(task_uuid) {
        await resumeItem(task_uuid);
        message.success(t('common.successText'));
        await reload();
      }

      async function handleDelete(task_uuid) {
        await deleteItem(task_uuid);
        message.success(t('common.successText'));
        await reload();
      }

      async function handleBulkDelete() {
        if (getSelectRows().length == 0) {
          message.warning(t('common.batchDelHintText'));
        } else {
          createConfirm({
            iconType: 'warning',
            title: t('common.hintText'),
            content: t('common.delHintText'),
            async onOk() {
              for (const item of getSelectRows()) {
                await deleteItem(item.uuid);
              }
              message.success(t('common.successText'));
              await reload();
            },
          });
        }
      }

      function handleSuccess() {
        reload();
      }

      function onFetchSuccess() {
        // 演示默认展开所有表项
        nextTick(expandAll);
      }

      return {
        registerTable,
        registerDrawer,
        handleEdit,
        handlePause,
        handleResume,
        handleDetail,
        handleDelete,
        handleSuccess,
        onFetchSuccess,
        expandAll,
        collapseAll,
        handleBulkDelete,
        t,
      };
    },
  });
</script>
